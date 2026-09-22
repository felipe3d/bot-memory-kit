# CS-032A — Canal mínimo de operador HomeLab para P-0

**Estado:** BLOCKED  
**Tipo:** preflight de aplicação bloqueado por conectividade; nenhuma mutação

## Objetivo

Definir um canal de operador sem argumentos para executar somente a preparação P-0 do publicador técnico no HomeLab, sem `NOPASSWD: ALL`, shell arbitrário, senha em chat, acesso a AgentKnowledge ou acesso fora da allowlist.

## Desenho proposto

| Item | Valor proposto | Limite |
|---|---|---|
| Wrapper | `/usr/local/libexec/ak-real-publisher-p0` | root-owned `root:root`, modo 0750, conteúdo fixo e revisionado; não aceita argumentos, stdin, env controlável, URL, path, ref ou comando externo. |
| Regra sudoers | permitir somente `fac` executar exatamente o wrapper via `sudo -n` | Sem wildcard, shell, editor, `SETENV`, `NOPASSWD: ALL`, `sudo -u` arbitrário ou outros binários. |
| Papel técnico | `ak-real-publisher` | O wrapper cria/verifica somente usuário e roots P-0 aprovados; não usa `fac` como publicador. |
| Auditoria | `/var/lib/ak-real-publisher/audit` root-owned | Evento sanitizado com revisão, resultado e read-backs; sem nota, segredo, env ou token. |
| Remoção | wrapper de rollback separado, também sem argumentos | Revoga/remove somente recursos P-0 enumerados; não toca vault, sync, profiles, GTD, CRM ou P1-A2. |

## Sequência futura

1. Operador humano cria o wrapper e a regra sudoers conforme revisão aprovada.
2. Read-back verifica owner, modo, checksum aprovado e regra sudoers exata.
3. Executar `sudo -n /usr/local/libexec/ak-real-publisher-p0` em ambiente sem conteúdo real.
4. Verificar usuários, roots, auditoria e rollback; qualquer divergência bloqueia CS-032.

## Proibições

- Não acessar AgentKnowledge, Obsidian, vault, sync, homes Hermes, credenciais, `.env`, tokens ou notas.
- Não criar systemd service, timer, repo, key, publisher real ou conteúdo.
- Não aceitar parâmetros ou permitir que conteúdo recuperado influencie o wrapper.

## Anexo A — wrappers, hashes e sudoers exatos

**Estado:** desenho documental; os textos abaixo não foram escritos no HomeLab.

### Wrapper P-0

Path: `/usr/local/libexec/ak-real-publisher-p0`  
Owner/mode: `root:root`, `0750`  
SHA-256 esperado: `def12e2bc99acb212c8f71606c0422a3ba438dad5ed19380f75288ddfd7b3c0c`

```sh
#!/bin/sh
set -eu
[ "$#" -eq 0 ] || exit 64
exec env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /bin/sh -c '
set -eu
user=ak-real-publisher
root=/var/lib/ak-real-publisher
audit=/var/lib/ak-real-publisher/audit
id "$user" >/dev/null 2>&1 && exit 20
[ ! -e "$root" ] || exit 21
/usr/sbin/useradd --system --create-home --home-dir "$root" --shell /usr/sbin/nologin "$user"
/usr/bin/install -d -o "$user" -g "$user" -m 0700 "$root"
/usr/bin/install -d -o root -g root -m 0700 "$audit"
printf "{\"event\":\"p0-bootstrap\",\"result\":\"created\"}\n" > "$audit/p0.json"
/usr/bin/chown root:root "$audit/p0.json"
/usr/bin/chmod 0600 "$audit/p0.json"
/usr/bin/id "$user"
/usr/bin/stat -c "%n %a %U %G" "$root" "$audit" "$audit/p0.json"
'
```

### Wrapper de rollback

Path: `/usr/local/libexec/ak-real-publisher-p0-rollback`  
Owner/mode: `root:root`, `0750`  
SHA-256 esperado: `6334428744cbacf71e301f2259f806610d94749dc0ae0a49137b08d2d142d30c`

```sh
#!/bin/sh
set -eu
[ "$#" -eq 0 ] || exit 64
exec env -i PATH=/usr/sbin:/usr/bin:/sbin:/bin /bin/sh -c '
set -eu
user=ak-real-publisher
root=/var/lib/ak-real-publisher
audit=/var/lib/ak-real-publisher/audit
[ -d "$audit" ] || exit 30
/usr/sbin/userdel -r "$user" 2>/dev/null || true
/usr/bin/rm -rf "$root"
/usr/bin/install -d -o root -g root -m 0700 "$audit"
printf "{\"event\":\"p0-bootstrap\",\"result\":\"rolled-back\"}\n" > "$audit/p0-rollback.json"
/usr/bin/chown root:root "$audit/p0-rollback.json"
/usr/bin/chmod 0600 "$audit/p0-rollback.json"
/usr/bin/id "$user" >/dev/null 2>&1 && exit 40 || true
[ -e "$root" ] && exit 41 || true
/usr/bin/stat -c "%n %a %U %G" "$audit" "$audit/p0-rollback.json"
'
```

### Regra sudoers

Path: `/etc/sudoers.d/ak-real-publisher-p0`  
Owner/mode: `root:root`, `0440`  
SHA-256 esperado: `8be61e8e722c65b78c88c2d07cd3962d090b95254289841a6815b8b62c489b25`

```sudoers
# CS-032A: fixed no-argument P-0 operator channel
Defaults:fac !setenv
fac ALL=(root) NOPASSWD: /usr/local/libexec/ak-real-publisher-p0, /usr/local/libexec/ak-real-publisher-p0-rollback
```

### Read-backs e rollback da aplicação futura

1. Escrever os dois wrappers e a regra como arquivos novos, com os owners/modes acima.
2. Conferir SHA-256 dos três arquivos e `visudo -cf /etc/sudoers.d/ak-real-publisher-p0`.
3. Executar `sudo -n /usr/local/libexec/ak-real-publisher-p0` sem argumentos; aceitar somente exit 0, 20 ou 21 conforme baseline documentado.
4. Ler de volta `id ak-real-publisher`, `stat` da root/auditoria e evento sanitizado; nunca ler AgentKnowledge.
5. Executar o wrapper de rollback sem argumentos; confirmar ausência do usuário/root e retenção root-only da auditoria.
6. Na falha de checksum, visudo, owner/mode ou read-back, remover somente os três arquivos CS-032A e usar o wrapper de rollback se o publicador tiver sido criado.

## Aprovação futura

Aplicar este CS exige aprovação separada que nomeie wrapper, checksum, regra sudoers, rollback e read-backs. A aprovação de CS-032A não autoriza P-0, CS-033, Gate R de execução ou conteúdo real.

## Estado de aplicação

**BLOCKED:** os dois caminhos autorizados ao HomeLab falharam no preflight. Nenhum wrapper/sudoers foi criado. Evidência: `program/evidence/CS-032A-apply-preflight.md`.

## Evidência

Nenhuma evidência operacional nova.