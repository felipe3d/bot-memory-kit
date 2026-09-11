# Memória canônica em Obsidian e segredos unattended com 1Password

## Escopo e conclusão

Pesquisa documental para um kit reutilizável Hermes em Mac notebook, Linux HomeLab e Oracle VPS. Nenhuma configuração ativa, conta, cofre ou credencial foi consultada ou modificada. As recomendações abaixo são **proposta arquitetural**, não implantação validada nos hosts.

**Recomendação:** Markdown curado em um vault Obsidian exclusivo para conhecimento compartilhável; memórias Hermes locais como índices/resumos derivados; segredos operacionais em vaults 1Password dedicados; uma identidade de automação por host e função; execução privilegiada por broker separado do agente. Não replicar o vault pessoal inteiro nem o diretório de estado Hermes.

“Obsidian como memória canônica” é uma decisão deste projeto, não um recurso nativo de memória de agentes anunciado nas fontes consultadas. A base técnica é simples: notas são arquivos Markdown locais, editáveis por outros programas; o cache de metadados é reconstruível.[11] Hermes documenta suas próprias memórias `MEMORY.md` e `USER.md`, carregadas como snapshot no início da sessão, e recomenda não compartilhar o mesmo Hermes home entre processos agentes.[9]

## 1. Separar conhecimento, estado e credenciais

| Camada proposta | Autoridade | Replicação e acesso |
|---|---|---|
| Conhecimento aprovado | Markdown do vault `AgentKnowledge` | Somente material classificado para o host consumidor |
| Propostas de atualização | Inbox por host/agente | Não promovidas automaticamente a fatos |
| Índices, embeddings e resumos | Derivados descartáveis | Reconstruídos a partir da revisão canônica |
| Memória Hermes por perfil | Contexto local e referências à base | Sem sincronizar `~/.hermes` integralmente |
| Sessões, logs, tokens OAuth | Estado local privado | Fora do vault e do pacote reutilizável |
| Segredos de aplicações | Vaults 1Password de automação | Resolução no executor, não na conversa |
| Token inicial do executor | Armazenamento protegido por host | Nunca no próprio template que depende dele |

Estrutura sugerida, com nomes ilustrativos:

```text
AgentKnowledge/
  README.md
  canonical/{people,projects,decisions,runbooks}/
  inbox/{mac-notebook,homelab,oracle}/
  archive/
```

Cada nota canônica deve registrar `id`, `status`, `owner`, `scope`, `sensitivity`, `source`, `verified_at` e `revision`. Caminhos de instalação variam por host; o kit recebe um caminho explícito, não presume `/Users/fac` no Linux.

**Política de atualização proposta:** agentes enviam propostas com origem e evidência; um reconciliador promove após validação e, para fatos sensíveis ou conflitantes, aprovação humana. Usar revisão-base/hash para detectar alteração concorrente, escrita atômica e histórico recuperável. Um lock local não resolve concorrência entre máquinas. Memória canônica é verdade editorial revisável, não prova de estado atual: portas, processos e versões continuam exigindo consulta ao host.

Conteúdo importado de páginas, notas e chats deve permanecer dado não confiável até revisão; não convertê-lo automaticamente em instrução de sistema. Segredos, dumps de ambiente e transcrições brutas não entram na memória canônica.

## 2. Sincronização portátil e acesso ao Obsidian

Obsidian Headless é um cliente independente da aplicação desktop, documentado como **open beta**, com Node.js 22 ou posterior. Não confundir com Obsidian CLI, que controla a aplicação desktop.[12] O cliente fornece sincronização pontual e contínua, e funciona em Linux; a ausência de preservação de birthtime no Linux não impede a sincronização.[5][6]

Comandos oficiais relevantes, apenas referência — **não executados nesta pesquisa**:

```text
ob login
ob sync-setup --vault <id-ou-nome> --path <caminho-local>
ob sync --path <caminho-local>
ob sync --path <caminho-local> --continuous
ob sync-status --path <caminho-local>
```

O login interativo solicita senha e MFA quando habilitado; o setup do vault solicita a senha de criptografia ponta a ponta quando omitida. Logout e unlink removem credenciais armazenadas nos respectivos escopos documentados.[5][6] Portanto, o cliente tem estado sensível local: **headless não significa sem credenciais**, e este estado não deve virar arquivo de memória, backup público ou anexo de chat.

