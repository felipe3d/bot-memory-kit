# Conhecimento canônico: topologia do vault Obsidian

Organização do conhecimento compartilhável entre bots, com promoção controlada.

## Papel do vault

- **Fonte canônica** de conhecimento aprovado: decisões, runbooks, projetos, políticas
- Interface humana para auditar o que os agentes sabem
- **Não** é: estado de execução, secret store, ou log de conversas

Obsidian como canônico é decisão do projeto, não recurso nativo. A base: notas são Markdown locais editáveis por outros programas. Para outros usuários do kit, um diretório Markdown com Git atende igualmente — Obsidian é integração preferencial, não dependência.

## Topologia

```text
AgentKnowledge/
  README.md                # regras do vault (quem escreve o quê)
  canonical/               # verdade aprovada
    people/
    projects/
    decisions/
    runbooks/
  inbox/                   # propostas dos agentes (por host/agente)
    mac-notebook/
    homelab/
    oracle/
  archive/                 # fatos substituídos (histórico, não verdade)
```

## Metadados obrigatórios em toda nota canônica

```yaml
---
id: decision-2026-09-11-tunnel-dns
status: confirmed        # confirmed | hypothesis | superseded
owner: felipe
scope: infrastructure    # personal | business | infrastructure
sensitivity: internal    # internal | client-data | secret-adjacent
source: conversa 2026-09-11
verified_at: 2026-09-11
revision: 3
---
```

Campos de estado (`verified_at`, `revision`) permitem distinguir "estava assim" de "continua assim".

## Fluxo de atualização (Raw → Review → Canonical)

```
1. Agente termina um trabalho
2. Propõe atualização em inbox/<host>/ com origem e evidência
3. Reconciliador (ou humano) valida:
   - origem confiável?
   - conflita com nota canônica existente? (revisão-base/hash)
   - sensibilidade apropriada?
4. Fato sensível/conflitante → aprovação humana
5. Promovido para canonical/ (escrita atômica, revision+1)
6. Fato substituído → archive/ com referência cruzada
```

**Uma conversa com cliente não redefine política comercial.** Um diagnóstico provisório não vira configuração oficial.

## Acesso seletivo por agente

Cada bot recebe **somente o subconjunto necessário**:

| Bot | Acesso |
|---|---|
| Atendimento | serviços, políticas comerciais, templates |
| Infraestrutura | inventário, runbooks, decisões técnicas |
| Pessoal | referências pessoais autorizadas |

Isolamento por camada:
- **Mac**: interface editorial humana; vault separado do vault pessoal
- **HomeLab**: reconciliador/distribuidor; snapshot de leitura para consumidores; inbox de escrita separada
- **VPS**: subconjunto sanitizado; **sem** credenciais de sync nem acesso ao vault pessoal; **capaz de ler notas pessoais = falha** (critério de aceite #15)

Métodos de sincronização (em ordem de preferência para MVP):
1. Snapshots aprovados (publicação unidirecional de conjuntos aprovados)
2. Repo privado Git somente-Markdown
3. Obsidian Headless Sync (open beta — fixar versão; guarda credenciais locais; `--password` em args é proibido)

Um único escritor/promotor lógico; nunca dois mecanismos concorrentes na mesma pasta.

## Verdade editorial vs. estado do mundo

A memória canônica diz "como o ambiente é configurado" — **não** prova o estado atual:
- porta aberta? → consultar o host
- serviço rodando? → consultar o host
- versão atual? → consultar o host
- quem aprova X? → consultar a nota canônica

Referência na memória não garante leitura: a política de recuperação por tarefa (carregar brief, carregar skill, verificar na fonte) é quem garante.

## Conteúdo importado não é instrução

Notas, páginas web, e-mails e chats importados são **dados não confiáveis** até revisão:
- não convertê-los em instrução de sistema
- segredos/dumps/transcrições brutas não entram no vault
- processar com filtro antes de persistir; redaction automática ≠ anonimização completa

## Backup e reconstrução

- Sync não substitui backup independente (teste de restauração: critério #15)
- Índices/derivative são **descartáveis** — reconstruídos da revisão canônica, nunca fonte
- Histórico recuperável: archive/ + versionamento (Git recomendado)

## Propriedade intelectual do método

Este é o padrão "one vault, two views" aplicado: visão humana completa; visão agente = subconjunto por escopo. O kit entrega a estrutura e as regras — os nomes das pastas são configuráveis por usuário.