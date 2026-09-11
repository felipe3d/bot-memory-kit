# Pesquisa: base implementável para `bot-memory-kit`

## Escopo e conclusão

Pesquisa documental nas páginas oficiais vigentes do Hermes, consultadas nesta execução. Este relatório é **planejamento, não implantação**: nenhum perfil/bot foi criado, nenhuma configuração foi alterada, nenhum host remoto foi acessado e nada foi publicado. Os comandos abaixo são referências para uma etapa futura aprovada, não execução realizada.

**Conclusão:** o kit pode ser uma skill orquestradora com entrevista explícita, templates e validação local. O Hermes já oferece perfis independentes, seleção de skills e aprovação de memória/skills.[1][2][3]

Também oferece retomada de sessões e checkpoints de arquivos.[5][6]

O contrato de consentimento por host, a curadoria item a item e os checkpoints semânticos do processo precisam ser definidos pelo kit — não se deve confundi-los com garantias automáticas do produto.

Recomendação de desenho: **skill reutilizável + dados privados por execução + aplicação separada após aprovação**. Uma distribuição de perfil é uma opção posterior para entregar um agente inteiro, mas não é um mecanismo de sincronização de memórias pessoais.[4]

## 1. O que existe nativamente

| Necessidade | Evidência oficial | Consequência para o kit |
|---|---|---|
| Criar agente isolado em estado | `hermes profile create NAME`; cada perfil tem config, memória, skills, sessões e estado próprios.[1] | Criar um destino novo, com nome explicitamente aprovado. |
| Começar com skills mínimas | `hermes profile create research --no-skills`; marcador `.no-bundled-skills` impede seeding também em updates.[3] | Melhor opção documentada para seleção positiva, sem copiar todo o catálogo. |
| Bot na interface Desktop | Bot Mode apresenta cada perfil como bot, com Bot Chat canônico, avatar e rotinas; a criação expõe modelo, SOUL, skills, toolsets e MCPs.[8] | Perfil CLI é a primitiva; a apresentação Desktop deve ser validada na versão instalada. |
| Bot em mensageiro | Cada perfil pode executar gateway separado e usar token próprio; token locks evitam duplicação em plataformas documentadas.[1] | Perfil não equivale a registrar automaticamente uma conta/token no provedor. Configuração de canal é etapa separada. |
| Persona e diretório | `SOUL.md` orienta comportamento; `terminal.cwd` controla diretório inicial.[1] | Gerar persona e workspace explícitos, mas não chamar isso de sandbox. |
| Memória curada | `MEMORY.md` e `USER.md`, carregados como snapshot no início da sessão; ferramentas add/replace/remove.[2] | Transferir apenas fatos aprovados e testar carregamento em sessão nova. |
| Retomada | `hermes --resume ID`, retomada por título e `--in DIR`; sessões guardam histórico e metadados em SQLite.[5] | Guardar ID + perfil + host + diretório, além de um checkpoint próprio. |

### Criação segura versus clonagem

`--clone` **copia `.env`**, além de config, SOUL e skills; não significa “sem segredos”. `--clone-from` seleciona fonte e implica clonagem de configuração/skills/SOUL. `--clone-all` copia memória e outros componentes, mas exclui histórico, checkpoints e cron conforme a documentação atual.[1]

**Recomendação do kit:** não usar clonagem como padrão. A criação vazia com `--no-skills` evita importar capacidades e credenciais por acidente. Toda migração deve partir de uma lista positiva aprovada, sem copiar `.env`, `auth.json`, caches, logs, transcripts ou diretórios inteiros de perfil.

Os perfis também não isolam todas as credenciais de ferramentas: no host, subprocessos mantêm o `HOME` real por padrão, e certos logins OAuth são compartilhados pelo root; `terminal.home_mode: profile` separa o HOME das ferramentas, mas não constitui contenção de sistema operacional.[1]

### Comandos candidatos, somente após aprovação

