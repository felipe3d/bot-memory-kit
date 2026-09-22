# CS-031 — Gate de execução: prova de perímetro N-01/N-02

**Estado:** VERIFIED  
**Data:** 2026-09-18  
**Escopo executado:** só a prova de perímetro com a sonda sintética e canários; nenhum conteúdo, vault, AgentKnowledge, credencial, Gate R ou projeção.

## Execução e resultados

Todas as fases R-00–R-04 foram executadas na VPS.

| Fase | Resultado |
|---|---|
| R-00 baseline | Passou; os três usuários e as quatro raízes estavam ausentes antes da criação. |
| R-01 criação | Passou; identidade da sonda e canários criados com shell nologin, home próprio e permissões 0700. |
| R-02 canários | Passou; cada owner criou seu próprio arquivo sintético 0600, sem conteúdo sensível. |
| R-03 provas negativas | Passou: identidade sem grupo privilegiado; raízes 0700; a sonda não leu canários alheios; controles positivos lidos; nenhum mount suspeito; ambiente da sonda limpo; o destino TEST-NET falhou sem fallback. |
| R-04 limpeza | Passou; três identidades, homes, roots e canários removidos; read-back confirmou ausência; a pasta de auditoria root-owned permaneceu intacta até o read-back final. |

## Limites e interpretação

- Isso prova o perímetro da sonda sintética criada neste CS; não prova isolamento de hosts reais, conteúdo real, dados ou segredos fora do escopo do piloto.
- A sonda foi removida; nenhum acesso persistente permanece.
- A auditoria root-owned em `/var/tmp/cs031-perimeter-audit/` foi retida conforme retenção aprovada; a limpeza de qualquer conteúdo real está fora deste CS.
- Para qualquer aprovação futura de dados reais ou escopo ampliado, um novo change set / gate específico é obrigatório.
