# Retomada — bots pessoais úteis, sem refactor amplo

## Missão autorizada nesta próxima sessão

Revisar pontualmente os documentos do programa para refletir a direção abaixo e preparar uma entrega funcional de aprendizado assistido. Executar a revisão documental inteira sem pedir aprovação por arquivo. Não implementar automações nem acessar fontes privadas, hosts ou credenciais nesta revisão. Não iniciar sessões recursivamente.

## Acordo com o usuário

O propósito é criar bots especializados, com memória bem definida e acesso ao contexto necessário para trabalhar bem para seu proprietário. Ele é o principal usuário, sozinho. Isolamento rigoroso é prioritário quando dados ou capacidades forem expostos a outras pessoas; rodar na VPS não torna um bot compartilhado.

Separar especialização de permissão: um bot pode consultar contexto autorizado de outra área sem copiar o sistema inteiro para sua memória ou assumir suas funções. Consulta não equivale a autorização para alterar dados, enviar mensagens ou apagar registros. Preservar proteção de credenciais e controles de ações de impacto.

A IA identifica padrões, redige candidatas, propõe fonte, destino e validade. A pessoa só aprova, rejeita ou ajusta sugestões em português simples. Não pedir YAML, IDs, scope, TTL ou redação manual de notas. Não impor uma nova aprovação só para detalhar um plano já autorizado.

## Leitura inicial

Carregar a skill bot-memory-kit. Ler, nesta ordem:
1. program/CURRENT.md
2. program/work-packages/WP-033-assisted-candidate-curation.md
3. program/DECISIONS.md
4. program/ROADMAP.md
5. program/contracts/MEMORY-CONTRACT.md
6. program/contracts/BOT-POLICY-MATRIX.md
7. program/change-sets/CS-034-assisted-candidate-curation.md
8. program/handoffs/CS-034.md
9. program/evidence/CS-032-p0-run.md

PLAN.md é histórico, não o plano operacional vigente. Consultá-lo somente se necessário. A direção acordada neste handoff substitui a premissa documental de isolamento máximo para todo bot pessoal; não concede novos acessos operacionais.

## O que preservar

- Pilotos GTD, CRM, gateway, integrações, permissões existentes, backups e rotas: não modificar.
- Obsidian como conhecimento, Mindwtr como tarefas, Odoo como CRM.
- Estrutura AgentKnowledge, proveniência, revisão humana e correção de memória.
- Evidências históricas: não reescrever testes como se comprovassem capacidades novas.
- Mudanças preexistentes no Git: inspecionar status e preservar; sem commit/push nesta revisão.

## Estado conhecido e limites

Os documentos relatam que o ensaio de publicação VPS com fixture sintética foi testado e removido. Não há pipeline real permanente comprovada por esse ensaio. A descoberta local autorizada encontrou canonical/ sem arquivos. Isso indica falta do fluxo de geração de candidatas, não uma obrigação de o usuário criar notas. Não afirmar que toda a fundação está concluída nem que toda segurança foi testada. Há cabeçalhos históricos inconsistentes: separar conclusão documentada, prova disponível e verificação atual.

## Revisão a executar

Atualizar somente documentos necessários em program/: estado atual, roteiro, decisões, contratos afetados, proposta ativa, WP e handoff. Não criar uma cadeia adicional de códigos ou gates. Referências técnicas ficam internas.

1. Priorizar especialização, memória útil e revisão/correção.
2. Distinguir uso pessoal de exposição a terceiros; não revogar controles funcionais só por conveniência.
3. Remover a publicação dedicada na VPS como pré-requisito universal do primeiro resultado útil; mantê-la como alternativa adiada se necessária.
4. Distinguir consultar fontes autorizadas de persistir cópias: não perpetuar a proibição absoluta de todo contexto GTD/CRM; não espelhar estado vivo nem segredos na memória.
5. Tornar coerente a revisão humana: permitir mostrar a candidata sanitizada ao proprietário no canal privado autorizado, sem despejar conteúdo fonte em logs ou canais alheios.
6. Definir uma aprovação por entrega delimitada, cobrindo implementação, testes, retries seguros e rollback. Parar só por novo acesso/privilégio não previsto, decisão material, risco inesperado ou falha sem recuperação segura.

## Próxima entrega proposta — não executar nesta revisão

Escolher e justificar um bot pessoal existente e uma fonte concreta de baixo risco, sem inventariar dados privados nesta etapa. Se a fonte não puder ser determinada pelos documentos autorizados, formular uma única escolha em linguagem simples, sem placeholders técnicos.

Resultado esperado: IA lê fonte autorizada → sugere conhecimento com origem → pessoa aprova/ajusta → memória é registrada → conversa nova recupera e usa corretamente → correção e retirada são testadas. Sugestões rejeitadas não viram memória. Conteúdo importado nunca comanda ferramentas. A publicação VPS só é incluída se necessária ao caso escolhido.

Preparar um pacote executável e enxuto que nomeie fonte/destinos, comportamento, testes, reversão e limites de autonomia. Não confundir autorização desta revisão documental com autorização de execução real.

## Encerramento

Rodar git diff --check e verificar também documentos não rastreados; validar coerência entre estado, decisões, roteiro, contratos e handoff. EVIDENCE.md só muda com prova operacional nova; revisão documental não é essa prova.

Responder sem jargões: o que preservou, o que simplificou, qual primeiro resultado o usuário verá e a única decisão realmente pendente. Deixar handoff atualizado para a implementação. Não iniciar outro agente automaticamente nem montar orquestrador/cron/Kanban por efeito deste prompt.
