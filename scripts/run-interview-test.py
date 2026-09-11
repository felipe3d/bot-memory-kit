#!/usr/bin/env python3
"""
run-interview-test.py — harness de teste do loop de entrevista do bot-memory-kit.

Roda dentro do sandbox Linux (container) ou localmente com HERMES_HOME apontando
para test-homes/. Simula um usuário fictício respondendo às perguntas do skill
para validar o checkpoint, o fluxo de estados e a persistência.

Uso:
  HERMES_HOME=test-homes/linux-hermes python3 scripts/run-interview-test.py
  HERMES_HOME=test-homes/mac-sandbox python3 scripts/run-interview-test.py --local

O usuário fictício é definido em tests/fixtures/fake-user.yaml.
"""
import json, os, sys, time, subprocess, argparse, yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
DEFAULT_HOME = os.path.join(REPO_ROOT, "test-homes", "linux-hermes")
FIXTURE = os.path.join(REPO_ROOT, "tests", "fixtures", "fake-user.yaml")

def load_fixture():
    with open(FIXTURE) as f:
        return yaml.safe_load(f)

def read_checkpoint(hm):
    p = os.path.join(hm, "checkpoint.json")
    if not os.path.exists(p):
        return None
    with open(p) as f:
        return json.load(f)

def write_checkpoint(hm, data):
    p = os.path.join(hm, "checkpoint.json")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    data["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with open(p, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return p

def hermes_query(hm, query, model=None, local=False, ollama_key=None):
    """Envia uma query ao Hermes e retorna a resposta."""
    if local:
        cmd = ["hermes", "chat", "-q", query, "-Q"]
        env = {**os.environ, "HERMES_HOME": hm}
    else:
        cmd = ["docker", "run", "--rm",
               "-v", f"{hm}:/hermes-home",
               "-e", "HERMES_HOME=/hermes-home"]
        if ollama_key:
            cmd += ["-e", f"OLLAMA_API_KEY={ollama_key}"]
        cmd += ["--entrypoint", "sh",
                "nousresearch/hermes-agent:latest",
                "-c", f'timeout 120 hermes chat -q "{query}" -Q']
        env = {**os.environ}
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=130, env=env)
        # filtra linhas de banner/saída não-resposta
        lines = [l for l in (r.stdout + r.stderr).splitlines()
                 if l.strip()
                 and not l.startswith("[sandbox]")
                 and l.strip() not in ("Goodbye! ⚕",)
                 and "Hermes Agent v" not in l
                 and "Available Tools" not in l]
        return "\n".join(lines[-10:]) if lines else r.stdout.strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT]"
    except Exception as e:
        return f"[ERROR: {e}]"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--local", action="store_true", help="run locally (no Docker)")
    ap.add_argument("--home", default=DEFAULT_HOME, help="HERMES_HOME path")
    ap.add_argument("--max-rounds", type=int, default=20, help="max interview rounds")
    args = ap.parse_args()

    hm = os.path.abspath(args.home)
    fixture = load_fixture()
    persona = fixture["persona"]

    # carrega chave ollama se não local
    ollama_key = None
    if not args.local:
        env_file = os.path.expanduser("~/.hermes/.env")
        if os.path.exists(env_file):
            for line in open(env_file):
                if line.startswith("OLLAMA_API_KEY="):
                    ollama_key = line.split("=",1)[1].strip().strip("'\"")
                    break

    print(f"[harness] persona: {persona['name']}")
    print(f"[harness] HERMES_HOME: {hm}")
    print(f"[harness] modo: {'local' if args.local else 'docker'}")
    print()

    # Inicia: envia o gatilho do kit
    checkpoint = read_checkpoint(hm)
    if checkpoint and checkpoint.get("phase") == "INTERVIEW":
        print(f"[harness] retomando entrevista existente (phase={checkpoint['phase']})")
    else:
        checkpoint = {
            "schema_version": 1, "kit_version": "0.1.0",
            "run_id": f"test-{int(time.time())}",
            "phase": "INTENT", "host_id": "", "profile_id": "",
            "workspace": hm, "session_id": "",
            "approved_scope": None, "selected_items": [],
            "completed_steps": [], "blocked_reason": None,
            "next_step": "trigger", "current_query": None,
            "current_response": None, "interview_answers": {}, "updated_at": ""
        }
        write_checkpoint(hm, checkpoint)

    # Loop de entrevista
    for rnd in range(args.max_rounds):
        cp = read_checkpoint(hm)
        if cp is None:
            print("[harness] checkpoint sumiu — abortando")
            break
        phase = cp.get("phase", "")
        print(f"\n[harness] round {rnd+1}, phase={phase}")

        if phase in ("SCOPE_APPROVED", "PLAN_READY", "WAITING_IMPLEMENTATION_APPROVAL",
                      "COMPLETE", "BLOCKED", "PAUSED"):
            print(f"[harness] entrevista concluída (phase={phase})")
            print(f"[harness] respostas coletadas: {len(cp.get('interview_answers',{}))}")
            break

        # A pergunta atual do skill (ou gatilho inicial)
        query = cp.get("current_query")
        if not query or phase == "INTENT":
            query = "iniciar bot-memory-kit"
        else:
            # Se há uma pergunta pendente, responde como o usuário fictício
            answer = answer_as_persona(query, persona)
            print(f"  Q: {query}")
            print(f"  A: {answer}")
            # grava resposta no checkpoint
            cp["interview_answers"][f"q{len(cp['interview_answers'])+1}"] = {
                "question": query,
                "answer": answer
            }
            cp["current_response"] = answer
            write_checkpoint(hm, cp)

            # agora pede ao skill para processar a resposta e avançar
            query = f"retomar bot-memory-kit (resposta: {answer})"

        # envia ao Hermes no sandbox
        print(f"  → enviando ao sandbox...")
        resp = hermes_query(hm, query, local=args.local, ollama_key=ollama_key)
        print(f"  ← resposta: {resp[:200]}")

        # O skill deve ter atualizado o checkpoint com a próxima pergunta
        cp = read_checkpoint(hm)
        if cp:
            cp["current_query"] = extract_question(resp, cp)
            write_checkpoint(hm, cp)

    # resultado final
    cp = read_checkpoint(hm)
    if cp:
        print(f"\n[harness] fase final: {cp.get('phase')}")
        print(f"[harness] respostas: {json.dumps(cp.get('interview_answers',{}), indent=2, ensure_ascii=False)[:500]}")

