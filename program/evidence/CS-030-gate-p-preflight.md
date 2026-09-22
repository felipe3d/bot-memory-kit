# CS-030 — Gate P: pré-requisito P-01

**Estado:** BLOCKED antes de qualquer mutação  
**Data:** 2026-09-18  
**Gate:** P da Fase 2, revisão 2.3 / Anexo 2.2.

## Checagem mínima executada

| Papel | Operação somente leitura | Resultado |
|---|---|---|
| Publicador HomeLab | `sudo -n true` via alias local `k` | `denied`: autenticação interativa exigida. |
| Consumidor VPS | `sudo -n true` via MCP Oracle | `ok`. |

## Consequência

P-01 exige criar os usuários isolados `ak-pilot-publisher` e `ak-pilot-consumer`, com homes e raízes de teste novas. Como o publicador não pode ser criado no HomeLab sem autenticação interativa, a sequência foi interrompida **antes** de criar usuário, diretório, chave, repositório, audit store, manifesto ou qualquer outro recurso.

Não foi solicitado nem aceito segredo/senha. Não houve fallback para executar o publicador como `fac`, pois isso violaria o Anexo 2.2.

## Próximo gate necessário

O operador precisa disponibilizar um mecanismo não interativo e de menor privilégio para criar/remover somente os recursos sintéticos do piloto no HomeLab, ou executar manualmente a preparação estritamente enumerada e fornecer read-backs sanitizados. Isso exige uma revisão/aprovação de remediação separada; Gate P não autoriza ampliar privilégios por inferência.
