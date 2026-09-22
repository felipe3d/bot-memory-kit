# CS-030 Gate R — decisão sobre dados reais de AgentKnowledge

**Estado:** APPROVED  
**Tipo:** planejamento/documentação  
**Autoridade:** gate separado para qualquer uso de dados reais; não autoriza acesso, importação, publicação ou recuperação.

## Objetivo

Definir requisitos do subconjunto real e prova negativa de produção antes de qualquer publicação para a VPS. O Gate R restringe qualquer dado real ao menor conjunto autorizado; ele não é uma extensão implícita do piloto sintético.

## Requisitos do subconjunto real

1. **Escopo/audiência explícitos** — definir um único `scope` de produção e uma `audience` de produção. Nenhum item fora desse escopo pode ser publicado.
2. **Sensibilidade limitada** — somente `public` e `internal`, e apenas se o registro tiver classificação positiva. `restricted`, `prohibited`, inbox, archive, histórico e estado vivo ficam excluídos.
3. **Base de prova por item** — nenhum dado real entra em projeção sem `id` canônica, `status: canonical`, `verified_at`, `source.locator`, `scope`, `audience`, `sensitivity` e `expiry`/condição de validade. Sem esses campos, é `BLOCKED`.
4. **Manifesto assinado e TTL** — toda publicação real exige manifesto com hash, TTL, revision, anti-replay e assinatura externa verificável.
5. **Rollback de conteúdo** — despublicar/remove de um item errado sem reescrever histórico do repositório, com trilha de auditoria.

## Evidências exigidas antes de qualquer execução

- Prova positiva de filtro: somente itens allowlisted são selecionados; fixtures negativas nunca publicam IDs ou metadados.
- Prova de exclusão: tentativa de incluir `restricted`/`prohibited` ou registro incompleto falha fechado.
- Prova de revogação: removendo a identidade/grant, a publicação para de receber updates e o consumidor recusa entrega, mesmo que já tenha leitura local.
- Prova de ausência de fallback: nem o vault pessoal, sincronizador, credenciais de outro papel ou cache amplo são consultados em falha.

## Não escopo

Nenhuma criação/alteração de host, vault, repositório, publicador, consumidor, credencial, serviço, transporte, sync, cron ou rota. Não lê notas, transcrições, conteúdo pessoal ou dados reais de negócio. Não gera projeção real.

## Gate e aprovação

Este Gate R permite apenas aprovar a definição documental do subconjunto e dos testes. Nenhuma execução ou produção é autorizada por este documento. Para produzir dados reais, precisa de uma aprovação separada com alvo, responsável e revisão explícitas.

## Aprovação registrada

**Aprovado pelo usuário em 2026-09-18:** decisão Gate R sobre escopo e prova para dados reais, sem execução, acesso, importação ou publicação.

## Evidência

Nenhuma evidência nova. Somente documentação; qualquer implementação ainda é bloqueada sem nova aprovação explícita.
