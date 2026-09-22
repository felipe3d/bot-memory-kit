# CS-030 — Acesso 24/7 ao subconjunto autorizado de AgentKnowledge

**Estado:** BLOCKED  
**Revisão:** 2.6 — Gate P executado; limpeza do repositório pendente  
**Work package:** WP-030 — isolamento do AgentKnowledge e VPS  
**Janela/host:** nenhuma; proposta documental. Qualquer host, identidade, cofre, transporte ou credencial permanece não descoberto e não alterado.

## Problema e resultado esperado

A VPS pode precisar recuperar, 24/7, somente conhecimento `canonical` vigente de um subconjunto explicitamente autorizado de `AgentKnowledge`. Ela não pode receber acesso ao vault pessoal nem herdar credenciais, sessão, sync, home Hermes ou acesso de outro papel.

**Resultado proposto para decisão:** preferir uma projeção publicada fora do vault pessoal (alternativa C), com leitura da VPS por identidade técnica exclusiva e escopo fixo. A projeção contém somente registros elegíveis após filtro positivo de `scope`, audiência, status e sensibilidade. Não é um vault compartilhado, não aceita escrita da VPS e não é fonte canônica.

O Gate D selecionou documentalmente Git privado dedicado + deploy key read-only como candidata de piloto, não de produção. Esta revisão detalha apenas o desenho; nenhum recurso é descoberto, criado ou aplicado.

## Escopo

### Incluído nesta proposta

- Comparar três arquiteturas para leitura 24/7 do subconjunto autorizado.
- Definir fronteiras, identidade técnica mínima, fail-closed, rollback e provas negativas obrigatórias.
- Definir gates separados para discovery, spike e aplicação.

### Alternativas comparadas

| Alternativa | Desenho | Vantagens | Riscos/resíduos | Parecer |
|---|---|---|---|---|
| A. Vault dedicado + identidade técnica mínima | Um vault separado contém apenas a projeção autorizada; a VPS usa conta técnica read-only, exclusiva desse vault. | Separação física compreensível; ACL do fornecedor pode ser direta. | Ainda introduz outro vault/sincronizador, membro técnico e possível confusão entre cópia e canônico. É preciso provar que convite, links, histórico, cache e clientes não dão visibilidade ao vault pessoal. | Aceitável apenas se C não atender disponibilidade/recuperação; exige prova forte do limite por vault. |
| B. Broker allowlisted/default-deny | A VPS chama um broker que autentica a identidade, calcula ACL e devolve apenas resultados permitidos; todas as rotas e scopes não allowlisted negam. | Centraliza auditoria, expiração, busca citada e revogação. | Maior superfície e complexidade; uma falha de autorização, indexação, cache ou rota pode expor metadados/conteúdo. O broker precisa acessar uma fonte, portanto não resolve por si só a fronteira do vault. | Não selecionar como primeiro passo. Pode ser camada futura sobre C, após testes isolados. |
| C. Sem acesso compartilhado ao vault — projeção publicada | Um processo aprovado no lado autorizado materializa uma projeção read-only, sanitizada e versionada; a VPS lê somente essa publicação por identidade própria. Vault pessoal nunca é montado, sincronizado nem credenciado na VPS. | Menor privilégio e fronteira mais simples: a VPS não possui caminho técnico ao vault; rollback é revogação da publicação/identidade. Evita sobreposição de sincronizadores. | Exige definir publicação, retenção, atualização, integridade e disponibilidade; a projeção pode ficar defasada e não pode conter `restricted` sem decisão posterior. | **Recomendada para spike**, inicialmente apenas `public`/`internal` explicitamente elegíveis, com recuperação fail-closed. |

### Descoberta Fase 0 — concluída (documental, sem host/credencial/conteúdo)

| Pergunta | Fato verificado | Consequência |
|---|---|---|
| Vault dedicado com membro técnico pode ser read-only? | A documentação atual do Obsidian Sync diz que permissões granulares não são suportadas; colaboradores recebem as mesmas permissões do proprietário, exceto convidar. E2EE requer que cada colaborador informe a senha de criptografia. | **A não satisfaz leitura técnica imutável.** Mesmo que uma conta separada só seja convidada ao vault dedicado, ela recebe capacidade de escrita naquela cópia e exige credencial/senha local. `pull-only` é comportamento do cliente, não ACL. |
| Headless reduz privilégio por si só? | Headless é beta, requer autenticação de conta e `sync-list-remote` enumera vaults disponíveis à conta; `sync-unlink` remove credenciais locais. | Não usar a conta pessoal no VPS. A opção A continua exigindo cliente, estado de credencial e uma conta técnica distinta; isso não atende o objetivo mais simples de não compartilhar vault. |
| Há identidade técnica mínima para bootstrap de credenciais? | Service Accounts do 1Password têm acesso e permissões imutáveis por vault, não podem acessar vaults Personal/Private/Employee/Shared padrão e podem ser revogadas. | É adequada somente para segredo de bootstrap de um produtor/broker futuro, em vault de automação separado. Não concede nem substitui ACL de AgentKnowledge e não deve residir no agente VPS. |
| A projeção sem vault compartilhado é viável conceitualmente? | Obsidian armazena notas como Markdown local; o contrato do programa já define projeções derivadas read-only e o `setup-vault.py` separa `canonical`, `inbox` e `archive`. | **C permanece a candidata para Fase 1.** A Fase 1 deve usar dados e publicação sintéticos; a tecnologia concreta de publicação continua não selecionada. |