```bash
hermes profile create NOME_APROVADO --no-skills
hermes profile show NOME_APROVADO
hermes -p NOME_APROVADO skills list
hermes -p NOME_APROVADO setup
hermes -p NOME_APROVADO chat
```

A sintaxe de perfil e setup vem do guia de perfis; `--no-skills` é explicitamente documentado no guia de skills.[1][3] Na implementação, verificar `--help` e versão no host autorizado antes de construir comandos. Preferir `-p` explícito a `profile use`, para não mudar o default persistente do usuário. A criação também pode gerar alias em `~/.local/bin/`, um efeito colateral que deve aparecer no plano aprovado.[1]

## 2. Segurança: limites reais e decisões propostas

### Controles documentados

- Perfil separa **estado**, não acesso ao filesystem. `SOUL.md` não impõe fronteira de workspace; backend local mantém os privilégios do usuário.[1]
- O modo atual documentado para aprovação de comandos é `smart`; `manual` pede aprovação para comandos classificados perigosos; modos headless têm políticas próprias. Nenhum desses modos equivale a pedir autorização para toda leitura ou toda ação possível.[7]
- `memory.write_approval: true` exige aprovação das escritas via mecanismo de memória; em superfícies não interativas elas ficam pendentes. `skills.write_approval: true` sempre coloca alterações de skills em staging, inclusive da revisão em background.[2][3]
- `/memory pending|approve|reject` e `/skills pending|diff|approve|reject` fornecem revisão explícita; notificações de memória desligadas não desligam escritas.[2]
- `HERMES_WRITE_SAFE_ROOT` restringe `write_file`/`patch`, não o terminal. Guards e deny rules são defesa em profundidade, não sandbox completa.[7]
- Diretórios `skills.external_dirs` podem ser modificados se forem graváveis; permissões do filesystem são necessárias se o catálogo compartilhado precisar ser somente leitura.[3]
- Memórias são inspecionadas quanto a padrões de injeção/exfiltração e Unicode invisível; esse scanner não demonstra ausência de todo segredo ou de toda afirmação incorreta.[2]

**Política recomendada, ainda não aplicada:** aprovações de memória e skills ativadas no perfil de destino; comandos perigosos em modo manual; ações headless perigosas negadas; sem YOLO, cron, publicação ou gateway automático. Se for necessária garantia forte de “não escrever/não acessar”, usar permissões e backend restrito, não apenas instruções.

### Contrato de descoberta multi-host proposto

O consentimento deve ocorrer **antes da descoberta**, não depois de ler um inventário sensível. A entrevista pode listar hosts que o usuário informar; não deve enumerar rede, perfis, contas, sessões ou diretórios privados só para sugerir opções.

Para cada host, registrar apenas:

- identificador local e método autorizado de conexão;
- perfil de origem e perfil/diretório de destino;
- raízes permitidas, exclusões e classes de informação autorizadas;
- permissão `metadata_only`, `read_selected` ou `apply_selected`;
- limites da operação, momento da aprovação, validade e possibilidade de revogação.

**Separar autorizações:** descobrir metadados ≠ ler conteúdo ≠ persistir fatos ≠ transferir para outro host ≠ configurar credenciais ≠ iniciar serviços. Um host indisponível produz estado bloqueado; não autoriza ampliar o escopo ou usar outro caminho de acesso.

Esse contrato é uma **proposta do kit**, não uma API nativa documentada. Recursos existentes de SSH/MCP/backend não substituem autorização do usuário. Nome de host em memória também não comprova o ambiente em execução.

### “Sem segredos armazenados”: definição operacional

A promessa implementável deve ser: **nenhum segredo em artefatos, checkpoints, memória, skills ou relatórios do kit**. Não prometer que todo o Hermes deixa de armazenar credenciais: o produto usa `.env`/`auth.json` e pode aproveitar autenticação existente.[1][4]

Regras propostas:

1. Não ler nem copiar arquivos de credenciais. Registrar requisito e presença/ausência, nunca valor, prefixo, hash de senha ou dump de ambiente.
2. Usar nomes de variáveis e referências a configuração externa; autenticação deve ocorrer por setup seguro/local fora da entrevista.
3. Não solicitar tokens em chat. A documentação de skills prevê setup seguro no CLI e orienta configurar localmente quando a superfície é mensageiro.[3]
4. Processar conteúdo autorizado com filtro antes de persistir; examinar também URLs com query, connection strings, cabeçalhos, scripts e exemplos. Redação automática não é prova de anonimização completa.
5. Não colocar transcripts ou dados brutos no pacote compartilhável. Sessões persistem histórico e tool outputs; compressão não é exclusão de dados pessoais.[5]
6. Rejeitar dumps amplos e registrar somente “item excluído por sensibilidade”. Não gravar a evidência contendo o próprio segredo.

## 3. Empacotamento de skills e portabilidade

Skills são documentos `SKILL.md` com frontmatter e carregamento progressivo. Suportam arquivos auxiliares em `references/`, `templates/`, `scripts/` e outros diretórios documentados; instalações de GitHub/URL copiam os auxiliares locais **referenciados**, não todo arquivo arbitrário do repositório.[3]

**Estrutura proposta (não criada nesta pesquisa):**

```text
bot-memory-kit/
  SKILL.md
  references/
    consent-and-discovery.md
    selection-and-safety.md
    resume-protocol.md
  templates/
    interview.md
    execution-manifest.json
    checkpoint.json
    approval-plan.md
  scripts/
    validate_manifest.py
    validate_checkpoint.py
    scan_artifacts.py
```

`SKILL.md` deve ter gatilho explícito: invocar `/bot-memory-kit` ou pedir diretamente a criação/curadoria de bot com o kit; menção casual a “memória” não deve disparar descoberta. Invocar a skill autoriza **começar a entrevista**, não instalar, migrar ou alterar perfis. A documentação confirma slash commands para skills, mas o gate de intenção é parte do procedimento proposto.[3]

A entrevista deve produzir: objetivo, identidade/persona, superfície CLI/Desktop/gateway, capacidades necessárias, toolsets/MCPs, origem de skills, fatos pessoais permitidos, hosts e limites, política de atualização, critérios de sucesso e aprovação do plano.

### Seleção, dependências e isolamento

- Separar seleção de skills de seleção de ferramentas/MCPs: conhecimento não habilita automaticamente uma capacidade.
- Catalogar por nome exato, origem, versão/hash, dependências, compatibilidade e justificativa. Aprovar cada skill e cada memória; não usar “copiar tudo e remover depois”.
- Verificar auxiliares referenciados e dependências antes de declarar instalação completa.
- Não usar symlink para catálogo de outro perfil como solução padrão: a skill pode ser editada no local de origem.[3]
- Skills de projeto exigem confiança explícita; têm precedência sobre locais e externas e passam por scanner. Logo, registrar proveniência evita validar uma skill e acabar carregando outra de mesmo nome.[3]
- Bundles apenas carregam várias skills; skills ausentes são puladas, não erro fatal. Não tratar bundle carregado como prova de pacote completo.[3]

### Skill kit versus distribuição de perfil

Uma distribuição possui `distribution.yaml`, SOUL, config, skills e outros componentes; instala/atualiza por `hermes profile install/update`, inclusive a partir de diretório local. Memórias, sessões e credenciais são domínio de cada instalação, não conteúdo distribuído.[4]

Isso é adequado para uma fase futura de entrega de **modelo de agente**, não para transportar memórias reais. Por padrão, atualização substitui arquivos de domínio da distribuição; `config.yaml` é preservado salvo `--force-config`, e `distribution_owned` permite restringir o conjunto atualizado.[4]

**Não usar `profile export` como sanitização:** export exclui `.env`/`auth.json` por nome, mas pode incluir memórias, sessões, logs e conteúdo pessoal; a documentação afirma que não há varredura de conteúdo de skills/memórias/persona nesse caminho.[4]

