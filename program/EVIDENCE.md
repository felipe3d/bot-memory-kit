# Evidence index

| ID | Status | Afirmação | Evidência primária |
|---|---|---|---|
| E-001 | histórico corroborado | P0 identificou superfície Telegram ampla antes da contenção | `/Users/fac/dev/P0-memoria-bots-2026-09-17.md` |
| E-002 | histórico corroborado | P1-A restringiu Telegram dos especialistas e removeu operações MCP proibidas | `/Users/fac/dev/P1-A-contencao-telegram-2026-09-17.md` |
| E-003 | verificado no handoff | P1-A2 usa release dedicado 0.21.3; DBs schema 30 com quick_check ok | `/Users/fac/dev/HANDOFF-memoria-bots-P1A2-2026-09-18.md` |
| E-004 | histórico corroborado | GTD/Mindwtr foi aplicado e verificado; T1 físico do iPhone permanece pendente | `TODO.md` e `~/.hermes/bmk-backups/VERIFY-GTD.md` |
| E-005 | histórico corroborado | AgentKnowledge Mac↔HomeLab teve gate bidirecional; isso não prova fronteira de credencial VPS | `TODO.md`; P0 §§5.3–5.4 |
| E-006 | verificado documentalmente agora | Obsidian Sync compartilhado não oferece permissões granulares; colaboradores recebem as permissões do proprietário, exceto convidar | https://obsidian.md/help/sync/collaborate (consulta pública em 2026-09-18) |
| E-007 | verificado documentalmente agora | 1Password Service Accounts permitem escopo imutável por vault e não podem acessar vaults Personal/Private/Employee/Shared padrão | https://www.1password.dev/service-accounts/get-started ; https://www.1password.dev/service-accounts/security/ (consulta pública em 2026-09-18) |
| E-008 | verificado em spike sintético | Filtro positivo, negação de identidade sintética, write-deny, revogação e falha de integridade operam fail-closed no modelo local CS-030 | `program/evidence/CS-030-phase-1-synthetic-spike.md` |
| E-009 | verificado em discovery documental | GitHub deploy key é exclusiva de um repositório e read-only por padrão; deploy key não expira automaticamente | `program/evidence/CS-030-gate-d-discovery.md`; https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys |
| E-010 | verificado em Gate H mínimo | GitHub/VPS candidatos foram identificados por metadados; produtor e audit store permanecem bloqueados, sem acesso a conteúdo ou segredo | `program/evidence/CS-030-gate-h-minimal.md` |
| E-011 | verificado em preflight Gate P | HomeLab negou `sudo -n`; VPS aceitou, mas nenhuma mutação iniciou sem o publicador isolado | `program/evidence/CS-030-gate-p-preflight.md` |
| E-012 | verificado em piloto Gate P VPS-only | Publicação/validação sintética, key revocation, limpeza VPS e ausência posterior do repositório passaram; não certifica N-01/N-02 reais | `program/evidence/CS-030-gate-p-vps-only-run.md` |
| E-013 | verificado | CS-034: preflight, helper/skill locais, 23 testes automáticos, aprovação/rejeição/correção/retirada humanas reais, 3 conversas novas no Desktop com recuperação citada e uso correto | `program/evidence/CS-034-local-learning-run.md` |

Não incluir segredos, dumps de configurações, state.db, conteúdo pessoal ou dados de clientes neste índice.
