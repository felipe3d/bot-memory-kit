# WP-032 — Preparação da pipeline real

**Estado:** VERIFIED
**Tipo:** P-0 executado e limpo; nenhum conteúdo real
**Change set:** `change-sets/CS-032-real-pipeline-preparation.md`

## Resultado

P-0 foi executado somente com fixture sintética e limpo integralmente, incluindo read-back de ausência do repositório. A preparação de pipeline está encerrada; a primeira publicação real depende da CS-033.

## Fora de escopo

Identidades, hosts, vault, credenciais, repo, pipeline, conteúdo, publicação e Gate R de execução.

## Paths/capacidades permitidos

Somente documentos em `program/**`.

## Tarefas

- [x] Definir arquitetura, componentes e controles mínimos.
- [x] Separar preparação técnica de primeiro conteúdo real.
- [x] Definir tabela P-0 com comandos, baselines, read-backs, parada e rollback; nenhuma execução.
- [x] Aplicar P-0 com fixture sintética, revogar identidades e confirmar ausência posterior do repo.

## Encerramento

**Verificado:** P-0 não acessou conteúdo real e foi limpo. `CS-033-first-real-publication.md` agora concentra a única aprovação necessária para a primeira publicação mínima real; este WP não a autoriza.