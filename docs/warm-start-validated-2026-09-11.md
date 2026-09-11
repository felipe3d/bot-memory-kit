# Warm-start validado end-to-end (2026-09-11, ~03:28)

## Setup
- Skill atualizada: warm-start na fase INTERVIEW do SKILL.md (não só no template)
- Regras novas: run COMPLETE = fechado ("iniciar" cria run novo); nunca auto-responder em single-query
- state.db do sandbox arquivado (nenhum run anterior visível); sessões antigas movidas
- **Correção crítica de infra: `-e HERMES_WRITE_SAFE_ROOT=/hermes-home`** obrigatório nos runs —
  a imagem oficial fixa o safe root em `/opt/data` (efêmero), o que bloqueava toda escrita durável
  (achado: "Write denied: outside HERMES_WRITE_SAFE_ROOT").

## Comportamento observado (run bmk-20260911-0328)

### Round 1 — cartão de confirmação
- 7 fatos listados com origem (user profile / memória / entrevista / checkpoint arquivado)
- Detectou ambiguidade real ("Felipe" vs "Felipe Teste" do teste anterior) e pediu confirmação
- Blocos 4–5 declarados perguntas abertas ("limites não são herdados de runs antigas")
- Run anterior COMPLETE tratado como fechado; novo run criado

### Round 2 — resposta do usuário (confirma + corrige + descarta)
- 7/7 itens ratificados, 2 correções aplicadas ao ledger:
  1. `maquinas_vps`: VPS Oracle ARM é a ÚNICA sempre ligada (correção, status superseded no old)
  2. `nome`: "Felipe Teste" descartado como valor de teste (superseded)
- Entrevista pulou Blocos 1–3 (confirmados) e foi direto ao Bloco 4 (pergunta 12)

### Ledger no checkpoint
- `known_facts`: 7 fatos, cada um com fact/status/source/verified_at
- `corrections`: 2 registros completos (old → new, status superseded)
- `phase: INTERVIEW`, checkpoint durável em bmk-backups/ ✅

## Aprendizados
1. **HERMES_WRITE_SAFE_ROOT da imagem (=/opt/data) precisa ser sobrescrito** para writes duráveis
   no volume. Adicionar ao setup-linux-sandbox.sh.
2. Run COMPLETE arquivado não deve ser retomado por "iniciar" (regra agora no SKILL.md).
3. Nunca auto-responder em single-query mode (regra agora no SKILL.md: BLOCKED awaiting_user_input).
4. O harness atualizado detecta cartão de confirmação e responde como persona (known_facts/corrections).
