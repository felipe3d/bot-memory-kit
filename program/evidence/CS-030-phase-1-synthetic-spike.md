# CS-030 — Evidência da Fase 1: spike sintético local

**Estado:** VERIFIED somente para o ambiente sintético local  
**Data:** 2026-09-18  
**Limite:** nenhum host, vault, credencial, conta, serviço, rede, conteúdo de AgentKnowledge ou produção foi acessado ou alterado.

## Implementação exercitada

- `scripts/cs030_synthetic_spike.py`: modelo em memória de publicação derivada, identidade `synthetic-vps`, filtro positivo, revogação e verificação de integridade.
- `tests/test_cs030_synthetic_spike.py`: fixtures exclusivamente sintéticas com IDs `AK-SPIKE-*` e locators `synthetic://`.
- Não há filesystem discovery, chamadas de rede, integração Obsidian/Headless/1Password, token real, caminho de vault ou identidade real no spike.

## Comando e resultado

```text
python3 -m unittest discover -s tests -v
Ran 6 tests
OK
```

`git diff --check` também passou após os testes.

## Cobertura demonstrada

| Requisito CS-030 | Teste sintético | Resultado |
|---|---|---|
| N-03: apenas scope/status/sensibilidade elegíveis | `test_reader_receives_only_current_canonical_allowed_scope`; `test_noncanonical_restricted_prohibited_and_expired_records_are_excluded` | Passou: retorna somente `canonical`, scope/audiência permitidos, `public`/`internal` e não expirado. |
| N-04: VPS não escreve/influencia fonte | `test_reader_cannot_write_or_mutate_the_publication` | Passou: operação de escrita recebe `PermissionError`; publicação não muda. |
| N-05: revogação falha fechada | `test_revocation_fails_closed_without_mutating_published_records` | Passou: revogação bloqueia leitura e preserva o artefato para auditoria. |
| N-06: falha de integridade não amplia acesso | `test_tampered_publication_fails_closed` | Passou: alteração após publicação invalida digest e retorna ausência. |
| Identidade sem grant | `test_unknown_synthetic_identity_receives_no_projection` | Passou: identidade diferente não recupera conteúdo. |

## Limites não demonstrados

- N-01 e N-02 não podem ser provados por este spike porque não há VPS, vault pessoal, credencial, serviço de publicação ou runtime real — por desenho e por aprovação da Fase 1.
- O controle de identidade é propositalmente sintético e não equivale a autenticação, armazenamento de segredo, isolamento de SO, ACL de fornecedor, auditoria externa ou disponibilidade 24/7.
- O digest detecta adulteração no modelo, não substitui assinatura, transporte autenticado, chave protegida, armazenamento imutável ou verificação independente.
- Fase 2 permanece bloqueada. Antes dela, uma revisão do CS deve separar discovery de aplicação, nomear tecnologia, alvo, identidade, retenção, integridade, rollback e verificações reais.
