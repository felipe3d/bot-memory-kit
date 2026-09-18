# Decisions

## ADR-001 — O repositório é o plano de controle

**Estado:** aprovada em 2026-09-17  
**Decisão:** `bot-memory-kit/program/` é a fonte de estado de trabalho. Sessões são descartáveis e leem `CURRENT.md` + WP + decisões.  
**Consequência:** nenhum chat longo é necessário para retomar; cada WP tem gate e handoff próprios.

## ADR-002 — Autoridades permanecem separadas

**Estado:** histórica corroborada  
**Decisão:** Obsidian guarda conhecimento revisado; Mindwtr, tarefas/projetos; Odoo, CRM; memória Hermes, resumos mínimos; skills, procedimentos.  
**Consequência:** nenhum bot copia estado vivo de negócio para memória persistente.

## ADR-003 — Isolamento deve ser técnico

**Estado:** histórica corroborada  
**Decisão:** prompt, skill e nome de perfil não constituem fronteira. Toolsets, MCPs, credenciais e backend precisam impor o escopo.  
**Consequência:** bots compartilhados permanecem bloqueados até demonstração de isolamento.

## ADR-004 — Preservar piloto P1-A2

**Estado:** aprovada em 2026-09-18  
**Decisão:** manter release dedicado, unit/drop-in e backups P1-A2 até change set explícito de promoção ou rollback.  
**Consequência:** este programa não altera a infraestrutura do gateway por efeito colateral.

## ADR-005 — Candidata não é conhecimento canônico

**Estado:** histórica corroborada  
**Decisão:** bot/host escreve proposta em inbox com proveniência; promoção a canonical exige reconciliador e revisão adequada ao risco.  
**Consequência:** recuperação normal não apresenta inbox como verdade.
