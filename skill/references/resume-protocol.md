# Protocolo de checkpoint e retomada

Como o kit sobrevive a interrupções e continua de onde parou — sem depender do transcript.

## Três conceitos diferentes de retomada (não confundir)

| Tipo | Mecanismo | Quando usar |
|---|---|---|
| Retomar conversa | `hermes --resume <session_id>` | continuar o diálogo do kit |
| Recuperar arquivos | checkpoints nativos Hermes (opt-in, shadow Git) | desfazer mudanças de arquivo |
| **Retomar o processo do kit** | **checkpoint próprio do kit** | continuar após interrupção, troca de máquina, ou sem transcript |

O checkpoint do kit é o mecanismo principal — os outros são auxiliares. Distribuições de perfil não carregam sessões; o checkpoint precisa bastar sozinho.

## Schema do checkpoint

```json
{
  "schema_version": 1,
  "kit_version": "0.1.0",
  "run_id": "bmk-20260911-0146",
  "phase": "WAITING_IMPLEMENTATION_APPROVAL",
  "host_id": "mac-notebook",
  "profile_id": "",
  "workspace": "/hermes-home",
  "session_id": "20260911_014540_076aef",
  "approved_scope": {"status": "...", "items": ["..."]},
  "consent": {"<host>": {"granted_at": "...", "scope": "...", "expires_at": "..."}},
  "selected_items": ["profile:foca", "..."],
  "rejected_item_ids": [],
  "completed_steps": ["trigger", "interview_complete", "..."],
  "verification_results": {},
  "blocked_reason": null,
  "next_step": "apply_on_user_approval",
  "current_query": null,
  "current_response": null,
  "interview_answers": {},
  "updated_at": "..."
}
```

Máquina de estados: `INTENT → INTERVIEW → SCOPE_APPROVED → CONSENT_PER_HOST → DISCOVERY → SELECTION → ARCHITECTURE → PLAN_READY → WAITING_IMPLEMENTATION_APPROVAL → APPLY → VERIFY → COMPLETE`, com ramos `BLOCKED`/`PAUSED` de qualquer fase.

## Regras de persistência

1. **Toda transição é persistida atomicamente** (write temp + rename) — intenção antes da ação, resultado verificado depois.
2. Cada resposta de entrevista → checkpoint imediato (round a round).
3. Backup durável em `<home>/bmk-backups/checkpoint.json` a cada fase (proteção contra falha do arquivo primário).
4. **Nunca** no checkpoint: segredos, tokens, dados brutos, URLs autenticadas, conteúdo de conversa além das respostas.

## Retomada: procedimento

```
1. Ler checkpoint → validar schema_version e integridade
2. Mostrar resumo curto ao usuário: fase, o que já foi feito, próximo passo
3. Verificar:
   a. identidade: host_id e profile_id batem com o ambiente atual?
   b. consentimento: expires_at vigente? revogado?
   c. realidade: steps em completed_steps ainda são verdade?
4. Divergência em qualquer verificação → BLOCKED com motivo
5. Continuar da primeira etapa pendente; nunca repetir respondidas
```

### Ação interrompida entre executar e gravar

Se a execução anterior morreu após uma ação mas antes de registrar o resultado:
- **Ler o destino primeiro** (o perfil existe? o arquivo foi criado?)
- Se já existe → registrar como concluído, seguir
- Se parcial → decidir: completar ou reverter, com registro
- **Nunca repetir cegamente** a criação (idempotência: critério #7)

### Validação em cada retomada

- `schema_version` suportado
- `consent` vigente por host
- `phase` ∈ máquina de estados conhecida
- `selected_items` ainda aprovável (sem mudança de escopo)
- Backup existe e é consistente

## Bloqueio concorrente

Duas sessões não podem aplicar simultaneamente:
- arquivo de lock `<workspace>/bmk.lock` com `run_id` e timestamp
- ao iniciar APPLY: se lock existe e < 15 min → `BLOCKED` ("outra execução ativa")
- lock removido ao COMPLETE/BLOCKED final

## Bloqueios legítimos (`BLOCKED`)

| Situação | Ação |
|---|---|
| Host indisponível | BLOCKED[host]; prosseguir com demais hosts só se autorizado |
| Consentimento expirado | pedir re-consentimento |
| Versão do Hermes incompatível | relatar versões; não improvisar flags |
| Skill ausente na instalação | relatar; instalar é etapa aprovada |
| Escopo mudou | nova aprovação antes de prosseguir |
| Conflito de conteúdo | decisão humana |
| Lock ativo | aguardar/informar; não duplicar execução |

`BLOCKED` nunca é contornado com "aproximadamente o mesmo" recurso.

## Retomada pelo usuário

- **"retomar bot-memory-kit"** → ler checkpoint → resumo curto → verificar → continuar
- **"consultar bot-memory-kit"** → só status (fase, steps, pendências) — sem avançar
- Usuário pode dizer "desiste de X" → ajustar escopo → **nova aprovação** se muda o plano

## Após COMPLETE

- Fase → `COMPLETE`; histórico preservado
- Skill não mantém rotinas nem background jobs
- Manutenção futura = nova mudança delimitada ("adicionar bot X"), reutilizando inventário e decisões, revalidando o que envelheceu

## Limpeza

Ao COMPLETE:
- remover `bmk.lock`
- preservar: checkpoint final, backup, respostas da entrevista (dados privados da execução)
- o transcript da sessão pode ser descartado — o checkpoint carrega tudo que importa