Distribuições são não assinadas por padrão. A página consultada descreve assinatura, lockfile e `--dry-run` de update como recursos futuros; não inventar esses flags no kit. Exclusões do instalador também não impedem o autor de cometer segredos ao usar Git.[4]

## 4. Memória seletiva e continuidade

Os limites padrão documentados são 2.200 caracteres para `MEMORY.md` e 1.375 para `USER.md`, configuráveis. Overflow gera erro, não compactação silenciosa; duplicates exatos são rejeitados e replace/remove usam substring única.[2]

**Proposta de classificação:**

| Categoria | Destino proposto |
|---|---|
| Preferência pessoal estável e consentida | `USER.md` |
| Fato estável do ambiente, qualificado por host/perfil | `MEMORY.md` |
| Procedimento reutilizável | Skill ou referência |
| Evidência, justificativas, conflitos, seleção pendente | Dados privados da execução |
| Etapas concluídas, próximo passo, permissões vigentes | Checkpoint semântico |
| Token, senha, cookie, chave privada, connection string autenticada | Nunca persistir no kit |

Cada fato candidato deve ter origem, escopo, validade, justificativa e decisão `aprovar/rejeitar/adiar`. Conflitos não devem ser resolvidos por palpite. Não transferir afirmações de um host como se fossem fatos do destino. Limites efetivos devem ser lidos na configuração autorizada, não presumidos pelos defaults.

### Três conceitos diferentes de retomada

1. **Retomar conversa:** `hermes -p PERFIL --resume ID --in DIRETORIO` combina seleção explícita de perfil com retomada documentada; validar sintaxe instalada antes do uso. `--in` fixa workspace e impede restaurar silenciosamente o cwd anterior.[1][5]
2. **Recuperar arquivos:** checkpoints nativos são opt-in, usam shadow Git e podem falhar sem interromper a ferramenta. Há exclusões por tamanho/escopo, retenção e pruning. Não garantem rollback de operações externas ou de todo estado do perfil.[6]
3. **Retomar o processo do kit:** manifesto/checkpoint próprio contendo decisões e próximos passos. Necessário para continuar mesmo sem o histórico de chat original — por exemplo, após mudança de máquina ou perda/pruning da sessão. Distribuições não levam sessões.[4][5]

### Checkpoint semântico proposto

Campos mínimos: `schema_version`, `kit_version`, `run_id`, `phase`, `host_id`, `profile_id`, `workspace`, `session_id`, `approved_scope`, `approval_reference`, `selected_items`, `rejected_item_ids`, `completed_steps`, `verification_results`, `blocked_reason`, `next_step`, `updated_at`. Valores identificadores devem ser preservados exatamente; não incluir dados brutos, autenticação ou URLs autenticadas.

Fluxo proposto:

```text
INTERVIEW → SCOPE_APPROVED → DISCOVERY → SELECTION
          → PLAN_READY → WAITING_IMPLEMENTATION_APPROVAL
          → APPLY → VERIFY → COMPLETE
                     ↘ BLOCKED / PAUSED
```

Persistir transições de forma atômica; registrar intenção antes de uma ação e resultado verificado depois. Na retomada: validar schema e integridade, identidade de host/perfil/workspace, vigência de consentimento e realidade das etapas marcadas concluídas. Se a execução anterior foi interrompida entre ação e gravação do resultado, primeiro ler o destino; não repetir cegamente criação ou instalação. Qualquer mudança de escopo ou conteúdo aprovado exige nova aprovação.

Na fase atual, o estado correto de um futuro fluxo é `PLAN_READY` ou `WAITING_IMPLEMENTATION_APPROVAL`, não `APPLY`. Os nomes de fases/campos acima são proposta local, não schema nativo Hermes.

## 5. Critérios de aceite para uma implementação futura

