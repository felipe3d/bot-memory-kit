# Handoff — Piloto real no MacBook

**Data:** 2026-09-11  
**Status:** pronto para iniciar uma nova sessão; **nenhuma alteração no Hermes de produção foi feita ainda**.

## Objetivo da próxima sessão

Executar a **Fase 3** do Bot Memory Kit no MacBook, de forma gradual e com aprovação humana por etapa:

1. Criar e verificar `AgentKnowledge/` dentro do vault real sincronizado do Obsidian.
2. Rodar a entrevista real com warm-start, usando a memória real do Hermes como hipóteses confirmáveis.
3. Produzir e aprovar o plano de bots, memória, skills e acessos.
4. Criar **somente o bot-piloto aprovado** no `~/.hermes` real.
5. Verificar o resultado em uma sessão nova antes de declarar pronto.

**Não assumir que o primeiro bot será `infra`.** A entrevista e a aprovação final definem o piloto. `infra` é apenas o candidato atual mais natural.

---

## Repositório e release

- Repo local: `/Users/fac/dev/bot-memory-kit`
- Repo público: <https://github.com/felipe3d/bot-memory-kit>
- Release: <https://github.com/felipe3d/bot-memory-kit/releases/tag/v1.0.0>
- Branch: `main`
- Último commit confirmado antes deste handoff: `b86faa1` (VAULT_SETUP); commits posteriores incluem curadoria/release/warm-start/autostart. **Na nova sessão, rodar `git -C /Users/fac/dev/bot-memory-kit log --oneline -5` e `git status --short` para confirmar o estado atual.**

## Estado do kit

### Validado no sandbox

O ciclo completo foi exercitado no Docker com Hermes v0.21.1 + `ollama-cloud`/`glm-5.3`:

```text
entrevista → warm-start → gates de aprovação → VAULT_SETUP
→ APPLY com --no-skills → VERIFY T1–T16 → COMPLETE
```

Achados reais já corrigidos:

1. Perfil criado sem `--no-skills` semeia o catálogo inteiro → flag agora obrigatória no `SKILL.md`.
2. Checkpoint/PLAN em `/opt/data` se perde entre containers → artefatos duráveis obrigatórios em `<HERMES_HOME>/bmk-backups/`.
3. Docker oficial fixa `HERMES_WRITE_SAFE_ROOT=/opt/data` → sandbox deve sobrescrever com `HERMES_WRITE_SAFE_ROOT=/hermes-home` para gravar no volume.
4. Run `COMPLETE` não é retomado por `iniciar`; apenas `retomar` pode continuar um run ativo.
5. Single-query sem usuário não deve supor respostas → bloquear `awaiting_user_input`.
6. Warm-start confirmado: cartão com fatos+origem, correções `superseded`, blocos de segurança/autonomia sempre abertos.

### Arquivos principais

- `skill/SKILL.md` — fluxo, gates, APPLY, VAULT_SETUP.
- `skill/references/` — consentimento, seleção, memória, segredos, conhecimento canônico, retomada.
- `skill/templates/` — entrevista, checkpoint, acceptance tests.
- `scripts/setup-vault.py` — cria/verifica vault de conhecimento de forma idempotente.
- `scripts/setup-linux-sandbox.sh` — sandbox Docker.
- `docs/verify-complete-2026-09-11.md` — evidências T1–T16.
- `docs/warm-start-validated-2026-09-11.md` — evidência do warm-start.

---

## Ambiente real — MacBook

### Hermes

- App: `/Applications/Hermes.app`
- CLI: `/Users/fac/.hermes/hermes-agent/venv/bin/hermes`
- Hermes home real: `/Users/fac/.hermes`
- Perfil atual: `default`
- Não modificar outro perfil.
- Modelo atual desta conversa: `gpt-5.6-terra` via `openai-codex` (não presumir o modelo da próxima sessão; consultar configuração/modelo ativo antes de APPLY).
- Para APPLY, o kit recomenda `glm-5.3` ou modelo equivalente/mais forte; avisar se a fase estiver em Flash.

