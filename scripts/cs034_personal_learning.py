#!/usr/bin/env python3
"""CS-034 — Helper local de aprendizado assistido (piloto pessoal do Mac).

Componente stdlib-only (sem rede, shell, subprocess externo ou chamadas de modelo).
O assistente de IA desta conversa redige candidatas a partir da fonte autorizada;
este helper valida, persiste e recupera — não simula um LLM.

Fluxo:
    fonte allowlisted → propose() cria candidata em inbox
    → cartão sanitizado para revisão humana
    → decide(approve) promote para canonical / decide(reject) descarta
    → revise() cria nova revisão candidata (correção)
    → decide(withdraw) arquiva e bloqueia recuperação
    → retrieve() retorna somente canônicos vigentes com citação
    → recover() restaura transação incompleta
    → rollback() desabilita o piloto e arquiva tudo

Segurança:
    - Valida origem/binding da decisão, não autentica criptograficamente o operador.
    - O operador Desktop é parte confiável neste piloto.
    - NÃO é fronteira de segurança contra agente com ferramentas amplas.
    - Filtro de conteúdo é heurístico/conservador, não detector universal.

Paths:
    Fonte:  /Users/fac/dev/bot-memory-kit/program/handoffs/SESSION-PROMPT-PERSONAL-BOTS.md
    Vault:  /Users/fac/dev/Obsidian/felipe/AgentKnowledge/
    Backup: /Users/fac/.hermes/bmk-backups/cs034-personal-learning/

Uso (CLI):
    python3 -B scripts/cs034_personal_learning.py cards
    python3 -B scripts/cs034_personal_learning.py retrieve
    echo '{"statement":"...","utility":"...","valid_days":90}' | python3 -B scripts/cs034_personal_learning.py propose
    echo '{"actor":"owner","channel":"desktop-private",...}' | python3 -B scripts/cs034_personal_learning.py decide
    echo '{"id":"AK-...","draft":{...},"reference":"desktop:..."}' | python3 -B scripts/cs034_personal_learning.py revise
    python3 -B scripts/cs034_personal_learning.py recover
    python3 -B scripts/cs034_personal_learning.py rollback
"""
import hashlib
import os
from pathlib import Path
import stat


class Refused(Exception):
    """Operação negada (fail closed). Mensagens nunca contêm input não confiável."""


def digest(data):
    """SHA-256 hex de bytes ou string."""
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def safe_path(path):
    """Valida path absoluto sem '..' e sem symlinks em qualquer componente."""
    path = Path(path)
    if not path.is_absolute() or '..' in path.parts:
        raise Refused('invalid_path')
    for part in [*reversed(path.parents), path]:
        if part.is_symlink():
            raise Refused('symlink')
    return path


def read_bytes(path, limit):
    """Lê até `limit` bytes de arquivo regular (não symlink, link único). Refused se exceder."""
    path = safe_path(path)
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            raise Refused('not_regular_single_link')
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise Refused('quota')
    return data


def read_source(path, allowed, expected_digest):
    """Lê somente a seção 'Acordo com o usuário' de `path`, se for igual a `allowed` e o digest bater."""
    path, allowed = safe_path(path), safe_path(allowed)
    if path != allowed:
        raise Refused('source_not_allowed')
    # Bound the whole document too; only the section is returned to the analyzer.
    raw = read_bytes(path, 65536).decode('utf-8')
    heading = '## Acordo com o usuário'
    lines = raw.splitlines()
    if lines.count(heading) != 1:
        raise Refused('section_changed')
    start = lines.index(heading) + 1
    section = []
    for line in lines[start:]:
        if line.startswith('#'):
            break
        section.append(line)
    text = '\n'.join(section).strip()
    if not text or len(text.encode()) > 8192:
        raise Refused('quota')
    if digest(text) != expected_digest:
        raise Refused('source_changed')
    return {'text': text, 'sha256': digest(text), 'locator': str(path) + '#acordo-com-o-usuario'}


