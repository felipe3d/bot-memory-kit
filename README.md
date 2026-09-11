# Bot Memory Kit

Kit replicável para descobrir necessidades, planejar e implantar bots e memória no Hermes Agent.

## Estado

Pesquisa e planejamento em andamento. Não é um instalador funcional. Nenhum perfil, cofre, vault ou regra sudo é alterado nesta fase. A implementação será iniciada após revisão do plano e aprovação do usuário.

## Requisitos acordados

- Skill principal com gatilhos explícitos; não iniciar por perguntas genéricas sobre memória.
- Entrevista adaptativa sobre trabalho, vida pessoal, hobbies, necessidades, privacidade e autonomia.
- Descoberta autorizada e somente leitura de ambiente, capacidades e gerenciadores de credenciais.
- Um ou vários computadores; um proprietário por bot, sem sincronizar state.db entre processos.
- Skills, ferramentas, MCPs, conhecimento e permissões seletivos por bot.
- Obsidian/Markdown como conhecimento canônico; memória nativa compacta, skills procedimentais e histórico separados.
- Auditoria e migração com backup, aprovação e validação; nada apagado silenciosamente.
- Segredos fora de chat, logs e memória; referências e identidades limitadas. 1Password é adaptador inicial candidato, não dependência obrigatória.
- Diferenciar Apple Passwords, Keychain e automação não interativa. Não prometer acesso irrestrito a cofres pessoais.
- Privilégios administrativos por operações autorizadas, não senha sudo armazenada nem NOPASSWD universal.
- Estado persistente fora da conversa, retomada, bloqueio concorrente e reconciliação de operações interrompidas.
- Instalação inicial e manutenção sob demanda; sem rotinas automáticas criadas implicitamente.

## Separação de dados

Este repositório deve conter apenas método, documentação, templates, scripts e testes. Respostas pessoais, inventários reais, backups, credenciais e estado de implantação pertencem a um diretório privado externo.

## Próximas entregas

1. Pesquisa citada sobre Hermes, memória e segredos.
2. Plano com escopo MVP, decisões, riscos, etapas e critérios de aceitação.
3. Revisão independente e correções.
4. Aprovação antes da implementação e de alterações no ambiente do usuário.
