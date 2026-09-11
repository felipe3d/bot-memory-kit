# Migração de memória: auditoria, classificação e transferência

Como auditar a memória existente e migrar fatos aprovados para os novos bots.

## Princípios

1. **Nada é apagado.** A auditoria classifica; não apaga. O perfil original continua intacto.
2. **Migração por item.** Cada fato tem decisão `aprovar/rejeitar/adiar` com origem e justificativa.
3. **Lista positiva.** Transferência parte de lista aprovada — nunca "copiar tudo e limpar depois".
4. **Testar em sessão nova.** Memória injetada é snapshot do início da sessão; só uma sessão nova prova o efeito.

## Ordem da migração (sempre)

```
BACKUP → INVENTÁRIO → CLASSIFICAÇÃO → APROVAÇÃO → MIGRAÇÃO → TESTE
```

### Atalho: fatos já confirmados na entrevista (warm-start)

Se a entrevista rodou com **warm-start** (cartão de confirmação — ver `templates/interview.md`), os fatos chegam à migração **pré-classificados**:

| Registro no checkpoint | Classificação herdada |
|---|---|
| `known_facts[x].status=confirmed` | aprovado para migração (origem + `verified_at` já registrados) |
| `known_facts[x].status=superseded` | não migra o valor antigo; migra o novo |
| `corrections[y]` | proposta para o canon (inbox do vault) — aprovação separada |
| lacuna preenchida | fato novo, `source: entrevista` |

Nesse caminho, a fase de classificação só precisa julgar o que **não** apareceu na entrevista. A revisão de memória e a entrevista são o mesmo gesto: **o usuário corrige a memória enquanto responde**, em vez de revisar uma tabela seca depois.

### 1. Backup (antes de qualquer coisa)

```bash
cp -r <hermes_home>/memories /backup-dest/memories-$(date +%Y%m%d-%H%M%S)
```

Registrar caminho do backup no checkpoint. Sem backup, a fase não inicia.

### 2. Inventário

Ler e listar (sem expor valores):
- `MEMORY.md` do perfil de origem (limite 2.200 chars) — entradas e tamanho
- `USER.md` (limite 1.375 chars) — entradas e tamanho
- Skills com `created_by: agent` (curador) vs. instaladas do hub

### 3. Classificação

| Categoria | Destino proposto |
|---|---|
| Preferência pessoal estável e consentida | `USER.md` do novo perfil |
| Fato estável do ambiente (qualificado por host/perfil) | `MEMORY.md` do novo perfil |
| Procedimento reutilizável | Skill |
| Conhecimento de domínio | Vault canônico (ver canonical-knowledge.md) |
| Histórico/evidência/justificativas | Dados privados da execução (não migra) |
| Pendência operacional | Controle do projeto |
| Token/senha/cookie/chave | **Nunca** migra |
| Duplicado/possivelmente obsoleto | Sinalizar; revisão humana; não excluir às cegas |

### 4. Limites e escrita

- Limites reais lidos da config do perfil destino (defaults: MEMORY 2.200 / USER 1.375 — podem diferir).
- Overflow gera **erro**, não compactação silenciosa — consolidar no mesmo turno (merge de entradas relacionadas) e re tentar.
- `replace`/`remove` usam substring única; substring ambígua = erro, refinar.
- Duplicado exato é rejeitado pelo Hermes.

### 5. Verificação

1. `memory` tool: adicionar → ler de volta (tool mostra estado vivo)
2. **Sessão nova** no perfil destino → confirmar que a memória aparece no system prompt
3. Conferir limite: header mostra `N/2200 chars`
4. Inventário final == itens aprovados

## O que nunca migra

- Transcrições de sessão (histórico pertence ao perfil de origem)
- `.env`, `auth.json`, tokens OAuth
- Caches, logs, `state.db`
- Conteúdo sensível mencionado em conversa (registrar "[não persistido]")

## Conflitos

Fatos conflitantes não são resolvidos por palpite:
- registrar ambos com origem
- marcar `conflito` no checkpoint
- decisão humana antes da migração
- não transferir afirmação de um host como fato do destino

## Memória do kit vs. memória do Hermes

| O quê | Onde |
|---|---|
| Respostas da entrevista, decisões, pendências | checkpoint + dados privados da execução |
| Fatos aprovados para o novo bot | MEMORY.md / USER.md do novo perfil |
| Conhecimento compartilhável | Vault canônico |
| Estado do kit (fases, consentimentos) | checkpoint (nunca na memória do Hermes) |

O skill **não** grava o progresso do kit na memória nativa do Hermes — o checkpoint é a fonte. A memória nativa do novo perfil recebe somente fatos de domínio aprovados.