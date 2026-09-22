# CS-031 — Prova real de perímetro VPS para N-01/N-02

**Estado:** AWAITING_APPROVAL  
**Work package:** WP-031 — perímetro real sem conteúdo  
**Janela/host:** proposta documental; nenhum host, identidade, credencial, vault ou conteúdo foi acessado.

## Problema e resultado esperado

O piloto CS-030 validou o mecanismo sintético, mas não certificou N-01 e N-02 no runtime VPS real. Antes de qualquer projeção de AgentKnowledge ou Gate R, este change set propõe provar tecnicamente que uma identidade VPS dedicada não acessa o vault pessoal nem credenciais de outros papéis.

A prova é de **perímetro**, não de conteúdo: não lê notas, não busca AgentKnowledge, não lista vaults, não abre segredos e não cria uma projeção.

## Escopo proposto

1. Criar, em fase posterior aprovada, uma identidade Linux VPS descartável `ak-perimeter-probe`, sem grupo privilegiado, home Hermes, mount, cron ou serviço.
2. Aplicar uma allowlist fechada de superfícies de observação e canários não secretos sintéticos.
3. Executar N-01/N-02 apenas contra essa identidade e as superfícies explicitamente aprovadas.
4. Registrar auditoria sanitizada, revogar/remover a identidade e confirmar limpeza.

## Fora de escopo

- Acessar qualquer vault, nota, Obsidian/Headless, sync, AgentKnowledge, state.db, home Hermes, conteúdo pessoal, dado de cliente, dado GTD/CRM ou projeção real.
- Ler valores de `.env`, credenciais, tokens, chaves, sessões, keyrings, 1Password, SSH agent ou configuração integral.
- Criar consumidor de produção, repo, deploy key, publisher, cron, serviço, transporte ou Gate R.
- Testar N-03–N-06, disponibilizar 24/7 ou recuperar conteúdo.

## Superfícies allowlisted propostas

| Classe | Operação futura permitida | Evidência permitida | Negação requerida |
|---|---|---|---|
| Identidade | UID/GID, grupos e capabilities de `ak-perimeter-probe` | nomes lógicos, UID/GID, booleanos | ausência de sudo/admin/grupos de integração |
| Filesystem | `stat`/teste de existência somente em paths exatos de canários sintéticos e raízes proibidas declaradas | existência/owner/mode, nunca conteúdo | sem mount ou travessia a vault/home/secret store alheio |
| Processo/serviço | ambiente do processo da sonda e mounts do namespace da sonda | nomes de mount/booleanos sanitizados | sem sockets, agentes ou serviços de sync expostos |
| Rede | tentativa controlada somente para endpoints-canário sintéticos/loopback de teste | código de negação, sem URL/credencial real | sem rota/fallback ao vault ou secret backend |
| Credencial sintética | canários sem segredo, criados exclusivamente para a prova | ID lógico e resultado de acesso | canário de outro papel inacessível; canário próprio só se explicitamente concedido |

Nenhuma superfície pode ser adicionada por inferência. Path, endpoint, usuário, comando e canário reais serão preenchidos apenas num anexo aprovado de aplicação.

## N-01 — VPS não acessa vault pessoal

A identidade de prova deve falhar fechada ao tentar somente os paths/mounts/endpoints-canário definidos no anexo. O relatório registra `denied|absent`, sem listar árvores, nomes de notas, conteúdo, URLs autenticadas ou detalhes de vault.

**Aceite:** não há mount, cliente, sessão, rota, token ou artefato utilizável para listar/ler o vault. Um resultado ambíguo, uma permissão transitiva ou qualquer necessidade de abrir conteúdo é falha e interrompe.

## N-02 — VPS não acessa credenciais alheias

A identidade de prova recebe canários próprios sem valor secreto. Ela tenta acessar somente canários de outros papéis e superfícies explicitamente declaradas. Não serão lidos envs, keyrings, homes ou arquivos de credenciais existentes.

**Aceite:** tentativa não autorizada falha; nenhuma credencial pessoal, de sync, reconciliador ou outro perfil é montada, herdada ou resolvível. Uma inspeção que exigiria mostrar valor, nome sensível ou configuração ampla resulta em `BLOCKED`.

## Plano futuro de aplicação

| Passo | Mudança proposta | Leitura posterior | Rollback |
|---|---|---|---|
| R-00 | Aprovar anexo com alvo VPS, identidade, canários, paths e comandos exatos | revisão humana do inventário fechado | cancelar sem mutação |
| R-01 | Criar identidade descartável e raízes sintéticas isoladas | UID/grupos/modes e ausência de grants | remover identidade e raízes exatas |
| R-02 | Criar canários não secretos por papel, somente fora de vault/secret store | IDs lógicos e modes | remover canários exatos |
| R-03 | Executar N-01/N-02 com logs sanitizados e controles positivos | resultados, reason codes e read-back | parar e revogar na primeira ambiguidade |
| R-04 | Remover identidade, canários e raízes; reter auditoria mínima | ausência dos alvos e auditoria legível | não restaurar sem novo gate |

