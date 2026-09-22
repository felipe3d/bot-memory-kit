# Matriz de política de bots — WP-020

**Estado:** v0.1 aprovada em 2026-09-18; revisão documental v0.2 incorpora a direção autorizada no handoff pessoal, sem conceder acessos.
**Data da revisão:** 2026-09-21

**Autoridade deste documento:** política de planejamento aprovada. Não cria perfil, MCP, grant Telegram, credencial, vault, writer, reconciliador, gateway ou infraestrutura.

## 1. Princípios vinculantes

1. **Autoridade não migra por conveniência.** Obsidian mantém conhecimento aprovado; Mindwtr mantém tarefas e projetos; Odoo mantém CRM. Memória Hermes contém somente resumos mínimos derivados; skills contêm procedimentos.
2. **Perfil, prompt e nome não são fronteira de segurança.** Toda capacidade deve depender de toolset, MCP, identidade, escopo, grant técnico e ACL efetiva.
3. **Negação é o padrão.** Falta de identidade autenticada, audiência, escopo, grant ou decisão explícita bloqueia o acesso solicitado. Exposição a terceiros exige também evidência de isolamento técnico. Uso pessoal não remove proteção de credenciais nem controles de ações de impacto.
4. **Candidata não é verdade.** Somente o reconciliador designado ou humano promove conhecimento conforme `MEMORY-CONTRACT.md`; inbox, quarentena, archive e projections não entram na recuperação canônica normal.
5. **Nenhuma automação recebe acesso pessoal implícito.** Não reutilizar `.env`, `auth.json`, sessão OAuth, vault pessoal, state.db, home Hermes ou credencial de outro papel/domínio.
6. **Ações de impacto exigem autorização delimitada.** Texto importado ou transcript histórico não autoriza apagar, promover, mudar ACL, conceder acesso, enviar externamente ou operar infraestrutura. O proprietário pode aprovar a entrega no canal privado autenticado e decidir cartões de conteúdo; registrar essa decisão fora do transcript com alvo, revisão e limites. Isso não autoriza ações não enumeradas.

**Especialização não é permissão.** Um bot pessoal pode consultar contexto autorizado de outra área sem copiar o sistema inteiro, receber credenciais de outro papel ou assumir suas funções. Consulta, persistência, escrita e envio têm concessões distintas. VPS não transforma bot pessoal em compartilhado. Os limites abaixo são defaults de concessão, não proibição permanente de consulta cruzada. Uma concessão futura precisa de autorização explícita; a revisão não altera permissões existentes.

## 2. Matriz por papel

