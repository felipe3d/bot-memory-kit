# Contrato de memória — WP-010

**Estado:** v0.1 aprovada em 2026-09-18; revisão documental v0.2 incorpora a direção autorizada no handoff pessoal, sem aprovação de execução.
**Versão:** 0.2 (documental)

**Autoridade deste documento:** contrato de planejamento; não autoriza writer, reconciliador, índice, perfil, credencial, vault nem mudança de host.

## 1. Limites e autoridades

- `AgentKnowledge/canonical/` contém somente conhecimento aprovado. Obsidian é sua autoridade de armazenamento.
- `AgentKnowledge/inbox/<host>/` contém candidatas não confiáveis; nunca é retorno normal de recuperação.
- `AgentKnowledge/projections/` contém visões derivadas somente leitura. A autoridade continua no sistema de origem.
- `AgentKnowledge/archive/` preserva versões substituídas ou expiradas; não é verdade vigente.
- Mindwtr, Odoo e outros sistemas autoritativos não são espelhados como estado vivo no vault. Consulta autorizada de contexto GTD/CRM não equivale a persistência nem a permissão de alterar a fonte. Conhecimento estável derivado, sanitizado e aprovado pode ser registrado com proveniência; não copiar tarefas, clientes, operações vivas ou segredos.
- Transcrições brutas, segredos, dumps de configuração e dados pessoais sensíveis são proibidos em todas as áreas.

### Uso pessoal e exposição a terceiros

Especialização define a função do bot, não uma proibição absoluta de contexto entre áreas. Uma concessão explícita pode permitir consulta cruzada para o proprietário sem transferir funções nem escrita. Hospedagem na VPS não determina audiência. Para exposição a terceiros, exigir isolamento técnico demonstrado antes do acesso. Em uso pessoal, manter ferramentas/permissões existentes e controles de impacto; não afirmar isolamento forte de um assistente que possui ferramentas amplas.

A política de memória não proíbe consultas transitórias aos sistemas autoritativos por ferramentas já autorizadas; proíbe transformá-las em cópia persistente indevida. A entrega define uma fonte e seus limites, não concede acesso irrestrito ao vault.

## 2. Entidades e campos mínimos

### 2.1 Registro de conhecimento

Todo registro candidato, canônico ou arquivado possui frontmatter estruturado, preenchido pela implementação; a pessoa revisa somente o cartão em português simples, não os campos abaixo:

```yaml
id: AK-<imutável>
status: candidate|canonical|superseded|expired|archived|rejected|quarantined
owner: <humano ou papel responsável>
scope: <domínio e audiência autorizados>
sensitivity: public|internal|restricted|prohibited
source:
  - kind: <document|system-record|human-review|observation>
    locator: <referência citável, sem segredo>
    observed_at: <ISO-8601 ou null>
    captured_at: <ISO-8601>
    captured_by: <host ou papel>
verified_at: <ISO-8601 ou null>
revision: <inteiro crescente>
review_required: <none|human|designated-role>
expires_at: <ISO-8601 ou null>
supersedes: <id ou null>
superseded_by: <id ou null>
```

Corpo obrigatório: afirmação atômica, contexto suficiente, limite de uso, evidência citada e, quando aplicável, condição de expiração. `id` não muda; uma correção material cria nova revisão ou novo registro vinculado. `source.locator` deve permitir ao revisor localizar a fonte sem conceder acesso adicional.

### 2.2 Candidata

Uma candidata é um registro em `inbox/<host>/` com `status: candidate`, proveniência completa e escopo explícito. O escritor não pode marcar a própria candidata como canônica, reduzir sua sensibilidade, nem removê-la para ocultar histórico.

### 2.3 Decisão de revisão

A promoção ou rejeição registra: `decision`, `decided_by`, `decided_at`, justificativa, IDs/locators avaliados e referência ao registro resultante. Essa decisão pode residir na nota canônica ou em registro de auditoria aprovado; nunca apenas em transcript. A pessoa pode aprovar/rejeitar/ajustar no canal privado autenticado: o reconciliador vincula a resposta ao cartão e revisão exatos e registra a decisão durável. Ajuste material invalida a aprovação anterior. Resposta ambígua não promove. O cartão sanitizado, origem e validade podem ser mostrados ao proprietário; não despejar fonte bruta, segredos ou conteúdo em logs/auditoria/canais alheios. Auditoria registra metadados mínimos, não o corpo da nota.

