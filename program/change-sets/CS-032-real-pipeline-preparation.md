# CS-032 — Preparação da pipeline real de AgentKnowledge

**Estado:** AWAITING_APPROVAL  
**Base:** Gate R aprovado em `CS-030-gate-r-data-decision.md`  
**Tipo:** planejamento/documentação; nenhuma criação, acesso ou conteúdo real.

## Objetivo

Definir a pipeline de menor privilégio que poderá, em CS posterior, publicar um subconjunto real explicitamente aprovado de AgentKnowledge para a VPS. Este CS prepara arquitetura, identidades, controles e verificações; não acessa AgentKnowledge nem cria recursos.

## Arquitetura proposta

```text
Fonte AgentKnowledge canônica
  → publicador read-only separado (lado autorizado)
  → filtro positivo + manifest assinado + auditoria
  → repositório/projeção dedicado
  → consumidor VPS read-only + validação online/fail-closed
```

A VPS nunca monta, sincroniza ou recebe credencial do vault pessoal. O repositório contém somente a projeção aprovada, nunca vault, inbox, archive, state.db, homes Hermes, secretos ou transcrições.

## Componentes propostos, ainda não criados

| Componente | Papel / privilégio mínimo | Proibido |
|---|---|---|
| Publicador | identidade técnica read-only sobre o subconjunto que um CS posterior permitir; gera manifest e publica apenas a projeção | editar canônico, promover, alterar ACL, ler fora do allowlist |
| Repositório de projeção | privado, dedicado e sem histórico anterior; uma audiência por repo | vault completo, múltiplos grants, Actions, LFS, forks, dados proibidos |
| Consumidor VPS | identidade técnica read-only; fetch online, valida assinatura/TTL/revisão e só entrega conteúdo válido | push, admin, fallback a cache/vault/sync/credencial alheia |
| Chaves | deploy key por função/repo; chave de assinatura separada | reutilização de chaves pessoais, agent forwarding, tokens no agente |
| Auditoria | eventos sanitizados, fora da projeção, acesso separado do consumidor | payload, segredo, conteúdo de nota, URL autenticada |

## Controles obrigatórios antes de CS-033

1. Identidade de publicador e consumidor separadas, removíveis e com storage protegido.
2. Pin SSH do destino, assinatura externa do manifest e trust anchor fora do repositório.
3. Manifest com `scope`, audiência, sensitivity, revision, TTL, anti-replay, lista exata de arquivos e hash.
4. Filtro fail-closed que exclua por padrão qualquer item sem classificação/proveniência/campo obrigatório.
5. Auditoria sanitizada e rollback que revogue identidades antes de remover recursos.
6. Read-back independente de repo, keys, ref, manifesto e limpeza.

## Não escopo

- Criar conta, usuário, diretório, repo, chave, publisher, consumer, manifest, cron, serviço, sync ou roteamento.
- Ler, listar, buscar, copiar, classificar ou publicar AgentKnowledge.
- Definir o primeiro `scope` real; isso pertence a CS-033 e aprovação posterior.
- Qualquer acesso a vault, credencial, secret store, conteúdo pessoal, GTD/CRM ou Gate R de execução.

## Plano futuro de aplicação

| Fase | Pré-condição | Resultado | Gate posterior |
|---|---|---|---|
| P-0 | CS-032 aprovado e anexo de alvos/identidades preenchido | pipeline técnica pronta para criação | gate de aplicação CS-032 |
| P-1 | pipeline criada e verificada sem conteúdo | evidência de isolamento, assinatura, revogação e rollback | CS-033 documental |
| P-2 | CS-033 com scope/audiência/sensibilidade explícitos | primeira publicação mínima real | gate de publicação CS-033 |

### Decisão registrada — publicador simplificado

**Aprovado pelo usuário em 2026-09-18:** usar `fac` no HomeLab como publicador controlado por script fixo, sem sudo. Essa decisão elimina CS-032A como pré-requisito de P-0, mas reduz o isolamento de SO do publicador. A VPS continua read-only e sem acesso ao vault pessoal.

## Anexo A — recursos e identidades da pipeline

**Estado do anexo:** proposto documentalmente em 2026-09-18; os alvos abaixo não existem por efeito deste CS e não autorizam qualquer acesso ao vault.

| Item | Alvo proposto | Limite vinculante |
|---|---|---|
| Publicador | HomeLab, usuário existente `fac`, script fixo `~/bin/ak-real-publisher` | Sem sudo; script aceita zero argumentos e só poderá ler o subset que CS-033 aprovar. O trade-off é que o publicador compartilha o perímetro de SO de `fac`. |
| Consumidor | VPS Oracle, usuário Linux novo `ak-real-consumer`, raiz `/var/lib/ak-real-consumer` | Só fetch/validação/entrega de projeção válida; sem push, vault, Obsidian, sync, fallback de cache ou credencial alheia. |
| Repositório | privado novo `felipe3d/agentknowledge-vps-projection` | Única audiência/grant; histórico inicialmente vazio; sem Actions, LFS, forks, submodules ou dados até CS-033. |
| Deploy key do publicador | `ak-real-publisher-rw`, privada somente em `/home/fac/.local/share/ak-real-publisher/.ssh/` | Write habilitado somente no repo de projeção; leitura é implícita no Git e não equivale a admin ou acesso a outro repo. |
| Deploy key do consumidor | `ak-real-consumer-ro`, privada somente em `/var/lib/ak-real-consumer/.ssh/` | Read-only, exclusiva do repo, sem agent forwarding, backup automático, token pessoal ou fallback. |
| Assinatura do manifesto | chave Ed25519 nova do publicador em `/home/fac/.local/share/ak-real-publisher/signing/`; âncora pública pinada em `/var/lib/ak-real-consumer/trust/` | Chave privada nunca vai a Git, auditoria, chat ou VPS; a pública vem de canal de provisionamento aprovado, não do repo. |
| Confiança SSH | fingerprint Ed25519 oficial de `github.com`, known_hosts exclusivo de cada papel | `StrictHostKeyChecking=yes`; sem aceitar chave nova automaticamente. |
| Auditoria | HomeLab, `/home/fac/.local/state/ak-real-publisher/audit`, modo 0700 | Fora do repo e inacessível ao consumidor; só IDs, revisão, decisão, hash, TTL, status e reason code — nunca payload/nota/segredo. |
| Retenção | auditoria mínima 30 dias; projeção/repo conforme CS-033, nunca como backup de vault | Purge, retenção de conteúdo e cópias fora do controle exigem política própria. |
| Ref e anti-replay | `refs/heads/production`, revisão monotônica e estado local do consumidor em `/var/lib/ak-real-consumer/state/` | OID/revisão aprovados por read-back externo; downgrade, ref divergente, TTL/assinatura inválidos falham fechados. |