def answer_as_persona(question, persona):
    """Gera uma resposta baseada no perfil do usuário fictício."""
    q_lower = question.lower()

    # mapeamento simples de palavras-chave → resposta do persona
    if any(w in q_lower for w in ["áreas", "responsabilidade", "vida", "trabalho"]):
        return f"Sou {persona['name']}, {persona['role']}. Trabalho com {persona['business']}. Tenho {len(persona['machines'])} computadores que uso para trabalho e infraestrutura. Hobbies: {', '.join(persona['hobbies'])}."

    if any(w in q_lower for w in ["tempo", "ocupam", "rotina", "repete"]):
        return f"O que mais consome tempo: {persona['time_sinks']}."

    if any(w in q_lower for w in ["delegar", "assistente", "gostaria"]):
        return f"Gostaria de delegar: {persona['wants_to_delegate']}."

    if any(w in q_lower for w in ["ferramenta", "usados", "aplicativos", "terminais", "sites"]):
        return f"Uso: {', '.join(persona['tools'])}. Fontes: {persona['knowledge_sources']}."

    if any(w in q_lower for w in ["usaria", "clientes", "equipe", "quem"]):
        return f"Os agentes seriam usados por: {persona['audience']}."

    if any(w in q_lower for w in ["aprovação", "não pode", "privacidade", "sair"]):
        return f"Exige aprovação: {persona['requires_approval']}. Não pode sair: {persona['cannot_leave_device']}."

    if any(w in q_lower for w in ["prefer", "central", "especialista", "sob demanda", "proativas"]):
        return f"Prefiro: {persona['interaction_style']}."

    # resposta genérica
    return persona.get("default_answer", "Não tenho certeza, mas acho que depende do contexto.")

def extract_question(resp, cp):
    """Tenta extrair a próxima pergunta da resposta do skill."""
    # Heurística simples: a resposta do skill contém a próxima pergunta
    # (o skill escreve no checkpoint; se não, pega a última linha)
    if not resp:
        return None
    lines = [l.strip() for l in resp.splitlines() if l.strip()]
    for l in reversed(lines):
        if "?" in l:
            return l
    return lines[-1] if lines else None

if __name__ == "__main__":
    main()