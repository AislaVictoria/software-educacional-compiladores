# Entrega — Trabalho 1

## Primeira etapa do projeto

Nesta primeira etapa, preparei a base do meu software educacional, que será voltado ao estudo da linguagem Python. Optei por trabalhar inicialmente com um subconjunto reduzido da linguagem, formado por variáveis, tipos básicos, operadores, estruturas condicionais e comandos simples de saída. Essa escolha foi importante para manter o projeto viável e permitir que os conteúdos sejam desenvolvidos gradualmente, sem tentar abranger toda a linguagem de uma só vez.

Também organizei o projeto em duas partes principais: frontend e backend. O frontend apresenta a interface ao usuário, enquanto o backend disponibiliza as rotas que serão utilizadas nas próximas etapas. Para testar essa comunicação, implementei a rota `/api/hello`, que retorna a mensagem “Hello, World!”. Ao acessar a aplicação, o frontend consulta essa rota e apresenta o resultado na tela.

Para tornar o ambiente reproduzível, criei um Dockerfile para cada serviço e um arquivo `docker-compose.yml` para iniciar os contêineres juntos. Dessa maneira, a pessoa que for executar o projeto não precisa instalar manualmente as dependências da aplicação. Basta ter Docker e Docker Compose instalados, executar o comando indicado no README e acessar a aplicação pelo navegador.

A documentação também explica a estrutura das pastas, as tecnologias escolhidas, os comandos de inicialização e encerramento e o procedimento de validação em uma instalação limpa. Considero que essa organização é importante porque o README não serve apenas para cumprir uma exigência: ele também ajuda outras pessoas a entenderem o projeto e me ajuda a retomar o trabalho futuramente.

Como resultado, a primeira versão já possui uma estrutura funcional e preparada para receber o analisador léxico, sintático e semântico nas próximas etapas.


# Trabalho 2 — Segunda etapa do projeto

Nesta segunda etapa, transformei a tela inicial em uma interface que representa melhor a finalidade do software educacional. Agora, o usuário consegue visualizar que o projeto trabalha com a linguagem Python, escrever ou colar um código-fonte, editar esse conteúdo e solicitar o seu processamento.

Também disponibilizei três exemplos relacionados ao subconjunto escolhido para o projeto: variáveis e tipos básicos, operações aritméticas e estrutura condicional. A seleção de um exemplo preenche o editor, mas não bloqueia a edição. Essa escolha foi pensada para que o estudante possa observar um programa pronto, fazer alterações e testar diferentes possibilidades.

A comunicação entre as partes passou a ser feita de forma real. Quando o botão de análise é acionado, o frontend envia uma requisição `POST` para o endpoint `/api/analyze`, contendo o código em formato JSON. O backend valida os dados recebidos e responde informando se o código foi aceito, além da quantidade de caracteres e linhas. A análise do conteúdo ainda não é realizada, porque será construída nas próximas etapas.

Tive cuidado especial com as situações de erro. Código vazio, conteúdo composto apenas por espaços, requisições sem JSON e falhas de comunicação recebem mensagens específicas e compreensíveis. Dessa forma, o sistema não fica limitado ao cenário em que tudo dá certo e também não expõe informações internas desnecessárias.

Como a proposta da etapa também destaca a importância dos testes automatizados, criei testes para as rotas do backend, para os exemplos, para as validações e para os elementos essenciais da interface. Os testes da primeira etapa, como `Hello, World!` e o healthcheck, continuam sendo executados para verificar regressões. Ao todo, foram aprovados 15 testes automatizados nesta etapa.

Acredito que esta versão representa uma evolução importante porque o projeto deixou de ser apenas uma aplicação mínima e passou a ter uma porta de entrada real para o futuro analisador. O estudante já pode interagir com o sistema, experimentar códigos e receber respostas claras, enquanto a arquitetura permanece preparada para receber as análises léxica, sintática e semântica.