### Sequência futura de aplicação P-0

1. Criar roots/usuários técnicos isolados e verificar UID, grupos, modes, ausência de mounts/sync/home Hermes.
2. Criar repo privado vazio e read-back: owner, privado, integrações desabilitadas e nenhum grant inesperado.
3. Gerar e registrar deploy keys por função; confirmar read-only no consumidor e write limitado ao repo no publicador.
4. Provisionar trust anchor e known_hosts pinado; verificar assinatura de fixture sintética sem AgentKnowledge.
5. Criar validador consumidor fail-closed, auditoria e rotina de rollback; executar P-1 somente com fixture sintética.
6. Revogar keys e remover todas as identidades/roots/repos de P-0 se qualquer read-back divergir.

### Comandos/read-backs exigidos antes de aplicação

O futuro anexo de execução deve fixar, sem placeholders: comandos de criação e remoção por path/usuário exatos; comandos de read-back de usuários, groups, modes, repo, keys, ref, assinatura, TTL e auditoria; resultado esperado de cada teste; e owner da reversão. Nenhum comando pode usar inventário global, shell arbitrário, `sudo` amplo, token pessoal, clone de perfil ou leitura de AgentKnowledge.

### Tabela final P-0 — comandos, baselines e rollback

**Estado:** planejamento documental; nenhum comando desta tabela foi executado. Os comandos usam somente recursos novos enumerados. Como o HomeLab anteriormente exigiu autenticação interativa para `sudo`, P-0 deve parar antes da primeira criação no publicador se não houver canal de operador aprovado; nunca usar `fac`, senha em chat ou NOPASSWD amplo como fallback.

| Passo | Comando/ação futura | Baseline / read-back | Rollback |
|---|---|---|---|
| P0-00 | Em cada host, verificar somente ausência dos usuários `ak-real-publisher`/`ak-real-consumer` e das roots do Anexo A; checar repo exato inexistente | Todos ausentes; colisão bloqueia sem sobrescrever | Cancelar sem mutação |
| P0-01 | Criar `ak-real-publisher` no HomeLab e `/var/lib/ak-real-publisher` 0700, shell nologin; criar `ak-real-consumer` na VPS e `/var/lib/ak-real-consumer` 0700 | `id`, `getent`, `stat` confirmam owner/mode e ausência de grupos privilegiados, mounts/sync/home Hermes | `userdel -r` e `rm -rf` somente nos nomes/paths exatos; preservar auditoria mínima |
| P0-02 | Criar repo privado vazio `felipe3d/agentknowledge-vps-projection`, sem Actions/LFS/forks/submodules | API/read-back confirma owner, privado, vazio e integrações desabilitadas | Remover repo exato após revogar chaves; confirmar ausência |
| P0-03 | Gerar deploy key nova por papel e chave Ed25519 de manifesto; armazenar privadas apenas nas roots técnicas; registrar públicas no repo/trust anchor | `stat` 0600 para privadas, read-back de ID/key no repo, consumidor read-only, publicador limitado ao repo | Revogar ambas as keys, remover privadas/âncora e confirmar negação |
| P0-04 | Pin known_hosts GitHub e trust anchor do manifesto no consumidor; criar validador fail-closed sem AgentKnowledge | Verificar fingerprint, assinatura de fixture sintética, TTL, hash, ref e anti-replay | Remover validador/trust roots exatos após revogar chaves |
| P0-05 | Publicar uma fixture sintética única por pipeline; consumidor fetch online/valida, tentativa push do consumidor deve negar | Read-back de árvore allowlisted, hash/assinatura/TTL válidos, push negado e log sanitizado | Revogar keys, remover repo/roots/usuários, confirmar ausência; nenhum conteúdo real |

### Critérios de parada

Qualquer necessidade de acessar AgentKnowledge, abrir credencial existente, herdar ambiente, listar configuração ampla, executar shell arbitrário, aceitar chave SSH nova, reutilizar chave/conta pessoal ou ignorar um read-back resulta em `BLOCKED`. P0-05 é a última ação deste CS; a seleção de um scope real pertence exclusivamente ao CS-033.

## Aprovação futura

Este CS não autoriza aplicação. Antes de criar a pipeline, a aprovação deverá nomear a revisão, anexo de alvos, recursos, identities, comandos, read-backs e rollback exatos; qualquer conteúdo real continua exigindo CS-033 separado.

## Evidência

P-0 concluído e limpo, incluindo ausência posterior do repo. Ver `program/evidence/CS-032-p0-run.md`.