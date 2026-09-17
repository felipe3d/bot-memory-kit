# TODO — Bot Memory Kit

## Sincronização do `AgentKnowledge/` no HomeLab

**Status:** RESOLVED — gate bidirecional passou com SHA-256 idêntico; plano diário ativo.

### Contexto

O bootstrap local foi concluído e validado no MacBook em 2026-09-16:

- Vault criado em `/Users/fac/dev/Obsidian/felipe/AgentKnowledge/`.
- `setup-vault.py --check` passou sem problemas.
- Run privada: `/Users/fac/.hermes/bot-memory-kit-runs/macbook-20260916-094149/`.

O Obsidian Sync nativo foi validado em 2026-09-17 nas duas direções:

- Mac → HomeLab: arquivo chegou com SHA-256 idêntico (`a31722ad…28be`).
- HomeLab → Mac: arquivo chegou com SHA-256 idêntico (`f8c4344c…15cc`).
- A nota diária gerada no HomeLab chegou ao Mac com SHA-256 idêntico (`e0e80d65…bc9b`).
- Nenhum mecanismo paralelo de sincronização foi instalado.

### Automação diária

O plano `~/.hermes/bmk-backups/PLAN-DAILY-0600.md` foi aprovado e aplicado. O HomeLab executa `mindwtr-daily-plan.timer` todos os dias às 06:00 America/Sao_Paulo (`Persistent=true`). O gerador é somente leitura no Mindwtr e grava atomicamente em `AgentKnowledge/projections/daily/`.

Evidências: `~/.hermes/bmk-backups/VERIFY-DAILY-0600.md`.

### Acesso remoto

Incidente resolvido: a chave `id_ed25519_kubuntu` havia saído do `ssh-agent` e foi recarregada pelo Keychain. Os aliases `Kubuntu-Remote` e `Kubuntu-Remote-Tmux` também foram atualizados para a topologia real: `ProxyJump oracle` → `127.0.0.1:9022` na VPS → HomeLab. Acesso local e remoto foram testados.

## Pesquisa do sistema de projetos e tarefas — concluída (2ª rodada, pós-entrevista)

**Status:** PILOTO GTD APLICADO E VERIFICADO — perfil `gtd` isolado, skill única, modelo `glm-5.3`, MCP Mindwtr com 27 ferramentas, toolsets restritos e testes T1–T10 executados; backup cron 02:30 E2E (AES+RSA+Dropbox 7-3-5); issue upstream **#1233** aberta (https://github.com/dongdongbh/Mindwtr/issues/1233). Pendência física: T1 no iPhone (`T1-configuracao-iphone-mac.md`). Evidências do bot: `~/.hermes/bmk-backups/VERIFY-GTD.md`.

### Histórico de método

A 1ª rodada (Vikunja/OpenProject/Plane, 54 fontes) foi reclassificada como levantamento técnico provisório por ter precedido a entrevista funcional. A entrevista foi concluída e confirmada em 2026-09-16; a 2ª rodada de pesquisa foi executada com os critérios funcionais corretos (GTD pessoal, FOSS/self-hosted, VPS, Mac+iPhone offline editável, formato aberto, API).

Artefatos da 2ª rodada (`deleg_c9087c8c`, 6 subagentes):

- Síntese e matriz: `/Users/fac/.hermes/bot-memory-kit-runs/macbook-20260916-094149/memoria/investigacoes/sistema-projetos-tarefas/sintesis-2.md`
- Resultados brutos: `subtask-{0..5}-result.json` no mesmo diretório
- Entrevista funcional: `interview-project-management.md` no mesmo diretório
- Checkpoint durável: `/Users/fac/.hermes/bmk-backups/checkpoint.json`

### Shortlist (2ª rodada)

1. **Mindwtr** — melhor encaixe global (GTD nativo, iOS nativo FOSS offline, servidor self-hosted na VPS, REST/CLI/MCP); risco: projeto jovem, issue de recorrência pós-sync. Recomendado para piloto condicionado a spike de aceitação.
2. **Taskwarrior 3 + TaskChampion Sync Server** — melhor automação e maturidade do núcleo; gargalo: nenhum cliente iOS FOSS maduro (Taskchamp é piloto condicional; recorrência leitura-no-iOS).
3. **organice + WebDAV + arquivos Org** — máxima portabilidade (texto aberto auditável); UX menor, conflitos por arquivo.

Eliminados com evidência: Vikunja, Plane, OpenProject, Leantime, Kaneo (sem fila de mutações offline; service worker cacheia apenas o shell), stacks CalDAV/VTODO (sem cliente iOS FOSS maduro), Joplin Server (licença não-FOSS), Logseq (self-host alpha), Notesnook (self-host sem suporte), Anytype (não-OSI), Super Productivity (API CRUD apenas no desktop Electron).

### Próxima ação

Aprovar e executar o plano de spike em `spike-mindwtr-plano.md` (mesmo diretório da `sintesis-2.md`): versão 1.3.0 congelada, dataset sintético `SPIKE-`, testes T1–T6 + negativos, ambiente descartável, limpeza completa ao final. Nada é instalado antes da aprovação.

### Critério para avançar

Aprovação explícita do próximo passo e, antes de qualquer spike, definição de SLO/RPO/RTO, dataset sintético, versões congeladas, testes negativos e teste obrigatório de export/restore, incluindo: edição offline real no iPhone (modo avião), recorrência pós-sync, conflito concorrente Mac+iPhone e restauração a partir do backup da VPS.

## 2026-09-17 — Automações GTD ativas
- Follow-up de Aguardando: diário 08:00 (VPS, timer mindwtr-followup), alerta só p/ vencidos/sem follow-up no tópico GTD do Telegram. Validado E2E (envio + silêncio).
- Revisão semanal read-only: segunda 06:15 (HomeLab, timer mindwtr-weekly-review), grava projectings/weekly/revisao-<W>.md (sync Obsidian → Mac).
- Plano diário 06:00 já ativo desde o APPLY anterior.
- Skill gtd atualizada (crons reais documentados) e sincronizada com a VPS.
