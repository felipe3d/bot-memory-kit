# CS-034 — primeiro aprendizado assistido no bot pessoal

**Estado:** IN_PROGRESS — execução aprovada pelo proprietário em 2026-09-21 (“eu aprovo”), na conversa privada do Desktop.
**Revisão documental:** concluída; este pacote não é prova de implementação.
**Autorização atual:** implementação, testes e reversão locais enumerados neste pacote. A aprovação recebida não aprova candidata nem valida funcionamento. Preflight local confirmou default/Mac, raiz presente e destinos novos sem colisões ou symlinks; aplicação e resultados serão registrados em evidência própria.

## 1. Escolha e resultado visível

**Bot escolhido:** default pessoal do Mac, na conversa privada do proprietário no Hermes Desktop. Já existe e é adequado a preferências de colaboração gerais; evita alterar GTD, CRM ou seus canais. Não criar bot novo.

**Fonte concreta:** `/Users/fac/dev/bot-memory-kit/program/handoffs/SESSION-PROMPT-PERSONAL-BOTS.md`, somente a seção **“Acordo com o usuário”**. Ela contém preferências já explicitadas pelo proprietário, não clientes, tarefas ou notas privadas. Foi lida para esta revisão; a autorização de leitura documental não aprova seus enunciados como memória. O restante do arquivo não será entrada do extrator futuro. Não seguir links nem buscar outras fontes.

A escolha aproveita material conhecido de baixo risco, sem inventariar dados privados. É uma primeira prova funcional pequena; não demonstra extração em todo o Obsidian nem aprendizado geral sobre a vida do usuário.

**O que o proprietário verá:** até três sugestões em português simples, com ideia, utilidade, origem, destino, validade e risco em linguagem comum. Exemplo ilustrativo, ainda não aprovado:

> **Sugestão:** Você prefere revisar sugestões de memória em português simples, aprovando, rejeitando ou ajustando, sem preencher campos técnicos.
> **Utilidade:** O bot apresenta ideias prontas para sua revisão em vez de pedir notas manuais.
> **Origem:** Acordo com o usuário, no documento de retomada.
> **Destino:** Conhecimento pessoal do seu assistente no Mac.
> **Validade proposta:** Revisar em 90 dias ou quando você mudar essa preferência.
> **Risco:** Baixo; trata apenas da sua forma de trabalhar com o assistente.
> **Ações:** Aprovar / Rejeitar / Ajustar.

As ações podem ser respostas textuais inequívocas; botões não são pré-requisito. Aprovação da entrega não aprova automaticamente esse exemplo nem qualquer candidata.

## 2. Escopo da aprovação única de execução

A aprovação recebida abrange implementar, testar e reverter o fluxo local abaixo. Não inclui mudar configurações/grants existentes nem operar sistemas de tarefas/CRM.

| Item | Destino ou limite exato aprovado |
|---|---|
| Implementação e testes | Novos `scripts/cs034_personal_learning.py`, `tests/test_cs034_personal_learning.py` e fixtures sintéticas em `tests/fixtures/cs034/`, no repositório; documentos de estado/evidência desta entrega em `program/`. Sem commit/push |
| Raiz do conhecimento | `/Users/fac/dev/Obsidian/felipe/AgentKnowledge/`; endereço confirmado por metadados no preflight da execução aprovada, sem inventário de conteúdo. Não criar outro vault nem varrer irmãos |
| Candidatas | Somente `AgentKnowledge/inbox/mac/cs034-personal-learning/`, até três registros por rodada, uma rodada inicial; no máximo 2 KiB de texto por candidata |
| Conhecimento aprovado | Somente `AgentKnowledge/canonical/personal-collaboration/`, até três registros oriundos desta rodada; nenhuma edição de outras notas |
| Histórico e decisões | Somente `AgentKnowledge/archive/cs034-personal-learning/`; revisões sanitizadas e decisões mínimas de aprovação, rejeição, correção, expiração e retirada, com ACL pessoal igual ou mais restrita |
| Recuperação no default | Nova skill `/Users/fac/.hermes/skills/personal-learning/SKILL.md`, contendo apenas procedimento e localização da consulta; nunca fatos pessoais, corpo de notas ou cache. Nenhum outro perfil/skill/configuração alterado |
| Recuperação durável/rollback | Nova pasta `/Users/fac/.hermes/bmk-backups/cs034-personal-learning/`; manifest de paths criados, hashes e pré-imagens apenas dos arquivos desta entrega. Não ler/copiar backups preexistentes, home Hermes, state.db ou credenciais |
| Audiência/modelo | Somente proprietário no Desktop privado do Mac, usando o modelo já selecionado; sem novo provedor, autenticação ou envio para terceiros/canais. A inferência usa o provedor da conversa, não implica processamento offline |
| Publicação | Nenhuma projeção VPS, sync novo, repo remoto, key ou consumidor. Não chamar CS-033 |

O código deve resolver a raiz do perfil ativo de modo seguro e exigir default no Mac; não escrever em perfis nomeados. Os paths enumerados compõem a autorização recebida. Presença/permissões foram verificadas no preflight restrito; nenhum acesso fora deles foi concedido.