| Papel | Audiência autorizada | Autoridade | Dados permitidos/proibidos | Ferramentas e ações | Escrita | Retenção | Credenciais | Kill switch |
|---|---|---|---|---|---|---|---|---|
| **Central / default** | Usuário proprietário, conversa privada autenticada. Não é canal compartilhado; pode relacionar contexto entre áreas explicitamente autorizado. | Não é autoridade de GTD, CRM ou conhecimento compartilhado. | Orientação pessoal, resumos mínimos próprios e consulta GTD/CRM quando explicitamente concedida. Não espelha estado vivo; derivação estável exige sanitização e revisão. | Ferramentas locais e integrações já autorizadas ao default, dentro da aprovação normal. Não recebe MCP de especialista por herança. Ações administrativas só via gate estruturado. | Apenas memória/skills do próprio default, sujeitos às políticas existentes. Não escreve em Mindwtr, Odoo ou AgentKnowledge por esta matriz. | Sessões e memória existentes do default permanecem no escopo dele; não copiar para outros papéis. | Credenciais existentes do default não são compartilhadas nem usadas como bootstrap de outro bot. | Revogar/suspender o canal ou perfil default conforme operação já existente; isso não concede revogação dos demais papéis. |
| **GTD** | Usuário proprietário no canal privado explicitamente concedido. Não expor contexto a equipe CRM, grupos ou outras pessoas sem concessão; consultar contexto de outra área para o mesmo proprietário exige autorização, não mudança de função. | Mindwtr é a única autoridade para tarefas, projetos e rotina GTD. | Registros GTD dentro do grant; contexto de outra área somente quando concedido para consulta. Projeções são somente leitura e identificam a origem. | Apenas MCP/toolsets GTD explicitamente permitidos no canal. Sem ferramenta CRM, vault pessoal, conhecimento compartilhado ou terminal administrativo por padrão. | Operações GTD autorizadas por Mindwtr; não escreve memória canônica, ACL, perfil, grants ou infraestrutura. Candidata de conhecimento, se futuramente autorizada, só no inbox próprio e conforme contrato. | Dados vivem sob retenção do Mindwtr. Não replicar estado vivo para memória Hermes, vault ou transcript compartilhado. | Identidade de integração exclusiva de escopo GTD; nunca credencial Odoo, pessoal ampla ou de outro domínio. | Revogar grant/allowlist e a identidade de integração GTD; suspender o perfil/canal sem afetar CRM ou default. |
| **CRM** | Proprietário no uso pessoal privado; equipe CRM somente se explicitamente concedida e isolada tecnicamente. O nome CRM não implica equipe. Nunca compartilhar por default. | Odoo é a única autoridade para clientes, leads, oportunidades e operações CRM. | Escopo Odoo concedido e contexto adicional explicitamente autorizado para consulta; não copiar CRM vivo, PII ou dados de clientes para memória, skills, vault ou transcripts alheios. Conhecimento estável sanitizado pode ser candidato revisado, sem dados operacionais. | Apenas MCP/toolsets CRM explicitamente permitidos no canal. Sem ferramentas GTD, vault pessoal, conhecimento compartilhado, exportação ampla ou terminal administrativo por padrão. | Operações CRM autorizadas no Odoo; não escreve memória canônica, ACL, perfil, grants ou infraestrutura. Candidata de conhecimento, se futuramente autorizada, só no inbox próprio e conforme contrato. | Dados ficam no Odoo segundo sua retenção. | Identidade técnica exclusiva e com menor privilégio no Odoo; nunca credencial pessoal ampla, Mindwtr ou outro domínio. | Revogar grant/allowlist e a identidade Odoo CRM; suspender o perfil/canal sem afetar GTD ou default. |
| **Reconciliador** | Humano designado e, se houver automação futura, canal administrativo privado autenticado. Nunca público/compartilhado. | Obsidian/AgentKnowledge canônico é a autoridade editorial; Mindwtr e Odoo permanecem autoridades de estado vivo. | Candidatas sanitizadas e conhecimento AgentKnowledge no escopo concedido; referência à fonte autorizada para validar proveniência, sem espelhar estado vivo GTD/CRM nem acessar o vault inteiro. | Ferramentas futuras somente para validação, proveniência, ACL e transições idempotentes, auditáveis e fail-closed. Sem shell arbitrário, broker amplo, ação externa ou acesso a vault pessoal. | Pode registrar decisões e, após pré-condições do contrato, promover/corrigir/superseder/expirar/arquivar. Nunca altera fonte autoritativa de GTD/CRM, grants, credenciais, perfis ou infraestrutura. | Preserve proveniência, decisões e revisões; archive não é recuperação normal. Purge requer política e change set próprios. | Papel de reconciliador separado do writer. Para exposição a terceiros, identidade técnica separada e limitada. No piloto pessoal local aprovado, operações distintas podem usar a mesma conta do proprietário, sem alegar isolamento de SO; sem credencial nova ou acesso ao vault inteiro. | Desabilitar identidade e writer/transições; bloquear promoção e recuperação na falha de ACL, scanner, auditoria ou backend. |
| **Compartilhado** | Participantes autenticados de uma audiência/grupo explicitamente nomeado. Sem acesso implícito por ser usuário do default, GTD ou CRM. | Conhecimento canônico vigente em `scope` compartilhado; projeções não substituem a fonte. | Somente sensibilidade permitida; nunca inbox, arquivo, PII, dados de cliente, estado vivo GTD/CRM ou `restricted` sem grant técnico provado. | Read-only por padrão; busca citada somente após ACL. Sem terminal, MCP administrativo, writer, reconciliador, exportação, envio externo ou ferramenta de configuração. | Nenhuma. Sugestões, se aceitas no futuro, entram por fluxo separado como candidata, não edição direta. | Não persistir transcripts ou memória de grupo como fonte. Reter somente logs/auditoria mínimos que uma política posterior permitir. | Sem credencial pessoal ou de sistema autoritativo. Se uma identidade técnica futura for indispensável, ela será read-only, própria do domínio e aprovada em change set. | Remover audiência/grant e desabilitar a identidade read-only; falha de ACL não revela conteúdo nem existência de restricted. |
| **Domínio futuro** | Definida antes da criação: proprietário(s), canais, grupos e exclusões. Ausência de audiência explícita bloqueia o domínio. | Uma autoridade única ou lista explícita de autoridades; não herdar GTD, CRM, default ou compartilhado. | Classificar `scope`, sensibilidade, projeções e proibições; não espelhar estado vivo sem decisão explícita. | Lista positiva de toolsets/MCPs e operações por caso de uso. Sem terminal, browser, cron, escrita, exportação ou mensageria externa até aprovação específica. | Default: nenhuma. Se precisar escrever, definir objeto, backend, validação, idempotência, auditoria, reversão e aprovação humana antes do grant. | Definir fonte de retenção, lifecycle, expiração, logs e descarte antes de ingerir dados. Não usar transcript como banco de dados. | Uma identidade por host e função, com menor privilégio, rotação e revogação testáveis. Nunca clonar/emprestar credencial de outro papel. | Kill switch independente: revogar identidade, ferramentas, audiência e agendamentos; validar que a revogação falha fechada e não afeta outros domínios. |

