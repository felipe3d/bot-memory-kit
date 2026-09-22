# Roteiro — bots pessoais úteis

**Direção vigente:** acordo em `handoffs/SESSION-PROMPT-PERSONAL-BOTS.md`. Revisão documental concluída; execução de CS-034 aprovada, `IN_PROGRESS`, com uma candidata aguardando decisão de conteúdo.

| Trabalho | Situação e finalidade | Dependência real |
|---|---|---|
| WP-000 | Controle documental existente | Manter estado, decisões e handoff coerentes; sem commit nesta revisão |
| WP-010 / WP-020 | Contrato e matriz historicamente aprovados; revisão v0.2 distingue pessoal e compartilhado | Preservar autoridades, proveniência, revisão e controles de impacto; aprovação documental não comprova runtime |
| WP-030 / WP-031 / WP-032 | Histórico de isolamento/perímetro/pipeline e ensaios sintéticos | Consultar evidência específica quando necessário; não declarar fundação integralmente testada |
| **WP-033 / CS-034** | **Entrega em execução: helper/skill locais instalados, testes automáticos passaram, candidata aguardando revisão humana** | Aprovação de execução já recebida; faltam decisão de conteúdo e conversas novas reais |
| CS-033 / publicação VPS | Alternativa adiada; publicação real continua bloqueada no registro histórico | Retomar somente se o caso exigir consumo remoto; não bloqueia aprendizado local |
| WP-040 | Recuperação citada, correção, retirada e provas negativas | Exercitar o subconjunto necessário dentro de CS-034, sem exigir concluir toda a suíte antes de entregar valor |
| WP-050 | Possível domínio novo | Só depois de demonstrar utilidade em bot existente e decidir o caso; não criar outro bot por padrão |

## Ordem prática

Implementação local CS-034 e testes automáticos concluídos → revisar a candidata → comprovar recuperação em conversa nova, correção e retirada reais → decidir a próxima necessidade com o usuário.

Não existe dependência universal “publicar na VPS antes de aprender”. Bot pessoal remoto continua pessoal; exposição a terceiros exige a fronteira técnica correspondente antes de expor dados ou capacidades.

## Preservações

GTD, CRM, P1-A2, gateway, integrações, permissões existentes, backups e rotas ficam intactos. Obsidian guarda conhecimento, Mindwtr tarefas e Odoo CRM. Consulta autorizada entre áreas não transfere funções, nem autoriza copiar estado vivo ou segredos para memória.

A implementação recebeu uma aprovação da entrega inteira; não se pedirá nova aprovação para detalhar etapas já cobertas. A pessoa continuará aprovando/rejeitando/ajustando cada sugestão em português simples. Novo acesso/privilégio, decisão material, risco inesperado ou falha sem recuperação segura interrompem a execução.
