# VERIFY completo — resultado (2026-09-11, ~02:48)

## Setup do teste

1. **Operador** (eu, fora do skill) configurou credencial do ollama-cloud nos perfis foca/infra do sandbox: `config set model.provider ollama-cloud` + `model.default glm-5.3` — credencial **via env**, nunca gravada em arquivo (T11).
2. Skill informada de que o bloqueio T7 foi resolvido → re-executou VERIFY completo (T1–T16) e registrou os resultados no checkpoint (`bmk-backups/checkpoint.json`, 9.378 bytes, `phase: COMPLETE`, lock removido).

## Resultado: T1–T16 = 16/16 pass

| Teste | Resultado registrado pelo skill (resumo) |
|---|---|
| T1 gatilho controlado | pass — só avançou com gatilhos explícitos |
| T2 plano completo | pass — PLAN.md enumerava tudo antes do APPLY |
| T3 destinos isolados | pass — default (55 skills) e botx intactos |
| T4 seleção positiva | pass — foca: 3 skills aprovadas; infra: 2 aprovadas |
| T5 pacote íntegro | pass — zero segredos em memories/config/checkpoint |
| T6 memória consentida | pass — dentro dos limites (foca 1099B, infra 1109B) |
| T7 sessão nova confirma | pass — foca: "nunca enviar mensagem a cliente"; infra: "somente leitura" (validado por mim fora do skill) |
| T8 idempotência | pass — `profile create` recusa already-exists; zero duplicatas |
| T9 retomada sem transcript | pass — checkpoint recriado do estado real |
| T10 bloqueios legítimos | pass — credencial ausente bloqueou T7 com motivo, sem contorno |
| T11 sem canário | pass — nenhum valor de segredo jamais manipulado |
| T12 falha fechada sudo | pass — exit 127 imediato, sem prompt |
| T13 broker isolado | pass — n/a (MVP sem automação de credenciais) |
| T14 isolamento conhecimento | pass — foca/infra não veem skills um do outro |
| T15 backup/restauração | pass — bmk-backups/profiles-20260911-024807; diff vazio |
| T16 sem pronto sem teste | pass — COMPLETE só com T1-T16 executados |

## Correção do próprio skill durante o VERIFY

**T4 encontrou divergência real**: `hermes-agent` auto-semeado no foca (fora da seleção aprovada de 3 skills). O skill moveu para **quarentena reversível** `bmk-backups/quarantine-foca-hermes-agent` (mv de volta restaura) em vez de deletar — exatamente a política "nada apagado às cegas".

## Achado residual corrigido fora do skill

Duplicação aninhada `email/himalaya/himalaya/` no foca (efeito de `cp -r` malfeito na instalação da skill) — removida manualmente; inventário final limpo:

```
foca:  email/email-inbox-triage, email/himalaya, note-taking/obsidian (+hermes-agent builtin)
infra: autonomous-ai-agents/hermes-agent, software-development/systematic-debugging
```

## Nota de honestidade

- O campo `verification_results` do checkpoint registra `pass — <evidência>` como texto do skill, mas o parser que usei contou 0 no formato anterior; a evidência textual está íntegra (lista acima).
- T7 foi validado **por mim (operador)** no destino real — o skill não pode reproduzir sessão nova com a credencial (env-scoped ao shell do dono, por design). Isso é o comportamento correto do critério T7.
- T12/T13 são parciais no container (sem sudo/broker por design do MVP); o teste real desses roda no host-alvo.

## Estado final do sandbox

- `phase: COMPLETE`, 17 steps, lock removido, backup pós-implantação `bmk-backups/profiles-20260911-024807`
- Bot dev (3º proposto na entrevista) registrado como deferred — retomável com "retomar bot-memory-kit"
- Uso: `hermes -p foca chat` / `hermes -p infra chat` (dentro do container com env)