### Memória real a auditar durante a entrevista

O `default` possui memória próxima da capacidade. Na próxima sessão:

1. **Não copiar nem apagar imediatamente.**
2. Usar warm-start: apresentar um cartão de hipóteses extraídas de USER/MEMORY e pedir confirmação/correção.
3. Blocos de autonomia, privacidade, aprovação e custo são sempre perguntas abertas.
4. Correções ao USER/MEMORY original são propostas; não editar sem aprovação explícita.
5. Antes de qualquer migração: backup → inventário → classificação → aprovação por item → sessão nova de verificação.

### Obsidian

- Vault autoritativo do Mac: `/Users/fac/dev/Obsidian/felipe`
- Obsidian Sync nativo ativo (`.obsidian/core-plugins.json` contém `"sync": true`).
- `remotely-save` está instalado como diretório, mas desativado (`community-plugins.json = []`). Usuário autorizou desinstalar, mas a desinstalação é cosmética e não é pré-requisito do piloto.
- **Criar o knowledge vault do kit como subpasta:**

```text
/Users/fac/dev/Obsidian/felipe/AgentKnowledge/
```

Isso garante que ele herda o Sync nativo existente.

### HomeLab

Verificado em 2026-09-11:

- Obsidian snap `1.13.7` instalado: `/snap/bin/obsidian`.
- Vault sincronizado: `/home/fac/Obsidian/Felipe`.
- Sync nativo ativo no core plugins.
- 764 Markdown notes no HomeLab, mesmo total do Mac.
- `! INBOX.md` idêntico byte-a-byte: 10.364 bytes nos dois lados.
- SDDM autologin existente para `fac` / Plasma.
- Autostart criado e validado:

```text
/home/fac/.config/autostart/obsidian.desktop
Exec=/snap/bin/obsidian
```

- Obsidian Sync exige app aberto; autologin + autostart tornam isso automático após boot.
- Não instalar outro mecanismo de sync (Git/Headless/Remotely Save) sem necessidade. O Sync nativo já cobre o vault.

---

## Política de segurança obrigatória

### Consentimento por host

Separar autorizações:

```text
metadata_only ≠ read_selected ≠ apply_selected
≠ configure_credentials ≠ start_services
```

Para o piloto MacBook, pedir e registrar primeiro `metadata_only`; leitura do vault e apply exigem aprovações próprias.

### Segredos

- 1Password é a fonte canônica para credenciais pessoais.
- Não pedir, ler, imprimir ou registrar senha/API key em chat, checkpoint, skill ou vault.
- Bots recém-criados não recebem credenciais.
- 1Password Service Accounts + broker isolado pertencem a etapa posterior, após piloto de bot e memória.

### Privilégios

- Não usar senha sudo armazenada.
- `sudo -n` + regras específicas é o desenho posterior.
- Sem `NOPASSWD: ALL`.
- Para o piloto Mac, nenhuma regra sudo precisa ser criada.

### Criação do bot

Nunca usar clone:

```bash
# obrigatório no futuro APPLY, após plano aprovado
hermes profile create <nome> --no-skills
```

Criar com `--no-skills`, instalar somente skills aprovadas uma a uma, aplicar SOUL/config/memória aprovados, comparar o inventário final com `selected_items`.

---

## Fluxo recomendado para a nova sessão

### Etapa 0 — Preparar e confirmar, sem mudanças

1. Carregar skills relevantes: `hermes-agent`, `hermes-memory-systems`, `hermes-profile-management`, `obsidian` e `iterative-planning`/`writing-plans` se for necessário planejar mais profundamente.
2. Conferir estado do repo local e release.
3. Criar um diretório privado de run **fora do repositório e fora do vault**, por exemplo:

```text
/Users/fac/.hermes/bot-memory-kit-runs/macbook-<timestamp>/
```

Ele conterá checkpoint, consentimentos, plano e backups. Não colocar valores de segredos.
4. Confirmar com o usuário que o escopo inicial é MacBook, somente metadados.