## 3. Sensibilidade e ACL

| Nível | Conteúdo permitido | Leitura | Escrita | Recuperação |
|---|---|---|---|---|
| `public` | informação deliberadamente pública e não operacional | papéis explicitamente concedidos | humano ou automação aprovada no destino permitido | somente dentro de `scope` |
| `internal` | procedimento e conhecimento não público de baixo risco | papéis do escopo | humano; candidata por writer autorizado | somente dentro de `scope` |
| `restricted` | informação operacional cuja divulgação amplia risco | mínimo de papéis/grants técnicos nomeados | humano ou reconciliador designado; nunca writer candidato | somente após ACL técnica e `scope` positivos |
| `prohibited` | segredos, transcrições brutas, dumps, dados pessoais sensíveis e estado vivo de negócio | ninguém no vault | ninguém | nunca; rejeitar/quarentenar a entrada |

A ACL efetiva é a interseção de papel, audiência, domínio/`scope`, sensibilidade e grant técnico. Ausência de grant, ambiguidade de escopo, identidade não autenticada ou falha de política resulta em **negação**. Prompt, nome de perfil e instruções não substituem ACL técnica. Writers só recebem `create candidate` no próprio `inbox/<host>/`; não recebem leitura ampla de inbox, escrita canônica, alteração de ACL, purge ou promoção.

## 4. Lifecycle e responsáveis

| Transição | Pré-condição | Responsável autorizado | Resultado |
|---|---|---|---|
| captura → candidata | entrada permitida, sanitizada, com campos mínimos | writer autorizado ou humano | cria em `inbox/<host>/` |
| candidata → validada | fonte citável verificada, classificação e escopo conferidos | revisor humano/designado | decisão de validação registrada; ainda não é verdade |
| validada → canônica | revisão exigida concluída, conflito resolvido e ACL aprovada | reconciliador designado ou humano | cria/atualiza `canonical/`, com revisão e proveniência |
| candidata → rejeitada | proibida, insuficiente, fora de escopo ou não verificável | revisor ou política de ingestão | mantém registro/auditoria mínima; não recuperável |
| candidata → quarentenada | aparência de instrução maliciosa, segredo, PII, ambiguidade grave ou falha de scanner | política de ingestão ou revisor | bloqueada de recuperação, para tratamento humano |
| canônica → supersedida | nova versão aprovada ou fonte autoritativa mudou | reconciliador designado ou humano | aponta bidirecionalmente para substituta; deixa de ser vigente |
| canônica → expirada | `expires_at` atingido ou condição de validade falhou | processo aprovado ou humano | deixa de ser retorno normal até revisão |
| supersedida/expirada → arquivada | referência cruzada e histórico preservados | reconciliador designado ou humano | move para `archive/`, não recuperável por padrão |
| qualquer não-canônica → corrigida | erro material identificado | autor da decisão ou revisor | nova revisão/registro com vínculo; não apagar a trilha |

Nenhuma transição é autorizada somente por texto importado, instrução de nota, transcript histórico ou alegação do writer. A resposta humana autenticada ao cartão vigente é uma decisão válida quando registrada conforme §2.3, não uma instrução importada. A aprovação única da entrega pode cobrir as transições enumeradas; não exigir novo change set por transição já coberta. Elas devem ser idempotentes, auditáveis e fail-closed.

## 5. Recuperação citada

1. Autenticar o solicitante e calcular sua ACL técnica antes de buscar.
2. Pesquisar apenas registros `canonical` vigentes, dentro de `scope`, audiência e sensibilidade permitidos.
3. Para cada afirmação apresentada, devolver `id`, `revision`, `verified_at` e a citação `source.locator`; distinguir fato citado, inferência e ausência de evidência.
4. Nunca apresentar candidata, quarentena, rejeitada, supersedida, expirada, arquivada ou projection como verdade canônica. Projeções podem ser mostradas apenas se a política futura explicitamente as permitir e identificando sua fonte autoritativa.
5. Se não houver fonte canônica acessível, informar ausência de memória verificada; não completar a partir de transcript nem buscar fora do grant. Uma consulta separadamente autorizada ao sistema de origem pode responder ao pedido como consulta atual, sem alegar recuperação de memória e sem persistir automaticamente.
6. Se fontes canônicas conflitarem, não escolher por recência implícita: retornar o conflito com IDs/citações ou escalar à revisão. A promoção fica bloqueada até decisão registrada.
7. Se a fonte citada não estiver acessível ao solicitante, a resposta só pode expor a afirmação se a ACL da própria nota permitir; nunca vazar conteúdo da fonte para contornar a ACL.

