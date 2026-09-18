# WP-040 — Avaliação de recuperação e isolamento

**Estado:** PLANNED  
**Tipo:** planejamento e testes sintéticos

## Resultado esperado

Suíte de aceitação que prova recuperação útil e citada, separação entre perfis e resistência a instruções em conteúdo recuperado.

## Fora de escopo

Dados pessoais reais, alteração de pilotos, acesso compartilhado real ou automação de promoção.

## Pré-requisitos

WP-010 e WP-020 aprovados.

## Tarefas

- [ ] Especificar fixtures sintéticas de fatos, correções e conflitos.
- [ ] Definir cenários cross-profile GTD/CRM/compartilhado.
- [ ] Definir teste de nota hostil como dado, não instrução.
- [ ] Definir métricas: citação, precisão, vazamento, revogação e degradação.

## Gate

Aprovação antes de executar contra perfis reais ou fontes não sintéticas.
