# CS-035 — publicação AgentKnowledge para VPS pessoal

**Estado:** VERIFIED
**Data:** 2026-09-21
**Autorização:** proprietário autorizou publicar o AgentKnowledge inteiro para a VPS, com consumo read-only.

## Decisão

O AgentKnowledge do Mac (vault Obsidian) é sincronizado para a VPS via repo Git bare. A VPS faz pull read-only; o Mac é a origem canônica. Todos os subdiretórios (canonical, inbox, archive, projections) são publicados — o Hermes da VPS é pessoal do proprietário, não compartilhado.

## Arquitetura

```
Mac (origem canônica)
  /Users/fac/dev/Obsidian/felipe/AgentKnowledge/  (repo Git, branch main)
    ↓ git push
VPS (ubuntu@137.131.137.124)
  ~/ak-sync.git  (bare repo)
  ~/AgentKnowledge/  (clone read-only, pull only)
  ~/.hermes/skills/personal-learning/SKILL.md  (procedimento de consulta)
```

- Sem deploy keys de GitHub, sem intermediário externo.
- SSH já autorizado (chave Oracle no agent do Mac).
- Sem credenciais copiadas; o AgentKnowledge não contém segredos.

## Verificado

- Bare repo criado em `~/ak-sync.git` na VPS.
- AgentKnowledge inicializado como repo Git no Mac, commit com 15 arquivos.
- Push Mac → VPS funcionando (`4dda040`).
- Clone na VPS em `~/AgentKnowledge/` com branch `main` ativa.
- `git pull` na VPS retorna `Already up to date`.
- Skill `personal-learning` instalada no default da VPS com paths ajustados.
- Nota canônica `AK-CS034-d162c634a1c24dd8` acessível na VPS.

## Limites

- A VPS não faz push nem commit; é consumidora read-only.
- O helper `cs034_personal_learning.py` não está instalado na VPS; as operações de propose/decide/revise ficam no Mac.
- Sem cron de sync automático; o pull é manual (`git pull` na VPS ou ssh remoto).
- Não testa isolamento de SO nem exposição a terceiros — o Hermes da VPS é pessoal.

## Rollback

Para reverter: remover `~/AgentKnowledge/` e `~/ak-sync.git` na VPS, remover a skill `personal-learning` da VPS, e remover o remote/`.git` do AgentKnowledge no Mac (ou manter sem push).