# WP-010 — Contrato de memória

**Estado:** VERIFIED — aprovado em 2026-09-18
**Tipo:** planejamento  
**Change set:** nenhum
**Entregável:** `program/contracts/MEMORY-CONTRACT.md` (contrato v0.1 aprovado)

## Resultado esperado

Contrato aprovado para captura, inbox, validação, promoção, recuperação, correção, supersessão, expiração e arquivamento do conhecimento.

## Fora de escopo

Criar reconciliador, alterar vault, migrar notas, configurar Headless ou modificar perfis.

## Entradas autorizadas

`program/**`, política `AgentKnowledge/README.md` e fontes documentais autorizadas.

## Tarefas

- [x] Definir entidades, campos mínimos, níveis de sensibilidade e ACL.
- [x] Definir transições de lifecycle e responsável por cada uma.
- [x] Definir recuperação citada e comportamento na ausência/conflito de fontes.
- [x] Especificar testes negativos para candidatos, supersessão e prompt injection.

## Gate

Aprovação explícita do contrato antes de implementar writer, reconciliador ou índice.
