# CS-033 — primeira publicação real mínima de AgentKnowledge

**Estado:** BLOCKED — descoberta de metadados concluída sem candidata; publicação não iniciada
**Tipo:** pacote único de aprovação e execução reversível
**Base:** Gate R (`CS-030-gate-r-data-decision.md`) aprovado; P-0 sintético da CS-032 verificado e limpo.
**Não é evidência:** este documento não acessa, classifica, copia nem publica conteúdo real.

## 1. Objetivo e limite

Publicar **uma única** projeção real, temporária e verificável de AgentKnowledge para o consumidor técnico da VPS. A publicação não cria uma nova autoridade: Obsidian/AgentKnowledge canônico continua sendo a fonte de verdade.

A execução inteira abaixo, incluindo retries seguros, verificações, revogações e cleanup, é uma única unidade de aprovação. Não reabre Gate D, H, P ou P-0.

### Autorização registrada — descoberta de metadados

**Aprovada pelo usuário em 2026-09-21 18:21 -03:** descoberta limitada de metadados para apresentar uma única candidata à aprovação final. Esta autorização permite ler somente os campos de frontmatter necessários para verificar elegibilidade (`id`, `status`, `scope`, `audience`, `sensitivity`, `verified_at`, `revision`, `expires_at`, `owner` e presença de `source.locator`) em `AgentKnowledge/canonical/`. Ela não permite ler corpo, título, locator, conteúdo de `source`, anexos, inbox, archive, projections, vault fora dessa raiz, credenciais, hosts ou serviços; não permite copiar, classificar, criar recursos ou publicar. A saída desta descoberta será somente uma recomendação sanitizada com ID, scope, sensibilidade, revisão e expiração; nenhum item é aplicado sem a aprovação final literal da seção 9.

**Resultado da descoberta em 2026-09-21 18:21 -03:** a raiz autorizada `AgentKnowledge/canonical/` continha 0 arquivos regulares (e 4 diretórios). Portanto não havia frontmatter, ID canônico, scope ou sensibilidade para recomendar. Nenhum corpo, título, locator, anexo, inbox, archive, projection, vault adicional, credencial, host ou serviço foi lido. A publicação permanece `BLOCKED`; não há item substituto automático.

**Próximo desenho aprovado como direção de produto:** `CS-034-assisted-candidate-curation.md` propõe que a IA gere candidatas a partir de uma fonte que será aprovada, e que o usuário apenas aprove/rejeite cartões simples. CS-034 não autoriza leitura nem implementação; CS-033 continua bloqueada até existir uma candidata promovida por esse fluxo.

## 2. Subconjunto proposto — seleção positiva

O aprovador designa no texto de aprovação **um único ID canônico** (`<AK-ID>`). O publicador só pode ler e projetar esse registro se, no momento da aplicação, todas as condições forem verdadeiras:

1. o ID é exatamente o ID aprovado, sem glob, busca semântica, diretório ou seleção por similaridade;
2. `status: canonical`, `scope: <SCOPE-APROVADO>` e `audience: vps-projection` estão presentes e são iguais aos aprovados;
3. `sensitivity` é `public` ou `internal`, explicitamente aprovada abaixo; `restricted`, `prohibited`, inbox, archive, histórico, projeções existentes e estado vivo são negados;
4. há `verified_at`, `source.locator`, `revision` inteiro, owner e `expires_at` (ou condição explícita de validade) válidos;
5. o corpo é uma afirmação atômica de conhecimento, sem segredo, PII sensível, transcript bruto, dump de configuração, credencial, dado de GTD/CRM, instrução executável ou material fora do escopo;
6. tamanho do arquivo é no máximo 16 KiB; a árvore publicada tem exatamente esse arquivo, `manifest.json` e `manifest.sig` e totaliza no máximo 24 KiB.

Ausência, ambiguidade ou erro em qualquer condição resulta em `BLOCKED`, sem buscar candidatos alternativos e sem publicar metadado, nome, hash ou trecho do registro recusado.

## 3. Audiência, sensibilidade, retenção e TTL