- Gatilho inicia entrevista, sem leitura de perfis/hosts não autorizados.
- Plano enumera arquivos, alias, configurações, capabilities e qualquer serviço afetado.
- Destino explicitamente selecionado e sem alterações no perfil default ou em outros perfis.
- Criação sem skills bundled quando solicitado; inventário final corresponde exatamente à seleção aprovada.
- Pacote valida frontmatter, caminhos, auxiliares, dependências e ausência de segredo; zero fixture real de usuário em testes.
- Item de memória só é aplicado após consentimento e dentro do limite real; leitura de volta e sessão nova confirmam efeito.
- Checkpoint sobrevive a interrupção e permite continuar sem transcript; repetição é idempotente.
- Host negado/indisponível, versão incompatível, skill ausente, consentimento expirado e conflito de conteúdo produzem bloqueio explícito.
- Nenhuma alegação de “bot pronto” sem teste real no destino/superfície escolhidos. Gateway só inicia com autorização separada e credenciais configuradas localmente.

Estes são testes propostos; **nenhum teste de criação, migração ou bot foi executado nesta pesquisa**.

## 6. Incertezas e divergências que importam

1. **Documentação online versus instalação:** este relatório prova capacidades documentadas, não disponibilidade na versão local/remota. Antes de implementar, levantar versão e `--help` em cada host autorizado. Não foi determinada uma versão mínima única para todos os recursos.
2. **Skills locais envelhecidas:** a skill auxiliar carregada `hermes-profile-management` afirma ausência de switcher Desktop e sugere que criação não semeia skills; o site atual documenta múltiplos perfis no Desktop e seeding padrão, com `--no-skills` opcional.[3][8] A skill `hermes-agent` também menciona default manual de aprovação, enquanto o guia atual diz smart.[7] Priorizar o site; nenhuma skill instalada foi alterada, pois a autorização desta tarefa limita a entrega a pesquisa local.
3. **Gate de escrita não é confinamento universal:** não extrapolar aprovação da ferramenta `memory`/`skill_manage` para todos os meios de escrita do mesmo usuário de SO. O próprio guia ressalta limites dos guards de arquivo.[2][7]
4. **Sem garantias de “zero segredos” do export:** a exclusão por filename é menos forte que sanitização de conteúdo. O kit exige política própria e testes.[4]
5. **Retomada não é transação:** documentação de sessões e checkpoints não estabelece exactly-once para ações multi-host; o journal/idempotência devem ser implementados e testados.[5][6]
6. **Desktop e backend evoluem separadamente:** a documentação descreve clocks de atualização diferentes; não assumir que toda UI documentada existe no cliente conectado.[8]
7. **Criação de conta/token de bot externo:** não foi encontrado nestas fontes suporte que dispense o cadastro/autenticação no provedor; tratar como configuração externa pendente, não capacidade garantida de `profile create`.[1]
8. **Sincronização de memória entre hosts:** uma distribuição mantém memórias por máquina. Um provedor externo exige pesquisa e consentimento próprios; está fora do MVP recomendado.[4]

## Resultado desta pesquisa

Foram consultadas fontes oficiais via busca/extrator web e lidas as seções relevantes que estavam truncadas nos resultados. A entrega é este relatório e um ledger de URLs para validação das citações. Não houve escrita em sistemas externos nem instalação do kit. Os únicos artefatos deliberados da tarefa estão no diretório `bot-memory-kit`; as ferramentas web também mantêm seu cache local de extrações.

## Sources

[1] https://hermes-agent.nousresearch.com/docs/user-guide/profiles
[2] https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
[3] https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
[4] https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions
[5] https://hermes-agent.nousresearch.com/docs/user-guide/sessions
[6] https://hermes-agent.nousresearch.com/docs/user-guide/checkpoints-and-rollback
[7] https://hermes-agent.nousresearch.com/docs/user-guide/security
[8] https://hermes-agent.nousresearch.com/docs/user-guide/desktop
