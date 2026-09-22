# WP-030 — Isolamento do AgentKnowledge e VPS

**Estado:** BLOCKED
**Tipo:** Gate P VPS-only executado; exclusão do repositório pendente
**Change set:** `change-sets/CS-030-agentknowledge-vps-24x7.md`

## Resultado esperado

Change set detalhado para acesso 24/7 a um subconjunto autorizado de conhecimento, com prova de menor privilégio, rollback e gates distintos para discovery, spike e aplicação.

## Fora de escopo

Instalar Headless, criar vault remoto, mudar transportes, remover writers HomeLab, expor vault pessoal, ou fazer discovery de host/credencial/conteúdo sem aprovação específica.

## Entradas autorizadas

Nesta revisão: `CURRENT.md`, este WP, CS-030, `DECISIONS.md`, `EVIDENCE.md`, `contracts/MEMORY-CONTRACT.md`, `contracts/BOT-POLICY-MATRIX.md`, evidências da Fase 1 e Gate D, handoff WP-030 e prompt `handoffs/session-prompt-CS-030-phase2-design.md`, na ordem do prompt. Históricos não apontados não são entrada autorizada.

## Paths/capacidades permitidos

Somente artefatos documentais em `program/**`. Não há capacidade autorizada para hosts, vaults, credenciais, identidades, serviços, transportes ou conteúdo de AgentKnowledge.

## Guardrails

- Não sincronizar `state.db`, homes Hermes ou credenciais.
- Não expor o vault pessoal inteiro a Headless nem confiar em selective sync como fronteira.
- Não alterar gateway, release, unit, backups, perfis, credenciais, vaults ou rotas Telegram sem change set aprovado.
- A ausência de aprovação específica bloqueia qualquer discovery de host/credencial e qualquer spike.

## Tarefas

- [x] Verificar opções reais de credencial/membro técnico por vault, somente metadados autorizados. **Fase 0 aprovada e concluída documentalmente; não houve host, credencial ou conteúdo consultado.**
- [x] Comparar vault dedicado, broker allowlisted/default-deny e alternativa sem acesso compartilhado ao vault.
- [x] Definir spike isolado, evidência negativa de acesso e plano de rollback.
- [x] Propor CS-030 sem aplicar.
- [x] Gate H mínimo: GitHub, VPS e produtor HomeLab responderam apenas com metadados; nenhum conteúdo/segredo foi lido, conforme `evidence/CS-030-gate-h-minimal.md`.
- [x] Anexo 2.2: defaults de conta/repo, usuários isolados, chaves, auditoria, confiança, TTL, ref e limpeza preenchidos documentalmente; nenhum recurso criado.
- [x] Gate P preflight P-01: HomeLab negou `sudo -n`; VPS aceitou, mas nenhuma criação começou sem o publicador isolado; evidência em `evidence/CS-030-gate-p-preflight.md`.

## Critérios de aceite

- [x] Positivo: CS-030 compara as três alternativas, recomenda uma opção condicional e declara scope, rollback e verificações.
- [x] Negativo: CS-030 exige prova de que a VPS não acessa vault pessoal, credenciais alheias nem conteúdo fora do scope.
- [x] Negativo: nenhum host, conteúdo, credencial, vault ou serviço foi consultado/alterado; a Fase 0 limitou-se a documentação pública e código do repositório.
- [x] Operacional sintético: N-03 a N-06 e negação de identidade sintética sem grant passaram; evidência em `evidence/CS-030-phase-1-synthetic-spike.md`.
- [x] Documental: Gate D foi executado somente contra metadados/documentação; definiu a candidata Git privado dedicado + deploy key read-only e o piloto, em `evidence/CS-030-gate-d-discovery.md`.
- [ ] Operacional real: N-01 a N-06 exigem CS revisado com alvos exatos e gate de aplicação separado.

## Gate

**Para avançar exige:** Gate P está encerrado no escopo sintético. N-01/N-02 reais e qualquer dado/projeção real exigem WP/change set e Gate R separados; não há nova execução autorizada por este WP.

## Handoff de encerramento

- Verificado: revisão documental 2.0 do CS-030; desenho não equivale a implementação.
- Alterado: CS-030, WP-030, CURRENT.md e handoff WP-030; EVIDENCE.md e contratos preservados, sem evidência operacional nova.
- Bloqueado: alvos concretos, mecanismo de confiança, armazenamento e identidades, anexo de comandos, criação/execução do piloto e qualquer aplicação real. Fase 1 e Gate D documental já concluídos.
- Próximo passo único: decisão humana sobre bloqueios/anexo do CS-030; Gate H se necessário e Gate P somente para revisão concreta aprovada. Estado AWAITING_APPROVAL.