O cliente oferece modos `bidirectional`, `pull-only` e `mirror-remote`: o segundo ignora alterações locais para upload; o terceiro também reverte alterações locais.[5] Esses modos são comportamento do cliente, **não autorização de segurança contra um agente capaz de reconfigurá-lo**. Exclusões de pastas também não substituem controle de acesso.

### Topologia recomendada

- **Mac notebook:** interface editorial humana; vault de conhecimento separado do vault pessoal; um único mecanismo de sync por cópia local.
- **HomeLab:** candidato a reconciliador e distribuidor sempre ativo, condicionado à disponibilidade real. Conta de sincronização separada do usuário do agente; snapshot de leitura para os consumidores; inbox de escrita separada.
- **Oracle VPS:** receber apenas subconjunto sanitizado, preferencialmente sem sessão Obsidian da conta pessoal. Não disponibilizar credenciais do sync nem acesso ao vault pessoal ao processo do agente.

Para a primeira versão, snapshots aprovados ou um repositório privado somente de Markdown simplificam distribuição e revisão. A documentação aceita edição externa e menciona Git entre as alternativas de sincronização; isso não torna um plugin Git parte nativa obrigatória.[11] Headless Sync pode ser um backend opcional quando a assinatura e a beta forem aceitáveis. Usar um só escritor/promotor lógico e evitar dois mecanismos concorrentes na mesma pasta é recomendação operacional deste relatório.

**Bootstrap Obsidian:** operador autentica fora do chat e prepara a cópia; serviço roda posteriormente com estado protegido. Não passar senha real em `--password` numa chamada de ferramenta visível: o argumento pode aparecer em logs ou inspeção de processos. As páginas consultadas não estabelecem uma identidade de serviço por vault com escopo equivalente ao 1Password Service Account; não presumir essa granularidade. O README também documenta que `--json` desativa prompts e exige `--password` para setup E2EE, incompatível com simplesmente “deixar o prompt seguro” nesse modo.[6]

E2EE do transporte/serviço não elimina os arquivos Markdown legíveis na cópia local.[11][12] Proteger disco, usuário, backups e permissões; sync não substitui backup independente e teste de restauração.

## 3. 1Password CLI: o caminho unattended suportado

### Autenticação humana versus identidade de serviço

A integração CLI com o aplicativo desktop solicita autenticação e usa métodos como Touch ID, senha do dispositivo e outros mecanismos de desbloqueio.[4] É adequada para ações supervisionadas, mas não deve ser tratada como garantia de cron após reboot/logout.

Para automação, Service Accounts autenticam via `OP_SERVICE_ACCOUNT_TOKEN`, suportam `op read`, `op inject` e `op run`, e requerem CLI 2.18.0 ou posterior.[1][2] A documentação limita acesso aos vaults selecionados; não permite conceder acesso aos vaults embutidos Personal, Private, Employee nem ao Shared padrão.[1]

Pontos importantes para o kit:

- Criar vaults exclusivos de automação e conceder somente `read_items`, salvo necessidade justificada. As permissões, acesso a vaults e acesso a Environments da Service Account são imutáveis; alterar escopo exige nova conta.[1]
- O token é mostrado uma única vez na criação e deve ser protegido como senha; a criação via CLI admite expiração por `--expires-in`.[1]
- `OP_CONNECT_HOST` e `OP_CONNECT_TOKEN` têm precedência sobre `OP_SERVICE_ACCOUNT_TOKEN`. O launcher deve controlar explicitamente esse ambiente para evitar autenticação no backend errado.[2]
- Há quotas/rate limits; IDs de item e vault podem reduzir chamadas. Não resolver o mesmo segredo repetidamente a cada pensamento do agente.[2]

### Injeção sem imprimir valores

`op run --env-file=... -- <programa>` resolve referências e fornece segredos ao subprocesso por variáveis de ambiente durante sua execução; stdout/stderr têm mascaramento padrão.[3] Exemplo conceitual de template sem valores reais:

```dotenv
API_TOKEN=op://automation-homelab/example-service/token
```

```text
op run --env-file=/caminho/refs.env -- /caminho/executor-aprovado
```

