# Risks

| ID | Risco | Estado | Controle/condição de saída |
|---|---|---|---|
| R-001 | VPS acessar o vault pessoal por credencial ampla | aberto | identidade técnica ou broker default-deny; prova negativa antes de produção |
| R-002 | Memória cruzar fronteiras GTD/CRM/compartilhado | aberto | ACL antes de busca, testes interperfil e ausência técnica de grants |
| R-003 | Sessões voltarem a se perder em contexto | mitigado | `CURRENT.md`, WPs pequenos, handoff curto e um WP mutável |
| R-004 | Piloto gateway ser alterado acidentalmente | mitigado | ADR-004 e guardrail explícito em todo WP |
| R-005 | Candidatas virarem fatos automaticamente | aberto | reconciliador, proveniência, revisão e supersessão |
| R-006 | Novo bot ganhar capacidade destrutiva implícita | aberto | matriz de grants, wrappers/gates e testes negativos |
