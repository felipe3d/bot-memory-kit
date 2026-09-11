#!/usr/bin/env python3
"""
run-interview-test.py — harness do loop de entrevista do bot-memory-kit.

Simula um usuário fictício (tests/fixtures/fake-user.yaml) respondendo às
perguntas do skill no sandbox Linux (container), via `hermes chat -q` com
`--resume` para manter o contexto entre rounds.

Uso (com o python do venv Hermes, que tem PyYAML):
  ~/.hermes/hermes-agent/venv/bin/python3 scripts/run-interview-test.py
  ~/.hermes/hermes-agent/venv/bin/python3 scripts/run-interview-test.py --reset
  ~/.hermes/hermes-agent/venv/bin/python3 scripts/run-interview-test.py --max-rounds 5

O estado (session_id do Hermes + Q&A + última pergunta) persiste em
test-homes/linux-hermes/interview-session.json — o harness pode ser
interrompido e retomado, igual ao usuário real.
"""
import json
import os
import re
import subprocess
import sys
import time

import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_HOME = os.path.join(REPO_ROOT, "test-homes", "linux-hermes")
FIXTURE = os.path.join(REPO_ROOT, "tests", "fixtures", "fake-user.yaml")
IMAGE = "nousresearch/hermes-agent:latest"
INNER_TIMEOUT = 110

# Respostas por tema — primeira regra cujas palavras-chave aparecem na pergunta vence,
# e cada regra só é usada uma vez (perguntas repetidas caem na genérica).
RULES = [
    ("areas",     ("área", "responsabilidade", "dividir", "sua vida")),
    ("time",      ("tempo", "ocupam", "dedicar")),
    ("solo",      ("sozinho", "equipe", "clientes diretamente", "trabalha")),
    ("projects",  ("paralelo",)),
    ("routine",   ("repete", "rotina", "consome")),
    ("forget",    ("atras", "lembre", "detalhes", "esquece")),
    ("delegate",  ("delegar", "gostaria de delegar")),
    ("always_on", ("horário", "24/7", "disponibilidade", "fixo")),
    ("where",     ("onde", "acontece", "obsidian", "e-mail", "calendário")),
    ("reliable",  ("confiáv", "desorganizad")),
    ("tools",     ("ferramenta", "aplicativos", "terminais", "navegadores", "usa no dia")),
    ("audience",  ("usaria", "quem ", "público")),
    ("permissions", ("poderia", "preparar", "alterar", "enviar", "contratar")),
    ("approval",  ("aprova",)),
    ("privacy",   ("sair", "privacidade", "externo", "secreta", "sensível")),
    ("style",     ("central", "especialista", "encaminha", "prefere")),
    ("proactive", ("demanda", "proactiv", "proactiva", "notifica")),
    ("cost",      ("custo", "tolerância", "manutenção")),
]


def persona_answer(question, persona, used_keys):
    q = question.lower()
    for key, kws in RULES:
        if key in used_keys:
            continue
        if any(k in q for k in kws):
            used_keys.add(key)
            return answer_for(key, persona, question)
    return persona.get("default_answer", "Depende do contexto.")