O arquivo de referências pode ser distribuído sem o valor secreto, mas nomes e IDs ainda podem revelar metadados internos. Preferir aliases públicos no kit e mapeamento por host fora do chat.

**Limite de segurança:** mascaramento não é sandbox. O programa recebe o segredo e pode copiá-lo, transformá-lo ou transmiti-lo. Não usar `printenv`, dumps de configuração, `op read` com saída para o chat, `--no-masking`, shell tracing ou segredos em argumentos. `op inject` materializando arquivos exige uma política adicional de permissões, descarte e backup; evitar quando variável de ambiente ou canal privado satisfaz o executor.

### Bootstrap: quem entrega o primeiro segredo?

A variável `OP_SERVICE_ACCOUNT_TOKEN` precisa existir antes de `op` resolver os demais segredos.[2] Guardar a única cópia desse token num item que depende do próprio token cria uma dependência circular — não resolve inicialização após reboot.

Procedimento proposto, executado pelo operador em canal local seguro:

1. Criar Service Account com escopo mínimo e recuperar o token uma vez; guardar a cópia administrativa no 1Password conforme orientação oficial.[1]
2. Provisionar a cópia operacional no armazenamento protegido do host, fora de Git, Obsidian, prompt, histórico de shell e parâmetros visíveis de ferramentas.
3. Launcher/broker recupera o token e o coloca apenas no ambiente do processo `op`; retira-o do ambiente do executor final quando não necessário. Não pressupor que `op run` o elimine automaticamente.
4. Resolver somente segredos da operação autorizada; executar; retornar status e saída sanitizada, nunca o material resolvido.
5. Testar reinício, ausência de login humano, indisponibilidade da rede, expiração, revogação e rotação. Falhar fechado, sem fallback para a conta pessoal do aplicativo desktop.

O armazenamento de bootstrap pode ter adaptadores diferentes: helper Keychain no Mac, armazenamento de credenciais do gerenciador de serviços ou secret store do host no Linux/cloud. Esses adaptadores são **design proposto, ainda não validados**; não presumir TPM no HomeLab ou na VPS. Um arquivo plaintext restrito reduz exposição casual, mas não equivale a armazenamento criptografado e contraria a recomendação oficial de não guardar o token em plaintext.[1]

1Password Connect é alternativa com REST API privada e cache na infraestrutura, permitindo reconsultas sem as mesmas quotas após a primeira busca.[13] Acrescenta serviço, credenciais de bootstrap, armazenamento e manutenção: não é necessário para a primeira versão com três hosts, salvo requisitos de cache/disponibilidade que justifiquem o custo.

## 4. Apple Passwords não é sinônimo de Keychain

| Componente | O que a documentação estabelece | Consequência |
|---|---|---|
| Apple Passwords / Senhas | Aplicativo de senhas, passkeys, Wi-Fi e códigos; integração com iCloud Keychain e AutoFill.[7] | Não assumir interface oficial headless Linux/VPS para recuperação arbitrária de segredos |
| iCloud Keychain | Sincroniza credenciais entre dispositivos aprovados; usa recursos da implementação Data Protection no Mac.[7][10] | Não é simplesmente o arquivo `login.keychain` |
| Keychain file-based | Implementação tradicional, arquivos login/System, ACLs; utilizável fora de contexto de usuário.[10] | Pode integrar bootstrap Mac, condicionado a ACL e disponibilidade/desbloqueio |
| Data Protection Keychain | Exige contexto de login do usuário, access groups e entitlements de assinatura; indisponível a um daemon `launchd` fora desse contexto.[10] | API SecItem não concede acesso irrestrito a todas as credenciais pessoais |
| Keychain Access / Acesso às Chaves | UI para ambas as implementações, com diferenças de itens apresentados.[10] | Não é o mesmo aplicativo que Passwords |
| CLI `security` | Suporte de keychain focado principalmente na implementação file-based.[10] | Não prometer `security find-generic-password` como leitor universal do app Passwords |

A Apple recomenda a API SecItem e, onde viável, Data Protection; para programas fora do contexto de usuário, a technote indica file-based.[10] A escolha precisa considerar daemon versus agente de sessão, ACLs, entitlements, reboot e prompts de autorização. Não recomendar desbloquear globalmente um chaveiro pessoal ou conceder acesso a qualquer aplicativo só para eliminar prompts.