### Etapa 1 — VAULT_SETUP no vault real

1. Dry-run:

```bash
/Users/fac/.hermes/hermes-agent/venv/bin/python3 \
  /Users/fac/dev/bot-memory-kit/scripts/setup-vault.py \
  --dry-run \
  --path /Users/fac/dev/Obsidian/felipe/AgentKnowledge \
  --hosts mac-notebook,homelab,oracle \
  --owner felipe
```

2. Mostrar a lista prevista e pedir aprovação explícita.
3. Aplicar o script (sem `--dry-run`).
4. Rodar `--check` e registrar o resultado.
5. Confirmar Sync: aguardar a pasta chegar em `/home/fac/Obsidian/Felipe/AgentKnowledge/`, sem escrever no HomeLab.

### Etapa 2 — Entrevista real com warm-start

1. Gatilho explícito: `iniciar bot-memory-kit`.
2. Gerar cartão de confirmação a partir da memória real do perfil `default` e somente de conteúdo de vault autorizado.
3. Pedir confirmação/correção; registrar `known_facts` e `corrections` no checkpoint privado.
4. Pular apenas Blocos 1–3 que tenham confirmação; nunca pular Blocos 4–5.
5. Produzir proposta de bots, host proprietário, skills, ferramentas/MCPs, conhecimento do vault e limites.

### Etapa 3 — Plano e primeiro gate

1. Plano durável em:

```text
<run-dir>/PLAN.md
```

E uma cópia/artefato no local de backup do kit conforme o caminho que for definido para o run.
2. Mostrar as mudanças propostas incluindo:
   - paths;
   - aliases;
   - perfil novo;
   - SOUL;
   - skills;
   - config;
   - memórias;
   - acesso ao vault;
   - o que explicitamente fica de fora (gateway, cron, segredos, sudo).
3. Esperar aprovação explícita para APPLY.

### Etapa 4 — APPLY do piloto MacBook

Só após aprovação:

1. Criar lock de run.
2. Backup do estado alvo/original antes de tocar.
3. Criar **somente o bot aprovado** com `--no-skills`.
4. Aplicar SOUL/config/memória/skills individualmente.
5. Nenhum gateway, cron, Service Account ou sudo neste piloto inicial.
6. Configurar escopo de leitura do `AgentKnowledge`; bots escrevem somente em `inbox/mac-notebook/`.

### Etapa 5 — VERIFY real

Executar os testes aplicáveis T1–T16. O piloto não pode ser declarado pronto sem:

- sessão nova comprovando memória;
- inventário final igual à lista aprovada;
- bot com acesso à pasta autorizada do vault;
- bot sem acesso a pasta fora do escopo;
- retomada pelo checkpoint;
- backup existente e legível;
- re-execução idempotente;
- nenhum segredo em artefato/saída.

T12/T13 (sudo/broker) podem ficar `skipped` com justificativa explícita, pois estão fora do primeiro piloto.

---

## Critérios para encerrar a nova sessão

- O `AgentKnowledge/` real existe no Mac e foi verificado no HomeLab via Sync.
- Entrevista real e correções estão registradas, sem segredos.
- Plano aprovado ou bloqueado claramente — não avançar por inferência.
- Se APPLY ocorreu: bot-piloto criado com seleção positiva e VERIFY real concluído.
- Se faltar uma decisão do usuário, deixar fase `PAUSED`/`BLOCKED` com `next_step` claro e não improvisar.

## Não fazer na nova sessão

- Não criar o bot diretamente no HomeLab antes do piloto MacBook.
- Não instalar outro sync no HomeLab.
- Não usar `/opt/data` ou `/tmp` para checkpoint/PLAN durável.
- Não retomar uma run `COMPLETE` com `iniciar`.
- Não desinstalar remotly-save como parte do piloto; é opcional e não bloqueia nada.
- Não usar credenciais existentes do perfil default em um novo bot por clone ou copy.
