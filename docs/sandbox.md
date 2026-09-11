# Ambiente de teste sandbox

Sandboxes isolados para desenvolver o bot-memory-kit **sem tocar em nenhum host, cofre, vault, memória ou perfil real.**

- **Mac sandbox** (`HERMES_HOME` isolado): valida skill, entrevista, criação de perfil e seleção de skills.
- **Linux sandbox** (Docker/OrbStack): valida o cenário headless/automático (HomeLab/VPS).

## Linux sandbox (Docker)

Setup documentado e ativado por script: **`scripts/setup-linux-sandbox.sh`**.

```bash
./scripts/setup-linux-sandbox.sh            # prepara Docker + configura provider/modelo
./scripts/setup-linux-sandbox.sh --check    # só verifica ambiente Docker
./scripts/setup-linux-sandbox.sh chat "p"   # configura e roda 1 chat headless
```

Detalhes completos: **[docs/sandbox-linux.md](sandbox-linux.md)**.

## Mac sandbox (`HERMES_HOME` isolado)

```bash
export HM="$HOME/dev/bot-memory-kit/test-homes/mac-sandbox"
HERMES_HOME=$HM hermes profile create <nome> --no-skills   # criação
HERMES_HOME=$HM hermes -p <nome> skills list               # seleção
HERMES_HOME=$HM hermes profile delete <nome>               # remoção
```

## Validações já feitas

### Mac sandbox (HERMES_HOME isolado)
- Hermes v0.21.1 (git install) reconhece `HERMES_HOME` isolado; sandbox começa com **0 skills, memória vazia**.
- `profile create --no-skills` cria com **apenas o builtin `hermes-agent`** (sem catálogo) e memória vazia — confirma a **seletividade de skills por bot**.
- **Efeito colateral capturado:** `profile create` gera alias global `~/.local/bin/<nome>` apontando para o sandbox. O kit deve tratar/excluir isso.

### Linux sandbox (container `nousresearch/hermes-agent:latest`)
- Imagem oficial v0.21.1 (mesma versão do host, multi-arch arm64/amd64).
- `HERMES_HOME` isolado em volume; **sem UI Desktop** (Bot Mode visual) — somente CLI/perfis.
- **Provider funcionando de ponta a ponta:** `ollama-cloud` + `glm-5.3` respondem a chat headless (`hermes chat -q`) via `OLLAMA_API_KEY` injetada por env.

## Cuidados

1. **Nunca execute `hermes` sem `HERMES_HOME` apontando para `test-homes/`** — tocaria o `~/.hermes` real.
2. `profile create` no sandbox **ainda cria alias global** `~/.local/bin/<nome>` — remover após o teste.
3. Não versionar conteúdo de runtime (`test-homes/` está no `.gitignore`).
4. Remover perfis de teste com `rm -rf test-homes/mac-sandbox/profiles/<nome>` (o `hermes profile delete` exige confirmação interativa).
