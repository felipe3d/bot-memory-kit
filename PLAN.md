# Plano de Implementação — bot-memory-kit (revisado v2)

Data: 2026-09-10 · Fase: WAITING_IMPLEMENTATION_APPROVAL
Base: `hermes-research.md` + `memory-secrets-research.md`. Fontes citadas nestes relatórios apontam para páginas oficiais (Hermes docs, 1Password dev, Obsidian, Apple); nas seções de segurança, links diretos são indicados quando relevantes.
Revisto por: subagente independente (2026-09-10) — correções C1/C2/A1-A3/M1-M5/B1-B3 aplicadas nesta v2.

Princípio central: **o kit é uma skill orquestradora + templates + scripts, com dados privados por execução e nenhuma alteração de ambiente sem aprovação.** O Hermes já fornece perfis, seleção de skills, aprovação de memória e retomada; o kit adiciona gating de intenção, consentimento multi-host, curadoria item a item, checkpoints semânticos, e segurança de segredos/privilégios com isolamento real do executor.

## 0. Decisões de escopo e política (MVP)

### Criação de perfis
- **Não usar clonagem de perfil como padrão.** `--clone` copia `.env`; `--clone-all` copia memórias mas exclui histórico/cron/checkpoints. Toda migração parte de lista positiva aprovada, sem copiar `.env`, `auth.json`, caches, logs, transcripts ou diretórios inteiros ([Hermes profiles](https://hermes-agent.nousresearch.com/docs/user-guide/profiles)).
- **Criar perfis com `hermes profile create NOME --no-skills`** e selecionar skills positivamente ([Hermes skills](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)).
- Preferir `-p <perfil>` explícito a `profile use`, para não mudar o default persistente. Registrar no plano aprovado os efeitos colaterais (ex.: alias em `~/.local/bin/`).

### Conhecimento e memória
- **Obsidian/Markdown canônico** para conhecimento compartilhável aprovado; memórias Hermes locais como índices/resumos derivados. Ver topologia em §1.
- Migração de memória por item aprovado, dentro dos limites reais (`MEMORY.md` 2.200, `USER.md` 1.375 chars); `replace/remove` por substring única, sem compactação silenciosa.

### Segredos e privilégios
- **1Password Service Accounts** como adaptador inicial (host→SA→vault). Nunca valores em chat/logs/artefatos/memória; só referências `op://` com aliases públicos e mapeamento por host fora do chat.
- **Apple Passwords / Keychain** documentados como alternativas **supervisoras somente**, não base multiplataforma automática (diferença entre app Senhas, iCloud Keychain, keychain file-based e Data Protection; CLI `security` cobre principalmente file-based — [Apple TN3137](https://developer.apple.com/documentation/technotes/tn3137-on-mac-keychains)).
- **Privilégios:** operações aprovadas com `sudo -n` + regras sudoers específicas; falha fechada, sem senha armazenada nem `NOPASSWD: ALL` universal.
- **Executor em conta de sistema separada** (não a do usuário/do dono do cofre). Mesmo usuário do broker destrói a separação. Ver §5.

### Aprovação e continuidade
- Política de aprovação do perfil de destino: `memory.write_approval: true`, `skills.write_approval: true`, aprovação de comandos em modo `manual`; **negar** ações headless perigosas, sem YOLO/cron automático/publicação por padrão. Aplicar por perfil criado pelo kit, sem tocar no default ([Hermes memory/skills/security docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory)).
- **Gatilho explícito:** `/bot-memory-kit` (iniciar/retomar/consultar). Menção casual a "memória" não inicia descoberta, leitura ou alteração. Iniciar o gatilho autoriza começar a **entrevista**, não instalar/migrar.
- **Duas aprovações humanas separadas:** (1) escopo antes da descoberta; (2) plano antes do APPLY.
- **Gateway (cron/VPS 24/7) só inicia com autorização separada** e credenciais/configuração locais. Não é efeito colateral de criar um perfil.
- **Estado persistente** em checkpoint próprio + journal idempotente, independente do transcript (ver §3 e §6).

## 1. Estrutura alvo do kit

```text
~/dev/bot-memory-kit/
├── README.md
├── PLAN.md                 (este arquivo)
├── hermes-research.md      (pesquisa citada — capacidades Hermes)
├── memory-secrets-research.md (pesquisa citada — memória/segredos/obsidian)
├── skill/                  (conteúdo instalável da skill Hermes)
│   ├── SKILL.md
│   ├── references/
│   │   ├── consent-and-discovery.md
│   │   ├── selection-and-safety.md
│   │   ├── memory-migration.md
│   │   ├── secrets-and-privileges.md
│   │   ├── canonical-knowledge.md      # topologia do vault (nova)
│   │   └── resume-protocol.md
│   ├── templates/
│   │   ├── interview.md
│   │   ├── execution-manifest.json
│   │   ├── checkpoint.json
│   │   ├── approval-plan.md
│   │   └── broker/                     # launcher + allowlist (novo, C1)
│   │       ├── launcher.example.env
│   │       └── operations.example.yaml
│   └── scripts/
│       ├── discover.py
│       ├── validate_manifest.py
│       ├── validate_checkpoint.py
│       └── scan_artifacts.py
├── docs/
│   ├── multi-host.md          # topologia Mac/HomeLab/VPS (reflete C1/C2/A2)
│   ├── security.md            # ameaças, limites, egress, home_mode
│   └── maintenance.md
└── tests/fixtures/            # somente dados fake, nunca dados reais
```

### Topologia do conhecimento canônico (A2) — espelha memory-secrets-research
Estrutura de vault ilustrativa (nomes configuráveis, não fixos):
```text
AgentKnowledge/
  README.md
  canonical/{people,projects,decisions,runbooks}/
  inbox/{mac-notebook,homelab,oracle}/
  archive/
```
- Cada nota canônica registra `id`, `status`, `owner`, `scope`, `sensitivity`, `source`, `verified_at`, `revision`.
- **Promoção:** agentes enviam propostas com origem/evidência para `inbox/`; um **reconciliador** promove após validação e, para fatos sensíveis ou em conflito, aprovação humana. Usar revisão-base/hash contra conflito concorrente, escrita atômica, backup recuperável.
- **Isolamento de conhecimento:** a VPS só recebe subconjunto sanitizado, **sem sessão Obsidian da conta pessoal** e incapaz de ler notas pessoais. HomeLab recebe snapshot de leitura; inbox de escrita separada.
- Obsidian Headless é **open beta**; se adotado, fixar versão e validar com `ob --help`. `headless ≠ sem credenciais` (guarda estado de login local) — proteger disco/backups/usuário.
- Memória canônica é **verdade editorial revisável, não prova de estado atual**: portas, processos, versões exigem consulta ao host.

## 2. Fluxo de etapas (máquina de estados canônica)

```text
INTENT (gatilho explícito)
  → INTERVIEW (adaptativa; salva apenas respostas aprovadas)
  → SCOPE_APPROVED (aprovação 1/2 — escopo antes de descoberta)
  → CONSENT_PER_HOST (antes de qualquer leitura de host)
  → DISCOVERY (somente leitura; metadados e capacidades, nunca conteúdo de segredos)
  → SELECTION (skills, toolsets, MCPs, memória por item, fontes)
  → ARCHITECTURE (bots, host proprietário, conhecimento canônico, topologia)
  → PLAN_READY (manifesto + plano de aprovação → aprovação humana)
  → WAITING_IMPLEMENTATION_APPROVAL (aprovação 2/2 — antes do APPLY)
  → APPLY (backup → implantação idempotente por passo → verificação)
  → VERIFY (testes de aceitação no destino real)
  → COMPLETE / BLOCKED / PAUSED
```
Estado atual desta fase: `WAITING_IMPLEMENTATION_APPROVAL` (nunca `APPLY`).

Regras:
- **Separar classes de autorização:** descobrir metadados ≠ ler conteúdo ≠ persistir fatos ≠ transferir para outro host ≠ configurar credenciais ≠ iniciar serviços. Host indisponível → `BLOCKED`, sem ampliar escopo nem usar caminho alternativo não autorizado.
- Cada transição persistida atomicamente; intenção antes da ação, resultado verificado depois.
- Interrupção: **ler o destino antes de repetir**; idempotente, sem exactly-once presumido sem teste.
- Mudança de escopo ou conteúdo aprovado exige nova aprovação.

## 3. Checkpoint semântico (M1)

Campos mínimos (`templates/checkpoint.json`): `schema_version`, `kit_version`, `run_id`, `phase` (da máquina em §2, incl. `WAITING_IMPLEMENTATION_APPROVAL`/`BLOCKED`/`PAUSED`), `host_id`, `profile_id`, `workspace`, `session_id`, `approved_scope`, `approval_reference`, `selected_items`, `rejected_item_ids`, `completed_steps`, `verification_results`, `blocked_reason`, `next_step`, `updated_at`. Identificadores preservados exatamente. Sem dados brutos, autenticação ou URLs autenticadas.
- Validação do checkpoint: schema, integridade, identidade host/perfil/workspace, **vigência do consentimento**, realidade das etapas marcadas concluídas. Validar por `scripts/validate_checkpoint.py`.
- `scripts/scan_artifacts.py`: ausência de segredo-canário (ver §6). `validate_manifest.py`: schema + fronteiras.

## 4. Descoberta de segredos e autenticação

Fase `DISCOVERY` detecta **presença/ausência e versão, nunca valores**:
- 1Password CLI (`op --version`); presença de Service Accounts/Connect (sem listar vaults/abrir itens por padrão).
- Senhas da Apple / Keychain (presença do app e do utilitário `security`; **sem `find-generic-password` sem autorização explícita e escopo**).
- Bitwarden/outros gerenciadores instalados.
- Nomes de variáveis de ambiente de automação relevantes (**somente nomes**, jamais valores).
- Helpers de bootstrap (keychain file-based, secret store do gerenciador de serviços).

Regra dura: **nenhum segredo em artefatos, checkpoints, memória, skills ou relatórios.** Referências `op://` com aliases públicos; mapeamento por host fora do chat.

### Bootstrap unattended (M2 — multi-SA, sem plaintext)
1. **Por host**: operador cria Service Account com escopo mínimo (só `read_items` salvo justificativa) e recupera o token uma vez; guarda cópia administrativa no 1Password. Permissões/acesso a vaults/Environments são **imutáveis** — alterar escopo exige nova SA (https://www.1password.dev/service-accounts).
2. **Mapa host→SA→local de storage operacional**, documentado fora do chat (ex.: `storage: keychain-helper` no Mac, `secretstore` gerenciado no Linux/VPS).
3. **Proibido** token em plaintext (contraria recomendação oficial; risco documentado necessário). Provisionar cópia operacional no armazenamento protegido do host, fora de Git/Vault/prompt/histórico/parâmetros visíveis de ferramentas.
4. Launcher/broker recupera o token só no ambiente do processo `op`; não expõe ao executor final. `OP_CONNECT_HOST`/`OP_CONNECT_TOKEN` têm precedência sobre `OP_SERVICE_ACCOUNT_TOKEN` — o launcher controla esse ambiente para evitar auth no backend errado.
5. Resolver apenas segredos da operação autorizada; retornar status sanitizado.
6. **Testar** reboot sem login humano, ausência de rede, expiração, revogação, rotação. Falha fechada, sem fallback para conta pessoal.

## 5. Privilégios e isolamento do executor (C1, C2)

### 5.1 Isolamento real (C1)
- **Executor/broker em conta de sistema separada** (ex.: usuário de serviço dedicado). O agente não lê nem altera o diretório privado do broker, executável, allowlist, templates ou configuração do launcher.
- Broker aceita **operações fixas** com argumentos validados; **nunca** shell arbitrário, referência `op://` arbitrária ou URL de destino controlada livremente pelo modelo.
- **Egress de rede limitado**; sanitizar stdout, temporários, telemetria e crash dumps; auditoria registra operação/identidade/horário/resultado, nunca valor.
- Mesmo `sudo`, shell amplo, mount gravável do broker, acesso root ou socket administrativo **destroem a separação**. Perfis Hermes organizam estado; **não** substituem isolamento de SO.
- Este broker é um componente novo do kit (`templates/broker/`) com allowlist e fixtures de teste — ver C1.

### 5.2 HOME real dos subprocessos (C2)
- Subprocessos no host mantêm o `HOME` real por padrão e certos logins OAuth são compartilhados; `terminal.home_mode: profile` separa o HOME dos subprocessos do perfil, mas **não é contenção de SO** ([Hermes profiles/security](https://hermes-agent.nousresearch.com/docs/user-guide/security)).
- Decisão: **definir `terminal.home_mode: profile`** nos perfis de destino criados pelo kit e documentar que a separação de HOME não é sandbox.
- Critério de teste: um subprocesso do perfil de destino **não lê** `.env`, keychain ou credenciais do usuário real (ver §6).

### 5.3 Sudo não interativo
- Preferir usuário não privilegiado sempre que possível.
- Necessário: regras sudoers específicas + `sudo -n`, comandos/argumentos validados, programas auxiliares protegidos contra alteração. `NOPASSWD: ALL` nunca é padrão.
- **Falha fechada**: sem prompt; bloquear e informar, nunca pedir senha no chat.
- No Mac: usar mecanismos apropriados (helper/agente de sessão) sem desbloquear globalmente o chaveiro pessoal.

### 5.4 Superfície não interativa (VPS/gateway) (M3)
- Decisão explícita: no VPS, `cron_mode`/`unattended_mode` negam ações headless perigosas e **penduram** escritas de memória/skills que exijam aprovação (ou usam conjunto pré-aprovado explicitamente), em vez de aplicar sem revisão. Sem esse comportamento verificado, o gateway não inicia.
- Gateway só sobe com autorização separada e credenciais configuradas localmente.

## 6. Critérios de aceitação (testes futuros; nenhum executado)

1. Gatilho inicia entrevista sem ler perfis/hosts não autorizados.
2. Plano enumera arquivos, alias, config, capabilities, serviços afetados.
3. Destino explícito; default e outros perfis intactos.
4. Criação sem skills bundled (`--no-skills`); inventário final == seleção aprovada.
5. Pacote valida frontmatter, paths, auxiliares, deps, zero segredo; fixtures nunca reais.
6. Memória só aplicada após consentimento e dentro do limite real; leitura de volta + sessão nova confirmam.
7. **Retomada valida identidade e vigência de consentimento; ação de criação não repetida se o destino já existir** (lê o destino antes de repetir).
8. Host negado/indisponível, versão incompatível, skill ausente, consentimento expirado, conteúdo em conflito → `BLOCKED` explícito.
9. Sem "bot pronto" sem teste real no destino/superfície escolhidos.
10. Segredo-canário **não** aparece em tool outputs, conversa, logs, histórico, backups, memória (inclui exceções e subprocessos).
11. **Isolamento de SO**: token de um host/SA incapaz de acessar vault de outro; **e** executor em usuário separado não alcança o diretório privado do broker nem credenciais do usuário real (complementa o escopo de SA com isolamento de nível SO — B3).
12. Rotação/revogação exercitada; indisponibilidade **não** causa fallback inseguro.
13. **Reboot sem login humano** (VPS 24/7): broker resolve segredos e volta a funcionar, **ou** falha fechada documentada; sem depender de sessão gráfica desbloqueada.
14. Toda operação `sudo -n` **negada em modo não interativo não solicita senha**, apenas falha e informa (A1).
15. **Conhecimento**: VPS incapaz de ler notas pessoais; reconstrução de índices sem perda da fonte Markdown; restauração de backup testada; escrita concorrente na inbox detectada como conflito e promoção rastreável (A2).
16. Subprocesso do perfil de destino não lê `.env`/keychain do usuário real (C2).

## 7. Incertezas a resolver na implementação

- Versão exata do Hermes e flags (`--no-skills`, `terminal.home_mode`, `write_approval`, `cron_mode`/`unattended_mode`) em cada host; validar com `--help` autorizado.
- Divergências entre skills locais e documentação atual; priorizar o site oficial.
- Disponibilidade/sintaxe do Obsidian Headless (beta), se adotado.
- Permissões e planos reais de 1Password SA / quotas / Connect.
- Comportamento de reinício de helpers de bootstrap no Mac/Linux/VPS.

## 8. Entregas

**Fase 1 (concluída — sem tocar ambiente):**
- ✅ README, .gitignore, LICENSE, repo Git local
- ✅ Relatórios de pesquisa citados
- ✅ PLAN.md revisado (esta v2, com correções da revisão independente)

**Fase 2 (após aprovação do usuário — sem alterar hosts):** esqueleto da skill (`SKILL.md`, references, templates incl. `broker/`, scripts, fixtures fake) + docs.

**Fase 3 (após aprovação de alterações):** piloto no primeiro host com consentimento por etapa, backup e teste real.

**Nenhum perfil, cofre, vault, regra sudo, memória ou host foi alterado; nenhum dado real foi coletado.**
