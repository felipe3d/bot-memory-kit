# WP-033 — Curadoria assistida de conhecimento

**Estado:** VERIFIED — todas as provas funcionais exigidas foram executadas com decisão humana real e conversas novas no Desktop.
**Revisão documental:** concluída sob `handoffs/SESSION-PROMPT-PERSONAL-BOTS.md`.
**Change set:** `change-sets/CS-034-assisted-candidate-curation.md`.

## Resultado esperado

O default pessoal do Mac aprende preferências de colaboração a partir do acordo já documentado no handoff. A IA identifica e redige candidatas; o proprietário aprova, rejeita ou ajusta cartões simples. Uma conversa nova recupera e usa somente conhecimento vigente, com origem; correção e retirada funcionam.

## Revisão documental anterior (concluída)

Somente documentos necessários em `program/`. Fonte da proposta escolhida sem inventário privado: seção "Acordo com o usuário" de `handoffs/SESSION-PROMPT-PERSONAL-BOTS.md`. Ler esse documento para planejamento não autoriza promover suas afirmações à memória.

Não acessar notas, hosts ou credenciais, criar scanner/perfil/serviço, escrever inbox/canonical, implementar recuperação ou publicar na VPS. Preservar alterações preexistentes, sem commit/push. Não iniciar outro agente, sessão recursiva, cron ou Kanban.

## Aceite documental — concluído

- [x] Especialização separada de permissão; uso pessoal separado de exposição a terceiros.
- [x] Consulta de contexto GTD/CRM autorizável sem espelhar estado vivo ou transferir autoridade.
- [x] Fonte concreta de baixo risco, bot existente e destinos propostos nomeados no CS.
- [x] Uma aprovação cobre implementação, testes, retries seguros e reversão; nada exige aprovação por arquivo.
- [x] Cartões sanitizados podem ser mostrados ao proprietário no canal privado; conteúdo bruto não vai para logs/canais alheios.
- [x] Publicação dedicada na VPS retirada do caminho obrigatório.
- [x] Testes de recuperação nova, rejeição, correção, retirada e injeção definidos e executados.

## Aceite funcional — concluído

- [x] 23 testes automáticos passaram (17 desta entrega, 6 do spike preexistente).
- [x] Preflight local passou sem colisões/symlinks; nenhuma descoberta privada adicional.
- [x] Helper e testes no repo, skill `personal-learning` no default.
- [x] Aprovação humana real: candidata aprovada, promoteu para canonical, lida de volta.
- [x] Conversa nova real 1: recuperação citada com ID, revisão, origem e validade.
- [x] Uso correto real: formato de cartão em português simples, sem campos técnicos.
- [x] Retirada real: canonical vazio, tombstone no archive, conversa nova confirma ausência.
- [x] Correção real: ajuste de validade 90→120 dias, rev. 2 aprovada, conversa nova lê versão corrigida.
- [x] Evidência e limites: `../evidence/CS-034-local-learning-run.md`.

## Estado final

Uma nota canônica vigente (`AK-CS034-d162c634a1c24dd8` rev. 2, validade 120 dias). Archive com rev. 1 superseded e rev. 1 retirada. Inbox e cards vazios.

## Limites que persistem

- Isolamento de SO ou contenção de agente malicioso não provados; operador Desktop é parte confiável.
- Detecção universal de PII/injeção não provada; filtro é conservativo/heurístico.
- Retirada pelo assistente em conversa nova sem intervenção da sessão de controle não provada.
- Pipeline VPS, sync e segurança integral não testados.

## Próximo passo

Nenhum gate pendente. O proprietário decide se amplia fontes, adiciona domínios ou mantém como está.