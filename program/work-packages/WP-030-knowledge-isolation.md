# WP-030 — Isolamento do AgentKnowledge e VPS

**Estado:** PLANNED  
**Tipo:** descoberta e planejamento

## Resultado esperado

Change set detalhado para acesso 24/7 a um subconjunto de conhecimento, com prova de menor privilégio e rollback.

## Fora de escopo

Instalar Headless, criar vault remoto, mudar transportes, remover writers HomeLab ou expor vault pessoal.

## Pré-requisitos

WP-010 e WP-020 aprovados.

## Tarefas

- [ ] Verificar opções reais de credencial/membro técnico por vault, somente metadados autorizados.
- [ ] Comparar vault dedicado, broker allowlisted e alternativas sem sobrepor sincronizadores.
- [ ] Definir spike isolado, evidência negativa de acesso e plano de rollback.
- [ ] Propor CS-030 sem aplicar.

## Gate

Aprovação específica para discovery de host/credencial e, separadamente, para o spike.
