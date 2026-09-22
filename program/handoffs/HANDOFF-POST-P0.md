# Handoff — pós P-0 / preparação para CS-033

**Estado:** P-0 do CS-032 foi `VERIFIED` e limpo. Nenhum AgentKnowledge, nota, vault ou dado real foi acessado/publicado.  
**Última evidência:** `program/evidence/CS-032-p0-run.md` confirma pipeline sintética, revogação e ausência posterior do repo.

## Concluído

- Arquitetura e controles de Gate R aprovados documentalmente.
- CS-031 provou o perímetro de sonda sintética N-01/N-02 e removeu a sonda.
- P-0 validou pipeline vazia: `fac` como publicador HomeLab sem sudo, consumidor VPS read-only, manifesto assinado, push deny, revogação e limpeza.
- O repo de teste foi removido; não há deploy key, usuário técnico, root de consumidor ou material de chave de P-0 remanescente.

## Não provado / não autorizado

- Nenhuma nota real, `scope` real, conteúdo do vault ou projeção real.
- Separação de SO do publicador: o usuário aprovou `fac` como compromisso de simplicidade; a VPS continua sem vault/sync.
- CS-033, qualquer seleção de dados e toda publicação real.

## Processo a partir daqui — reduzir solicitações ao usuário

O usuário quer menos interrupções. A próxima sessão deve agrupar decisões e pedir **um único pacote de aprovação**, em vez de uma cadeia de perguntas pequenas:

1. preparar CS-033 e seu anexo completo sem acessar conteúdo;
2. reunir no mesmo documento o `scope` proposto, audiência, sensibilidade, volume máximo, TTL, seleção positiva, manifest, auditoria, rollback, testes e comandos/read-backs;
3. pedir uma aprovação única para aplicar a primeira publicação mínima real;
4. dentro de um gate aprovado, executar autonomamente todos os passos reversíveis, retries de conectividade, verificação e cleanup; só interromper por divergência de escopo, acesso a conteúdo não autorizado, privilégio novo, dado sensível, ação externa irreversível ou falha sem rollback seguro.

Não reabrir gates concluídos nem pedir confirmação para operações já explicitamente incluídas no gate atual.

## Próximo passo único

Abrir sessão de planejamento de CS-033 com o prompt `program/handoffs/SESSION-PROMPT-CS-033.md`. Sem acesso a AgentKnowledge até o pacote de aprovação final.