## Aprovação explícita

Este documento não autoriza criação ou discovery. Para executar o futuro R-00–R-04, será necessário um gate que nomeie os alvos reais e diga explicitamente:

> Aprovo a execução do CS-031, revisão e anexo de alvos explicitamente aprovados, exclusivamente para criar, verificar e remover a sonda de perímetro N-01/N-02 sem conteúdo. Não autorizo leitura de vault, AgentKnowledge, segredos, credenciais existentes, dados reais, Gate R ou qualquer projeção.

## Anexo A — defaults para prova de perímetro N-01/N-02

**Estado do anexo:** desenho documental aprovado para preenchimento em 2026-09-18; nenhuma identidade, raiz, canário ou teste foi criado/executado.

| Item | Default proposto | Limite |
|---|---|---|
| Host | `oracle-vps`, único alvo de R-00–R-04 | Nenhum HomeLab, Mac, vault ou serviço de produção entra neste CS. |
| Sonda | usuário Linux novo `ak-perimeter-probe`, sem shell interativo, sudo, grupo privilegiado, cron, serviço, mount ou home Hermes | Descartável; só acessa sua raiz. |
| Canários | usuários novos `ak-perimeter-canary-personal` e `ak-perimeter-canary-sync`, cada qual com uma raiz e arquivo não secreto próprios | Os canários contêm apenas texto fixo `CS031-CANARY`; não representam, apontam ou copiam segredo real. |
| Raízes | `/var/tmp/cs031-perimeter-probe`, `/var/tmp/cs031-perimeter-canary-personal`, `/var/tmp/cs031-perimeter-canary-sync` | Modo 0700, owner do papel correspondente; sem links simbólicos, bind mount ou submount. |
| Auditoria | `/var/tmp/cs031-perimeter-audit`, root-owned 0700, com eventos sanitizados root-only | Só IDs lógicos, operações, exit/status e booleans; nenhum path sensível, valor, secret ou stdout bruto. |
| Ambiente da sonda | `env -i` com `PATH` mínimo fixo, diretório de trabalho na raiz da sonda | Sem herança de env, agente, socket, keyring ou variável de login. |
| Prazo | execução manual única, máximo 15 min, sem cron/timer/serviço | Remove sonda, canários e raízes imediatamente após os read-backs; auditoria permanece conforme retenção aprovada. |

### Allowlist de superfícies e comandos futuros

| ID | Superfície | Operação permitida | Saída permitida | Nega/aceita |
|---|---|---|---|---|
| S-01 | identidade da sonda | `id`, `getent` somente para os três usuários CS-031 | UID/GID, grupos e homes dos usuários sintéticos | Nega sudo/grupo privilegiado/herança de papel alheio. |
| S-02 | raízes CS-031 | `stat`, `namei -l`, `test -e` somente nas quatro raízes do anexo | owner, mode, tipo e existência | Exige 0700, owner correto e ausência de link/submount. |
| S-03 | namespace da sonda | `findmnt`/`mountinfo` filtrado pelo namespace/processo da sonda, com relatório apenas booleano por classe | `vault_mount=false`, `secret_mount=false`, `unexpected_mount=false` | Qualquer mount fora de roots/sistema básico falha. |
| S-04 | ambiente limpo | executar a sonda com `env -i`; comparar somente nomes de variáveis allowlisted | lista allowlisted e booleano de divergência | Qualquer variável/agent/socket não allowlisted falha. |
| S-05 | canários sintéticos | tentativa de `stat`/leitura pela sonda nos canários alheios; controle positivo só pelo owner canário | `denied|allowed`, sem conteúdo | Sonda deve receber negação para ambos os canários. |
| S-06 | rede | nenhuma conexão externa; somente `AF_UNIX`/TCP de canário criado no próprio teste, se necessário | código de negação/allowlist | Ausência de endpoint externo e de fallback é obrigatória. |

### Critérios N-01/N-02 neste anexo

- **N-01:** prova somente que a sonda não possui mount, root, serviço ou rota de teste que a conecte a uma fonte de vault. Não inspeciona um vault real. Para estender a prova a qualquer path/serviço real, um anexo posterior deve nomear essa superfície e obter gate próprio.
- **N-02:** prova que a sonda não herda ambiente e não lê canários de papéis alheios. Não abre nem enumera credenciais reais. Qualquer necessidade de fazê-lo bloqueia este CS e exige change set separado.
- Falha, ambiguidade, saída inesperada ou tentativa de ampliar a allowlist resulta em `BLOCKED`, remove a sonda/canários e preserva somente auditoria sanitizada.

### Gate de execução futuro

Antes de executar, a aprovação deve referenciar explicitamente esta tabela final de comandos e o anexo; qualquer mudança em identidade, root, comando ou saída exige nova revisão.

