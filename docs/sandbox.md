# Ambiente de teste sandbox

Permissões de acesso ao sandbox Mac notebook. Nada aqui é secreto; os segredos só são injetados quando necessário para validar fluxos.

## Por que sandbox

- **Isolamento:** `HERMES_HOME` aponta para `test-homes/`, separado do `~/.hermes` real.
- **Nenhum host, cofre, vault, memória ou perfil real é alterado.**
- Docker (Linux) para validar automático/headless/`sudo -n`; Mac sandbox para validar a skill e a entrevista.

## Uso

```bash
export HM=/Users/fac/dev/bot-memory-kit/test-homes/mac-sandbox
HERMES_HOME=$HM hermes profile create <nome> --no-skills   # criação
HERMES_HOME=$HM hermes -p <nome> skills list               # seleção
HERMES_HOME=$HM hermes profile delete <nome>               # remoção
```

## Validações já feitas (2026-09-10)

### Mac sandbox (HERMES_HOME isolado)
- Hermes v0.21.1 (git install) reconhece `HERMES_HOME` isolado; sandbox começa com **0 skills, memória vazia**.
- `profile create --no-skills` cria com **apenas o builtin `hermes-agent`** (sem catálogo) e memória vazia — confirma a **seletividade de skills por bot** (requisito central do kit).
- **Efeito colateral capturado:** `profile create` gera alias global `~/.local/bin/<nome>` apontando para o sandbox. **Criar perfis em `HERMES_HOME` de teste ainda cria alias global do usuário real** — o kit deve tratar/excluir isso (o alias não deve sobreviver à remoção).

### Linux sandbox (container `nousresearch/hermes-agent:latest`)
- Imagem oficial v0.21.1 (mesma versão do host, multi-arch arm64/amd64).
- `HERMES_HOME` isolado em volume; **sem UI Desktop** (Bot Mode visual) — somente CLI/perfis.
- **Provider funcionando de ponta a ponta:** `config set model.provider ollama-cloud` + `model.default glm-5.3`, com `OLLAMA_API_KEY` injetada por env, responde a chat headless (`hermes chat -q`). Imagem não tem UI Desktop nem `sudo`.

## Provedor no sandbox Linux

```bash
# config (persistido no volume /hermes-home)
HERMES_HOME=/hermes-home hermes config set model.provider ollama-cloud
HERMES_HOME=/hermes-home hermes config set model.default glm-5.3

# chat headless (chave injetada por env, nunca impressa)
OLLAMA_API_KEY=<value da chave real via env> \
  hermes chat -q "pergunta" -Q
```

**Nota de validação (2026-09-11):** o provider real usa base_url default `https://ollama.com/v1` (não o homelab). O config de produção (`homelab.fibradev.com/api/llm/dyn_bonsai`) estava **fora do ar** (HTTP 502/403) — não usar esse endpoint como default no sandbox; o `ollama-cloud` nativo funciona.


## Cuidados

1. **Nunca execute os comandos acima sem `HERMES_HOME` apontando para `test-homes/`.** Sem o env var, `hermes profile create` tocaria o seu `~/.hermes` real.
2. **O alias global `~/.local/bin/<nome>` é criado como efeito colateral** mesmo no sandbox — remover após criação/remoção do perfil de teste.
3. Não versionar conteúdo de runtime (`test-homes/` está no `.gitignore`).
4. Remover perfis de teste com `rm -rf test-homes/mac-sandbox/profiles/<nome>` (o comando `hermes profile delete` exige confirmação interativa que não se encadeia bem em shell).
