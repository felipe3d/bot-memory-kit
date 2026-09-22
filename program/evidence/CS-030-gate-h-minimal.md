# CS-030 — Gate H: discovery real mínimo (somente leitura)

**Estado:** BLOCKED  
**Data:** 2026-09-18  
**Autorização:** Gate H aprovado pelo usuário para GitHub, consumidor VPS, produtor, confiança/integridade e auditoria/limpeza.  
**Limite respeitado:** nenhuma criação ou alteração; nenhum vault, conteúdo, configuração integral, credencial, token, chave, sessão, segredo ou teste real N-01–N-06 foi acessado/executado.

## Metadados observados

| Grupo | Resultado sanitizado | Limite / consequência |
|---|---|---|
| GitHub | A sessão local `gh` identifica a conta `felipe3d` como ativa e expõe escopo `repo`. | Confirma uma conta candidata, mas não prova que ela pode criar o repositório privado proposto, nem seleciona conta/repo/admin técnico. Não houve chamada de criação nem consulta a repositório. |
| Consumidor VPS | O alvo lógico `oracle-vps` respondeu por MCP: Ubuntu Linux aarch64; papel de SO atual `ubuntu`; a raiz candidata nova `/var/tmp/cs030-pilot` estava ausente. | É candidata apenas para um ambiente novo de teste. Não foi criado diretório, usuário, chave, processo, audit store ou configuração. A ausência do path não prova isolamento. |
| Produtor | A reconsulta mínima após o usuário ligar o HomeLab respondeu pelo alias local `k`: Linux x86_64, papel de SO `fac`; a raiz candidata nova `/var/tmp/cs030-pilot-producer` estava ausente. | É candidata apenas para ambiente novo de teste. Não foram lidos home, vault, estado Hermes, configuração, credencial ou conteúdo. O isolamento de SO e a identidade técnica do publicador continuam indefinidos. |
| Confiança/integridade | A documentação oficial do GitHub publica fingerprints SSH para pinning de `github.com`; o GitHub exige verificar o fingerprint na primeira conexão. | A âncora concreta, modo de autenticação do manifest, assinatura/canal independente, anti-replay e política de clock continuam decisões humanas. Nenhuma conexão SSH ao GitHub ocorreu. |
| Auditoria/limpeza | Não há audit store separado nem owner/retenção definidos. A raiz candidata do consumidor está ausente, mas não pode ser usada como audit store sem desenho e aprovação separados. | **Bloqueia** o isolamento da auditoria e o anexo de limpeza. |

## Fonte e comandos mínimos

- Metadados GitHub: `gh auth status`; a saída contendo token mascarado não é reproduzida nesta evidência.
- Consumidor VPS: MCP `system_info` e comando limitado a identidade de SO, versão de kernel e teste de ausência do path candidato; sem leitura de home, `.env`, credenciais, configuração ou conteúdo.
- Produtor: primeira tentativa (HomeLab desligado) sem resposta; reconsulta após o usuário ligá-lo respondeu pelo alias local `k` com somente os metadados permitidos.
- Confiança SSH: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/githubs-ssh-key-fingerprints (consulta pública em 2026-09-18).

## Reconsulta limitada do produtor

A primeira consulta ocorreu enquanto o HomeLab estava desligado. Após o usuário informar que o ligou, a mesma consulta mínima e read-only foi repetida pelo alias local autorizado. Ela obteve somente: classe Linux/x86_64, papel de SO `fac` e ausência da raiz candidata nova. Não foi necessário usar o túnel reverso, e nenhum dado adicional foi lido.

## Decisões bloqueantes antes de Gate P

1. Definir isolamento de SO e identidade técnica do produtor `homelab-producer`; o host candidato está disponível, mas não foi validado além dos metadados mínimos.
2. Confirmar conta GitHub, repositório novo, papel administrativo técnico e método de autenticação sem reutilizar PAT/sessão/credencial pessoal.
3. Definir armazenamento protegido da deploy key, responsável e prazo de revogação.
4. Definir âncora SSH, autenticação independente do manifest, ref/anti-replay, TTL, clock skew e trust channel.
5. Definir audit store separado, retenção, responsável e inventário/limpeza fechados.

Sem essas decisões, o anexo da revisão 2.2 permanece incompleto e Gate P não pode ser solicitado. Não ampliar discovery por inferência.