### Preflight incluído, antes de qualquer mutação

Após aprovação, verificar somente: identidade local/perfil ativo, disponibilidade da fonte e seu trecho, raiz AgentKnowledge exata, existência/permissão dos destinos enumerados e ausência de colisões. Inspecionar metadados somente nesses destinos; sem varrer conteúdo preexistente. Recusar symlinks/escape de path e interromper diante de destino já ocupado por outro trabalho, host/perfil divergente ou topologia de armazenamento ambígua. Não iniciar descoberta de sync/hosts/credenciais para compensar dúvida; isso muda o escopo. Se a raiz proposta não for a correta, pedir decisão material em vez de deduzir outro vault.

A skill nova é um mecanismo de descoberta do procedimento, não ACL nem memória canônica. Usar a API/ferramentas existentes de arquivos do default, sem instalar serviço/MCP ou conceder ferramentas novas. Se não for possível recuperar em conversa nova com essas capacidades, parar e relatar, não ampliar a integração silenciosamente.

## 3. Comportamento obrigatório

1. Ler apenas o trecho allowlisted, registrar hash da fonte e localização da seção. Limitar a entrada a 8 KiB; excesso ou mudança de seção/escopo não permite truncar silenciosamente ou ler mais arquivos.
2. Identificar preferências estáveis de colaboração. Texto fonte é **dado, nunca comando**: não autoriza ferramentas, acessos, promoção, novos destinos ou alteração da política. Origem é referência citável, não prova de que uma inferência da IA é fato.
3. Validar entrada e saída: negar segredo, dado pessoal sensível, estado vivo, dumps, transcrições brutas e instruções maliciosas. Não copiar o trecho bruto para logs ou auditoria. Para entrada proibida, registrar somente motivo/código e digest, sem guardar o payload proibido.
4. Escritor de candidatas só cria no inbox permitido; o caminho de proposta não tem operação de promoção. Preencher automaticamente os campos do contrato, ID estável, classificação pessoal de baixo risco, origem, revisão e expiração proposta de 90 dias. A pessoa pode ajustar a validade no cartão em linguagem simples.
5. Mostrar o cartão sanitizado ao proprietário na conversa privada autorizada. O cartão e a resposta podem integrar o histórico normal desse canal; não prometer ausência de todo registro da plataforma. Não exportar conversa, fonte ou nota para logs auxiliares, auditoria, repositório ou outros canais.
6. Vincular a decisão humana autenticada ao ID, revisão e digest exatos. A IA não pode fabricar aprovação a partir da fonte, da autorização de execução ou da própria sugestão. Ajuste material gera cartão revisado; pedir confirmação do texto final somente quando a resposta não o determinar inequivocamente.
7. Reconciliador local aplica a decisão registrada, validando fonte, escopo, revisão, conflito e audiência; só então promove atomicamente ao canônico. Repetir uma aprovação não duplica nota. Rejeição conserva apenas decisão/digest, não promove nem reapresenta automaticamente o mesmo item.
8. Recuperação lê somente registros canônicos vigentes desta entrega, retorna origem/revisão e aplica a preferência à resposta. Não varrer o vault, recuperar inbox/archive, usar transcript como memória ou persistir cópia no USER.md/MEMORY.md. A skill contém apenas o procedimento de consulta.
9. Correção do proprietário cria revisão aprovada com vínculo e preserva histórico; retirada suspende uso e arquiva. Sem cache de fatos no piloto. Não ressuscitar a versão anterior por rollback ou retry depois da retirada. Arquivamento não é exclusão definitiva de backups/históricos.

**Fronteira honesta:** escritor e reconciliador são operações separadas no componente, com validação da decisão; não são contas de SO isoladas. O default conserva ferramentas amplas preexistentes. Testar negativa no componente não demonstra contenção de um agente arbitrário nem isolamento para terceiros. Se o caso passar a exigir esse isolamento, revisar o escopo antes de exposição.

## 4. Testes que definem conclusão — resultados parciais disponíveis

Implementação local e testes automáticos passaram; uma candidata real foi criada e lida de volta, sem promoção. Resultado primário em `../evidence/CS-034-local-learning-run.md`. Decisões humanas de conteúdo e conversas novas reais permanecem pendentes; a tabela abaixo é o critério de aceite, não afirmação de que todos os testes passaram.