| Propriedade | Limite vinculante |
|---|---|
| Audiência | Somente o processo `ak-real-consumer` na VPS; não há audiência humana, bot compartilhado, GTD, CRM ou default. |
| Escopo | O valor literal `<SCOPE-APROVADO>` incluído na aprovação; um escopo por publicação. |
| Sensibilidade permitida | Uma das duas opções explicitamente indicada na aprovação: `public` **ou** `internal`. |
| Volume inicial | Um registro, uma revisão, no máximo 16 KiB; três arquivos e 24 KiB no total. |
| TTL da projeção | No máximo 30 dias a partir da assinatura e nunca posterior ao `expires_at` do registro. |
| Retenção | A projeção e checkout são apagados na revogação/expiração. Auditoria sanitizada é retida por 30 dias; nunca inclui payload, título, locator, segredo ou conteúdo de nota. |

## 4. Identidades e limites já definidos

| Papel | Identidade/recurso | Limite |
|---|---|---|
| Publicador | `fac` no HomeLab, script fixo `~/bin/ak-real-publisher` | Sem sudo; zero argumentos; só lê o ID allowlisted após validação. O compromisso de isolamento de SO foi aprovado em CS-032. |
| Repositório | privado `felipe3d/agentknowledge-vps-projection` | Única audiência/grant; vazio antes da primeira publicação; sem Actions, LFS, forks ou submodules. |
| Key de publicação | `ak-real-publisher-rw` | Deploy key nova, read+write limitada a esse repo; privada apenas em `/home/fac/.local/share/ak-real-publisher/.ssh/`, modo 0600. |
| Consumidor | `ak-real-consumer` na VPS, `/var/lib/ak-real-consumer` | Fetch/validação/entrega somente de projeção válida; sem push, vault, Obsidian, sync, cache de fallback ou credencial alheia. |
| Key de consumo | `ak-real-consumer-ro` | Deploy key nova, somente leitura no repo; privada somente em `/var/lib/ak-real-consumer/.ssh/`, modo 0600. |
| Assinatura | nova Ed25519 do publicador; trust anchor pinada na VPS | Chave privada não sai do publicador; âncora pública chega por provisionamento aprovado, nunca do repositório. |
| Auditoria | `/home/fac/.local/state/ak-real-publisher/audit`, 0700 | Somente ID, revisão, decisão, hash, TTL, status e reason code; não acessível ao consumidor. |

Nenhuma chave pessoal, token, agent forwarding, `.env`, `auth.json`, state.db, home Hermes, vault completo ou sincronizador pode ser usado como fallback.

## 5. Formato vinculante da projeção

A árvore do ref `production` contém somente:

```text
projection/<AK-ID>.md
manifest.json
manifest.sig
```

`manifest.json` tem, no mínimo, `schema_version`, `publication_id` UUID novo, `scope`, `audience`, `sensitivity`, `issued_at`, `expires_at`, `revision`, `source_id`, `files` (path e SHA-256), `previous_manifest_hash` e `repo_ref`.

- A assinatura Ed25519 cobre os bytes exatos de `manifest.json`.
- `publication_id` e `revision` não podem ser repetidos; o consumidor mantém estado local 0700 com último `publication_id`, revisão e hash aceitos.
- `previous_manifest_hash` deve coincidir com o último manifesto aceito, exceto na publicação inicial, que usa `null` e exige estado vazio confirmado.
- Um OID/ref divergente, hash inválido, assinatura inválida, TTL expirado/futuro acima de 30 dias, downgrade, repetição, arquivo extra ou ausência de arquivo falha fechado.

## 6. Aplicação, read-backs e testes

Todos os comandos abaixo são futuros e só podem rodar após a aprovação única da seção 9. O operador usa ambiente mínimo (`env -i`) e `bash` para scripts; não há shell arbitrário recebido de conteúdo ou chat.