def answer_for(key, persona, question):
    name = persona["name"]
    if key == "areas":
        return (f"Sou {name}, {persona['role']}. Trabalho com {persona['business']}. "
                f"Grandes áreas: estúdio de fotografia/vídeo, infraestrutura de TI (HomeLab e VPS), "
                f"casa e família, e projetos de software como hobbies. "
                f"Máquinas: {', '.join(persona['machines'])}. Hobbies: {', '.join(persona['hobbies'])}.")
    if key == "time":
        return f"Mais tempo em: {persona['time_sinks']}. Gostaria de dedicar mais a fotografia e aos meus projetos de software."
    if key == "solo":
        return "Trabalho sozinho, mas falo diretamente com os clientes da Foca no atendimento."
    if key == "projects":
        return "Projetos paralelos: BetterFlickrUploader (app SwiftUI), automações do HomeLab e este sistema de bots/memória."
    if key == "routine":
        return f"Rotina repetitiva que consome tempo: {persona['time_sinks']}."
    if key == "forget":
        return "Costumo atrasar: acompanhamento de prazos de entrega e renovações de infraestrutura (domínios, backups)."
    if key == "delegate":
        return f"Gostaria de delegar: {persona['wants_to_delegate']}."
    if key == "always_on":
        return "A VPS Oracle roda 24/7; monitoramento de serviços e backups são rotinas contínuas. Tarefas em horário fixo: backup às 2h."
    if key == "where":
        return f"Fontes: {persona['knowledge_sources']}. Ferramentas: {', '.join(persona['tools'])}."
    if key == "reliable":
        return "Obsidian é confiável e canônico; e-mail e WhatsApp estão desorganizados."
    if key == "tools":
        return f"Uso diário: {', '.join(persona['tools'])}."
    if key == "audience":
        return f"Por ora só eu ({name}); atendimento a clientes é possibilidade futura."
    if key == "permissions":
        return ("Podem preparar rascunhos, consultar conhecimento aprovado e executar diagnósticos. "
                f"Exige minha aprovação: {persona['requires_approval']}.")
    if key == "approval":
        return f"Exige minha aprovação explícita: {persona['requires_approval']}."
    if key == "privacy":
        return f"Não pode sair do computador: {persona['cannot_leave_device']}."
    if key == "style":
        return f"Estilo: {persona['interaction_style']}."
    if key == "proactive":
        return "Atividades sob demanda; proativas apenas em horários definidos, resumo diário no máximo."
    if key == "cost":
        return "Custo moderado é aceitável; pouca manutenção manual. Uso glm-5.3 no dia a dia."
    return persona.get("default_answer", "Depende do contexto.")


def state_path(hm):
    return os.path.join(hm, "interview-session.json")


def read_state(hm):
    p = state_path(hm)
    if os.path.exists(p):
        with open(p) as f:
            return json.load(f)
    return None