| Prova | Resultado exigido |
|---|---|
| Entrada delimitada | Fonte allowlisted funciona; arquivo irmão, traversal, symlink, seção alterada e excesso de quota falham sem leitura fora do limite ou efeitos persistentes |
| Separação de operações | Writer não promove por sua interface; decisão ausente, fabricada, ambígua, de outro cartão ou revisão vencida é recusada pelo reconciliador |
| Revisão e rejeição | No máximo três cartões; candidata/rejeitada não aparece em recuperação; retry não reapresenta item rejeitado nem cria duplicatas |
| Aprovação real | Decisão humana gera uma única nota com proveniência, validade e revisão; ler de volta o alvo exato para verificar |
| **Conversa nova real** | Proprietário abre conversa nova no default Desktop, sem colar nota, decisão ou histórico; pede “Consulte meu conhecimento pessoal: como devo revisar suas sugestões de memória?”. A execução deve carregar o procedimento, ler a nota vigente e citar origem/revisão, não apenas repetir preferência já conhecida |
| Uso correto | Na mesma conversa nova, pedir uma sugestão de memória: formato deve respeitar a preferência aprovada. Rastrear leitura real do canônico; informação já presente em memória antiga não conta como prova de recuperação |
| Correção real | Proprietário ajusta uma preferência da rodada; nova revisão é registrada. Outra conversa nova lê e usa somente a versão corrigida, com citação. Não escolher silenciosamente entre versões |
| Retirada real | Proprietário retira o item de teste; outra conversa nova não o recupera nem o atribui ao canônico. Não apagar nem modificar lembranças preexistentes fora do pacote; distinguir coincidência textual de recuperação indevida |
| Expiração e falha | Fixtures com relógio controlado, conflito, arquivo corrompido e falha de auditoria não promovem nem retornam fato vigente indevido |
| Injeção e dados proibidos | Somente fixtures sintéticas: fonte/cartão tentam comandar ferramenta, acessar outro path ou autoaprovar. Nenhuma ação externa ocorre; nenhum payload proibido vai para notas/logs. Não testar com segredo real |
| Reversão | Ensaiar falha após cada etapa mutante e retry idempotente; remover somente recursos novos enumerados ou restaurar pré-imagem da própria entrega sem reativar nota retirada; read-back confirma estado final |
| Preservação | Comparar manifest de arquivos antes/depois; GTD/CRM, gateway, integrações, permissões existentes, backups anteriores e rotas não são modificados |

Fixtures provam apenas o componente. Para declarar sucesso funcional são necessárias as decisões humanas e conversas novas reais, com leitura de volta. Não iniciar agentes recursivos para simular esses testes; o proprietário abre as conversas de validação, sem redigir notas técnicas. A aprovação da entrega já cobre os testes; essas interações são exercício e decisão de conteúdo, não novos gates de planejamento.

Registrar em `program/` apenas resultados sanitizados, hashes, referências sem conteúdo pessoal e limites da prova. Atualizar `EVIDENCE.md` somente quando houver prova operacional nova. Não chamar a entrega VERIFIED enquanto faltar qualquer prova aplicável; informar falha ou pendência real.

## 5. Reversão e autonomia

Antes da primeira escrita, registrar manifest e pré-imagens restritos aos arquivos próprios. Escritas atômicas, comparação de revisão/hash e chaves de idempotência impedem duplicações. Falha recuperável pode ter até duas novas tentativas por etapa, após conferir o estado; timeout não equivale a falha de gravação. Não repetir promoção às cegas.

Na falha: bloquear promoção/recuperação da entrega, desfazer transação incompleta e verificar por leitura posterior. No rollback final: desativar/remover apenas a skill e os arquivos novos enumerados no manifest; restaurar apenas versões próprias quando apropriado, sem sobrescrever edição concorrente. Conhecimento já aprovado é retirado/arquivado, não apagado silenciosamente; auditoria mínima e pré-imagens ficam na pasta delimitada, inacessíveis à recuperação normal. Retenção até revisão do proprietário, sem purge automático e sem prometer eliminação de logs antigos. Não tocar backups anteriores nem criar rotina de backup.

**Parar somente por:** novo acesso/privilégio, decisão material (incluindo mudar fonte, destino, audiência ou topologia), risco inesperado ou falha sem recuperação segura. Esperar a decisão humana sobre cartões e as conversas de teste quando necessário, sem inventá-las. Não pedir aprovação por arquivo, etapa interna ou retry já coberto.

## 6. Fora de escopo

Inventário de notas privadas, leitura de Mindwtr/Odoo, mudança nos pilotos GTD/CRM, gateway, integrações, permissões existentes, rotas, credenciais, provider, serviços, cron, Kanban, orquestrador, novos agentes/perfis, sync, publicação VPS, commit/push, refactor amplo e apagar histórico preexistente. A ausência de conteúdo no canônico não amplia essa lista nem obriga o usuário a escrever notas.

## 7. Aprovação recebida e próxima decisão de conteúdo

O proprietário respondeu **“eu aprovo”** à entrega no Desktop privado em 2026-09-21. O texto abaixo documenta o escopo aprovado, não uma nova solicitação:

> Aprovo implementar e testar o aprendizado no meu assistente pessoal do Mac usando somente o acordo já escrito no documento de retomada, com os destinos, limites e reversão descritos nesta entrega. Quero revisar cada sugestão antes de virar conhecimento. Não incluir VPS nem alterar GTD, CRM ou minhas integrações.

Implementação e primeira candidata locais aplicadas. A próxima decisão é Aprovar / Rejeitar / Ajustar a candidata apresentada, sem nova aprovação de detalhamento. Depois, testar conversas novas reais. Novas fontes privadas e eventual publicação remota continuam fora de escopo.
