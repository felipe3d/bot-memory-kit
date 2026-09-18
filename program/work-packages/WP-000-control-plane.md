# WP-000 — Controle documental central

**Estado:** VERIFIED  
**Tipo:** documentação  
**Change set:** CS-000 (documental)  
**Dono:** usuário + sessão executora

## Resultado esperado

`program/` fornece um estado único, curto e versionado que permite iniciar qualquer etapa em sessão nova sem depender de transcrições.

## Fora de escopo

Gateway, release, units, backups, perfis, credenciais, vaults, rotas Telegram, serviços, timers, dados GTD/CRM e leitura de conteúdo pessoal.

## Entradas autorizadas

`README.md`, `PLAN.md`, `TODO.md`, P0, handoff P1-A2 e evidências já apontadas nos documentos criados.

## Paths permitidos

Somente `program/**`, `README.md` e `PLAN.md` no repositório. Não reescrever os documentos históricos P0/P1.

## Tarefas

- [x] Criar estrutura, templates, roadmap, estado, decisões, riscos e índice de evidências.
- [x] Criar os WPs iniciais e seus handoffs.
- [x] Atualizar README e PLAN para apontar o papel histórico e o plano de controle novo.
- [x] Validar links, status, tamanho do contexto inicial e ausência de segredos.
- [x] Commit documental exclusivo.

## Critérios de aceite

- [ ] Sessão nova encontra o próximo passo lendo `CURRENT.md`, WP e `DECISIONS.md`.
- [ ] Cada WP tem escopo, fora de escopo, gate e condição de encerramento.
- [ ] Estado operacional não sensível não foi copiado como configuração/dado para Git.
- [ ] Nenhum recurso externo foi alterado.

## Gate

Commit somente após validação documental. O próximo WP exige aprovação explícita do usuário.

## Handoff de encerramento

Será criado em `program/handoffs/WP-000.md`.
