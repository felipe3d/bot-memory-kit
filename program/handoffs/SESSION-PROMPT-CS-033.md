# Prompt — próxima sessão: CS-033 e pacote único de aprovação

Você trabalha no repositório `~/dev/bot-memory-kit`.

## Leitura obrigatória

1. `program/CURRENT.md`
2. `program/handoffs/HANDOFF-POST-P0.md`
3. `program/change-sets/CS-030-gate-r-data-decision.md`
4. `program/change-sets/CS-032-real-pipeline-preparation.md`
5. `program/evidence/CS-032-p0-run.md`
6. `program/contracts/MEMORY-CONTRACT.md`
7. `program/contracts/BOT-POLICY-MATRIX.md`
8. `program/DECISIONS.md`
9. `program/EVIDENCE.md`

Carregue a skill `bot-memory-kit` antes de agir.

## Objetivo

Elaborar **CS-033 — primeira publicação real mínima**, somente documentalmente. Não acesse AgentKnowledge, vault, notas, credenciais, hosts, sync ou serviços.

## Processo: uma aprovação, não uma cadeia de pedidos

O usuário quer menos interrupções. Produza um único pacote de aprovação que contenha, no mesmo CS-033:

- subconjunto proposto e critério de seleção positiva;
- audiência e sensibilidade permitidas;
- volume máximo inicial e TTL;
- campos mínimos/manifests/assinatura/anti-replay;
- identidade de publicador/consumidor e limites já aprovados;
- passos de aplicação, read-backs, testes negativos, auditoria e rollback;
- condições de parada;
- texto único de aprovação que permita toda a primeira publicação mínima real e o cleanup/revogação previsto.

Não faça perguntas intermediárias para decisões de baixo risco. Use defaults conservadores e marque os poucos itens que exigem decisão humana material. Não reabra Gate D/H/P ou P-0.

## Proibições

- Não ler, listar, buscar, classificar, copiar ou publicar conteúdo real.
- Não criar repo, usuário, key, script, serviço, timer, cron ou rota.
- Não pedir senha, token ou credencial em chat.
- Não alterar `EVIDENCE.md` sem prova operacional nova.
- Não aprovar nem executar CS-033 nesta sessão.

## Entregáveis

1. `program/change-sets/CS-033-first-real-publication.md` com estado `AWAITING_APPROVAL`.
2. WP/handoff/CURRENT atualizados de forma coerente.
3. Um único texto de aprovação final, limitado à publicação mínima real definida no CS.
4. `git diff --check` e validação estrutural.

## Regra de autonomia futura

Depois que o usuário aprovar o pacote final, trate todos os passos reversíveis, retries, verificações, revogações e cleanup já enumerados como autorizados. Pare apenas se o trabalho sair do `scope`, requerer privilégio/credencial nova, revelar dado sensível, envolver ação irreversível fora do rollback ou falhar sem recuperação segura.