def write_state(hm, st):
    st["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(state_path(hm), "w") as f:
        json.dump(st, f, indent=2, ensure_ascii=False)


def ollama_key():
    env_file = os.path.expanduser("~/.hermes/.env")
    if os.path.exists(env_file):
        for line in open(env_file):
            if line.startswith("OLLAMA_API_KEY="):
                return line.split("=", 1)[1].strip().strip("'\"")
    return None


SKIP_PAT = re.compile(
    r"Goodbye|Hermes Agent v|Available|session_id:|Tip:|Warning: Input|Shutting"
    r"|tirith|File-mutation|file\(s\) were NOT|git status|read_file|write_file"
    r"|HERMES_WRITE_SAFE_ROOT|^\s*[│╭╰─]|⢀|⣀|⣸|⣿|⢸|⣶|⣦|⣄|⠀|⠿|⠋|⣩|⠻|⠟|⢿|⣍|⠙"
    r"|^\s*browser|^\s*clarify|^\s*terminal|^\s*file|^\s*memory|^\s*session_search"
    r"|^\s*delegation|^\s*cronjob|^\s*todo|^\s*skills|^\s*github|^\s*vision"
    r"|^\s*image_gen|^\s*tts|^\s*messaging|^\s*spotify|^\s*web_search"
    r"|^\s*web_extract|^\s*toolsets|^\s*Toolset", re.I)


def run_round(hm, sid, message, key):
    """Envia mensagem ao Hermes no sandbox. Retorna (session_id, resposta_filtrada)."""
    if sid:
        inner = f'timeout {INNER_TIMEOUT} hermes --resume {sid} chat -q "$MSG" -Q'
    else:
        inner = f'timeout {INNER_TIMEOUT} hermes chat -q "$MSG" -Q'
    cmd = ["docker", "run", "--rm",
           "-v", f"{hm}:/hermes-home",
           "-e", "HERMES_HOME=/hermes-home",
           "-e", f"OLLAMA_API_KEY={key}",
           "-e", f"MSG={message}",
           "--entrypoint", "sh", IMAGE, "-c", inner]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           timeout=INNER_TIMEOUT + 40)
    except subprocess.TimeoutExpired:
        return sid, None, "[TIMEOUT]"
    except Exception as e:
        return sid, None, f"[ERROR: {e}]"

    out = (r.stdout or "") + (r.stderr or "")
    # session_id — sempre o último da saída
    sid_out = sid
    for m in re.finditer(r"session_id:\s*([A-Za-z0-9_]+)", out):
        sid_out = m.group(1)

    lines = [l for l in out.splitlines() if l.strip() and not SKIP_PAT.search(l)]
    answer = "\n".join(lines[-16:]) if lines else out.strip()[-500:]
    return sid_out, answer, None


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--home", default=DEFAULT_HOME)
    ap.add_argument("--max-rounds", type=int, default=25)
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()

    hm = os.path.abspath(args.home)
    if not os.path.isdir(hm):
        print(f"[harness] HERMES_HOME não existe: {hm}")
        sys.exit(1)

    persona = yaml.safe_load(open(FIXTURE))["persona"]
    key = ollama_key()
    if not key:
        print("[harness] OLLAMA_API_KEY não encontrada em ~/.hermes/.env")
        sys.exit(1)

    st = read_state(hm) if not args.reset else None
    if args.reset and os.path.exists(state_path(hm)):
        os.remove(state_path(hm))
    if not st:
        st = {"session_id": None, "round": 0, "qa": {}, "last_question": None,
              "question_num": 0, "done": False}

    used_keys = set()
    print(f"[harness] persona: {persona['name']} | home: {hm}")
    if st["session_id"]:
        print(f"[harness] retomando sessão {st['session_id']} "
              f"(round {st['round']}, pergunta {st['question_num']}/18)")

    for _ in range(args.max_rounds):
        if st.get("done"):
            print("[harness] entrevista já concluída; use --reset para recomeçar")
            break

        st["round"] += 1
        if not st["session_id"] or not st.get("last_question"):
            msg = "iniciar bot-memory-kit"
        else:
            ans = persona_answer(st["last_question"], persona, used_keys)
            st["qa"][f"q{len(st['qa']) + 1}"] = {
                "question": st["last_question"], "answer": ans}
            print(f"\n[round {st['round']}] Q: {st['last_question'][:110]}")
            print(f"[round {st['round']}] A: {ans[:160]}")
            msg = ans

        new_sid, resp, err = run_round(hm, st["session_id"], msg, key)
        if err:
            print(f"[harness] falha no round {st['round']}: {err}")
            break
        if new_sid:
            st["session_id"] = new_sid
            if st["round"] == 1:
                print(f"[harness] sessão iniciada: {new_sid}")

        st["last_response"] = resp or ""
        qlines = [l.strip() for l in st["last_response"].splitlines() if "?" in l]
        if qlines:
            st["last_question"] = qlines[-1]
            m = re.search(r"pergunta\s*(\d+)", qlines[-1], re.I)
            if m:
                st["question_num"] = int(m.group(1))
                print(f"[harness] progresso: pergunta {st['question_num']}/18")
            print(f"[round {st['round']}] skill: {resp[:260]}")
        else:
            st["done"] = True
            print(f"[round {st['round']}] skill (final): {resp[:400]}")
            print("[harness] sem nova pergunta — entrevista concluída")

        write_state(hm, st)

    st = read_state(hm) or st
    print(f"\n[harness] rounds: {st.get('round')} | respostas: {len(st.get('qa', {}))} "
          f"| pergunta atual: {st.get('question_num', 0)}/18 | done: {st.get('done')}")
    print(f"[harness] estado: {state_path(hm)}")


def persona_answer(question, persona, used_keys):
    """Resposta do usuário fictício; primeira regra não-usada cujas palavras batem vence."""
    q = question.lower()
    for key, kws in RULES:
        if key in used_keys:
            continue
        if any(k in q for k in kws):
            used_keys.add(key)
            return answer_for(key, persona, question)
    return persona.get("default_answer", "Depende do contexto.")


if __name__ == "__main__":
    main()