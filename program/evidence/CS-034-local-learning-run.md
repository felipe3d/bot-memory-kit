# CS-034 — execução local e limites da prova

**Estado:** VERIFIED — todas as provas funcionais exigidas foram executadas com decisão humana real e conversa nova no Desktop.
**Data local:** 2026-09-21, America/Sao_Paulo (timestamps de arquivos em UTC podem indicar 2026-09-22).
**Autorização:** proprietário respondeu “eu aprovo” à entrega delimitada, no Desktop privado. Não é aprovação de candidata.

## Preflight observado

- Host Darwin, usuário fac, home `/Users/fac`, HERMES_HOME `/Users/fac/.hermes`; perfil ativo default indicado pelo runtime. Nenhum perfil nomeado selecionado.
- Raiz AgentKnowledge aprovada presente. Destinos específicos de inbox/canonical/archive, skill, implementação e testes estavam ausentes; sem colisão nem symlinks nos componentes verificados. Sem inventário de notas ou descoberta de sync/hosts.
- Manifest restrito criado em `~/.hermes/bmk-backups/cs034-personal-learning/deployment-manifest.json`, com baseline de hashes do repositório, paths novos e hashes implantados. Pasta 0700, manifest 0600; nenhum backup anterior lido ou copiado.

## Implementação exercitada

- `scripts/cs034_personal_learning.py`: stdlib, CLI local, sem rede, shell de subprocess interno ou chamadas de modelo. A IA desta conversa redigiu a candidata a partir do trecho autorizado; o helper valida e persiste, não simula um LLM.
- `tests/test_cs034_personal_learning.py`: fixtures sintéticas criadas em diretórios temporários isolados; nenhuma fixture usa vault/credencial real. Não houve necessidade de criar arquivo adicional em `tests/fixtures/cs034/`.
- Skill `personal-learning` instalada apenas no default, descoberta por `skill_view`; contém procedimento, não corpo de memória. Descoberta nesta sessão não prova carregamento automático em conversa nova.
- Fonte fixada à seção autorizada, 957 bytes, SHA-256 `15effc23b6ce5a5e96e32832a0338314ef86762a383bbaa83172ec750219f4e0`. Mudança de digest ou seção é negada, sem expansão da fonte.

## Testes automáticos reais

Comando executado no repositório:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Resultado: **23 testes passaram**, sendo 17 desta entrega e 6 do spike sintético preexistente. Ciclos RED/GREEN foram observados antes da implementação dos comportamentos: fonte, candidata, decisões, correção/retirada, recuperação de transação, rollback e guard de runtime. A suíte roda com Python 3.9.6, sem instalar dependências.

Cobertura exercitada: fonte/paths permitidos, symlink/traversal/digest/quota, candidata fora de recuperação, decisão vinculada a ID/revisão/digest, rejeição/idempotência, correção com nova decisão, retirada, expiração, corrupção, duplicidade textual, payloads sintéticos proibidos, leitura que não busca corpo de inbox/archive, recuperação em processo Python novo, edições concorrentes e falhas após cada estágio de mutação de proposta/aprovação/rejeição/correção/retirada/rollback. Retirada mantém tombstone fora do rollback; rollback mantém marca de desabilitação e permite completar limpeza após recuperação sem reativar consulta.

Saída primária do último teste:

```text
test_noncanonical_restricted_prohibited_and_expired_records_are_excluded (test_cs030_synthetic_spike.ProjectionScopeTests) ... ok
test_reader_cannot_write_or_mutate_the_publication (test_cs030_synthetic_spike.ProjectionScopeTests) ... ok
test_reader_receives_only_current_canonical_allowed_scope (test_cs030_synthetic_spike.ProjectionScopeTests) ... ok
test_revocation_fails_closed_without_mutating_published_records (test_cs030_synthetic_spike.ProjectionScopeTests) ... ok
test_tampered_publication_fails_closed (test_cs030_synthetic_spike.ProjectionScopeTests) ... ok
test_unknown_synthetic_identity_receives_no_projection (test_cs030_synthetic_spike.ProjectionScopeTests) ... ok
test_only_allowlisted_section_with_expected_digest (test_cs034_personal_learning.SourceTests) ... ok
test_absolute_identity_cannot_read_outside_store (test_cs034_personal_learning.WorkflowTests) ... ok
test_all_mutating_stages_recover_without_duplicate_promotion (test_cs034_personal_learning.WorkflowTests) ... ok
test_correction_requires_new_decision_and_withdrawal_never_recalls (test_cs034_personal_learning.WorkflowTests) ... ok
test_decision_bound_to_card_and_retry_safe (test_cs034_personal_learning.WorkflowTests) ... ok
test_duplicate_semantic_record_conflict_blocks_promotion (test_cs034_personal_learning.WorkflowTests) ... ok
test_failed_withdrawal_does_not_resurrect_after_recovery (test_cs034_personal_learning.WorkflowTests) ... ok
test_faults_are_closed_until_recovery_and_retry (test_cs034_personal_learning.WorkflowTests) ... ok
test_malformed_state_cannot_escape_allowlisted_paths (test_cs034_personal_learning.WorkflowTests) ... ok
test_profile_guard_and_cli_synthetic_new_process (test_cs034_personal_learning.WorkflowTests) ... ok
test_proposal_is_idempotent_and_not_retrieved (test_cs034_personal_learning.WorkflowTests) ... ok
test_quota_expiration_and_corruption_fail_closed (test_cs034_personal_learning.WorkflowTests) ... ok
test_recovery_refuses_concurrent_edit (test_cs034_personal_learning.WorkflowTests) ... ok
test_rejection_has_no_recall_or_automatic_resuggestion (test_cs034_personal_learning.WorkflowTests) ... ok
test_retrieval_does_not_read_candidates_or_archive_notes (test_cs034_personal_learning.WorkflowTests) ... ok
test_rollback_archives_approved_and_blocks_recall (test_cs034_personal_learning.WorkflowTests) ... ok
test_unsafe_payloads_and_extra_capabilities_are_rejected (test_cs034_personal_learning.WorkflowTests) ... ok

----------------------------------------------------------------------
Ran 23 tests in 0.313s

OK```