### Tabela final R-00–R-04 — comandos/exatos propostos

Todos os comandos abaixo usam o alvo MCP/SSH autorizado futuramente para `oracle-vps`; nenhum usa HomeLab, vault, AgentKnowledge, conteúdo, segredo ou configuração existente. `sudo -n` deve ser usado somente para criar/remover os recursos CS-031 enumerados, nunca shell arbitrário. O operador executa no canal do host, não como a sonda, exceto onde a linha diz "identity = sonda".

| Passo | Comando/ação exata | Baseline e código esperado | Read-back obrigatório | Rollback/limpeza |
|---|---|---|---|---|
| R-00 | Na conta operadora da VPS, checar por existência de `ak-perimeter-probe`, `ak-perimeter-canary-personal`, `ak-perimeter-canary-sync` e das quatro raízes; registrar o resultado em evento root-owned sintético | Todos ausentes; qualquer existência → código de saída de recusa e nenhum recurso é criado | Read-back do inventário e do único artefato de auditoria criado | Cancelar sem mutação |
| R-01 | Criar as três contas Linux descartáveis com `useradd --system --create-home`, home dedicado, shell `/usr/sbin/nologin`; criar quatro raízes com `install -d -o <owner> -g <owner> -m 0700` | Contas novas e roots novos, exclusivamente CS-031 | `id` e `getent` para os três usuários; `stat -c` nas quatro raízes: root owner root 0700 para auditoria; papel correto 0700 para as demais | Remover as três contas e quatro raízes por nome/path exato, deixando somente auditoria |
| R-02 | Criar de cada papel canário um arquivo único `canary.txt` em sua raiz, modo 0600, conteúdo fixo `CS031-CANARY`; criar o artefato de auditoria vazio root-owned 0700 e log inicial | Somente conteúdo não secreto; nenhum path real ou valor sensível | `stat` root-owner/mode do audit e dos canários; nenhum payload registrado no audit | Remover somente os canários exatos e o audit inicial se R-00 falhar; não ler conteúdo real |
| R-03 | Executar cinco testes com a sonda e seu ambiente `env -i PATH=/usr/sbin:/usr/bin`, cwd e root próprios: `id`/grupos e ausência de grants; `stat`/`namei` sobre as roots CS-031; `findmnt -la -o TARGET,FSTYPE,SOURCE,OPTIONS` capturado, classificado por classe e gravado só booleanos; tentativa da sonda de `test -r` nos canários alheios de personal/sync e controle positivo pelos respectivos owners; tentativa de `connect()` a um endereço reservado de TEST-NET somente para verificar `EACCES`/`ECONNREFUSED`/`ENETUNREACH`, sem usar destino real | Códigos esperados: grants da sonda ausentes; roots CS-031 corretas; mounts não atribuídos a vault/secret; leitura dos canários alheios negada; controle positivo de cada owner lê somente o próprio canário; rede recebe negação/indisponibilidade sem fallback | Eventos por teste com `denied|allowed|error`, reason code, UID lógico e timestamp UTC; read-back do audit por operador root, sem conteúdo do teste | Se qualquer resultado não bater com o esperado, parar imediatamente, rotular `BLOCKED`, e remover sem tentar diagnóstico fora do anexo |
| R-04 | Remover os processos/arquivos/raízes CS-031 por nomes/paths exatos com `rm -rf` somente na allowlist e `userdel -r` dos três usuários; preservar audit root-owned | Não tocar nada fora da lista; falha de cleanup é bloqueio | `id`/`getent` ausente para os três usuários; `test -e` ausente nas três roots e nos canários; audit permanece legível root-only | Se algo permanecer, manter bloqueio, registrar resíduo e exigir remediação humana, sem restaurar acesso |

### Baseline e critérios de falha fechada

O baseline mínimo de R-00 é necessariamente limitado: só comprova ausência dos nomes/paths da sonda, canários e roots CS-031, não inventaria todo host. Isso é intencional para reduzir descoberta. Falha em baseline, criação, leitura posterior, revogação ou limpeza retorna `BLOCKED`, remove somente recursos CS-031 e não permite tentativa alternativa.

### Aprovação exata para execução futura

> Aprovo a execução do CS-031, Anexo A e tabela final R-00–R-04, exclusivamente para criar, verificar e remover a sonda de perímetro N-01/N-02 na VPS. Não autorizo leitura de vault, AgentKnowledge, segredos, credenciais existentes, dados reais, Gate R ou qualquer projeção.

### Estado final

**VERIFIED** — R-00–R-04 executados e limpos conforme `program/evidence/CS-031-real-perimeter-run.md`. A prova confirma o perímetro da sonda sintética e não certifica nada fora desse escopo.

## Evidência

Execução concluída em 2026-09-18: todas as fases passaram e foram removidas; ver `program/evidence/CS-031-real-perimeter-run.md`.
