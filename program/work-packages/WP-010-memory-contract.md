# WP-010 — Contrato de memória

**Estado:** PLANNED  
**Tipo:** planejamento  
**Change set:** nenhum

## Resultado esperado

Contrato aprovado para captura, inbox, validação, promoção, recuperação, correção, supersessão, expiração e arquivamento do conhecimento.

## Fora de escopo

Criar reconciliador, alterar vault, migrar notas, configurar Headless ou modificar perfis.

## Entradas autorizadas

`program/**`, política `AgentKnowledge/README.md` e fontes documentais autorizadas.

## Tarefas

- [ ] Definir entidades, campos mínimos, níveis de sensibilidade e ACL.
- [ ] Definir transições de lifecycle e responsável por cada uma.
- [ ] Definir recuperação citada e comportamento na ausência/conflito de fontes.
- [ ] Especificar testes negativos para candidatos, supersessão e prompt injection.

## Gate

Aprovação explícita do contrato antes de implementar writer, reconciliador ou índice.