**Conclusão documental:** nas fontes oficiais consultadas não foi identificado um contrato Apple Passwords equivalente a Service Accounts + `op run` para automação portátil unattended. Isso não é afirmação de impossibilidade absoluta de toda integração Apple; é limite da evidência e razão para não usá-la como fundação multiplataforma do kit.

## 5. Isolamento efetivo: referências não bastam

Proposta de fluxo de segurança:

```text
Agente sem credenciais
  -> operação tipada e autorizada
  -> broker/executor com usuário separado
  -> bootstrap local -> 1Password -> segredo somente no executor
  -> API de destino
  -> resultado filtrado para o agente
```

- Identidade distinta por host e, idealmente, por função. Vaults separados quando os conjuntos de segredos diferirem; a seleção de uma referência não reduz por si só a autorização concedida à Service Account.[1][3]
- O agente não recebe token, não lê diretório privado do broker e não altera executável, allowlist, template ou configuração do launcher.
- Broker aceita operações fixas com argumentos validados; nunca shell arbitrário, referência `op://` arbitrária ou URL de destino controlada livremente pelo modelo.
- Mesmo usuário de sistema, shell amplo, mount gravável do broker, acesso root ou socket administrativo podem destruir a separação. Perfis Hermes organizam estado; não substituem isolamento de SO.
- Limitar rede/egress do executor, sanitizar erros e impedir vazamento por stdout, arquivos temporários, telemetria e crash dumps. Auditoria registra operação, identidade, horário e resultado, não valor.
- A chave do próprio provedor LLM, quando necessária ao runtime, também deve ficar no processo de confiança que realiza a chamada; não dar ao shell do agente capacidade irrestrita de inspecionar esse processo.

## 6. Critérios para uma implementação futura

Não foram executados; são critérios de aceitação do kit:

1. Leitura da mesma revisão canônica nos hosts autorizados; VPS incapaz de ler notas pessoais.
2. Escritas concorrentes preservadas na inbox, conflito detectado e promoção rastreável.
3. Reconstrução dos índices sem perda da fonte Markdown e restauração de backup testada.
4. Inicialização unattended após reboot sem conta humana desbloqueada, ou documentação explícita de que o modo Mac é somente supervisionado.
5. Token de um host incapaz de acessar vault de outro; tentativa negada verificada com fixtures de teste.
6. Revogação/rotação exercitada; credencial antiga deixa de autorizar; indisponibilidade não causa fallback inseguro.
7. Segredo-canário não aparece em tool outputs, conversa, logs, histórico, backups ou memória; teste inclui exceções e subprocessos.
8. Broker não aceita shell, destinos arbitrários ou referências fora da allowlist; agente não lê nem modifica seu estado privado.
9. Testes com `op user get --me` podem validar identidade sem mostrar segredos, mas saída ainda contém metadados; resumir somente aprovação/reprovação no chat.[2]

## Limitações da pesquisa

Fontes oficiais online, sem teste de autenticação real, preços/plano contratado, permissões efetivas ou disponibilidade de hardware. Houve rate limit transitório do extrator e duas URLs inicialmente inválidas; novas consultas recuperaram as páginas corretas. O Headless está documentado como beta; antes de automatizar, fixar versão e consultar `--help`. Há diferença de grafia do valor de criptografia entre a página Sync (`e2ee`) e o README (`end-to-end`); não padronizar cegamente comandos de criação sem verificar a versão instalada.[5][6]

Este documento é um relatório de pesquisa e desenho de arquitetura; não prova que a integração ou o isolamento já estejam funcionando.

## Sources

[1] https://www.1password.dev/service-accounts/get-started
[2] https://www.1password.dev/service-accounts/use-with-1password-cli
[3] https://developer.1password.com/docs/cli/reference/commands/run
[4] https://developer.1password.com/docs/cli/app-integration
[5] https://obsidian.md/help/sync/headless
[6] https://github.com/obsidianmd/obsidian-headless
[7] https://support.apple.com/en-us/120758
[9] https://hermes-agent.nousresearch.com/docs/user-guide/features/memory
[10] https://developer.apple.com/documentation/technotes/tn3137-on-mac-keychains
[11] https://help.obsidian.md/Files+and+folders/How+Obsidian+stores+data
[12] https://obsidian.md/help/headless
[13] https://www.1password.dev/connect