## Aplicação real e leitura posterior

### Primeira candidata (rev. 1, validade 90 dias)

- `propose` executado; `cards` leu de volta uma candidata, revisão 1.
- Registro: `AK-CS034-76a98e324ccf3c09`; SHA-256 do arquivo `6cfb15a8f09b18ceb3e93788b0aa3a4554da58db0f40e464c8171463de498b65`.
- Proprietário aprovou em conversa privada. `decide` promoteu para canonical; `retrieve` lido de volta retornou 1 nota vigente com ID, revisão, origem e validade. Inbox vazio, cards vazio.
- **Conversa nova real 1:** proprietário abriu nova conversa no Desktop, sem colar nota ou histórico, e pediu "Consulte meu conhecimento pessoal: como devo revisar suas sugestões de memória?". O assistente carregou a skill, executou `retrieve`, citou ID `AK-CS034-76a98e324ccf3c09`, rev. 1, fonte e validade. Não repetiu preferência do contexto; leu do canonical.
- **Uso correto real:** na mesma conversa, proprietário pediu exemplo de sugestão de memória. O assistente apresentou cartão em português simples com Aprovar/Rejeitar/Ajustar, sem pedir campos técnicos — respeitando a preferência aprovada.
- **Retirada real:** proprietário pediu retirada em conversa nova. O assistente na conversa nova não executou a retirada (apenas recuperou). A retirada foi executada nesta sessão de controle via `decide` com `action: withdraw`; `retrieve` retornou 0 notas, canonical vazio, tombstone no archive. **Conversa nova real 2:** proprietário pediu consulta em nova conversa; o assistente informou corretamente que não há conhecimento vigente.

### Segunda candidata (rev. 2, validade 120 dias — teste de correção)

- Nova candidata proposta (`AK-CS034-d162c634a1c24dd8`, rev. 1, validade 90 dias) após a primeira ter sido retirada (o helper recusa repropor draft arquivado).
- Proprietário pediu ajuste: trocar validade de 90 para 120 dias. `revise` executado; rev. 1 arquivada como superseded, rev. 2 criada como candidate com validade 120 dias e segunda fonte (human-review).
- Proprietário aprovou rev. 2. `decide` promoteu para canonical; `retrieve` lido de volta retornou rev. 2, valid_days=120, expires 2027-01-20, 2 fontes.
- **Conversa nova real 3:** proprietário abriu nova conversa e pediu "Consulte meu conhecimento pessoal: como devo revisar suas sugestões de memória?". O assistente retornou a versão corrigida (rev. 2, 120 dias), não a original (rev. 1, 90 dias). Cita ID, revisão, fonte e validade correta.

### Estado final

- Canonical: 1 nota vigente (`AK-CS034-d162c634a1c24dd8` rev. 2, validade 120 dias).
- Archive: 2 notas .md (rev. 1 superseded + rev. 1 retirada) e 1 tombstone de retirada.
- State: 2 entries, 4 decisions registradas.
- Inbox e cards: vazios.

## O que ainda NÃO foi provado

- Isolamento de SO ou contenção de um agente malicioso com ferramentas amplas. Operador Desktop permanece parte confiável; a referência humana é atestada por ele. Rejeição de origem/binding inválidos não prova impossibilidade de forjar uma atestação por esse operador.
- Detecção universal de PII, prompt injection ou conflito semântico. Filtro é conservativo/heurístico; fonte fixada, ausência de execução de conteúdo e revisão humana complementam o controle. Duplicidade textual não é detecção de toda contradição.
- Pipeline permanente na VPS, sync, segurança integral, estado atual dos pilotos remotos ou ausência de mudanças feitas por outros processos externos. Esses sistemas não foram acessados nesta execução.
- Retirada executada pelo assistente em conversa nova sem intervenção da sessão de controle. O assistente na conversa nova apenas recuperou; a retirada foi executada pela sessão de controle com o digest correto.

## Preservação e próximo passo

Nenhuma alteração de GTD, CRM, gateway, integrações, permissões existentes, backups anteriores, rotas, provedor, cron/Kanban ou perfis nomeados. Sem commit/push. Evidências históricas não foram reescritas.

Próximo passo: CS-034 está VERIFIED. O piloto pessoal local está funcional com uma nota canônica vigente. Decisão futura do proprietário: ampliar fontes, adicionar domínios ou manter como está. Não há gate pendente.
