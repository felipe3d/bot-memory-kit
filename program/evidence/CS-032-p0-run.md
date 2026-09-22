# CS-032 — Execução P-0 com `fac` como publicador

**Estado:** BLOCKED na limpeza remota  
**Data:** 2026-09-18  
**Escopo:** pipeline vazia com fixture sintética; nenhum AgentKnowledge, vault, nota, dado real ou publicação real.

## Verificado

- Publicador HomeLab sob `fac` criou somente roots locais de pipeline, deploy key e chave de assinatura novas.
- Consumidor VPS técnico foi criado apenas para o ensaio e validou manifest assinado, hash, scope/audiência sintéticos e fixture única.
- Tentativa de push pelo consumidor read-only foi negada.
- Ambas deploy keys foram revogadas; leitura posterior retornou zero keys.
- Roots, chaves, checkout e usuário consumidor VPS foram removidos; roots e chaves do publicador HomeLab foram removidos.

## Limites

- A validação foi somente da fixture `synthetic.p0`; nada real foi lido ou publicado.
- O uso de `fac` reduz o isolamento de SO do publicador, conforme decisão aprovada.

## Limpeza remota concluída

O usuário informou exclusão manual do repositório. Leitura posterior independente confirmou ausência. A pipeline P-0 foi removida integralmente: repo, keys, roots e consumidor; nenhum AgentKnowledge foi acessado.

## Limites
