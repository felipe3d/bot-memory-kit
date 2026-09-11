# Changelog

## v1.0.0 (2026-09-11)

Primeira release pública — ciclo completo validado end-to-end em sandbox.

### Skill
- Fases: INTENT → INTERVIEW → SCOPE_APPROVED → CONSENT_PER_HOST → DISCOVERY
  → SELECTION → VAULT_SETUP → ARCHITECTURE → PLAN_READY
  → WAITING_IMPLEMENTATION_APPROVAL → APPLY → VERIFY → COMPLETE
- Warm-start: confirma memória existente com correção explícita (ledger `known_facts`/`corrections` no checkpoint)
- VAULT_SETUP: cria vault canônico dedicado com escopos de leitura por bot (bot de infra proibido de ler canonical/people)
- Gates de modelo por fase (APPLY exige glm-5.3+)
- Checkpoint durável obrigatório em `<HERMES_HOME>/bmk-backups/`; run COMPLETE nunca retomado por "iniciar"; nunca auto-responder em single-query

### Ferramentas
- `setup-vault.py` — criação idempotente do vault (dry-run, check, proteção de caminho)
- `setup-linux-sandbox.sh` — sandbox Docker (ollama-cloud + glm-5.3, WRITE_SAFE_ROOT corrigido)
- `run-interview-test.py` — harness de entrevista automática com usuário fictício

### Validações
- Entrevista 18/18, 3 gates, APPLY idempotente, VERIFY T1–T16 = 16/16 pass
- Limitações MVP documentadas (T12/T13 parciais no container; 1Password SA/broker desenhados não exercitados)
