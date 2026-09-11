# Checklist de testes de aceitação (VERIFY)

Cada item é executado no destino real e registrado em `verification_results` do checkpoint.
Resultado por item: `pass | fail | skipped (motivo)`.

## Referência cruzada com PLAN.md

| # | Teste | Critério |
|---|---|---|
| 1 | Gatilho controlado | Entrevista só inicia com gatilho explícito; menção casual não lê nada |
| 2 | Plano completo | Manifesto enumera arquivos, alias, config, capabilities, serviços afetados |
| 3 | Destino isolado | Default e outros perfis intactos (comparar inventário antes/depois) |
| 4 | Seleção positiva | Inventário final == `selected_items`; zero skills bundled não aprovadas |
| 5 | Pacote íntegro | SKILL.md valida; auxiliares presentes; zero segredo nos artefatos |
| 6 | Memória consentida | Cada fato aplicado após consentimento, dentro do limite; leitura de volta OK |
| 7 | Sessão nova confirma | Nova sessão no perfil destino mostra a memória injetada |
| 8 | Idempotência | Re-run do APPLY: nada duplicado; destino lido antes de qualquer criação |
| 9 | Retomada sem transcript | Novo processo lê checkpoint e continua corretamente |
| 10 | Bloqueios legítimos | Host off, consent expirado, versão incompatível → BLOCKED com motivo |
| 11 | Sem segredo-canário | Canário plantado em fixture não aparece em outputs/logs/artefatos |
| 12 | Falha fechada sudo | `sudo -n` negado → sem prompt, mensagem clara, sem travar |
| 13 | Broker isolado | Operações fora da allowlist negadas; agente não lê estado do broker |
| 14 | Isolamento de conhecimento | VPS/consumidor incapaz de ler notas fora do escopo |
| 15 | Backup/restauração | Backup existe; restauração testada em fixture |
| 16 | Sem "pronto" sem teste | Status final só com todos os testes passando no destino real |

## Execução típica

```bash
# 1. Inventário antes
hermes -p <nome> skills list
hermes profile list

# 2. Após APPLY
hermes -p <nome> skills list   # compara com selected_items
ls <home>/profiles/<nome>/memories/

# 3. Sessão nova confirma memória
hermes -p <nome> chat -q "cite um fato que você lembra sobre mim" -Q

# 4. Idempotência: re-executar APPLY → tudo "already exists", nada duplicado
```

## Fixtures

Testes usam `tests/fixtures/` (dados fake). Nunca dados reais do usuário em fixtures versionadas.