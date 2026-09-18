# Bot Memory Kit

Kit replicável para descobrir necessidades, planejar e implantar bots e memória no Hermes Agent — via entrevista guiada, gates de aprovação e verificação de aceitação.

**Status do kit:** ciclo completo validado end-to-end em sandbox (entrevista 18 perguntas → gates de aprovação → APPLY idempotente → VERIFY 16/16 → COMPLETE). O kit também subsidiou pilotos reais GTD/CRM, documentados fora do repositório com evidências próprias.

**Estado do programa:** o plano de controle atual está em [`program/`](program/README.md). Comece por [`program/CURRENT.md`](program/CURRENT.md), não por transcrições antigas nem pelo status histórico deste README.

## O que é

Uma skill Hermes que conduz a implantação de bots com memória isolada em quatro fases com aprovação humana explícita em cada transição crítica:

```
INTENT → INTERVIEW → SCOPE_APPROVED → CONSENT_PER_HOST → DISCOVERY
  → SELECTION → ARCHITECTURE → PLAN_READY
  → WAITING_IMPLEMENTATION_APPROVAL → APPLY → VERIFY → COMPLETE
```

- **Gatilho explícito**: só inicia com "iniciar/retomar/consultar bot-memory-kit". Menção casual a "memória" não dispara nada.
- **Seleção positiva**: perfis criados com `--no-skills`; cada skill/ferramenta/MCP aprovada item a item.
- **Segredos nunca no chat**: credencial via env/armazenamento protegido; o skill nunca lê, grava ou pede valores.
- **Checkpoint durável** em `<HERMES_HOME>/bmk-backups/` — sobrevive a interrupções e retomadas sem transcript.
- **Falha fechada**: bloqueios legítimos com motivo claro, sem contorno inseguro.
- **Nada apagado às cegas**: divergências vão para quarentena reversível.

## Estrutura

```text
skill/
├── SKILL.md                  # orquestrador das fases + gates
├── references/               # carregadas sob demanda
│   ├── consent-and-discovery.md   # consentimento multi-host, autorizações em camadas
│   ├── selection-and-safety.md    # seleção positiva, gate de modelo por fase
│   ├── memory-migration.md        # auditoria e migração de memória por item
│   ├── secrets-and-privileges.md  # 1Password SA, broker isolado, sudo -n
│   ├── canonical-knowledge.md     # topologia do vault Obsidian
│   └── resume-protocol.md         # checkpoint, retomada, idempotência
└── templates/
    ├── interview.md          # 18 perguntas em 5 blocos
    ├── checkpoint.json       # schema do checkpoint
    └── acceptance-tests.md   # T1-T16 de verificação

scripts/
├── setup-linux-sandbox.sh    # sandbox Docker idempotente (ollama-cloud + glm-5.3)
└── run-interview-test.py     # harness: entrevista automática com usuário fictício

docs/                         # validações e resultados de teste
hermes-research.md            # pesquisa citada: capacidades Hermes
memory-secrets-research.md    # pesquisa citada: memória canônica + segredos unattended
```

## Quick start

1. Instale a skill: copie `skill/` para `<HERMES_HOME>/skills/bot-memory-kit/`.
2. Diga: **"iniciar bot-memory-kit"**.
3. Responda a entrevista (18 perguntas, uma por vez, retomável).
4. Aprove escopo → seleção → plano (3 gates).
5. O skill aplica com idempotência e verifica com os 16 testes de aceitação.

Sandbox Linux para desenvolvimento/teste:

```bash
./scripts/setup-linux-sandbox.sh                 # prepara Docker + provider
./scripts/setup-linux-sandbox.sh chat "pergunta" # valida chat headless
```

## Requisitos acordados

- Um ou vários computadores; um proprietário por bot, sem sincronizar `state.db` entre processos.
- Skills, ferramentas, MCPs, conhecimento e permissões seletivos por bot.
- Obsidian/Markdown como conhecimento canônico; memória nativa compacta, skills procedimentais e histórico separados.
- Auditoria e migração com backup, aprovação e validação; nada apagado silenciosamente.
- Privilégios administrativos por operações autorizadas (`sudo -n` + regras específicas), não senha armazenada nem `NOPASSWD: ALL`.
- Estado persistente fora da conversa, retomada, bloqueio concorrente.
- Instalação inicial e manutenção sob demanda; sem rotinas automáticas criadas implicitamente.

## Separação de dados

Este repositório contém apenas método, documentação, templates, scripts e testes. Respostas pessoais, inventários reais, backups, credenciais e estado de implantação pertencem a um diretório privado externo (`test-homes/` é gitignored).

## Artefatos duráveis (dentro do HERMES_HOME do destino)

```text
bmk-backups/
├── checkpoint.json       # fonte de verdade da retomada
├── PLAN.md               # plano aprovado (T2)
├── profiles-<label>/     # backup pós-implantação
└── quarantine-<name>/    # quarentena reversível (nada apagado às cegas)
```

## Validações realizadas

| Teste | Resultado | Evidência |
|---|---|---|
| Entrevista completa (18 perguntas) | ✅ | `docs/verify-complete-2026-09-11.md` |
| Gates de aprovação (3 gates) | ✅ | idem |
| APPLY com `--no-skills` e idempotência | ✅ | `docs/retest-apply-2026-09-11.md` |
| VERIFY T1–T16 | 16/16 pass | `docs/verify-complete-2026-09-11.md` |
| Checkpoint durável + retomada sem transcript | ✅ | idem |
| Falha fechada (sudo/credencial) | ✅ | idem |

Limitações conhecidas (MVP): T12 (sudo) e T13 (broker) parciais no container; o teste real desses é no host-alvo. Segredos de produção (1Password SA, broker em conta separada) são documentados em `references/secrets-and-privileges.md` mas não exercitados no sandbox.

## Changelog

Veja [CHANGELOG.md](CHANGELOG.md).

## Licença

MIT — veja [LICENSE](LICENSE).