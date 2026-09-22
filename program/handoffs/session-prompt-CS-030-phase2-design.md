# Prompt — nova sessão: CS-030 / desenho da Fase 2

Você é o executor documental do WP-030 no repositório `~/dev/bot-memory-kit`.

## Ordem obrigatória de leitura

1. `program/CURRENT.md`
2. `program/work-packages/WP-030-knowledge-isolation.md`
3. `program/change-sets/CS-030-agentknowledge-vps-24x7.md`
4. `program/DECISIONS.md`
5. `program/EVIDENCE.md`
6. `program/contracts/MEMORY-CONTRACT.md`
7. `program/contracts/BOT-POLICY-MATRIX.md`
8. `program/evidence/CS-030-phase-1-synthetic-spike.md`
9. `program/evidence/CS-030-gate-d-discovery.md`
10. `program/handoffs/WP-030.md`

Carregue e siga a skill `bot-memory-kit` antes de alterar artefatos.

## Autorização e objetivo

Há autorização **somente para revisão documental** do CS-030: elaborar a proposta da Fase 2 para um piloto Git privado sintético da projeção de AgentKnowledge.

A arquitetura candidata já selecionada documentalmente é:

- repositório Git privado dedicado à projeção;
- consumidor VPS com deploy key SSH exclusiva e read-only por repositório;
- publicador separado no lado autorizado;
- manifesto de integridade e TTL;
- rollback por revogação da deploy key e remoção dos artefatos sintéticos do piloto.

Produza uma revisão do CS-030 com um plano de piloto preciso o bastante para futura aprovação humana, mantendo claramente `AWAITING_APPROVAL`.

## O que o CS revisado deve definir

1. **Artefatos propostos, ainda não criados:** repositório privado sintético, uma chave de deploy descartável, um consumidor de teste, um publicador de teste, arquivo de projeção sintética, manifesto, auditoria sanitizada e rotina de limpeza.
2. **Fronteiras:** fonte canônica/vault pessoal nunca entra no piloto; o repositório nunca recebe conteúdo real, `restricted`, `prohibited`, inbox, archive, estado Hermes, segredo, PII ou transcript.
3. **Identidade e menor privilégio:** a chave do consumidor é exclusiva do repositório, read-only, sem write/push/admin; o produtor não recebe acesso ao vault pessoal da VPS; nenhuma credencial pessoal, PAT, sessão OAuth ou credencial de sync é reutilizada.
4. **Manifesto:** campos mínimos, algoritmo/forma de integridade a validar, revisão, escopo sintético, sensibilidade sintética, TTL, origem sintética e comportamento fail-closed.
5. **Sequência futura de aplicação:** cada criação/modificação proposta, pré-requisito, responsável lógico, verificação de leitura posterior e passo de rollback correspondente.
6. **N-01 a N-06:** caso de teste, identidade, superfície, resultado de negação/aceite e evidência sanitizada esperada. Distinguir o que exige ambiente real autorizado do que o piloto sintético prova.
7. **Rollback e limpeza:** ordem de revogação, confirmação de falha fechada, remoção de recursos sintéticos e preservação de auditoria mínima.
8. **Gates:** separar inequivocamente (a) aprovação para criar/executar o piloto sintético; (b) aprovação para qualquer discovery de host/credencial real; (c) aprovação para qualquer dado/projeção real.
9. **Decisões pendentes:** não inventar host produtor, local de chave, conta GitHub, nome final de repositório, mecanismo de assinatura, cron, usuário de SO, serviço ou caminho de produção. Use placeholders explícitos e marque-os como bloqueios/decisões humanas.

## Proibições absolutas

Não execute discovery nem acesso a host, rede, conta, GitHub, repositório, vault, Obsidian, 1Password, credencial, token, chave, sessão, configuração, `.env`, `auth.json`, state.db, home Hermes, Markdown de AgentKnowledge ou conteúdo pessoal.

Não crie repositório, deploy key, usuário, diretório de host, serviço, timer, cron, storage, regra de rede, perfil, MCP, gateway, backup ou rota. Não instale dependências. Não rode `gh auth status`, `git remote`, SSH, API autenticada, browser login, comandos de inventário ou leitura de configuração.

Não marque N-01–N-06 como operacionais/verificados. Não altere `EVIDENCE.md` a menos que haja evidência nova real (não haverá nesta tarefa).

## Paths permitidos

Somente arquivos documentais em `program/**`: CS-030, WP-030, CURRENT e handoff WP-030, se necessários para refletir a revisão. Não altere contratos aprovados nem código/testes do spike.

## Encerramento obrigatório

1. Atualize status/handoff de forma coerente, mantendo `AWAITING_APPROVAL`.
2. Rode `git diff --check`.
3. Rode uma validação estrutural que confirme que o CS contém: artefatos, manifest, N-01–N-06, rollback, os três gates e decisões pendentes.
4. Reporte: arquivos modificados, validações executadas, decisões que permanecem humanas e a frase exata de aprovação necessária para criar/executar o piloto sintético.
