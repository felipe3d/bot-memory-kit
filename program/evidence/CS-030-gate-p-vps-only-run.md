# CS-030 — Gate P VPS-only: execução e limpeza parcial

**Estado:** BLOCKED na limpeza remota  
**Data:** 2026-09-18  
**Escopo executado:** somente o piloto Git privado sintético VPS-only da revisão 2.5 / Anexo 2.2. Nenhum HomeLab, vault, dado/projeção real, Gate H adicional ou Gate R foi acessado.

## Recursos criados e verificados

- duas contas Linux isoladas na VPS, com homes e raízes privadas de teste;
- repositório privado `felipe3d/agentknowledge-vps-projection-pilot`;
- deploy key read-only do consumidor e deploy key write-enabled do publicador, ambas exclusivas do repositório;
- chave Ed25519 nova para assinatura do manifesto, chave pública pinada no consumidor;
- known_hosts exclusivo com fingerprint Ed25519 oficial do GitHub verificado;
- uma publicação Git sintética na ref `pilot`, com manifesto, assinatura e payload de um registro `AK-SYN-*`.

## Verificações realizadas

| Caso | Resultado |
|---|---|
| P-01 contas/raízes/permissões | Passou; owner/mode read-back verificados. |
| Repositório e deploy keys | Passou; repo privado e as duas keys foram lidas de volta antes da revogação. |
| Integridade/assinatura/TTL/manifest | Passou; consumidor validou assinatura Ed25519, hash, schema, escopo, audiência, sensibilidade e TTL. |
| N-03 | Passou no piloto: árvore Git continha somente manifest, assinatura e payload sintético allowlisted. Isto não é ACL por arquivo do Git nem prova para dados reais. |
| N-04 | Passou: tentativa de push pela deploy key read-only foi negada. |
| N-05 | Passou parcialmente: deploy key do consumidor foi revogada; novo fetch foi negado e o publicador separado ainda fez fetch antes de sua própria revogação. Clone local ainda existia, mas não havia serviço/wrapper de entrega; portanto isto não prova controle de cache de produção. |
| N-06 | Passou no piloto: alteração local do manifest invalidou a assinatura e foi negada. |
| N-01/N-02 | Não certificados operacionalmente: o piloto não inspecionou mounts, credenciais ou vault real por desenho. |

## Revogação e limpeza

- Ambas as deploy keys foram removidas e a leitura posterior da API retornou zero deploy keys.
- Usuários, homes, chaves privadas, checkouts, raízes de publicador/consumidor e arquivos temporários da VPS foram removidos; read-back confirmou ausência.
- Auditoria sanitizada mínima foi preservada em `/var/tmp/cs030-pilot-audit/run-001.json`, owner root, modo 0700/0600, conforme retenção do piloto.

## Limpeza remota concluída

O usuário informou exclusão manual do repositório. Leitura posterior independente com `gh repo view felipe3d/agentknowledge-vps-projection-pilot` confirmou ausência em 2026-09-18. Com isso, o repositório, as deploy keys, os recursos VPS enumerados e as cópias de piloto foram removidos; permanece somente a auditoria sanitizada com retenção já declarada.

## Limites permanentes

N-01/N-02 não foram certificados contra vault ou credenciais reais. O piloto também não prova separação inter-host HomeLab → VPS, disponibilidade 24/7, nem autoriza dados/projeções reais. Esses temas exigem um WP/change set e Gate R separados.
