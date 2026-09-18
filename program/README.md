# Programa de Memória e Bots

Este diretório é o plano de controle do programa. Git/Markdown preserva o estado de trabalho; conversas são executores temporários.

## Leitura obrigatória para cada sessão

1. `CURRENT.md`
2. o work package ativo em `work-packages/`
3. `DECISIONS.md`

Leia somente as evidências apontadas pelo WP. Não reabra históricos longos sem uma lacuna concreta.

## Regras

- Um work package mutável por vez.
- `continue` não é autorização nem mudança de escopo.
- Uma sessão altera somente os paths e capacidades autorizados pelo WP.
- Mudança de host, gateway, release, unit, backup, perfil, credencial, vault ou rota requer change set e aprovação explícitos.
- Evidência distingue `verificado_agora`, `histórico_corrobado` e `pendente`.
- Não registrar segredos, conteúdo de `.env`, state.db, YAML integral de produção ou dados pessoais sensíveis.

## Ciclo

`PLANNED → IN_PROGRESS → AWAITING_APPROVAL | BLOCKED | VERIFIED`

Ao encerrar, atualizar o WP, `CURRENT.md`, `EVIDENCE.md` quando houver prova nova e o handoff do WP.