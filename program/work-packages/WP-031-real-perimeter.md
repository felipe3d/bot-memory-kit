# WP-031 — Perímetro real N-01/N-02 sem conteúdo

**Estado:** VERIFIED
**Tipo:** prova de perímetro executada e limpa
**Change set:** `change-sets/CS-031-real-perimeter-n01-n02.md`

## Resultado esperado

CS-031 que permita decidir, sem ampliar dados, se uma prova real de perímetro N-01/N-02 pode ser aplicada com identidade VPS descartável e superfícies allowlisted.

## Fora de escopo

Hosts, vaults, AgentKnowledge, credenciais, conteúdo, identidade, canários, repo, projeção, serviço, cron, Gate R e qualquer execução.

## Paths/capacidades permitidos

Somente artefatos documentais em `program/**`.

## Tarefas

- [x] Definir objetivo, escopo e proibições de prova real sem conteúdo.
- [x] Definir allowlist de superfícies, N-01/N-02, rollback e gates.
- [x] Preencher Anexo A com alvo VPS, identidades sintéticas, raízes, allowlist e critérios N-01/N-02; nenhuma execução.
- [x] Executado R-00–R-04 na VPS; prova N-01/N-02 do perímetro sintético passou; evidência em `evidence/CS-031-real-perimeter-run.md`.

## Gate

**Para avançar exige:** anexo de alvos e ações reais aprovado, seguido de gate de execução separado. Nenhum documento desta WP autoriza acesso por continuidade.
