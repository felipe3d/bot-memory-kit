# Interview Guide

## Warm-start: revisão de memória durante a entrevista

Quando o perfil atual **já tem memória** (USER.md/MEMORY.md injetados no system prompt) e/ou acesso autorizado ao vault, a entrevista **não recomeça do zero** — ela confirma e corrige:

1. **Cartão de confirmação antes do Bloco 1**: "Isto é o que já sei sobre você: [lista de fatos com origem e data]. Confirme ou corrija o que estiver errado."
2. **Perguntas viram confirmações**: "Você é o Felipe, fotógrafo, e a Foca é sua empresa? Corrija qualquer detalhe." — sempre com **opção explícita de correção**, nunca pergunta sim/não que force o "sim".
3. **Perguntas abertas somente para lacunas** — o que não está em memória.

### Ledger de fatos (cada resposta tem um destino)

| Resultado da confirmação | Registro no checkpoint (`known_facts`/`corrections`) |
|---|---|
| **Confirmado** | valor mantido; `verified_at` atualizado |
| **Corrigido** | valor novo entra; valor antigo → `superseded` (nunca apagado) |
| **Obsoleto** | não é mais verdade → arquivado com referência cruzada |
| **Lacuna** | resposta vira fato novo com `source: entrevista <data>` |

Correções de canon (USER.md original, vault) entram como **propostas** (`corrections[]` no checkpoint → inbox do vault), aplicadas com aprovação — a entrevista **não** edita a memória do perfil original sozinha.

### Guardrails

- **Fatos de identidade/contexto** (quem, o quê, onde, ferramentas) podem ser confirmados de memória.
- **Blocos 4 e 5** (privacidade, aprovação, autonomia, tolerância a custo) **não são confirmados de memória** — perguntas sempre abertas: eles definem os limites dos **novos** bots; assumir limites herdados do sistema antigo é perigoso.
- Nunca citar segredos no cartão de confirmação (nem valores, nem "você tem a chave X?" — só o catálogo, sem valores).
- Fato confirmado registra `source` e `verified_at` — "estava na memória" não é verdade, é hipótese até o usuário ratificar.

## Block 1: Life and responsibilities

1. "Como você dividiria sua vida hoje em grandes áreas de responsabilidade e interesse?"
2. "Quais dessas áreas ocupam mais tempo? E quais você gostaria de dedicar mais?"
3. "Você trabalha sozinho, em equipe, ou com clientes diretamente?"
4. "Quais projetos paralelos você mantém?"

## Block 2: Routines and difficulties

5. "O que se repete na sua rotina e consome tempo desnecessário?"
6. "O que costuma atrasar ou exigir que você lembre de detalhes?"
7. "O que você gostaria de delegar para um assistente de IA?"
8. "Existem tarefas que você faz em horários fixos ou que dependem de disponibilidade 24/7?"

## Block 3: Information and tools

9. "Onde cada atividade acontece: Obsidian, arquivos, e-mail, calendário, sistemas, sites?"
10. "Quais fontes são confiáveis e quais estão desorganizadas?"
11. "Quais ferramentas você usa no dia a dia (aplicativos, terminais, navegadores)?"

## Block 4: Autonomy, audience, and privacy

12. "Quem usaria cada agente — só você, sua equipe, ou clientes diretamente?"
13. "O que cada agente poderia ler, preparar, alterar, enviar ou contratar?"
14. "O que exige sua aprovação explícita antes de executar?"
15. "O que não pode sair do computador ou ser enviado a um provedor externo?"

## Block 5: Desired experience

16. "Você prefere falar com um assistente central que encaminha, ou diretamente com especialistas?"
17. "Quais atividades deveriam ser sob demanda versus proativas (notificações, rotinas)?"
18. "Qual sua tolerância a custo de API e manutenção?"

## Rules

- ONE question at a time. Wait for the answer.
- Save each Q&A to `checkpoint.json` immediately after the answer.
- If resuming, skip already-answered questions.
- Adapt follow-ups based on previous answers.
- Never ask for passwords, API keys, or credentials — those are configured separately.
- **Warm-start**: use existing memory/vault as confirmable hypothesis (cartão de confirmação), never as assumed truth — see Warm-start section above. Blocks 4–5 are always open questions.