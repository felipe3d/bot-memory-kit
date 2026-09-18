# Estado atual do programa

**Atualizado:** 2026-09-17  
**WP ativo:** WP-010 — contrato de memória (`PLANNED`)  
**Próximo passo único:** abrir uma sessão nova exclusivamente para detalhar o WP-010; nenhuma implementação fora do repositório está autorizada.

## Objetivo

Construir um ecossistema de bots com memória útil, revisável e isolada, preservando autoridades: Obsidian para conhecimento, Mindwtr para GTD e Odoo para CRM.

## Fatos verificados relevantes

- P0, P1-A e P1-A2 foram concluídos; o piloto do gateway usa release dedicado 0.21.3 e deve permanecer preservado.
- GTD e CRM são perfis/pilotos reais; suas operações e dados não fazem parte deste WP.
- Telegram dos especialistas está contido por allowlists; GTD e CRM usam somente MCPs permitidos no canal.
- AgentKnowledge existe como conhecimento estruturado; a arquitetura de acesso 24/7 com menor privilégio ainda não foi selecionada/aplicada.

## Pendências do programa

- Contrato completo de lifecycle, proveniência, ACL e expiração da memória.
- Matriz integral de bots, audiências, dados, grants e kill switches.
- Decisão e prova de isolamento para AgentKnowledge/VPS.
- Testes de recuperação citada, isolamento entre perfis e prompt injection em notas.
- Seleção do primeiro domínio novo após a fundação.

## Guardrails

- Não sincronizar state.db, homes Hermes ou credenciais.
- Não expor o vault pessoal inteiro a Headless nem confiar em selective sync como fronteira.
- Não alterar gateway, release, unit, backups, perfis, credenciais, vaults ou rotas Telegram sem change set aprovado.
- Não tratar transcript como fonte de verdade operacional.

## Leitura seguinte

1. `work-packages/WP-000-control-plane.md`
2. `DECISIONS.md`
3. `EVIDENCE.md`