import copy
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
import fcntl
import json
import re


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + '\n'


def stamp():
    return datetime.now(timezone.utc).isoformat()


def atomic(path, text):
    path = safe_path(path)
    temporary = safe_path(path.with_name(path.name + '.tmp'))
    fd = os.open(str(temporary), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(text)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(str(temporary), str(path))
        directory = os.open(str(path.parent), os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if temporary.exists():
            temporary.unlink()


def json_read(path):
    try:
        return json.loads(read_bytes(path, 1048576))
    except (ValueError, UnicodeError):
        raise Refused('corrupt_record') from None


def note_text(note):
    return '---\n' + encoded(note) + '---\n\n' + note['statement'] + '\n\n' + note['utility'] + '\n'


def note_read(path, expected):
    raw = read_bytes(path, 16384).decode('utf-8')
    if digest(raw) != expected:
        raise Refused('note_integrity')
    try:
        if not raw.startswith('---\n'):
            raise ValueError()
        return json.loads(raw.split('---\n', 2)[1])
    except (ValueError, IndexError):
        raise Refused('corrupt_note') from None


def validate_draft(draft):
    """Valida schema e conteúdo de um draft de candidata (statement, utility, valid_days).

    Rejeita segredos, emails, URLs, paths, instruções, dados operacionais e payloads grandes.
    Filtro conservador/heurístico — não é detector universal de PII ou injeção.
    """
    if not isinstance(draft, dict) or set(draft) != {'statement', 'utility', 'valid_days'}:
        raise Refused('draft_schema')
    days = draft['valid_days']
    if type(days) is not int or not 1 <= days <= 365:
        raise Refused('validity')
    for field in ('statement', 'utility'):
        text = draft[field]
        if not isinstance(text, str) or not text.strip() or len(text.encode()) > 2048:
            raise Refused('draft_quota')
        # Conservative screening, not a claim of universal PII/injection detection.
        if re.search(r'[\x00-\x1f]|```|https?://|[\w.+-]+@[\w.-]+|\b\d{5,}\b|(?:sk-|ghp_|cfk_)[\w-]+|-----BEGIN|(?:password|senha|secret|token|api[_ -]?key)\s*[:=]|ignore.{0,30}(?:instruction|instru)|(?:execute|executar|rode|run)\s+(?:comando|command|curl|bash|sudo|tool)|(?:autoaprovar|autoapprove)|\$\(|/Users/|/etc/', text, re.I):
            raise Refused('unsafe_draft')
        if re.search(r'\b(?:leads?|clientes?|tarefas? pendentes|transcript|transcrição|dump)\s*:', text, re.I):
            raise Refused('operational_or_raw_data')
    if len((draft['statement'] + draft['utility']).encode()) > 2048:
        raise Refused('draft_quota')


class Store:
    """Store do piloto CS-034: inbox, canonical e archive em subdiretórios próprios.

    Operações: propose, cards, decide, revise, retrieve, recover, rollback.
    Transações atômicas com journal pré-imagem para recuperação.
    Lock por flock no backup. State em JSON validado a cada operação.
    O operador Desktop é parte confiável; isto não é fronteira de SO.
    """
    def __init__(self, root, backup, source, source_digest):
        self.root, self.backup = safe_path(root), safe_path(backup)
        self.source, self.source_digest = safe_path(source), source_digest
        self.inbox = self.root / 'inbox/mac/cs034-personal-learning'
        self.canonical = self.root / 'canonical/personal-collaboration'
        self.archive = self.root / 'archive/cs034-personal-learning'
        self.state_file = self.archive / 'state.json'
        self.journal = self.backup / 'transaction.json'
        self.fail_after = None
        for directory in (self.inbox, self.canonical, self.archive, self.backup):
            safe_path(directory)
            directory.mkdir(mode=0o700, parents=True, exist_ok=True)
        if not self.state_file.exists():
            if any(any(d.iterdir()) for d in (self.inbox, self.canonical, self.archive)):
                raise Refused('existing_destination')
            atomic(self.state_file, encoded({'version': 1, 'entries': {}, 'decisions': [], 'files': {}}))

    @contextmanager
    def locked(self, allow_pending=False, allow_disabled=False):
        lock = safe_path(self.backup / 'lock')
        fd = os.open(str(lock), os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, 'r+') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX)
            if not (allow_pending or allow_disabled) and (self.backup / 'DISABLED').exists():
                raise Refused('disabled')
            if self.journal.exists() and not allow_pending:
                raise Refused('pending_transaction')
            yield

    def state(self):
        state = json_read(self.state_file)
        if not isinstance(state, dict) or state.get('version') != 1:
            raise Refused('state_schema')
        if (set(state) != {'version', 'entries', 'decisions', 'files'}
                or not isinstance(state['entries'], dict) or len(state['entries']) > 3
                or not isinstance(state['decisions'], list) or not isinstance(state['files'], dict)):
            raise Refused('state_schema')
        for identity, item in state['entries'].items():
            if (not re.fullmatch(r'AK-CS034-[a-f0-9]{16}', identity)
                    or not isinstance(item, dict) or item.get('status') not in ('candidate', 'canonical', 'rejected', 'archived')
                    or type(item.get('revision')) is not int or item['revision'] < 1
                    or not isinstance(item.get('digest'), str) or not re.fullmatch(r'[a-f0-9]{64}', item['digest'])):
                raise Refused('state_schema')
        for path, expected in state['files'].items():
            self.owned(path)
            if not isinstance(expected, str) or not re.fullmatch(r'[a-f0-9]{64}', expected):
                raise Refused('state_schema')
        return state

    def owned(self, path):
        path = safe_path(path)
        if path.parent not in (self.inbox, self.canonical, self.archive):
            raise Refused('outside_store')
        return path

    def commit(self, state, changes):
        changes = {self.owned(p): text for p, text in changes.items()}
        for path, text in changes.items():
            if text is None:
                state['files'].pop(str(path), None)
            else:
                state['files'][str(path)] = digest(text)
        changes[self.state_file] = encoded(state)
        before = {str(p): read_bytes(p, 1048576).decode('utf-8') if p.exists() else None for p in changes}
        atomic(self.journal, encoded({'before': before, 'after': {str(p): digest(t) if t is not None else None for p, t in changes.items()}}))
        try:
            for index, (path, text) in enumerate(changes.items(), 1):
                if text is None:
                    if path.exists():
                        path.unlink()
                else:
                    atomic(path, text)
                if self.fail_after == index:
                    raise OSError('synthetic_fault')
        except BaseException:
            # Leave the durable pre-image journal; retrieval is blocked until recovery.
            raise
        self.journal.unlink()

    def recover(self):
        with self.locked(allow_pending=True):
            if not self.journal.exists():
                return {'status': 'clean'}
            transaction = json_read(self.journal)
            # Preflight every target before restoring any; never overwrite a concurrent edit.
            for name, old in transaction['before'].items():
                path = self.owned(name)
                current = digest(read_bytes(path, 1048576)) if path.exists() else None
                if current not in (digest(old) if old is not None else None, transaction['after'][name]):
                    raise Refused('concurrent_edit')
            for name, old in transaction['before'].items():
                path = self.owned(name)
                if old is None:
                    if path.exists():
                        path.unlink()
                else:
                    atomic(path, old)
            # Retain restricted pre-images for review; never normal retrieval.
            saved = self.backup / ('recovered-' + digest(encoded(transaction))[:24] + '.json')
            atomic(saved, encoded(transaction))
            self.journal.unlink()
            return {'status': 'recovered'}

    def propose(self, draft):
        """Cria candidata em inbox a partir do draft e da fonte autorizada. Idempotente por fingerprint."""
        validate_draft(draft)
        source = read_source(self.source, self.source, self.source_digest)
        fingerprint = digest(encoded(draft))
        identity = 'AK-CS034-' + fingerprint[:16]
        with self.locked():
            state = self.state()
            existing = state['entries'].get(identity)
            if existing:
                if existing['status'] != 'candidate':
                    raise Refused('already_decided')
                return note_read(self.inbox / (identity + '.md'), existing['digest'])
            if len(state['entries']) >= 3:
                raise Refused('round_quota')
            now = stamp()
            note = dict(draft, id=identity, revision=1, status='candidate', owner='owner',
                        scope='personal.default.mac', sensitivity='internal',
                        source=[{'kind': 'document', 'locator': source['locator'], 'sha256': source['sha256'],
                                 'observed_at': None, 'captured_at': now, 'captured_by': 'mac'}],
                        verified_at=None, review_required='human',
                        expires_at=(datetime.fromisoformat(now) + timedelta(days=draft['valid_days'])).isoformat(),
                        supersedes=None, superseded_by=None)
            text = note_text(note)
            state['entries'][identity] = {'status': 'candidate', 'revision': 1, 'digest': digest(text), 'fingerprint': fingerprint}
            self.commit(state, {self.inbox / (identity + '.md'): text})
            return note

    def cards(self):
        """Lista candidatas pendentes (status=candidate) para revisão humana."""
        with self.locked():
            state = self.state()
            return [note_read(self.inbox / (identity + '.md'), item['digest'])
                    for identity, item in state['entries'].items() if item['status'] == 'candidate']

    def decide(self, decision):
        """Aplica decisão humana (approve/reject/withdraw) vinculada a ID, revisão e digest.

        Trusted adapter submits an ACTUAL owner's turn, never model/source approval.
        Binding and shape are validated here. This method cannot authenticate a
        human against a malicious operator with the same OS/file permissions.
        """
        if not isinstance(decision, dict) or set(decision) != {'actor', 'channel', 'reference', 'action', 'id', 'revision', 'digest'}:
            raise Refused('decision_schema')
        if (decision['actor'] != 'owner' or decision['channel'] != 'desktop-private'
                or not isinstance(decision['reference'], str)
                or not re.fullmatch(r'desktop:[A-Za-z0-9_.:-]{1,160}', decision['reference'])
                or decision['action'] not in ('approve', 'reject', 'withdraw')):
            raise Refused('decision_origin')
        with self.locked():
            state = self.state()
            decision_key = digest(encoded(decision))
            for previous in state['decisions']:
                if previous['key'] == decision_key:
                    current = state['entries'].get(decision['id'], {})
                    if current.get('status') != previous['result']['status'] or current.get('revision') != previous['result']['revision']:
                        raise Refused('stale_decision')
                    return previous['result']
            item = state['entries'].get(decision['id'])
            required = 'canonical' if decision['action'] == 'withdraw' else 'candidate'
            if (not item or item['status'] != required
                    or item['revision'] != decision['revision'] or item['digest'] != decision['digest']):
                raise Refused('decision_binding')
            directory = self.canonical if decision['action'] == 'withdraw' else self.inbox
            path = directory / (decision['id'] + '.md')
            note = note_read(path, item['digest'])
            changes = {path: None}
            if decision['action'] == 'approve':
                read_source(self.source, self.source, self.source_digest)
                validate_draft({k: note[k] for k in ('statement', 'utility', 'valid_days')})
                if note['scope'] != 'personal.default.mac' or note['sensitivity'] != 'internal':
                    raise Refused('note_scope')
                if datetime.fromisoformat(note['expires_at']) <= datetime.now(timezone.utc):
                    raise Refused('expired_candidate')
                for other_id, other in state['entries'].items():
                    if other_id != note['id'] and other['status'] == 'canonical':
                        existing = note_read(self.canonical / (other_id + '.md'), other['digest'])
                        if existing['statement'].strip().casefold() == note['statement'].strip().casefold():
                            raise Refused('conflict_requires_revision')
                note['status'], note['verified_at'] = 'canonical', stamp()
                note['decision'] = dict(decision, decided_at=note['verified_at'])
                text = note_text(note)
                changes[self.canonical / (note['id'] + '.md')] = text
                item.update(status='canonical', digest=digest(text))
            elif decision['action'] == 'withdraw':
                note['status'] = 'archived'
                changes[self.archive / (note['id'] + '-r' + str(note['revision']) + '.md')] = note_text(note)
                # Durable tombstone is outside rollback: a withdrawal never resurrects.
                atomic(self.archive / (note['id'] + '.withdrawn'), encoded({'id': note['id'], 'reference': decision['reference']}))
                item.update(status='archived')
            else:
                item.update(status='rejected')
            result = {'id': decision['id'], 'status': item['status'], 'revision': item['revision']}
            state['decisions'].append({'key': decision_key, 'decision': decision,
                                       'decided_at': stamp(), 'result': result})
            self.commit(state, changes)
            return result

    def revise(self, identity, draft, reference):
        """Cria nova revisão candidata a partir de uma nota existente (correção).

        A versão anterior é arquivada como superseded; a nova fica candidate
        e exige nova decisão humana. Withdrawn não é revisável.
        """
        validate_draft(draft)
        if not re.fullmatch(r'desktop:[A-Za-z0-9_.:-]{1,160}', reference):
            raise Refused('decision_origin')
        with self.locked():
            state = self.state()
            item = state['entries'].get(identity)
            if not item or item['status'] not in ('canonical', 'candidate') or (self.archive / (identity + '.withdrawn')).exists():
                raise Refused('not_revisable')
            directory = self.canonical if item['status'] == 'canonical' else self.inbox
            path = directory / (identity + '.md')
            old = note_read(path, item['digest'])
            if all(old[k] == draft[k] for k in draft) and old.get('correction_reference') == reference:
                return old
            archive = copy.deepcopy(old)
            archive['status'] = 'superseded'
            archive['superseded_by'] = identity + ':r' + str(old['revision'] + 1)
            note = dict(old, **draft)
            note.update(status='candidate', revision=old['revision'] + 1, verified_at=None,
                        correction_reference=reference, supersedes=identity + ':r' + str(old['revision']), superseded_by=None,
                        expires_at=(datetime.now(timezone.utc) + timedelta(days=draft['valid_days'])).isoformat())
            note.pop('decision', None)
            note['source'] = old['source'] + [{'kind': 'human-review', 'locator': reference,
                                              'observed_at': stamp(), 'captured_at': stamp(), 'captured_by': 'mac'}]
            text = note_text(note)
            changes = {path: None, self.archive / (identity + '-r' + str(old['revision']) + '.md'): note_text(archive)}
            changes[self.inbox / (identity + '.md')] = text
            item.update(status='candidate', revision=note['revision'], digest=digest(text))
            state['decisions'].append({'key': digest(reference + item['digest']),
                                       'decision': {'action': 'propose-correction', 'reference': reference, 'id': identity},
                                       'decided_at': stamp(), 'result': {'status': 'candidate', 'revision': note['revision']}})
            self.commit(state, changes)
            return note

    def rollback(self):
        """Desabilita o piloto: arquiva canônicos, rejeita candidatas, cria marca DISABLED.

        Tombstones de retirada permanecem. Auditoria não é apagada.
        """
        with self.locked(allow_disabled=True):
            state = self.state()
            changes = {}
            # Check every owned note before disabling or altering it.
            for identity, item in state['entries'].items():
                if item['status'] not in ('candidate', 'canonical'):
                    continue
                directory = self.canonical if item['status'] == 'canonical' else self.inbox
                path = directory / (identity + '.md')
                note = note_read(path, item['digest'])
                if item['status'] == 'canonical':
                    note['status'] = 'archived'
                    changes[self.archive / (identity + '-r' + str(note['revision']) + '.md')] = note_text(note)
                changes[path] = None
                item['status'] = 'archived' if item['status'] == 'canonical' else 'rejected'
            atomic(self.backup / 'DISABLED', encoded({'delivery': 'CS-034', 'reason': 'rollback', 'at': stamp()}))
            state['decisions'].append({'key': 'rollback', 'decision': {'action': 'rollback'}, 'decided_at': stamp()})
            self.commit(state, changes)
            return {'status': 'disabled', 'history_retained': True}

    def retrieve(self, now=None):
        """Retorna somente canônicos vigentes (não expirados, não retirados) com citação de origem."""
        with self.locked():
            state = self.state()
            results = []
            now = now or datetime.now(timezone.utc)
            for identity, item in state['entries'].items():
                if item['status'] != 'canonical' or (self.archive / (identity + '.withdrawn')).exists():
                    continue
                path = self.canonical / (identity + '.md')
                note = note_read(path, item['digest'])
                if datetime.fromisoformat(note['expires_at']) <= now:
                    continue
                results.append(dict(note, read_path=str(path), sha256=item['digest']))
            return results


SOURCE = Path('/Users/fac/dev/bot-memory-kit/program/handoffs/SESSION-PROMPT-PERSONAL-BOTS.md')
SOURCE_DIGEST = '15effc23b6ce5a5e96e32832a0338314ef86762a383bbaa83172ec750219f4e0'
KNOWLEDGE = Path('/Users/fac/dev/Obsidian/felipe/AgentKnowledge')
BACKUP = Path('/Users/fac/.hermes/bmk-backups/cs034-personal-learning')


def check_runtime(system, home, hermes_home, profile):
    """Guard de runtime: somente Darwin, /Users/fac, HERMES_HOME default. Recusa perfis nomeados."""
    if (system != 'Darwin' or home != '/Users/fac' or hermes_home != '/Users/fac/.hermes'
            or profile not in (None, '', 'default')):
        raise Refused('wrong_host_or_profile')
    safe_path(Path(hermes_home))


def main():
    """CLI entry point. Ações: propose, cards, decide, revise, retrieve, recover, rollback.

    propose/decide/revise recebem JSON por stdin (até 16KiB).
    Saída sempre JSON. Erros retornam 'refused_or_unavailable' sem vazar payload.
    """
    import argparse
    import platform
    import sys
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['propose', 'cards', 'decide', 'revise', 'retrieve', 'recover', 'rollback'])
    args = parser.parse_args()
    try:
        check_runtime(platform.system(), str(Path.home()), os.environ.get('HERMES_HOME', str(Path.home() / '.hermes')),
                      os.environ.get('HERMES_PROFILE'))
        if not safe_path(KNOWLEDGE).is_dir():
            raise Refused('knowledge_root_missing')
        # Read-only actions cannot create a new deployment implicitly.
        if args.action != 'propose' and not (KNOWLEDGE / 'archive/cs034-personal-learning/state.json').is_file():
            raise Refused('not_initialized')
        payload = None
        if args.action in ('propose', 'decide', 'revise'):
            raw = sys.stdin.buffer.read(16385)
            if len(raw) > 16384:
                raise Refused('input_quota')
            payload = json.loads(raw)
        store = Store(KNOWLEDGE, BACKUP, SOURCE, SOURCE_DIGEST)
        if args.action == 'propose':
            result = store.propose(payload)
        elif args.action == 'decide':
            result = store.decide(payload)
        elif args.action == 'revise':
            if not isinstance(payload, dict) or set(payload) != {'id', 'draft', 'reference'}:
                raise Refused('revision_schema')
            result = store.revise(payload['id'], payload['draft'], payload['reference'])
        else:
            result = getattr(store, args.action)()
        print(encoded({'ok': True, 'result': result}))
        return 0
    except (Refused, OSError, ValueError, TypeError, KeyError):
        # No raw payload, arbitrary path or traceback in chat/logs on rejection.
        print(encoded({'ok': False, 'error': 'refused_or_unavailable'}))
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
