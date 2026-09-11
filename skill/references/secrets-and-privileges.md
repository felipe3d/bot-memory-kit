# Segredos e privilégios: cofre, broker e sudo

Como lidar com credenciais e operações privilegiadas em agentes automáticos.

## Princípio central

**A memória informa qual acesso existe; o cofre guarda o segredo; uma ferramenta autorizada o usa sem mostrá-lo ao modelo.**

O skill NUNCA:
- pede senha/token/API key no chat
- grava segredo em checkpoint, memória, skill, log ou artefato
- imprime valor de segredo (nem com redaction desligada)
- usa `--no-masking` do `op run`
- armazena token de Service Account em plaintext

## Arquitetura em camadas

| Camada | Conteúdo | Exemplo |
|---|---|---|
| Catálogo de acessos | serviço, finalidade, referência, agentes autorizados | nota canônica |
| Cofre | valores das credenciais | 1Password (Service Accounts) |
| Executor/broker | usa a credencial, executa a operação | conta de serviço separada |
| Memória do bot | sabe consultar o catálogo | referência `op://`, nunca valor |

## Fluxo quando o bot precisa de um acesso

1. Consulta o catálogo do seu domínio
2. Verifica integração autorizada (referência `op://`)
3. Executa a operação via broker — credencial nunca aparece na conversa
4. Só pede intervenção humana se: ausente, expirada, revogada, ou requer MFA/autorização adicional

**Não vasculha o cofre procurando "qualquer senha que funcione".**

## 1Password Service Accounts (adaptador inicial)

- Autenticação: `OP_SERVICE_ACCOUNT_TOKEN` (CLI ≥ 2.18.0)
- Escopo mínimo: só `read_items`, vaults de automação dedicados
- Permissões/vaults são **imutáveis** — mudar escopo exige nova SA
- SA **não** acessa vaults Personal/Private/Employee/Shared padrão
- Token mostrado uma vez; cópia administrativa no cofre, cópia operacional no storage protegido do host

### Bootstrap unattended (por host)

```
1. Operador cria SA com escopo mínimo (fora do chat)
2. Token operacional → armazenamento protegido do host
   (keychain no Mac; secret store do gerenciador de serviços no Linux)
   NUNCA: plaintext, Git, vault de conhecimento, args visíveis de processos
3. Broker recupera o token só no ambiente do processo `op`
4. Resolve apenas segredos da operação autorizada; retorna status sanitizado
5. Falha fechada: sem token → bloqueia, não faz fallback para conta pessoal
```

`OP_CONNECT_HOST`/`OP_CONNECT_TOKEN` têm precedência sobre o token de SA — o launcher controla esse ambiente explicitamente.

### `op run` — injeção sem exposição

```bash
# refs.env (sem valores reais):
# API_TOKEN=op://automation-homelab/servico/token
op run --env-file=/caminho/refs.env -- /caminho/executor-aprovado
```

Mascaramento de stdout/stderr é padrão. **Mas mascarar não é sandbox** — o subprocesso recebe o valor. Por isso o executor roda em conta separada (abaixo).

## Broker/executor isolado (obrigatório para autonomia)

```
Agente (sem credenciais)
  → operação tipada e autorizada
  → broker em CONTA DE SISTEMA SEPARADA
  → bootstrap → cofre → segredo só no executor
  → API de destino
  → resultado filtrado para o agente
```

Regras:
- Agente **não** lê/modifica: diretório do broker, executável, allowlist, templates, config do launcher
- Broker aceita **operações fixas** com argumentos validados — nunca shell arbitrário, `op://` arbitrário ou URL livre do modelo
- Egress de rede limitado; sanitizar stdout, temporários, crash dumps
- Auditoria: operação, identidade, horário, resultado — **nunca valor**
- Mesmo usuário do SO = separação destruída

## Sudo não interativo

1. **Preferir usuário sem privilégio.** Serviços de usuário não precisam de sudo.
2. **Necessário:** regras sudoers específicas + `sudo -n`:
   - comandos e argumentos exatos (`/usr/bin/systemctl restart meu-servico`, não `systemctl *`)
   - script auxiliar protegido: root-owned, não editável pelo usuário do agente (script editável = shell root arbitrário)
   - **nunca** `NOPASSWD: ALL` como padrão do kit
3. **Falha fechada:** `sudo -n` sem autorização → falha imediata, sem prompt; bloqueia e informa; nunca pede senha no chat
4. Regra de consistência: se o agente pode editar o arquivo que o sudo executa, a regra sudo é inútil

## Apple Passwords / Keychain (alternativa supervisora)

- App **Senhas** ≠ keychain file-based ≠ Data Protection keychain
- CLI `security` cobre principalmente file-based; Data Protection exige contexto de login + entitlements
- **Sem** contrato headless unattended equivalente a Service Accounts — usar como **supervisado** no Mac apenas
- Não desbloquear keychain globalmente para eliminar prompts

## Provedores alternativos (kit é provider-agnostic)

| Provedor | Nota |
|---|---|
| 1Password | adaptador inicial recomendado (Service Accounts) |
| Bitwarden | cofre pessoal; automação via Secrets Manager — verificar plano |
| Apple | supervisório apenas (acima) |
| Arquivo protegido `chmod 600` | última opção; não protege contra mesmo usuário; documentar risco |
| OAuth/SSH keys/machine identity | preferir quando o serviço suportar — credencial dedicada > senha pessoal |

## Testes obrigatórios (antes de liberar automação)

1. Reboot sem login humano → broker resolve, **ou** falha fechada documentada
2. Sem rede → bloqueia, não fallback inseguro
3. Expiração/revogação/rotação → erro claro, sem loop infinito
4. Segredo-canário não aparece em: tool outputs, conversa, logs, histórico, backups, memória, exceções, subprocessos
5. Token do host A não acessa vault do host B (tentativa negada com fixtures)
6. `sudo -n` negado → sem prompt, mensagem clara
7. Broker: shell arbitrário, `op://` fora da allowlist, URL livre → **negado**