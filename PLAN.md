# Plano de Implementação — bot-memory-kit (revisado)

Data: 2026-09-10 · Fase: PLAN_READY (aguardando aprovação para implementar)
Base: `hermes-research.md` + `memory-secrets-research.md` (fonte citada [1] [2] [3]… = relatórios)

Princípio central desta revisão: **o kit é uma skill orquestradora + templates + scripts, com dados privados por execução e nenhuma alteração de ambiente sem aprovação.** O Hermes já fornece perfis, seleção de skills, aprovação de memória e retomada; o kit adiciona gating de intenção, consentimento multi-host, curadoria item a item, checkpoints semânticos e segurança de segredos.

## 0. Decisões de escopo (MVP)

- **Não usar clonagem de perfil como padrão.** `--clone` copia `.env`; `--clone-all` copia memórias mas exclui histórico/cron. Toda migração parte de lista positiva aprovada, sem copiar `.env`, `auth.json`, caches, logs ou diretórios inteiros.
- **Criar perfis com `hermes profile create NOME --no-skills`** e selecionar skills positivamente.
- **Obsidian/Markdown canônico** para conhecimento compartilhável aprovado; memórias Hermes locais como índices/resumos derivados.
- **Segredos: 1Password Service Accounts** como adaptador inicial (host→função→vault), com broker isolado. Nunca valores em chat/artefatos/memória. Apple Passwords/Keychain documentados como alternativas supervisoras, não base multiplataforma.
- **Privilégios:** operações aprovadas com `sudo -n` + regras específicas; falha fechada, sem senha armazenada nem `NOPASSWD: ALL` universal.
- **Estado persistente** em checkpoint próprio + journal idempotente, independente do transcript.
- Gatilho explícito: `/bot-memory-kit` (iniciar/retomar/consultar). Menção casual a "memória" não inicia nada.

## 1. Estrutura alvo do kit

```text
~/dev/bot-memory-kit/
├── README.md
├── PLAN.md                 (este arquivo)
├── hermes-research.md     (pesquisa citada)
├── memory-secrets-research.md
├── skill/                  (conteúdo instalável da skill Hermes)
│   ├── SKILL.md
│   ├── references/
│   │   ├── consent-and-discovery.md
│   │   ├── selection-and-safety.md
│   │   ├── memory-migration.md
│   │   ├── secrets-and-privileges.md
│   │   └── resume-protocol.md
│   ├── templates/
│   │   ├── interview.md
│   │   ├── execution-manifest.json
│   │   ├── checkpoint.json
│   │   └── approval-plan.md
│   └── scripts/
│       ├── discover.py
│       ├── validate_manifest.py
│       ├── validate_checkpoint.py
│       └── scan_artifacts.py
├── docs/                   (guias de manutenção, segurança, multi-host)
└── tests/fixtures/          (somente dados fake, nunca dados reais do usuário)
```

Dados privados por execução (respostas, inventário, credenciais) vivem **fora** deste repo, em diretório privado gitignored/separado.

## 2. Fluxo de etapas do kit

```text
INTENT (gatilho explícito)
  → INTERVIEW (adaptativa; salva apenas respostas aprovadas)
  → CONSENT_PER_HOST (antes de qualquer descoberta)
  → DISCOVERY (somente leitura; metadados e capacidades, não conteúdo de segredos)
  → SELECTION (skills, toolsets, MCPs, memória por item, fontes)
  → ARCHITECTURE (bots, host proprietário, conhecimento canônico, topologia)
  → PLAN_READY (manifesto + plano de aprovação → aprovação humana)
  → APPLY (backup → implantação idempotente por passo → verificação)
  → VERIFY (testes de aceitação no destino real)
  → COMPLETE / BLOCKED / PAUSED
```

Regras de fluxo:
- Consentimento por host antes de ler; cada classe de operação precisa de autorização separada (descobrir metadados ≠ ler conteúdo ≠ persistir ≠ transferir ≠ configurar credenciais).
- Cada transição é persistida atomicamente; intenção antes da ação, resultado verificado depois.
- Interrupção: ler o destino antes de repetir; idempotente, sem exactly-once presumido sem teste.
- Mudança de escopo exige nova aprovação.

## 3. Componentes e responsabilidades

