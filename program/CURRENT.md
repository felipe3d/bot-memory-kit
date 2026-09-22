# Estado atual do programa

**Atualizado:** 2026-09-21
**WP ativo:** WP-033 — curadoria assistida de conhecimento (`VERIFIED`); CS-035 publicação VPS (`VERIFIED`)
**Próximo passo único:** nenhum gate pendente. Piloto pessoal local funcional com nota canônica vigente. AgentKnowledge sincronizado Mac→VPS via Git bare. O proprietário decide se amplia fontes, adiciona domínios ou mantém como está.

## Objetivo

Bots pessoais especializados, com memória útil, recuperável e corrigível. Especialização não é proibição de consultar contexto autorizado de outra área. Obsidian permanece autoridade de conhecimento; Mindwtr de tarefas; Odoo de CRM. Consultar não concede escrita, envio, exclusão nem persistência de cópias.

Uso pessoal e exposição a terceiros são casos diferentes; hospedagem na VPS não torna um bot compartilhado. Isolamento rigoroso é requisito para dados/capacidades expostos a outras pessoas, sem dispensar proteção de credenciais e controles de ações de impacto nos bots pessoais.

## Estado documental, prova disponível e verificação atual

| Assunto | O que os documentos registram | Limite nesta revisão |
|---|---|---|
| P0, P1-A, P1-A2, GTD, CRM e gateway dedicado 0.21.3 | Pilotos existentes e preservados; allowlists e MCPs limitados por canal | Não consultamos hosts, perfis ou integrações; não certificamos seu estado atual |
| Contrato de memória e matriz | Aprovação histórica v0.1; direção pessoal incorporada na revisão v0.2 | Política não prova implementação nem todos os testes de segurança |
| Publicação P-0 | `evidence/CS-032-p0-run.md` relata teste com fixture, revogação e limpeza integral, inclusive repo | Cabeçalho histórico ainda diz BLOCKED; seção final relata limpeza. Não reescrevemos a evidência nem a revalidamos remotamente; não há pipeline real permanente comprovada |
| AgentKnowledge | Descoberta anterior relatou canonical vazio | Nesta execução, somente o destino CS-034 foi verificado: uma candidata no inbox, destino canônico próprio vazio; nenhuma varredura do restante do vault |
| CS-033 / publicação VPS | CS-035 executou publicação real: Git bare na VPS, clone read-only, skill instalada | O Hermes da VPS é pessoal do proprietário; sem cron de sync automático; pull manual |
| CS-034 | Execução verificada: helper e skill locais, 23 testes automáticos, aprovação/correção/retirada humanas reais, 3 conversas novas no Desktop com recuperação citada e uso correto | Uma nota canônica vigente (rev. 2, 120 dias). Ver `evidence/CS-034-local-learning-run.md` |
| CS-035 | Publicação VPS verificada: push Mac→VPS, clone read-only, skill personal-learning, nota canônica acessível na VPS | Sem cron; pull manual. Ver `evidence/CS-035-vps-publication.md` |

## Primeiro resultado útil

A IA lê apenas a seção “Acordo com o usuário” do handoff autorizado, sugere até três preferências de colaboração, mostra origem e validade ao proprietário e registra somente o que ele aprovar. Uma conversa nova deve recuperar a nota vigente com citação. Ajuste e retirada também serão testados. A fonte é concreta e já conhecida; nenhum inventário privado é necessário para escolhê-la.

## Limites preservados

- Não alterar pilotos GTD/CRM, gateway, integrações, permissões existentes, backups ou rotas.
- Não sincronizar state.db, homes Hermes ou credenciais; não conceder acesso ao vault inteiro nem tratar sync como ACL.
- Revisão documental anterior concluída. A aprovação posterior cobre somente os arquivos/destinos locais enumerados em CS-034; sem novos acessos, publicação VPS, commit ou push.
- Uma aprovação da entrega cobre implementação, testes, retries seguros e rollback enumerados. Revisão de cada candidata é decisão de conteúdo, não nova aprovação de infraestrutura.
- Parar por acesso/privilégio novo, decisão material, risco inesperado ou falha sem recuperação segura. Não criar novos gates para detalhar trabalho já autorizado.
- Gates e cabeçalhos de ensaios anteriores são históricos e específicos daqueles ensaios, não próximos passos automáticos do WP ativo.

## Leitura seguinte

1. `work-packages/WP-033-assisted-candidate-curation.md`
2. `DECISIONS.md`
3. `change-sets/CS-034-assisted-candidate-curation.md`
4. `handoffs/CS-034.md`
5. `contracts/MEMORY-CONTRACT.md` e `contracts/BOT-POLICY-MATRIX.md`

`PLAN.md` é histórico; `ROADMAP.md` orienta a sequência atual. `EVIDENCE.md` agora aponta também à prova operacional local CS-034, sem reescrever evidências históricas.