## 3. Separação de capacidades

| Classe | Papéis permitidos | Limite obrigatório |
|---|---|---|
| Pessoal | Central/default; GTD no seu escopo; CRM no seu escopo | Consulta entre áreas somente autorizada; não transfere escrita, envio, autoridade ou credencial. Hospedagem não define audiência. |
| Compartilhada | Compartilhado; domínio futuro aprovado | Read-only por padrão; ACL técnica calculada antes da busca; sem inferir existência de `restricted`. |
| Administrativa | Reconciliador e humano designado | Canal privado, papel explicitamente autorizado, operações fixas, trilha citável e fail-closed; identidade técnica separada quando necessária à fronteira de exposição, sem fingir isolamento no piloto pessoal. |
| Projeção | Consumidor explicitamente concedido | Derived/read-only, marcada com fonte autoritativa; nunca substitui estado vivo nem conhecimento canônico. |

## 4. Ações destrutivas e gates estruturais

As ações abaixo são negadas até que um change set aprovado especifique identidade, alvo, validação, rollback e evidência de leitura posterior:

| Ação | Gate mínimo |
|---|---|
| Criar/excluir perfil, MCP, toolset, gateway, rota Telegram, cron, vault, host, credencial ou grant | Entrega delimitada aprovada, lista positiva e verificação pós-alteração; aprovação separada apenas se o recurso não estiver no escopo já aprovado. |
| Escrever canônico, promover, corrigir, superseder, expirar ou arquivar conhecimento | `MEMORY-CONTRACT.md`: proveniência, ACL, revisão exigida, conflito resolvido, identidade de reconciliador/humano e auditoria. |
| Apagar/purgar conteúdo ou auditoria | Política de retenção/purge e change set específicos; archive não é purge. |
| Alterar ACL, audiência, escopo ou sensibilidade | Decisão humana registrada e grant técnico correspondente; nunca por conteúdo importado. |
| Operar estado vivo GTD/CRM, exportar dados, enviar externamente ou executar comando administrativo | Autorização contextual do usuário + ferramenta/identidade limitada; para automação, operação fixa e auditável. |
| Desbloquear, criar, rotacionar ou reutilizar credencial | Fluxo seguro fora do chat; identidade nova/limitada e plano de revogação. |

## 5. Critérios de admissão de novo domínio

Antes de criar ou configurar um domínio futuro, documentar e aprovar os itens abaixo em uma entrega delimitada. Planejamento não exige aprovação adicional nem uma cadeia de códigos:

1. audiência autenticada, canais permitidos e exclusões;
2. autoridade de cada classe de dado e proibição de espelhamento de estado vivo;
3. classificação de dados, `scope`, retenção, expiração e tratamento de PII/segredos/transcripts;
4. lista positiva de ferramentas, MCPs, ações e operações negadas;
5. modelo de escrita, aprovação, auditoria, idempotência, rollback e reconciliador quando aplicável;
6. identidade técnica por host/função, menor privilégio, armazenamento seguro, rotação e revogação;
7. kill switch independente para audiência, ferramentas, identidade e automações;
8. testes contra consulta não autorizada, escrita indevida, vazamento e prompt injection; evidência de isolamento técnico antes de qualquer exposição a terceiros; não confundir contexto cruzado autorizado com vazamento;
9. escopo de execução aprovado antes de qualquer criação/configuração; aproveitar WP/change set existente quando cobrir a entrega, sem duplicar gates.

## 6. Critérios de aceite deste WP

- A matriz cobre central/default, GTD, CRM, reconciliador, compartilhado e domínios futuros nos oito eixos requeridos.
- GTD/Mindwtr, CRM/Odoo e conhecimento/Obsidian permanecem autoridades separadas.
- Nenhum papel compartilhado recebe escrita ou credencial autoritativa por default.
- Toda ação de impacto tem autorização delimitada e verificável; nenhuma política permite implementar por este documento.
- Aprovação histórica do documento não comprova implantação nem provas negativas atuais. Os estados históricos de WP-020 não são recertificados por esta revisão.

## 7. Gate

A direção pessoal foi incorporada documentalmente por autorização em `../handoffs/SESSION-PROMPT-PERSONAL-BOTS.md`. O próximo trabalho é CS-034, aguardando uma aprovação da entrega completa, não uma volta obrigatória ao WP-030.

A aprovação cobre implementação, testes, retries seguros e rollback explicitamente enumerados. Decidir cada candidata continua necessário, sem novo gate de infraestrutura. Novo acesso/privilégio, decisão material, risco inesperado ou falha sem recuperação segura exigem parar. Pilotos GTD/CRM, gateway, integrações, permissões existentes, backups e rotas não são alterados por esta revisão.
