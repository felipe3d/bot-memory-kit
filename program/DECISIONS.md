# Decisions

## ADR-001 — O repositório é o plano de controle

**Estado:** aprovada em 2026-09-17  
**Decisão:** `bot-memory-kit/program/` é a fonte de estado de trabalho. Sessões são descartáveis e leem `CURRENT.md` + WP + decisões.  
**Consequência:** nenhum chat longo é necessário para retomar; cada WP tem gate e handoff próprios.

## ADR-002 — Autoridades permanecem separadas

**Estado:** histórica corroborada  
**Decisão:** Obsidian guarda conhecimento revisado; Mindwtr, tarefas/projetos; Odoo, CRM; memória Hermes, resumos mínimos; skills, procedimentos.  
**Consequência:** nenhum bot copia estado vivo de negócio para memória persistente. Consulta autorizada de contexto GTD/CRM é distinta de persistência; conhecimento estável e sanitizado derivado de uma fonte autorizada pode ser proposto e revisado, sem transferir autoridade.

## ADR-003 — Isolamento deve ser técnico

**Estado:** histórica corroborada  
**Decisão:** prompt, skill e nome de perfil não constituem fronteira. Toolsets, MCPs, credenciais e backend precisam impor o escopo.  
**Consequência:** bots compartilhados permanecem bloqueados até demonstração de isolamento. Bot pessoal, inclusive na VPS, não é compartilhado por localização. Sua especialização não impede consulta entre áreas explicitamente autorizada; permissões técnicas e controles de impacto continuam exigidos.

## ADR-004 — Preservar piloto P1-A2

**Estado:** aprovada em 2026-09-18  
**Decisão:** manter release dedicado, unit/drop-in e backups P1-A2 até change set explícito de promoção ou rollback.  
**Consequência:** este programa não altera a infraestrutura do gateway por efeito colateral.

## ADR-006 — A IA propõe; a pessoa aprova conhecimento

**Estado:** aprovada pelo usuário em 2026-09-21
**Decisão:** o usuário não redige manualmente notas estruturadas para bots. Uma automação futura, limitada a fonte de leitura explicitamente aprovada, identifica padrões e cria candidatas em inbox; a pessoa revisa cartões simples e só aprova, rejeita ou ajusta.
**Consequência:** candidatos nunca viram conhecimento canônico ou publicação VPS por decisão autônoma da IA; CS-034 define a etapa futura de curadoria assistida.

**Direção incorporada nesta revisão, autorizada por `handoffs/SESSION-PROMPT-PERSONAL-BOTS.md`:**
- Priorizar utilidade, especialização, revisão e correção em bot pessoal existente; publicação dedicada na VPS é alternativa, não pré-requisito universal.
- Permitir cartão sanitizado ao proprietário no canal privado autorizado. Isso não autoriza despejar a fonte em logs, auditoria ou canais alheios.
- A IA propõe fonte, destino, validade e estrutura; a pessoa decide em português simples, sem YAML/IDs/TTL ou redação manual.
- Uma aprovação por entrega delimitada cobre implementação, testes, retries seguros e rollback enumerados. A aprovação de cada cartão decide conteúdo; não abre novo gate técnico.
- Parar por novo acesso/privilégio, decisão material, risco inesperado ou falha sem recuperação segura. Não pedir nova aprovação só para detalhar plano já autorizado.
- CS-034 escolhe default privado local e a seção “Acordo com o usuário” do próprio handoff como fonte. Após a revisão documental, o proprietário aprovou a entrega (“eu aprovo”, 2026-09-21, Desktop privado). Execução IN_PROGRESS no escopo enumerado; essa decisão não aprova candidatas nem demonstra conclusão funcional.

## ADR-005 — Candidata não é conhecimento canônico

**Estado:** histórica corroborada  
**Decisão:** bot/host escreve proposta em inbox com proveniência; promoção a canonical exige reconciliador e revisão adequada ao risco.  
**Consequência:** recuperação normal não apresenta inbox como verdade.