Fontes públicas verificadas em 2026-09-18: [Obsidian Collaboration](https://obsidian.md/help/sync/collaborate), [Headless Sync](https://obsidian.md/help/sync/headless), [Obsidian Headless](https://obsidian.md/help/headless), [Obsidian data storage](https://help.obsidian.md/Files+and+folders/How+Obsidian+stores+data), [1Password Service Accounts](https://www.1password.dev/service-accounts/get-started) e [security model](https://www.1password.dev/service-accounts/security/). Nenhuma conta, host, vault existente, credencial, caminho privado ou nota foi consultado.

### Limites invariáveis da opção recomendada

- O artefato publicado é uma projeção derivada read-only, nunca `canonical`, inbox, archive, state.db ou home Hermes.
- A seleção é positiva: `status: canonical`, vigente, `scope` e audiência explicitamente permitidos, e sensibilidade autorizada. Ausência de campo/grant resulta em exclusão.
- A VPS não escreve em qualquer área de AgentKnowledge e não pode promover, alterar ACL, solicitar sincronização, regenerar a projeção ou acessar a fonte.
- A publicação não inclui segredos, PII sensível, transcrições, dumps, dados vivos de GTD/CRM, `prohibited`, inbox, archive ou conteúdo fora do subconjunto aprovado.
- A identidade técnica da VPS é exclusiva dessa leitura; não reutiliza credencial pessoal, de sync, de outro host/papel, `.env`, `auth.json`, sessão OAuth ou conta do reconciliador.
- Falha de autenticação, política, integridade, publicação ou auditoria nega a recuperação e não revela conteúdo nem existência de registros fora do grant.

## Fora de escopo

- Discovery de hosts, redes, serviços, provedores, contas, vaults, membros, chaves, tokens, sessões, configurações, paths locais ou conteúdo de AgentKnowledge.
- Criação, convite, remoção ou alteração de vault, membro, identidade, credencial, perfil, MCP, gateway, release, unit, backup, sincronizador, rota Telegram ou serviço.
- Instalação de Headless, broker, índice, storage, transporte, timer, cron, writer ou reconciliador.
- Migração de writers, alteração do piloto P1-A2, acesso GTD/CRM, ou leitura de dados pessoais.

## Pré-requisitos e baseline

1. Permanecem vinculantes `MEMORY-CONTRACT.md`, `BOT-POLICY-MATRIX.md`, ADR-003 e os guardrails de `CURRENT.md`.
2. Antes de cada fase, registrar apenas o baseline mínimo necessário, sem segredos nem dumps de configuração.
3. O subconjunto precisa ser definido por uma lista positiva revisável: scopes, audiência, sensibilidades, status, formato, TTL/expiração e comportamento para ausência/conflito.
4. A publicação só pode ser considerada depois de existir um produtor aprovado, uma política de sanitização e uma trilha de proveniência/citação compatível com o contrato.
5. O plano de disponibilidade, integridade, retenção e recuperação deve ser especificado antes da aplicação; 24/7 não justifica ampliar escopo.

## Provas negativas obrigatórias

A aprovação para dados reais depende de evidência reproduzível e sanitizada dos itens abaixo. A autorização anterior para executar testes sintéticos não certifica essas provas operacionais.

| ID | Afirmação negativa a provar | Método mínimo de teste | Resultado exigido |
|---|---|---|---|
| N-01 | A VPS não acessa o vault pessoal. | Com identidade, rede e runtime reais da VPS, tentar os caminhos de acesso definidos no spike: mount, sync/API, compartilhamento, link/convite, endpoint e caminho de transporte conhecidos. | Todas as tentativas negadas ou inexistentes; não há mount, cliente, token, rota, sessão nem artefato que permita listar/ler o vault. |
| N-02 | A VPS não acessa credenciais alheias. | Inspecionar por allowlist as superfícies autorizadas no runtime e executar testes de acesso cruzado contra credenciais pessoal, sync, reconciliador e outros papéis, sem revelar valores. | Ausência de arquivos/variáveis/montagens/handles e falha autenticada ou não autenticada nos testes cruzados; a identidade VPS não é aceita fora do serviço de projeção. |
| N-03 | A VPS não recupera conteúdo fora do scope. | Consultas com scope permitido, ausente, divergente, de outro domínio, `restricted`, `prohibited`, inbox, archive, expirada e ID adivinhado; repetir contra busca, listagem, metadados, erros, logs e cache. | Apenas itens elegíveis retornam; todos os demais falham fechados sem conteúdo, metadado sensível ou confirmação de existência. |
| N-04 | A VPS não escreve nem influencia a fonte. | Tentar criar/alterar/apagar projeção, canônico, ACL, filtros, publicação e auditoria pela identidade VPS e por entrada recuperada/injetada. | Negação e trilha de auditoria mínima; nenhum efeito persistente na fonte ou na política. |
| N-05 | Revogação corta acesso sem afetar outros papéis. | Revogar temporariamente a identidade/grant no spike e testar leitura VPS, produtor e consumidores não relacionados. | VPS falha fechada; produtor e papéis fora do grant permanecem intactos; restauração exige gate e leitura posterior. |
| N-06 | Falha operacional não amplia acesso. | Induzir falha controlada de publicação, ACL, integridade, backend e auditoria. | Sem fallback ao vault, sync, cache amplo ou credencial alternativa; resposta é ausência/erro seguro. |

A evidência deve registrar comando/ação, identidade de teste por papel, alvo lógico, horário, resultado, logs sanitizados e leitura posterior do alvo. Nunca registrar segredo, conteúdo pessoal, dump de configuração ou dados de cliente.

## Plano de aplicação

**Fase 0 — discovery documental (concluída):** aprovada explicitamente pelo usuário em 2026-09-18 e executada somente contra documentação pública e código do repositório. Os resultados estão em “Descoberta Fase 0”. Não leu conteúdo do vault, não abriu credenciais, não criou identidades e não alterou hosts.

**Fase 1 — escopo histórico do spike (concluído somente no modelo sintético local):** criar ambiente descartável com dados sintéticos e escopo sintético, uma identidade VPS sintética/mínima e uma publicação sintética. Exercitar N-01 a N-06 e rollback. Não conectar vault pessoal, AgentKnowledge real, identidade existente ou produção. O desenho do spike deve selecionar uma tecnologia de publicação somente após nova aprovação humana.

**Fase 1.5 — revisão documental para discovery de aplicação (concluída):** autorizada explicitamente pelo usuário em 2026-09-18, sem executar discovery. A revisão 1.5 definiu o escopo documental do Gate D abaixo; não autorizou leitura de hosts, vaults, credenciais, configurações ou conteúdo real.

**Gate D — escopo histórico aprovado e concluído somente documentalmente:** os grupos abaixo foram tratados sem acesso a recursos reais. Qualquer discovery real adicional exige o novo Gate H definido nesta revisão:

1. **Produtor autorizado:** identificar papel/host candidato, sem ler notas, vault, home Hermes, estado de sync ou configuração integral.
2. **Publicação candidata:** identificar tecnologia e serviço candidatos, versão/capacidades declaradas, limites de leitura, integridade, TTL, auditoria e revogação; não criar, instalar, autenticar nem listar dados.
3. **Identidade VPS:** identificar somente o tipo de identidade, emissor, escopo lógico, canal de armazenamento protegido e mecanismo de revogação; nunca abrir token, chave, sessão, variável, cofre ou referência secreta.
4. **Superfícies de prova:** enumerar alvos lógicos de N-01/N-02 — mount, cliente/sync, API, compartilhamento, sessão, armazenamento de segredo e egress — e o resultado esperado de negação; não executar tentativas ainda.
5. **Viabilidade do teste:** identificar ambiente isolado, dados sintéticos, responsáveis, logs sanitizados e rollback para um piloto; bloquear se exigir vault pessoal, identidade existente ou conteúdo real antes de gate próprio.

**Saída obrigatória do Gate D:** inventário de metadados sanitizado, uma única tecnologia candidata ou justificativa de bloqueio, desenho de piloto, lista de mudanças exata, rollback, testes N-01 a N-06 mapeados e uma revisão posterior deste CS. Ausência, ambiguidade ou incompatibilidade de qualquer controle é resultado `BLOCKED`, não permissão para ampliar descoberta.

**Proibido no Gate D:** leitura/listagem de Markdown, conteúdo de vault, histórico, cache, state.db, home Hermes, variáveis, arquivos de credencial, tokens, chaves, sessões, dumps de configuração; criação/convite de conta, identidade, vault, serviço, storage, regra de rede, instalação ou alteração de host.

### Gate H — resultado (BLOCKED após discovery mínimo)

O Gate H foi executado dentro do escopo aprovado e produziu somente metadados sanitizados. A conta local `felipe3d` é candidata no GitHub; `oracle-vps` é candidata de consumidor Ubuntu/aarch64 com uma raiz de teste ainda ausente; e, após reconsulta limitada com o HomeLab ligado, `homelab-producer` é candidato Linux/x86_64 com raiz de teste ausente. Também não há audit store separado, mecanismo de confiança/autenticação de manifesto ou confirmação de capacidade de criação de repositório.

Consequentemente, **Gate H permanece `BLOCKED` e Gate P não pode ser solicitado**: a disponibilidade do produtor deixou de ser bloqueio, mas isolamento de SO, identidade técnica, auditoria, confiança e capacidade administrativa continuam sem decisão/validação. A evidência, fontes, limites e decisões bloqueantes estão em `program/evidence/CS-030-gate-h-minimal.md`. Não houve criação/alteração, acesso a vault/conteúdo/configuração/credencial/segredo, nem teste real N-01–N-06.

### Gate D — resultado (concluído, metadados documentais)

- **Candidata única para piloto:** repositório Git privado dedicado à projeção + deploy key SSH exclusiva e read-only por repositório para o consumidor VPS.
- **Produtor:** papel lógico de publicador aprovado no lado autorizado; host físico não foi selecionado nem consultado.
- **Integridade/revogação:** revisão Git + manifesto de integridade/TTL a definir no piloto; revogação proposta é remover a deploy key. Deploy key não tem expiração nativa, portanto rotação e revogação exercitadas serão requisito obrigatório.
- **Resultado de segurança:** a candidata preserva a separação do vault, mas ainda não prova o isolamento de SO, a disponibilidade 24/7, armazenamento de chave ou N-01/N-06 no ambiente real.

A evidência sanitizada, superfícies N-01–N-06, desenho de piloto e bloqueios estão em `program/evidence/CS-030-gate-d-discovery.md`. Não houve consulta a host, conta, repositório, vault, credencial, configuração ou conteúdo real.

## Fase 2 — desenho do piloto Git privado sintético

**Estado: AWAITING_APPROVAL.** Revisão documental autorizada pelo handoff `session-prompt-CS-030-phase2-design.md`. Todos os recursos abaixo são **propostos, ainda não criados**. Esta seção rege a futura Fase 2; as fases anteriores são histórico, não autorização reutilizável. O piloto exercitará Git/SSH e um consumidor isolado de teste, não o bot, o gateway nem a recuperação canônica em produção.

### 1. Artefatos propostos e fronteiras

| ID | Artefato ainda não criado | Conteúdo/capacidade permitida | Alvo pendente |
|---|---|---|---|
| A-01 | Repositório privado novo e dedicado | Histórico inicialmente vazio; apenas projeção sintética, manifest e, se aprovado, envelope de assinatura. Sem forks, integrações, Actions, submodules ou LFS no piloto. | `<GIT_ACCOUNT>/<PILOT_REPO>` |
| A-02 | Um par de chaves de deploy descartável | SSH, exclusivo de A-01 e do consumidor; registro explicitamente read-only, write desabilitado. Privada nunca no Git, chat ou auditoria. | `<CONSUMER_KEY_STORAGE>` e `<DEPLOY_KEY_ID>` a registrar após criação autorizada |
| A-03 | Consumidor de teste isolado | Somente fetch/leitura e validação; sem push/admin, vault, sync ou ferramentas do Hermes. Execução manual, sem serviço permanente. | `<CONSUMER_HOST>`, `<CONSUMER_OS_ID>`, `<CONSUMER_TEST_ROOT>` |
| A-04 | Publicador de teste separado | Gera fixtures e publica somente em A-01. Identidade técnica distinta do consumidor e do administrador, sem privilégio administrativo do repositório. | `<PRODUCER_HOST>`, `<PRODUCER_OS_ID>`, `<PRODUCER_TEST_ROOT>`, `<PUBLISHER_AUTH>` |
| A-05 | Um arquivo `projection.synthetic.json` | JSON UTF-8 de registros fictícios `AK-SYN-*`, origem `synthetic://`, envelope `kind: projection`, nunca notas reais. | Relativo à raiz de A-01; nenhum caminho de produção |
| A-06 | `manifest.json` e eventual envelope de confiança | Integridade, revisão, lista positiva, origem, audiência, sensibilidade e TTL. | Raiz de A-01 e `<TRUST_ANCHOR_STORAGE>` separado |
| A-07 | Auditoria sanitizada | Eventos mínimos do ensaio e read-backs; fora do repositório de projeção, sem conteúdo, credencial ou identificadores pessoais. | `<AUDIT_STORE>`, `<AUDIT_RETENTION>` |
| A-08 | Rotina de limpeza e inventário do piloto | Lista fechada de IDs e paths criados; revoga chave e remove apenas recursos desse inventário. Não usa glob, descoberta recursiva nem limpeza genérica. | `<CLEANUP_ARTIFACT>` sob raiz de teste aprovada |

A fonte canônica e o vault pessoal **nunca entram no piloto**, nem como entrada, mount, link, cópia, backup ou dependência. O produtor não recebe acesso ao vault pessoal da VPS nem a qualquer vault real. O repositório nunca recebe conteúdo real, `restricted`, `prohibited`, inbox, archive, estado Hermes, segredo, PII ou transcript — nem em branches, tags, histórico, mensagens de commit, anexos, logs ou objetos descartados. Metadados de autoria dos commits usam identidade técnica sintética aprovada, não identidade pessoal herdada.

Fixtures negativas rotuladas `restricted`/`prohibited`, inbox/archive, outro scope ou expiradas serão geradas somente em memória no teste de pré-publicação, sem conteúdo pessoal e **nunca commitadas**. Rejeições não publicam seus IDs nem seus metadados. O repositório contém exclusivamente dados sintéticos elegíveis de uma única audiência/grant.

**Limite técnico do Git:** deploy key restringe por repositório, não por arquivo, ref, scope ou TTL. Um consumidor pode ler todo o histórico/refs/objetos acessíveis do repositório; filtros locais não são ACL Git. Por isso, nunca misturar grants nem enviar fixtures proibidas ao servidor. Ref allowlisted e TTL controlam a entrega pelo consumidor de teste, não a leitura bruta do Git nem cópias que já saíram. Não se promete confidencialidade retroativa nem expiração física dos objetos históricos. Qualquer cenário que exija essas garantias bloqueia esta candidata e exige nova decisão arquitetural.

### 2. Identidade e menor privilégio

- Consumidor: uma deploy key nova, exclusiva de A-01 e read-only explícito, sem write/push/admin ou uso em outro repositório. Sem agent forwarding, agente SSH compartilhado, fallback de identidade, helper de credenciais pessoal, sessão OAuth ou credencial de sync. Transporte valida a identidade do servidor por âncora aprovada; não desabilitar host-key checking nem confiar em descoberta de chave sem verificação.
- Publicador: identidade técnica separada, limitada à publicação em A-01; sem administração de chaves, conta ou vault. `<PUBLISHER_AUTH>` é decisão humana, nunca PAT pessoal ou credencial existente emprestada. O mecanismo pode exigir outro segredo técnico; sua criação, armazenamento e revogação precisam estar no inventário aprovado, sem segunda deploy key implícita.
- Administrador humano/técnico: `<REPO_ADMIN_ROLE>` provisiona e revoga recursos pelo mecanismo dedicado `<ADMIN_AUTH>`. Esta revisão não reutiliza login, PAT, sessão OAuth, 1Password ou credencial pessoal como bootstrap. Se não houver canal técnico autorizado, **BLOCKED**; não autenticar por conveniência.
- Isolamento: ambientes consumidor/publicador sem mounts de homes, vaults, estado Hermes, sockets de agentes ou secrets alheios. Identidades de SO, paths e controles concretos dependem de decisão e eventual Gate H. Consumidor não modifica executável, política, âncora de confiança nem auditoria; área temporária de fetch é separada da política e nunca fonte de confiança.
- Chave privada em armazenamento protegido aprovado, legível apenas pelo processo/papel necessário, sem backup ou exportação automática. Registrar apenas alias/fingerprint aprovado e ID do recurso em inventário protegido; relatório público usa aliases lógicos. Não escolher local de chave nesta revisão.
- Deploy keys não expiram automaticamente: `<KEY_REVOKE_DEADLINE>` e responsável são obrigatórios. Revogar ao fim do ensaio ou incidente; nenhum cron/timer implícito. Rotação: revogar a antiga, comprovar negação, gerar substituta apenas por autorização específica com inventário novo, sem reaproveitar a privada. A revisão atual propõe um único par descartável, não autoriza a segunda chave de um teste de rotação.

### 3. Manifest — formato e validação proposta

Nomes de arquivos são relativos ao artefato sintético, não caminhos reais. JSON estrito UTF-8, sem chaves duplicadas, campos inesperados, links simbólicos, caminhos absolutos ou traversal. O schema e limites máximos de bytes/registros serão fixados no anexo de execução antes da aprovação; não importar Markdown ou executar conteúdo.

| Campo mínimo | Regra proposta |
|---|---|
| `schema_version`, `kind`, `synthetic` | Versão de schema aprovada, `projection-manifest`, booleano `true` obrigatório |
| `pilot_id`, `publication_id` | Identificadores sintéticos únicos; impedir mistura entre ensaios |
| `revision`, `previous_revision` | Inteiro crescente e anterior explícita/null inicial; rejeitar replay/downgrade |
| `scope`, `audience`, `sensitivity` | `synthetic.cs030`, `synthetic-consumer`, `internal`; `synthetic: true` qualifica os dados, não cria uma quinta sensibilidade contratual |
| `origin` | `kind: synthetic-fixture`, locator `synthetic://cs030/phase2`; sem caminho, nota ou hostname pessoal |
| `publisher` | Alias lógico sintético, vinculado à âncora aprovada fora do repositório |
| `issued_at`, `verified_at`, `expires_at`, `ttl_seconds` | UTC ISO-8601; proposta de TTL máximo de 300 segundos, sujeita à aprovação; `expires_at = issued_at + ttl_seconds` |
| `files` | Lista exata de um payload: path `projection.synthetic.json`, tamanho em bytes, `sha256` hexadecimal e quantidade de registros |
| `policy_version` | Revisão da política local aprovada; o manifest não pode conceder grant nem substituir política |
| `integrity` | Algoritmo `SHA-256`, modo `<INTEGRITY_TRUST_MODE>` e referência lógica à âncora/envelope confiável |

Cada registro sintético conserva `id`, `revision`, `verified_at`, `source.locator`, owner/papel, scope, audiência, sensibilidade, status de origem simulado e expiração. O envelope distingue projeção derivada de fonte canônica; rótulo `canonical` nas fixtures simula elegibilidade, não promove conhecimento. Nenhuma saída é servida como fato real ou incorporada à memória Hermes.

**Forma de integridade proposta:** SHA-256 sobre os bytes exatos de `projection.synthetic.json`, sem normalização de newline, comparado ao digest do manifest. O manifest deve ser autenticado externamente: ou assinatura destacada dos seus bytes exatos, com verificador/chave pública pinados fora do Git, ou digest SHA-256 dos seus bytes entregue por canal independente autenticado e aprovado. `<INTEGRITY_TRUST_MODE>`, `<SIGNATURE_MECHANISM_OR_NONE>` e `<TRUST_CHANNEL>` permanecem decisões humanas bloqueantes; não selecionar algoritmo de assinatura por inferência. Hash junto ao payload detecta corrupção, **não autentica o produtor**. Hash/commit Git sozinho tampouco satisfaz essa autenticação.

A revisão Git concreta `<EXPECTED_COMMIT_OID>` e `<ALLOWED_REF>` ficam no envelope/registro de aprovação externo, ligado ao digest do manifest; não gravar no manifest o OID do commit que contém o próprio manifest (dependência circular). O ensaio valida o OID exato, e não apenas o nome mutável da branch. A política de leitura e a âncora nunca são carregadas como autoridade a partir da projeção.

**Ordem fail-closed:** autenticar transporte/identidade → fetch online restrito ao repo aprovado sem hooks/submodules/helpers externos → conferir commit/ref e âncora → autenticar bytes do manifest → validar schema, política, relógio/TTL/revisão → conferir lista de arquivos, tamanhos e hashes → validar todos os registros → registrar auditoria → entregar somente saída sintética citada. Qualquer divergência rejeita a publicação inteira. Relógio indisponível, regressivo ou fora de `<CLOCK_SKEW_BOUND>` nega; tolerância não estende `expires_at`. Exigir `issued_at <= now < expires_at` e TTL dentro do máximo aprovado. Registro expirado invalida entrega, ainda que o manifest esteja vigente.

Sem cache de resposta offline: cada recuperação exige nova autenticação/fetch online bem-sucedida, inclusive após revisão já baixada, e revalida TTL. Falha de rede, auth, auditoria, relógio, ref, hash ou assinatura invalida a entrega atual, sem retorno do último resultado bom. Conservar temporários para teste não permite servi-los; consumo bruto desses bytes está fora da garantia do wrapper e deve ser declarado em N-05. O piloto não promete disponibilidade 24/7: medir sucesso e negação na janela `<PILOT_WINDOW>` não é prova de operação contínua.

### 4. Sequência futura de aplicação e read-back

**Nada desta tabela é executado nesta revisão.** Cada passo só ocorre após resolução das decisões e Gate P válido para a revisão preenchida. Se exigir informação real desconhecida, parar e solicitar Gate H, sem ampliar discovery. Recursos devem nascer vazios; colisão com recurso existente interrompe, sem sobrescrever. O baseline é a ausência atestada do alvo novo no canal autorizado, não inventário do host/conta inteira. Falha de read-back interrompe a sequência e aciona a reversão correspondente.

| Passo | Criação/modificação proposta e pré-requisito | Responsável lógico | Leitura posterior obrigatória | Rollback correspondente |
|---|---|---|---|---|
| P-00 | Fixar anexo de alvos/ações/limites, janela, owners, inventário vazio, TTL, confiança e auditoria; obter gates | Humano aprovador | Conferência documental de ausência de placeholders de entrada, procedimentos para IDs/OIDs gerados e vínculo à revisão aprovada | Cancelar sem criar recurso |
| P-01 | Preparar apenas raízes/ambientes isolados A-03/A-04, trilha A-07 e rotina A-08, sem instalar serviço; inventário aprovado | Operador do piloto | Permissões e isolamento dos alvos exatos; escrita/leitura de evento sintético; não abrir segredo ou home | Remover apenas os recursos novos enumerados; preservar evento mínimo |
| P-02 | Criar A-01 privado vazio, sem features/integrações extras; canal técnico administrativo aprovado | Administrador | Ler configuração do repo exato: privado, vazio, sem grants inesperados; registrar alias/ID | Revogar acessos criados e excluir apenas A-01 após prova de negação |
| P-03 | Criar A-02 em storage aprovado, registrar pública em A-01 com write desabilitado; atribuir autenticação técnica limitada ao publicador conforme anexo | Operador de chaves + administrador | Ler metadados da key no repo: ID, associação e read-only; teste de leitura sintética e push negado após P-05; nunca ler privada em relatório | Revogar key e concessão técnica de publicação, confirmar remoção, remover privada pelo inventário |
| P-04 | Criar scripts de teste, fixtures, política e âncora independente; testar pré-publicação e manifest antes do upload | Publicador + revisor | Validador independente confirma payload elegível, hashes/TTL/origem; rejeições permanecem só em memória | Remover artefatos sintéticos locais e âncoras novas, sem tocar fonte |
| P-05 | Publicar apenas A-05/A-06/envelope aprovado em ref aprovada, autoria sintética; registrar OID fora do manifest | Publicador | Ler de volta o commit remoto pelo consumidor: árvore exata, bytes, digest, assinatura/âncora, histórico/refs do repo dedicado sem classes proibidas | Suspender entrega, revogar chave; excluir repo dedicado no rollback, não depender de reescrever histórico |
| P-06 | Executar leitura positiva e N-01–N-06 aplicáveis; falhas por mocks/injeção no processo isolado ou cópias locais, nunca em produção | Testador com identidade de consumidor + revisor independente | Read-backs de cada alvo conforme matriz abaixo; eventos completos antes de aceitar resultado | Parar testes e iniciar sequência de revogação/limpeza |
| P-07 | Revogar deploy key, comprovar negação online e do wrapper com clone pré-existente | Administrador + testador | Chave ausente nos metadados; nova operação autenticada negada; wrapper não serve bytes antigos, mesmo com TTL vigente | Não restaurar key; isolar processo se negação falhar e manter bloqueio |
| P-08 | Remover concessões/segredos técnicos exclusivos, repo, clones, temporários, âncoras e raízes criados; preservar A-07 mínimo | Operador + administrador | Ler alvos exatos de volta: repo ausente pelo canal administrativo autorizado, concessões revogadas, paths enumerados ausentes; auditoria retida legível | Interromper se alvo não corresponder ao inventário; sem recuperação/restauração automática |

Comandos executáveis e seletores concretos serão preenchidos no anexo aprovado, não adivinhados aqui. O anexo deve incluir comando/ação de cada linha, identidade, alvo exato, baseline, código/estado esperado, read-back independente e reversão. Não usar comandos de inventário global, `gh auth status`, `git remote`, SSH, APIs ou descoberta nesta tarefa documental.

### 5. N-01–N-06 — casos futuros e limite da prova

**Todos os testes abaixo estão PLANNED; nenhum é operacional/verificado nesta revisão.** O ensaio positivo deve entregar apenas uma amostra sintética elegível com citação sintética e revisão, nunca registrar o payload na auditoria. Para cada negativo incluir controle positivo na mesma superfície quando seguro, evitando confundir ACL com indisponibilidade geral.

| ID | Caso, identidade e superfície | Negação/aceite exigido | Evidência sanitizada esperada e limite |
|---|---|---|---|
| N-01 | Consumidor isolado tenta caminhos de fixture que representam mount, arquivo, sync/API, link/convite e transporte da fonte; usar somente stubs/alvos sintéticos aprovados | Negar acesso; nenhum fallback da projeção à fonte; ausência de mounts/integrações no ambiente criado | Alias do consumidor e superfícies, ação/exit/status, resultado sem conteúdo e read-back do isolamento. Isso prova apenas o sandbox. Vault pessoal, rotas/mounts/clientes e runtime real da VPS exigem Gate H e autorização explícita dos testes reais; nunca tentar caminhos reais por inferência |
| N-02 | Consumidor tenta acessar canários não secretos de outros papéis em sandbox: arquivo/env/mount, socket/agente, keyring e bootstrap simulados; testar identidade desconhecida contra a projeção | Canários alheios inacessíveis e identidade sem grant negada; identidade permitida lê apenas repo sintético | IDs lógicos, permissões e booleans de negação, sem valores. Não listar env/keyrings reais. Ausência de credenciais pessoais/sync/reconciliador no host real depende de Gate H com superfícies allowlisted e prova real autorizada |
| N-03 | Publicador testa filtro com fixtures em memória de scope ausente/divergente, outro domínio, sensibilidade ausente/restricted/prohibited, inbox/archive/expirada e ID adivinhado; consumidor consulta entrega/listagem/metadados/erros/logs/cache e tenta ref divergente/arquivo extra em cópia local | Só fixture elegível aceita; demais ausentes/negadas sem existência inferível; publicação inválida recusada inteira; nenhuma fixture proibida chega ao Git | Resumo por classe sem IDs rejeitados ou payload; read-back de árvore/histórico/refs exatos apenas do repo piloto. Ref fora de allowlist é negação do wrapper, não ACL Git. O Git oferece todo o repo ao portador da key; isolamento de dados reais não é demonstrado |
| N-04 | Consumidor tenta push de commit sintético inofensivo em ref de teste aprovada, escrita em política/âncora/auditoria/publicador e chamada admin sem credencial administrativa; payload com instrução injetada tenta alterar comportamento | Push/admin e escrita protegida negados; injeção tratada como dado, não execução. Alteração em checkout temporário pode ser possível, mas deve invalidar hash/entrega e jamais alterar fonte | Read-back independente do OID/refs remoto e política/âncora/auditoria; status de negação, sem credenciais. Se push inesperadamente funcionar, falha crítica: revogar, ler alvo e remover repo no rollback. Não afirmar que deploy key torna filesystem local read-only ou prova proteção do vault real |
| N-05 | Administrador revoga A-02; consumidor tenta nova leitura autenticada e recuperação com clone previamente baixado e TTL ainda vigente; publicador testa própria leitura com sua identidade separada | Nova leitura SSH negada; wrapper nega mesmo com cópia válida. Publicador segue autorizado até sua própria revogação; nenhum grant externo modificado | Metadado de remoção, códigos de negação e read-back do wrapper/controle positivo do publicador. Bytes já baixados ainda existem até limpeza: revogação não os apaga. Não consultar papéis reais alheios; isolamento entre outros bots continua pendente |
| N-06 | Testador injeta no sandbox falha de publicação, backend/rede, ACL, auditoria, clock/TTL, hash/assinatura, replay de revisão e ref divergente; sem mudar rede/serviço de produção | Qualquer falha impede entrega; sem fallback a vault, sync, credencial alternativa ou cache. Recuperação posterior só após validação integral e auditoria disponível | Eventos por causa, retorno seguro e read-back de ausência de entrega; indisponibilidade de auditoria registrada por observador independente sem payload. Não simular falha apagando logs existentes. Evidência vale apenas para mecanismo e ambiente sintéticos exercitados |

Registro mínimo por caso: `pilot_id`, revisão do CS, ID do teste, identidade/target lógicos, horário UTC, ação sanitizada, esperado/observado, resultado, reason code, revisão/digest sintético quando permitido e read-back. Guardar fora do repo sob acesso separado do consumidor. Não copiar stdout bruto, URLs autenticadas, IPs pessoais, paths de segredo, PII, transcripts ou valores de canários. Falha ao registrar auditoria bloqueia entrega; evidência ausente não conta como teste passado.

### 6. Rollback e limpeza

1. Em falha ou fim da janela, impedir novas publicações e **revogar primeiro a deploy key** A-02 pelo administrador; suspender a entrega local. Se revogação remota falhar, desabilitar consumidor no ambiente de teste aprovado, manter bloqueio e escalar — não declarar rollback concluído.
2. Ler metadados do repo exato para confirmar remoção. Com a identidade revogada, executar nova autenticação/leitura e tentativa de servir clone pré-existente: ambos devem negar no canal controlado. Não usar credencial alternativa no teste de negação. Conferir leitura do publicador antes de revogar sua concessão; não sondar vault ou outros bots.
3. Preservar auditoria mínima sanitizada, inventário e read-backs em A-07 conforme `<AUDIT_RETENTION>` e owner aprovados. Não preservar payload ou privada como evidência. Se auditoria estiver indisponível, manter consumidor bloqueado e obter registro independente antes da exclusão; não apagar rastros.
4. Revogar concessões/segredos técnicos exclusivos do publicador/admin criados para o piloto e remover material de chave conforme o inventário. Ordenar a revogação administrativa final após as operações de exclusão que ainda a exigem; o administrador conserva apenas a capacidade mínima até ler de volta a remoção do repo.
5. Excluir A-01 pelo ID exato e ler de volta sua ausência com o canal administrativo aprovado — falha da chave revogada sozinha não comprova exclusão. Remover clones, temporários, fixtures, scripts, âncoras e diretórios exclusivamente criados e registrados. Não tocar vault, P1-A2, GTD, CRM, backups ou configuração existente. Se algo foi criado fora da lista, interromper e pedir gate de remediação.
6. Confirmar ausência dos paths/recursos enumerados e presença legível da auditoria mínima; registrar resíduos do provedor/backups, se não houver garantia de eliminação física. Não prometer secure erase ou apagamento de cópias fora do controle. Restauração, nova chave ou repetição do piloto exigem aprovação humana nova.

A revisão documental não necessita rollback operacional: só altera os quatro documentos permitidos. Nenhuma limpeza é executada agora.

### 7. Três gates independentes

| Gate | O que uma aprovação futura permite | O que não permite / bloqueios |
|---|---|---|
| **Gate P — criar/executar piloto sintético (Fase 2)** | Apenas recursos, identidades técnicas novas, ações, testes e rollback enumerados no anexo preenchido e aprovado; Git privado dedicado e dados totalmente sintéticos | Não permite discovery genérico, credenciais pessoais, host/conta inferidos, conteúdo real, vault, bot, cron ou serviço de produção. Exige todas as decisões bloqueantes resolvidas, comandos/read-backs exatos e escopo de autenticação técnica autorizado |
| **Gate H — discovery de host/credencial real** | Somente após pedido separado que nomeie host/conta, superfícies, metadados, identidade, operações read-only, duração e evidência sanitizada; secrets sempre por canal seguro, nunca em relatório | Gate D documental não o satisfaz. Não cria/altera recursos, não lê valores secretos nem conteúdo de vault; não executa N-01/N-02 reais por autorização genérica. Os testes de acesso reais precisam de escopo explícito próprio neste gate/revisão |
| **Gate R — qualquer dado/projeção real** | Somente change set/revisão separado com grant de conteúdo, origem, público, retenção, controles e evidência operacional exigida N-01–N-06, aprovado humanamente | Nem Gate P nem Gate H autorizam dado real, importação de AgentKnowledge, promoção canônica, produção ou alteração dos contratos |

Gate P permite as interações pontuais de aplicação/read-back com os recursos sintéticos expressamente nomeados; não permite explorar o restante do host/conta. Se o preenchimento do anexo depender de consulta real, solicitar Gate H primeiro. O usuário pode fornecer alvos sem discovery, mas sua mera indicação não autoriza conexão nem prova isolamento. Não há sequência que transforme aprovação de desenho em aprovação automática de execução.

**Frase exata necessária para Gate P, somente após resolver os bloqueios e anexar alvos/ações concretos à revisão aprovada:**

> Aprovo o Gate P da Fase 2 do CS-030, na revisão e no anexo de alvos explicitamente aprovados, exclusivamente para criar, executar, verificar e limpar o piloto Git privado sintético descrito. Não autorizo discovery de host ou credencial real fora desses alvos, nem acesso a vault, dados ou projeções reais.

A frase sem revisão/anexo concretos ou com placeholders pendentes **não libera execução**; registrar a insuficiência e permanecer `AWAITING_APPROVAL`. Gate H e Gate R exigem pedidos separados, com alvos e escopo próprios; não cabem nessa frase.

### 8. Decisões pendentes — bloqueios humanos

Nenhum valor abaixo foi descoberto ou escolhido. Não inferir de memória, perfil, URLs históricas, Git local ou configurações.

| Decisão humana | Placeholders a preencher antes da execução | Critério de desbloqueio |
|---|---|---|
| Conta GitHub e repositório final | `<GIT_ACCOUNT>`, `<PILOT_REPO>`, `<REPO_ADMIN_ROLE>`, `<ADMIN_AUTH>` | Conta/repo dedicados e ações administrativas exatas, autenticação técnica autorizada sem reutilização pessoal |
| Host e isolamento do consumidor VPS | `<CONSUMER_HOST>`, `<CONSUMER_OS_ID>`, `<CONSUMER_TEST_ROOT>` | Alvos e fronteiras de SO explícitos; Gate H separado se necessária consulta real |
| Host e identidade do produtor | `<PRODUCER_HOST>`, `<PRODUCER_OS_ID>`, `<PRODUCER_TEST_ROOT>`, `<PUBLISHER_AUTH>` | Produtor separado sem vault; concessão limitada de publicação com revogação descrita |
| Chave, armazenamento e deadline | `<CONSUMER_KEY_STORAGE>`, `<KEY_REVOKE_DEADLINE>`, responsável por revogar | Storage protegido, descarte sem backup, sem agente compartilhado; ID da key será registrado somente quando criada |
| Confiança de SSH/manifest | `<SSH_HOST_TRUST>`, `<INTEGRITY_TRUST_MODE>`, `<SIGNATURE_MECHANISM_OR_NONE>`, `<TRUST_CHANNEL>`, `<TRUST_ANCHOR_STORAGE>` | Aprovar canal independente, verificador e âncora; digest co-localizado sozinho não basta |
| Ref, revisão e anti-replay | `<ALLOWED_REF>`, mecanismo protegido de revisão mínima e vínculo de `<EXPECTED_COMMIT_OID>` | Definir ref e como obter/registrar OID sintético após publicação; OID/ID da key são saídas de criação, não valores a adivinhar no desenho |
| TTL, limites e janela | Confirmar proposta de 300 segundos, `<CLOCK_SKEW_BOUND>`, limites de bytes/registros, `<PILOT_WINDOW>` | Valores explícitos e casos de expiração/clock aprovados; execução manual, nenhum cron/timer/serviço ou path de produção proposto |
| Auditoria e limpeza | `<AUDIT_STORE>`, `<AUDIT_RETENTION>`, `<CLEANUP_ARTIFACT>`, responsáveis/revisor | Retenção/purge próprios, acesso separado, inventário fechado e read-backs antes de apagar |
| Anexo de execução e gates | Revisão exata, comandos/ações/seletores, baseline, testes reais eventualmente autorizados | Nenhum placeholder de entrada pendente; IDs/OIDs gerados possuem procedimento aprovado de captura e read-back. Aprovações P/H/R não se substituem |

### 9. Anexo 2.2 — defaults aprovados para o piloto

**Estado do anexo:** proposto e documental. O usuário autorizou seu preenchimento em 2026-09-18, mas não autorizou criar recursos. Este anexo substitui os placeholders de entrada da seção 8 apenas para o piloto sintético; IDs, fingerprints de recursos e OIDs continuam saídas futuras de criação/read-back, nunca valores a adivinhar.

| Item | Valor proposto | Limite vinculante |
|---|---|---|
| Conta e repositório | `felipe3d/agentknowledge-vps-projection-pilot` | Repositório novo, privado, inicialmente vazio; sem forks, Actions, LFS, submodules, integrações ou dados reais. Se já existir, Gate P para sem sobrescrever. |
| Administrador | humano `felipe3d`, pela UI/canal de autenticação já autorizado no momento de Gate P | Nenhum PAT pessoal, sessão OAuth ou login existente é entregue ao publicador/consumidor. |
| Publicador | usuário novo `ak-pilot-publisher` no `oracle-vps`; raiz exclusiva `/var/tmp/cs030-pilot-publisher` | Distinto do consumidor, sem vault/home Hermes, agent forwarding ou ferramentas Hermes. A criação e as permissões exatas dependem de Gate P. |
| Consumidor | usuário novo `ak-pilot-consumer` no `oracle-vps`; raiz exclusiva `/var/tmp/cs030-pilot` | Somente fetch, validação e leitura; sem push/admin, vault, sync, credencial pessoal ou fallback. |
| Chave do consumidor | deploy key nova `cs030-consumer-ro`, privada em `/home/ak-pilot-consumer/.ssh/cs030_consumer_ro` | Exclusiva do repositório e configurada read-only. Sem passphrase compartilhada, agente SSH, backup automático ou reutilização. |
| Chave do publicador | deploy key nova `cs030-publisher-rw`, privada em `/home/ak-pilot-publisher/.ssh/cs030_publisher_rw` na VPS | GitHub exige leitura implícita para chave com escrita; ela terá write habilitado **somente** no repositório do piloto. Não equivale a chave write-only nem recebe admin. |
| Auditoria | `/var/tmp/cs030-pilot-audit` na VPS, fora de A-01, com owner `ak-pilot-publisher`; retenção de 7 dias ou até revisão humana, o que ocorrer primeiro | Consumidor não recebe acesso. Conteúdo é sanitizado; sem payload, chave, URL autenticada, PII ou conteúdo real. Cleanup não apaga auditoria antes do read-back. |
| Confiança SSH | `github.com` Ed25519 pinado em known_hosts exclusivo do consumidor, usando fingerprint oficial `SHA256:+DiY3wvvV6TuJJhbpZisF/zLDA0zPMSvHdkr4UvCOqU` | Sem `StrictHostKeyChecking=no`, sem aceitação automática de chave nova e sem agent forwarding. |
| Confiança do manifest | assinatura destacada Ed25519 nova para o piloto; privada em `/home/ak-pilot-publisher/.cs030/manifest_signing_ed25519`, pública em `/var/tmp/cs030-pilot/trust/manifest_signing_ed25519.pub` na VPS | A chave pública é criada/pinada antes da publicação e não vem do Git. Nenhuma chave existente é reutilizada. |
| Ref e anti-replay | `refs/heads/pilot`; revisão inicial `1`, estritamente crescente; estado consumidor `/var/tmp/cs030-pilot/state/last_accepted_revision` | OID esperado é capturado por read-back externo após publicação e vinculado ao manifest/envelope, nunca previsto no desenho. Ref/OID/regressão divergentes negam. |
| TTL e relógio | TTL máximo `300` s; `<CLOCK_SKEW_BOUND>` = `30` s; janela manual máxima `30` min | Sem cron, timer ou serviço permanente. Falha de relógio, TTL ou janela nega entrega. |
| Revogação | responsável: administrador humano; deadline: até cinco minutos após o fim da janela | Revogar ambas as deploy keys antes da limpeza. Nova chave/rotação fora da janela exige nova aprovação. |
| Limites | um payload `projection.synthetic.json`; máximo 10 registros e 64 KiB; somente audiência `synthetic-consumer` | Tudo sintético, elegível e de uma só audiência. Fixtures negativas ficam em memória e nunca vão ao Git. |

**Topologia sintética VPS-only:** o usuário autorizou esta revisão em 2026-09-18 após P-01 bloquear no HomeLab. Publicador, consumidor e auditoria ficam na VPS sob **contas Linux separadas**, em raízes distintas e sem acesso a vault/HomeLab. Isso elimina a necessidade de privilégio no HomeLab para o piloto, mas limita a evidência: ela demonstra separação entre papéis no mesmo host sintético e **não** prova ainda produtor HomeLab → consumidor VPS. Essa prova inter-host exige gate posterior separado.

**Sequência de Gate P preenchida:** P-00 registra este anexo e a janela; P-01 cria somente os ambientes/raízes VPS enumerados; P-02 cria somente A-01; P-03 cria/registra somente as duas deploy keys; P-04 cria as fixtures, política e chaves de manifest novas; P-05 publica somente a ref `pilot`; P-06 executa os casos planejados; P-07 revoga primeiro as duas deploy keys; P-08 remove apenas os IDs/paths criados e preserva a auditoria pelo prazo acima. Cada passo mantém o read-back e rollback da tabela P-00–P-08; qualquer colisão, precondição ausente ou divergência interrompe sem fallback.

Este anexo resolve os bloqueios documentais da revisão 2.2. Não prova capacidade de criação do repositório, isolamento efetivo de SO, provisionamento de usuário, armazenamento seguro, assinatura, N-01–N-06 ou disponibilidade; essas são verificações do próprio Gate P. Gate H não é reaberto por este anexo e Gate R continua não solicitado.

**Estado de Gate P:** `BLOCKED` antes de P-01. O HomeLab exigiu autenticação interativa para `sudo -n true`; a VPS aceitou a checagem, mas a sequência não iniciou porque ambos os ambientes isolados são pré-requisito. Nenhum recurso A-01–A-08 foi criado. Evidência: `program/evidence/CS-030-gate-p-preflight.md`.

### 11. Resultado do Gate P VPS-only

O Gate P da revisão 2.5 foi executado somente com recursos sintéticos na VPS. P-01 a P-07, a publicação/validação positiva e os testes limitados N-03/N-04/N-05/N-06 foram exercitados; N-01/N-02 não foram certificados. As duas deploy keys foram revogadas e os recursos VPS enumerados foram removidos, preservando auditoria sanitizada mínima.

A exclusão manual foi confirmada por leitura posterior: o repositório está ausente. Gate P VPS-only está limpo/verificado dentro do seu escopo sintético; N-01/N-02 e dados reais continuam fora do escopo e não certificados.

### 10. Estado de encerramento e evidência

Fase 0 documental, Fase 1 sintética local, Gate D e Gate H mínimo concluídos conforme E-006–E-010. O Gate P VPS-only foi executado e limpou os recursos VPS; a revisão 2.6 registra o bloqueio da exclusão remota do repositório. **Não há evidência para dados reais ou isolamento operacional completo.**

N-01/N-02 reais continuam pendentes; N-03–N-06 foram exercitados somente no piloto VPS-only, com os limites registrados na evidência. Nenhum recurso A-01–A-08 permanece na VPS além da auditoria sanitizada retida, e o repositório foi confirmado ausente. Gate P está limpo/verificado no escopo sintético; qualquer avanço para dados reais exige Gate R separado.
