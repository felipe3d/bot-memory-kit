# WP-020 — Matriz de bots e permissões

**Estado:** VERIFIED — matriz v0.1 aprovada explicitamente em 2026-09-18
**Tipo:** planejamento
**Change set:** nenhum
**Entregável:** `program/contracts/BOT-POLICY-MATRIX.md` (matriz v0.1 aprovada)

## Resultado esperado

Matriz aprovada para central/default, GTD, CRM, reconciliador, compartilhado e domínios futuros: audiência, autoridade, ferramentas, dados, escrita, retenção, credenciais e kill switch.

## Fora de escopo

Criar perfis, adicionar MCPs, mudar grants Telegram ou configurar credenciais.

## Entradas autorizadas

`program/**`, documentos P0/P1 e inventários técnicos permitidos.

## Tarefas

- [x] Mapear cada papel e seu backend autoritativo.
- [x] Separar capacidades pessoais, compartilhadas, administrativas e de projeção.
- [x] Definir ações destrutivas e gates estruturais.
- [x] Definir critérios mínimos para introduzir um novo domínio.

## Critérios de aceite

- [x] A proposta cobre os seis papéis e os oito eixos requeridos.
- [x] Autoridades, ACL fail-closed, credenciais separadas e kill switches independentes estão definidos.
- [x] Nenhum perfil, MCP, credencial, grant Telegram ou infraestrutura foi criado/alterado.

## Gate

A matriz em `program/contracts/BOT-POLICY-MATRIX.md` foi aprovada explicitamente. Qualquer perfil, MCP, credencial, grant Telegram ou infraestrutura continua exigindo change set aprovado separado.