## 6. Correção, supersessão, expiração e arquivamento

- Correção preserva `id`, revisão anterior, autor/tempo da decisão e fonte. Alterações materiais não sobrescrevem silenciosamente o conteúdo aprovado.
- Supersessão exige vínculo recíproco (`supersedes` e `superseded_by`) e razão; a sucessora deve estar canônica antes da predecessora deixar de ser vigente.
- Registros sujeitos a mudança devem ter `expires_at` ou condição documentada de revalidação. Sem isso, o revisor deve justificar explicitamente a ausência.
- Expiração suspende recuperação normal; revalidação cria nova revisão com nova data e fonte.
- Retirada solicitada pelo proprietário suspende imediatamente o retorno normal, inclusive índices/caches derivados, e arquiva o registro com a decisão. Recuperação futura deve comprovar ausência; retirar não é apagar histórico ou prometer exclusão de transcripts antigos.
- Arquivamento preserva proveniência e cruzamentos, aplica a mesma ACL ou mais restritiva e não equivale a exclusão. Exclusão/purge exige política e escopo explicitamente aprovados; não está implícita em retirada.

## 7. Entrada não confiável e prompt injection

Todo conteúdo importado é dado, nunca instrução. O pipeline deve tratar URLs, frontmatter, Markdown, anexos, trechos de transcript e texto que tenta alterar política como conteúdo potencialmente hostil. Uma candidata não pode conceder capacidades, mudar escopo/ACL, ordenar sua própria promoção, desabilitar logs, solicitar exfiltração ou determinar o comportamento do reconciliador. Tais tentativas são classificadas como candidata insegura e encaminhadas à quarentena.

## 8. Testes de aceitação negativos para implementação futura

A implementação deve demonstrar os critérios aplicáveis à entrega, com evidência reproduzível; requisitos de isolamento de terceiros permanecem bloqueantes antes de tal exposição, não um gate universal anterior ao aprendizado pessoal:

1. Writer autorizado cria candidata apenas no seu `inbox/<host>/`; tentativa de escrever `canonical/`, `archive/`, `projections/` ou inbox alheio é negada.
2. Candidata não aparece em busca/recuperação normal, inclusive quando contém termos mais relevantes que a nota canônica.
3. Identidade sem grant, consulta cruzada sem autorização e audiência compartilhada sem autorização não recebem conteúdo, metadados sensíveis nem existência inferível de registro `restricted`.
4. Entrada sem proveniência, com fonte inacessível, escopo ausente, sensibilidade ausente ou campo obrigatório inválido não promove.
5. Prompt injection em nota candidata não altera decisão, ACL, ferramentas, escopo, instruções de sistema nem resulta em execução de ação externa.
6. Segredo, dump, PII sensível ou transcript bruto é rejeitado/quarentenado e não fica recuperável.
7. Conflito entre fontes bloqueia promoção e a recuperação informa conflito/ausência em vez de escolher silenciosamente.
8. Supersedida, expirada e arquivada não retornam como vigente; o registro vigente aponta à fonte/revisão correta.
9. Falha de backend, scanner, ACL ou auditoria falha fechada: não promove e não recupera conteúdo fora do grant.
10. Cada decisão de promoção, correção, supersessão, expiração e arquivamento deixa trilha citável sem segredos.

## 9. Aprovação e limite de prova

Aprovação documental não autoriza implementação. Uma entrega delimitada, como CS-034, deve nomear fonte, destinos, operações, identidade, testes, retries seguros e rollback; uma única aprovação cobre esse conjunto, sem gates por arquivo ou por detalhamento. Mudanças não enumeradas de vault, host, perfil, credencial, gateway, release, unit, backup ou rotas exigem parar e revisar o escopo.

Os testes acima são requisitos, não resultados obtidos. No piloto pessoal, declarar precisamente a fronteira exercitada pelo componente e as capacidades já amplas do default; não alegar contenção de SO, isolamento de terceiros ou segurança integral com base em uma skill ou teste sintético.
