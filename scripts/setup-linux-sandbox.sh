#!/usr/bin/env bash
# =============================================================================
# setup-linux-sandbox.sh — prepara o sandbox Linux (Docker/OrbStack) do
# bot-memory-kit. Idempotente: pode rodar várias vezes sem duplicar nada.
#
# SEGURANÇA: nunca toca no ~/.hermes real. Todo o estado vive sob
# test-homes/linux-hermes (gitignored). A chave do provider só é injetada
# por env no runtime; NUNCA é gravada em arquivo, checkpoint ou log deste kit.
#
# Uso:
#   ./scripts/setup-linux-sandbox.sh                 # prepara e configura
#   ./scripts/setup-linux-sandbox.sh --check          # só verifica ambiente
#   ./scripts/setup-linux-sandbox.sh chat "pergunta"  # configura e roda 1 chat
#
# Provider/modelo default = ollama-cloud/glm-5.3; sobrescreva por env:
#   PROVIDER=... MODEL=... ./scripts/setup-linux-sandbox.sh chat "..."
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SANDBOX_DIR="$REPO_ROOT/test-homes/linux-hermes"
IMAGE="${HERMES_IMAGE:-nousresearch/hermes-agent:latest}"
PROVIDER="${PROVIDER:-ollama-cloud}"
MODEL="${MODEL:-glm-5.3}"
ACTION="setup"        # setup | check | chat
CHAT_QUERY=""

if [ $# -ge 1 ]; then
  case "$1" in
    --check|-c) ACTION="check" ;;
    chat|--chat) ACTION="chat"; CHAT_QUERY="${2:-}" ;;
    *) ACTION="setup"; CHAT_QUERY="" ;;
  esac
fi

log() { printf '[sandbox] %s\n' "$*"; }
die() { printf '[sandbox] ERRO: %s\n' "$*" >&2; exit 1; }

# --- Docker/OrbStack ---
docker_ready() { docker info >/dev/null 2>&1; }

if ! docker_ready; then
  if command -v orbctl >/dev/null 2>&1; then
    log "Docker (OrbStack) parado — iniciando..."
    orbctl start >/dev/null 2>&1 || die "falha ao iniciar OrbStack"
    for _ in $(seq 1 20); do docker_ready && break; sleep 1; done
  fi
fi
docker_ready || die "Docker não disponível. Inicie Docker/OrbStack e reexecute."
log "Docker pronto: $(docker version --format '{{.Server.Version}}' 2>/dev/null)"

if [ "$ACTION" = "check" ]; then
  log "Ambiente Docker OK. Sandbox isolado: $SANDBOX_DIR"
  exit 0
fi

mkdir -p "$SANDBOX_DIR"
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  log "Baixando imagem $IMAGE (primeira vez, pode demorar)..."
  docker pull "$IMAGE" >/dev/null || die "falha ao baixar imagem"
fi

# Configura provider/modelo (idempotente) e valida dentro do container.
_CONFIGURE_PY='import os, yaml
c = yaml.safe_load(open("/hermes-home/config.yaml"))
assert c["model"]["provider"] == os.environ["PROVIDER"], "provider"
assert c["model"]["default"] == os.environ["MODEL"], "model"
print("config ok:", c["model"]["provider"], c["model"]["default"])'

log "Configurando provider=$PROVIDER model=$MODEL..."
docker run --rm \
  -v "$SANDBOX_DIR:/hermes-home" \
  -e HERMES_HOME=/hermes-home \
  -e PROVIDER="$PROVIDER" -e MODEL="$MODEL" \
  -e PY="$_CONFIGURE_PY" \
  --entrypoint sh "$IMAGE" -c '
    set -e
    hermes config set model.provider "$PROVIDER" >/dev/null
    hermes config set model.default "$MODEL" >/dev/null
    python3 -c "$PY"
  ' 2>/dev/null || die "falha ao configurar model/provider"

# --- Chat headless de validação ---
if [ "$ACTION" = "chat" ]; then
  if [ -z "${CHAT_QUERY}" ]; then
    die "Forneça a pergunta: $0 chat \"sua pergunta\""
  fi
  if [ -z "${OLLAMA_API_KEY:-}" ] && [ -f "$HOME/.hermes/.env" ]; then
    OLLAMA_API_KEY="$(grep -E '^OLLAMA_API_KEY=' "$HOME/.hermes/.env" | head -1 | cut -d= -f2- | tr -d '"' | tr -d "'")" || true
  fi
  if [ -z "${OLLAMA_API_KEY:-}" ]; then
    die "Sem OLLAMA_API_KEY. Exporte-a por env (nunca será gravada)."
  fi
  log "Rodando chat headless: \"$CHAT_QUERY\""
  docker run --rm \
    -v "$SANDBOX_DIR:/hermes-home" \
    -e HERMES_HOME=/hermes-home \
    -e OLLAMA_API_KEY \
    -e CHAT_QUERY \
    --entrypoint sh "$IMAGE" -c 'timeout 120 hermes chat -q "$CHAT_QUERY" -Q' 2>&1
  log "Chat concluído (chave nunca impressa)."
fi

log "Sandbox Linux pronto. Veja docs/sandbox-linux.md."
