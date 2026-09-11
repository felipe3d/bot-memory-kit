# Seleção de skills, ferramentas e MCPs + segurança

Como selecionar capacidades por bot, com verificação e gates de segurança.

## Seleção positiva (nunca negativa)

A seleção é **lista positiva aprovada**: parte de zero e adiciona somente o necessário.

```bash
# Correto: cria sem catálogo e instala itens aprovados
hermes profile create <nome> --no-skills
hermes -p <nome> skills install <skill-id>   # um por vez, após aprovação
```

**Nunca:** clonar perfil existente (`--clone` copia `.env`; `--clone-all` copia memórias) e "remover depois".

## Catálogo por bot

Para cada skill/ferramenta/MCP selecionado, registrar no `selected_items` do checkpoint:

```json
{
  "id": "skill:foca-ops",
  "name": "foca-ops",
  "origin": "hub|local|inline",
  "version_or_hash": "…",
  "dependencies": ["himalaya"],
  "justification": "rascunhos de atendimento via e-mail",
  "approved_by_user": true
}
```

Verificar antes de declarar completo:
- auxiliares referenciados (`references/`, `templates/`, `scripts/`) instalados
- dependências externas presentes (binários, chaves)
- inventário final **==** seleção aprovada (critério de aceite #4)

## Skills e ferramentas são eixos independentes

Conhecimento não habilita capacidade:
- **Skill** = procedimento (como fazer)
- **Toolset** = poder executável (o que pode fazer)
- **MCP** = acesso a serviço externo

Um bot com skill de infra mas sem terminal não executa diagnósticos. Um bot com terminal irrestrito não precisa de skill para ser perigoso. Selecionar os dois eixos separadamente.

## Gate de modelo por fase (obrigatório antes de APPLY)

O skill lê `model.default` do perfil ativo e emite aviso por fase:

| Fase | Mínimo aceitável | Se abaixo |
|---|---|---|
| INTERVIEW / planejamento | qualquer razoável | segue |
| Curadoria item a item | razoável + aprovação humana por item | segue com gate |
| **APPLY** | glm-5.3 ou superior | **AVISA e recomenda troca** |
| Revisão crítica | modelo forte (Opus/Pro) | recomenda |

Modelos recomendados para APPLY (em ordem):
1. `glm-5.3` (default do kit, validado em sandbox/produção)
2. `nemotron-3-ultra`, `kimi-k3`, `qwen3.5:397b` (Ollama Cloud)
3. `claude-sonnet-4` / `claude-opus` (Anthropic, se `ANTHROPIC_API_KEY`)
4. `gpt-5.x`/`o3` (OpenRouter/OpenAI, se `OPENROUTER_API_KEY`)
5. `gemini-3-pro` (se `GEMINI_API_KEY`)

Se o modelo ativo não está mapeado → **pedir confirmação** ao usuário, não assumir.

## Política de aprovação do perfil criado

Todo perfil criado pelo kit recebe:

```yaml
memory:
  write_approval: true      # escritas de memória passam por aprovação
skills:
  write_approval: true      # alterações de skills em staging
approvals:
  mode: manual              # comandos perigosos sempre pedem
security:
  redact_secrets: true      # padrão, não desativar
```

E **sem** YOLO, cron automático, publicação ou gateway como efeito colateral. Gateway só com autorização separada (`consent[host].services`).

## Não confundir com sandbox

- `write_approval` cobre a ferramenta `memory`/`skill_manage`, **não** terminal ou `write_file` arbitrários.
- `terminal.home_mode: profile` separa o `HOME` dos subprocessos, **não** é contenção de SO.
- `HERMES_WRITE_SAFE_ROOT` limita `write_file`/`patch`, **não** comandos shell.

Isolamento real exige: usuário separado para executor, permissões de filesystem, egress de rede controlado (ver `secrets-and-privileges.md`).

## Proveniência de skills

- Skills de projeto têm precedência sobre locais/externas — registrar origem evita aprovar uma skill e carregar outra de mesmo nome.
- Não usar symlink para catálogo de outro perfil (editável na origem).
- Bundle carregado ≠ pacote completo; skills ausentes são puladas silenciosamente.

## Registro no checkpoint

Após SELECTION, `selected_items` deve listar **exatamente** o que foi aprovado. Na APPLY, o inventário final é comparado a essa lista — divergência = falha de verificação (critério #4).