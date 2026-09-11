# Re-teste APPLY limpo (2026-09-11, ~02:20)

## Setup
- Estado zerado (perfis foca/infra removidos, checkpoint limpo)
- Skill atualizada com instrução MANDATORY de --no-skills na fase APPLY
- Entrevista completa re-rodada via harness (17 rounds) + 3 gates manuais

## Resultado
- Entrevista: 16 respostas, skill propôs 3 bots (foca, infra, dev)
- Gate 1 (escopo): aprovado condicionalmente ✅
- Gate 2 (seleção): skills específicas por bot, write_approval, terminal read-only ✅
- Gate 3 (plano): APLICAR? → aprovado ✅
- APPLY: perfis criados COM --no-skills ✅ (comando confirmado nos transcripts)

## Correção do achado anterior validada
| Verificação | Antes | Re-teste |
|---|---|---|
| foca/skills | 13 categorias (catálogo) | 4 skills aprovadas |
| infra/skills | catálogo | 2 skills aprovadas |
| .no-bundled-skills marker | ausente | presente |
| memórias | corretas | corretas + limites inegociáveis |

## Achados residuais
1. Checkpoint durável em bmk-backups/ ficou vazio — skill gravou em /opt/data
   (efêmero). Corrigir: checkpoint sempre em <HERMES_HOME>/bmk-backups/.
2. Timeout do chat (280s) mata a saída mas o APPLY persiste — tratar
   assincronia no harness (poll do checkpoint em vez de esperar resposta).
3. Aliases em /opt/data/.local/bin são efêmeros no container — esperado,
   recriáveis via `hermes profile alias <nome>` (1 comando).
