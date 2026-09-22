# CS-030 — Gate D: discovery de aplicação mínimo

**Estado:** concluído somente como discovery de metadados documentais  
**Data:** 2026-09-18  
**Autorização:** Gate D de CS-030, aprovada explicitamente pelo usuário.  
**Limite executado:** nenhuma conexão a host, conta, repositório, vault, serviço, rede, credencial, configuração, sessão ou conteúdo real.

## Inventário sanitizado

| Item | Resultado de discovery | Fonte / limite |
|---|---|---|
| Consumidor | Papel lógico `VPS` 24/7, citado pelo problema CS-030; nenhum hostname, IP, processo ou configuração foi consultado. | CS-030 / autorização do usuário. |
| Produtor | Papel lógico separado: publicador aprovado no lado autorizado, sob controle de reconciliador/humano. Host físico **não selecionado** neste gate. | `MEMORY-CONTRACT.md` §§1, 4 e CS-030. |
| Artefato | Repositório Git dedicado e privado, contendo somente a projeção sanitizada e versionada; não é vault, fonte canônica, inbox, archive nem clone do vault pessoal. | Candidata documental; não existe/criado neste gate. |
| Canal VPS | Deploy key SSH exclusiva do repositório de projeção, **read-only** por padrão e sem acesso a outro repositório. | GitHub Deploy Keys docs; nenhuma chave criada/consultada. |
| Integridade | Commit/revisão Git + manifesto assinado ou hash publicado pelo produtor; o consumidor falha fechado se manifest/revisão/TTL não validar. | Requisito do futuro piloto; mecanismo de assinatura ainda não selecionado. |
| Revogação | Remover a deploy key do repositório dedicado e despublicar/revogar a revisão permitida; a chave não tem expiração nativa. | GitHub Deploy Keys docs; procedimento não executado. |
| Segredo de bootstrap | Se indispensável, fica fora da VPS-agente, em identidade/armazenamento técnico separado e de escopo mínimo. Não será PAT pessoal, sessão OAuth, credencial de sync ou vault pessoal. | Contrato/Matriz; mecanismo concreto bloqueado para fase posterior. |

## Tecnologia única candidata

**Git privado dedicado + deploy key SSH read-only por repositório** é a candidata para o piloto, não uma decisão de produção.

Justificativa verificada documentalmente:

- GitHub documenta que deploy key concede acesso a **um único repositório** e é read-only por padrão.
- A chave privada fica no servidor, não vinculada a conta pessoal; a opção de escrita não será habilitada.
- Revogação é possível removendo a chave, mas deploy keys não expiram automaticamente e podem ficar expostas se o servidor for comprometido. Portanto, o piloto exige armazenamento protegido, usuário de SO restrito, rotação/revogação exercitada e sem agent forwarding.
- GitHub alerta que deploy key com escrita equivale a privilégio amplo no repositório. Escrita na VPS é explicitamente excluída.

Fonte pública: https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managing-deploy-keys (consulta em 2026-09-18).

## Superfícies e provas negativas planejadas

| Prova | Superfície lógica a testar no piloto aprovado | Resultado exigido |
|---|---|---|
| N-01 vault pessoal | mounts, cliente Obsidian/Headless, diretórios de vault, URL/API/convite/compartilhamento e rotas de rede relativas ao vault. | Ausência/negação; nenhuma listagem ou leitura. |
| N-02 credenciais alheias | usuário do consumidor, ambiente do processo, mounts, arquivos permitidos, agentes/sockets, keyrings e caminhos de bootstrap permitidos. | Só a deploy key dedicada aparece no escopo permitido; nenhum segredo de papel pessoal, sync, produtor ou reconciliador é acessível. |
| N-03 scope | IDs adivinhados, referências Git fora do allowlist, arquivos fora do manifest, registro `restricted`/`prohibited`, inbox/archive/expirado e metadados de existência. | Nenhum conteúdo nem confirmação de existência fora da projeção válida. |
| N-04 escrita | push, alteração local, troca de remote/ref, edição de manifesto e comandos de administração usando a identidade VPS. | Todos negados; publicação e fonte preservadas. |
| N-05 revogação | remover a chave/grant em ambiente de piloto, depois testar leitura consumidor e produtor isoladamente. | Consumidor falha fechado; produtor e outros papéis não são afetados. |
| N-06 falhas | assinatura/hash/TTL inválido, repositório indisponível, ref divergente, auditoria ausente e rede negada. | Sem fallback a vault, sync, conta pessoal ou credencial alternativa. |

## Piloto proposto — ainda bloqueado

- Repositório novo, privado e exclusivamente sintético; histórico inicialmente vazio.
- Um único arquivo de projeção sintética e manifesto com TTL curto, sem Markdown real de AgentKnowledge.
- Par de chaves novo e descartável, exclusivo desse repositório e consumidor sintético; nunca reutilizar chave existente.
- Usuário de SO/ambiente isolado, sem montagem do vault e sem acesso aos homes/estado Hermes existentes.
- Logs de auditoria sanitizados: identidade lógica, revisão, resultado de validação e motivo de negação; nunca material secreto ou conteúdo de produção.
- Rollback: remover deploy key, remover repositório sintético e artefatos do ambiente isolado, e confirmar que a leitura falha fechada antes de qualquer limpeza adicional.

## Bloqueios e condição para Fase 2

Gate D não descobriu nem validou estado real de GitHub, conta, host, rede, storage de chaves, usuário de SO, publisher ou repositório. Antes de criar qualquer recurso, o CS-030 precisa ser revisado para enumerar os alvos reais, o responsável, armazenamento de chave, rotação, manifesto/assinatura, retenção, auditoria, rollback e comandos de verificação. Essa revisão requer aprovação humana separada para uma Fase 2 de piloto.
