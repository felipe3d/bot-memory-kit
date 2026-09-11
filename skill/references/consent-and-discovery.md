# Consentimento e descoberta multi-host

Protocolo de autorização por máquina e descoberta somente leitura do ambiente.

## Princípio central

**O consentimento acontece ANTES da descoberta, não depois.** Nenhuma leitura de host acontece sem escopo aprovado e consentimento por máquina registrado no checkpoint.

## Hierarquia de autorizações (nunca agrupar)

Cada classe exige autorização separada e explícita:

| Classe | O que autoriza | Registro no checkpoint |
|---|---|---|
| `metadata_only` | Listar perfis, skills, versões, capacidades | `consent[host].metadata_only = true` |
| `read_selected` | Ler conteúdo de arquivos/pastas específicos aprovados | `consent[host].read_selected = [paths]` |
| `apply_selected` | Criar/modificar os itens selecionados | `consent[host].apply_selected = [items]` |
| `configure_credentials` | Configurar referências de segredos | `consent[host].secrets = true` |
| `start_services` | Iniciar gateway/cron/serviço | `consent[host].services = true` |

**Nunca:** "descobrir" ≠ "ler conteúdo" ≠ "persistir" ≠ "transferir" ≠ "configurar credenciais" ≠ "iniciar serviços".

## Registro do consentimento

```json
{
  "consent": {
    "homelab": {
      "granted_at": "2026-09-11T10:00:00",
      "scope": "metadata_only",
      "expires_at": "2026-09-11T18:00:00",
      "revocable": true
    }
  }
}
```

Regras:
- Consentimento expira (sugestão: 8h). Expirado → `BLOCKED`, pedir de novo.
- Revogável a qualquer momento; o skill deve checar a cada fase.
- Host indisponível → `BLOCKED` com motivo; **não** ampliar escopo nem usar caminho alternativo.

## Descoberta: o que é permitido

**Fase `DISCOVERY` com `metadata_only`:**
- `hermes --version`, `hermes profile list`, `hermes skills list` (por perfil)
- Presença de ferramentas: `op --version` (1Password), `security` (macOS), `docker --version`
- Presença de env vars de automação (**nomes apenas, jamais valores**)
- Caminhos de config: `hermes config path`

**Nunca na descoberta:**
- Ler `.env`, `auth.json`, keychain, vaults, cookies, histórico
- `op item get`, `security find-generic-password`, qualquer leitura de valor secreto
- Varredura de rede além do host autorizado
- Enumerar perfis/contas/diretórios fora do escopo aprovado

## Fluxo por host

```
1. ESCOPO aprovado (fase SCOPE_APPROVED)
2. Para cada host informado pelo usuário:
   a. Perguntar: "Posso inspecionar <host> (somente leitura, metadados)?"
   b. Registrar consentimento + validade
   c. Executar descoberta metadata_only
   d. Se precisar ler conteúdo: pedir read_selected com lista específica
3. Host indisponível: registrar BLOCKED[host], continuar com os demais
   (nunca usar outro host como fallback sem autorização)
```

## Descoberta por máquina (topologia)

O kit nunca presume que o que existe no host A existe no host B. Para cada host:
- Versão do Hermes instalada
- Perfis existentes e seus nomes
- Skills instaladas por perfil
- Provider/modelo configurado
- Gerenciadores de credenciais detectados (presença, não conteúdo)
- Disponibilidade (24/7 vs. suspensível) — **perguntar ao usuário**, não inferir

## Registro das respostas

Toda resposta do usuário sobre consentimento vai para `checkpoint.consent[host]`, com timestamp. A entrevista **não** registra dados sensíveis — se o usuário mencionar um segredo verbalmente, o skill registra "[revelado em conversa; não persistido]" e segue.

## Falha fechada

Se qualquer verificação de consentimento falhar, o resultado é:
- fase → `BLOCKED`
- `blocked_reason` → string clara do que falta
- **nunca** pedir senha/token no chat para contornar
- **nunca** prosseguir com "aproximadamente o mesmo" caminho de acesso