| Fase | Ação limitada | Read-back obrigatório | Falha/rollback |
|---|---|---|---|
| A0 — pré-flight | Confirmar ausência dos dois usuários/roots, repo e keys antigos pelos nomes e paths desta CS; rodar `sudo -n true` nos dois alvos antes de criar qualquer recurso. | `id`, `getent`, `stat`, API do repo e lista exata de deploy keys mostram baseline; `sudo -n true` passa em ambos. | Se algum pré-requisito falhar, `BLOCKED`, sem criar primeiro recurso. |
| A1 — perímetro | Criar somente os usuários, roots 0700, repo vazio privado, chaves novas, known_hosts pinado e trust anchor desta CS. | UID/grupos/modes; owner/privacidade/vazio/integrations do repo; IDs de ambas keys; fingerprint GitHub e âncora; nenhum mount/sync/home Hermes no consumidor. | Revogar keys primeiro; remover repo, roots e usuários por nomes exatos; ler ausência. |
| A2 — validador | Instalar publicador de zero argumentos e validador consumidor fail-closed; validar uma fixture local não real antes de abrir o registro allowlisted. | Fixture tem assinatura/hash/TTL/revision válidos; push com key do consumidor é negado; logs são sanitizados. | Revogar/remover como A1; não ler AgentKnowledge se fixture falhar. |
| A3 — seleção e publicação | Ler somente o registro de ID literal aprovado; executar validações da seção 2 e gerar projeção/manifesto/assinatura. | Árvore tem exatamente três arquivos, um ID, hashes/assinatura/ref/TTL/revision/anti-replay válidos; API e clone independente confirmam privacidade e árvore exata. | Se seleção/validação falhar, não fazer commit/push. Se falhar após push, revogar e remover conforme A5. |
| A4 — consumo e negativas | Consumidor faz fetch online e valida antes de disponibilizar a projeção. Rodar negativos: push do consumidor; manifesto alterado; assinatura inválida; hash divergente; TTL expirado; replay/downgrade; arquivo extra; `restricted`/`prohibited`/incompleto. | Cada negativo é recusado sem fallback, sem payload no log e sem buscar vault/sync/cache amplo. | Qualquer aceitação inesperada é falha crítica: A5 imediatamente. |
| A5 — expiração, revogação e cleanup | Na expiração, divergência, solicitação de revogação ou falha crítica, bloquear entrega, revogar ambas as keys e apagar repo, checkout, roots, usuários, trust material e auditoria de payload inexistente. | Read-back independente confirma zero keys, repo ausente, usuários/roots/checkouts/trust ausentes e consumidor incapaz de fetch. A auditoria sanitizada de 30 dias permanece root-only quando requerida. | Recurso residual = `BLOCKED`; não ampliar token/credencial. Registrar nome exato e pedir remediação/manual read-back. |

## 7. Condições de parada

Pare e marque `BLOCKED` antes de acessar conteúdo se houver necessidade de credencial nova não enumerada, privilégio não aprovado, alteração de escopo/audiência/sensibilidade, seleção de segundo item, acesso a vault/sync/cache amplo, reuso de identidade, chave SSH nova não pinada, arquivo acima do limite ou ação irreversível sem rollback.

Após acesso ao único item, pare imediatamente e execute A5 se for revelado segredo, PII sensível, transcript, estado vivo, classificação inesperada, erro de validação, publicação fora da árvore exata ou qualquer teste negativo aceito. Não há substituição automática por outro registro.

## 8. Fora de escopo

- Todo item além do ID aprovado, qualquer busca/listagem/classificação prévia ou publicação recorrente.
- Novos bots, perfis, gateway, rota Telegram, serviço, timer, cron, backup, sync, writer, reconciliador ou mudança de autoridade.
- Leitura/escrita de Mindwtr, Odoo, GTD, CRM, inbox, archive, notas pessoais ou vault pessoal completo.
- Evidência de que a projeção real prova isolamento de todo o vault ou recuperação canônica multiusuário.

## 9. Texto único para aprovação humana

> **Aprovo a execução integral da CS-033, incluindo criação temporária da pipeline, verificações, testes negativos, revogação e cleanup enumerados. Designo exclusivamente o registro canônico `<AK-ID>` no escopo literal `<SCOPE-APROVADO>`, para a audiência `vps-projection`, com sensibilidade `<public|internal>`. Confirmo que ele pode ser disponibilizado somente ao consumidor técnico `ak-real-consumer` na VPS, em uma única projeção de até 16 KiB (24 KiB totais), com TTL máximo de 30 dias e nunca além de seu `expires_at`. Autorizo o acesso somente a esse ID após as validações fail-closed; qualquer divergência, dado sensível, necessidade de novo privilégio/credencial ou ação fora da CS deve parar e permanecer bloqueada.**

Os três valores entre `<…>` são a única decisão humana material: o ID, o escopo literal e uma classificação já positiva. O texto não pede nem aceita senha, token ou chave em chat.

## 10. Evidência esperada após execução

Só uma execução aprovada poderá adicionar evidência operacional: logs sanitizados, read-backs de recursos, resultados dos testes positivos/negativos, revogação e ausência posterior. O conteúdo do registro, título, locator e qualquer segredo não entram em `EVIDENCE.md`, chat ou auditoria.