| Componente | Faz | Não faz |
|---|---|---|
| `SKILL.md` | Coordena fases, carrega referências, respeita gates | Não lê/migra sem intenção explícita |
| `reference/*.md` | Orientações por tópico carregadas sob demanda | — |
| `templates/*.json` | Manifesto, checkpoint, plano de aprovação padronizados | Não guarda segredos |
| `scripts/discover.py` | Inventário somente leitura autorizado; detecta gerenciadores de credenciais sem abrir conteúdo | Não varre rede, não lista segredos, não lê vaults |
| `scripts/validate_*.py` | Valida schema, integridade, idempotência, fronteiras | Não executa ações externas |
| `scripts/scan_artifacts.py` | Verifica ausência de segredos-canário em artefatos | Não substitui varredura de segurança completa |
| `tests/fixtures/` | Dados fake para validar fluxo/testes | Nunca dados reais do usuário |

## 4. Descoberta de segredos e credenciais

Fase `DISCOVERY` deve detectar **presença/ausência e versão**, nunca valores:
- 1Password CLI (`op --version`), presença de Service Accounts/Connect (sem listar vaults por padrão, sem abrir itens);
- Senhas da Apple / Keychain (presença de aplicativo e utilitário `security`; sem `find-generic-password` sem autorização explícita e escopo);
- Bitwarden/outros gerenciadores instalados;
- variáveis de ambiente de automação relevantes (só nomes, jamais valores);
- helpers de bootstrap (Keychain file-based, secret store do gerenciador de serviços).

Regra dura: **nenhum segredo em artefatos, checkpoints, memória, skills ou relatórios.** Usar referências `op://` com aliases públicos, mapeamento por host fora do chat.

### Bootstrap unattended (proposta, a validar no host)
1. Operador cria Service Account com escopo mínimo; guarda cópia administrativa no 1Password.
2. Provisiona cópia operacional no armazenamento protegido do host (fora de Git/Vault/prompt/histórico).
3. Launcher/broker recupera o token só para o processo `op`; não expõe ao executor final.
4. Resolver apenas segredos da operação autorizada; retornar status sanitizado.
5. Testar reboot, ausência de login humano, indisponibilidade, expiração, revogação, rotação. Falha fechada.

## 5. Privilégios administrativos

- Preferir usuário não privilegiado sempre que possível.
- Para o necessário: regras sudoers específicas + `sudo -n`, comandos e argumentos validados, programas auxiliares protegidos contra alteração.
- `NOPASSWD: ALL` nunca é padrão do kit.
- Falha imediata sem prompt; bloquear e informar, não pedir senha no chat.
- No Mac: usar os mecanismos apropriados (Keychain helper/agente de sessão) sem promover desbloqueio global do chaveiro.

## 6. Critérios de aceitação (testes futuros)

1. Gatilho inicia entrevista sem ler perfis/hosts não autorizados.
2. Plano enumera arquivos, alias, config, capabilities, serviços afetados.
3. Destino explícito; default/outros perfis intactos.
4. Criação sem skills bundled; inventário final == seleção aprovada.
5. Pacote valida frontmatter, paths, auxiliares, deps, zero segredo; fixtures nunca reais.
6. Memória só aplicada após consentimento e dentro do limite; leitura de volta + sessão nova confirmam.
7. Checkpoint sobrevive interrupção; retomada sem transcript; repetição idempotente.
8. Host negado/indisponível, versão incompatível, skill ausente, consentimento expirado → bloqueio explícito.
9. Sem "bot pronto" sem teste real no destino/superfície escolhidos.
10. Segredo-canário não aparece em tool outputs, conversa, logs, histórico, backups ou memória.
11. Token de um host incapaz de acessar vault de outro; tentativa negada verificada com fixtures.
12. Rotação/revogação exercitada; indisponibilidade não causa fallback inseguro.

## 7. Incertezas a resolver na implementação (não nesta fase)

- Versão exata do Hermes e `--no-skills`/flags em cada host (validar com `--help` autorizado).
- Divergências entre skills locais e documentação atual (perfil de criação, default de aprovação).
- Disponibilidade e sintaxe do Obsidian Headless (beta), se adotado.
- Permissões e planos reais de 1Password Service Accounts / quota.
- Comportamento de reinício de helpers de bootstrap no Mac/Linux/VPS.

## 8. Entregas imediatas (Fase 1 — sem tocar ambiente)

1. ✅ README + .gitignore + repo Git local
2. ✅ Relatórios de pesquisa citados
3. ✅ Este PLAN.md revisado
4. ⏳ Revisão independente do plano (subagente) + correções
5. ⏳ Aprovação do usuário
6. → Fase 2: esqueleto da skill (`SKILL.md` + references/templates/scripts + fixtures) no repo
7. → Fase 3 (após aprovação de alterações): piloto no primeiro host

**Nenhum perfil, cofre, vault, regra sudo, memória ou host foi alterado; nenhum dado real foi coletado.**
