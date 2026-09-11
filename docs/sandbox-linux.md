# Sandbox Linux (Docker)

Sandbox para validar o fluxo **headless / automático** (cenário HomeLab/VPS) do bot-memory-kit, sem tocar em nenhum host real.

## O que é

- Container da imagem oficial `nousresearch/hermes-agent:latest` (mesma versão do host, v0.21.x, multi-arch arm64/amd64).
- `HERMES_HOME` isolado em volume `test-homes/linux-hermes` (gitignored) — **nunca** o `~/.hermes` real.
- Provider LLM real `ollama-cloud` + modelo `glm-5.3` por padrão.
- Valida o cenário **automático/24/7** que o Mac sandbox não simula: sem interação, sem TUI, headless.
- **Não tem UI Desktop** (Bot Mode visual) — somente CLI/perfis. A parte visual do Bot Mode só é validável no Desktop local.

## Setup — 1 comando

```bash
./scripts/setup-linux-sandbox.sh            # prepara Docker + configura provider/modelo
./scripts/setup-linux-sandbox.sh --check     # só verifica ambiente Docker
./scripts/setup-linux-sandbox.sh chat "pergunta"   # configura e roda 1 chat headless
```

Idempotente: rodar várias vezes não duplica nem quebra nada.

## Como funciona o script

1. **Docker/OrbStack**: inicia automaticamente via `orbctl start` se estiver parado.
2. **Diretório isolado**: garante `test-homes/linux-hermes`.
3. **Imagem**: baixa `nousresearch/hermes-agent:latest` na primeira vez.
4. **Config**: `hermes config set model.provider ollama-cloud` + `model.default glm-5.3` dentro do container, e valida lendo o `config.yaml` de volta.
5. **Chat (opcional)**: roda `hermes chat -q "<pergunta>" -Q` com a `OLLAMA_API_KEY` injetada por env.

Provider/modelo override:
```bash
PROVIDER=qwen MODEL=qwen3.5:397b ./scripts/setup-linux-sandbox.sh
```

## Segurança da chave

- A `OLLAMA_API_KEY` é **lida do `.env` do host no momento do chat** e passada por env ao container; **nunca** é gravada em arquivo, checkpoint, memória, log ou chat.
- Se você exportar `OLLAMA_API_KEY` no shell, o script usa essa; senão tenta carregar de `~/.hermes/.env`.
- Nenhum segredo transita por artefatos do kit.

## Provedor: nota importante

O provider `ollama-cloud` usa base_url default **`https://ollama.com/v1`** (autentica com `OLLAMA_API_KEY`). Não aponte o sandbox para endpoints proxy self-hosted sem testar a conectividade antes: na validação de 2026-09-11, um endpoint proxy de produção estava fora do ar (HTTP 502/403) e confundiu o diagnóstico — o default nativo do `ollama-cloud` funcionou.

## Validações feitas (2026-09-11)

| Teste | Resultado |
|---|---|
| `--check` com Docker pronto | ✅ `Docker pronto: 29.4.0` |
| Setup idempotente (2×) | ✅ `config ok: ollama-cloud glm-5.3` |
| Chat headless `hermes chat -q` | ✅ responde `sandboxok`, exit 0 |
| Imagem oficial | ✅ v0.21.1 arm64/amd64 |

## Comandos úteis (dentro do container)

```bash
HERMES_HOME=/hermes-home hermes profile list          # perfis
HERMES_HOME=/hermes-home hermes -p <nome> skills list # skills por perfil
HERMES_HOME=/hermes-home hermes profile create <nome> --no-skills  # criação sem catálogo
```

## O que NÃO fazer

- **Nunca** executar `hermes` na raiz do repo sem `HERMES_HOME` apontando para `test-homes/` — tocaria o `~/.hermes` real.
- Não assumir que o container tem `sudo` (a imagem não inclui) — o teste de `sudo -n` é outro cenário/provisionamento.
