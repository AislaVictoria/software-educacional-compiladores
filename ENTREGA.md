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

# Trabalho 3 — Análise Léxica

## Desenvolvimento do scanner

Na terceira etapa, implementei o analisador léxico
do software educacional. O objetivo foi transformar
o código-fonte inserido pelo estudante em uma sequência
de tokens que pudesse ser utilizada nas etapas
seguintes do compilador.

O scanner foi desenvolvido em Python e percorre
o código caractere por caractere, identificando
palavras reservadas, identificadores, números,
textos, operadores e delimitadores.

Cada token possui informações sobre seu tipo,
lexema, linha e coluna. Essas informações permitem
identificar a posição de cada elemento no código.

Também implementei o tratamento de erros léxicos.
Quando um caractere não reconhecido é encontrado,
o scanner registra sua posição e continua a análise,
permitindo apresentar os demais tokens reconhecidos.

A interface foi atualizada para mostrar a tabela
de tokens, a quantidade de elementos encontrados
e os diagnósticos léxicos.

Essa etapa estabeleceu a base necessária para
a implementação do analisador sintático.

# Trabalho 4 — Análise Sintática e AST

## Objetivo da etapa

Na quarta etapa, desenvolvi o analisador sintático
do software educacional, utilizando os tokens
produzidos pelo scanner da etapa anterior.

O objetivo foi permitir que o estudante compreenda
não apenas quais elementos existem no código,
mas também como esses elementos se organizam
segundo as regras de uma linguagem de programação.

## Definição da gramática

Defini uma gramática formal em EBNF para representar
o subconjunto de Python utilizado pelo software.

Esse subconjunto inclui atribuições, literais,
expressões aritméticas, relacionais e lógicas,
chamadas de print e estruturas condicionais.

A gramática também estabelece regras de precedência,
associatividade e organização dos blocos por indentação.

A documentação apresenta exemplos válidos e inválidos,
os símbolos terminais e não terminais e as limitações
da linguagem reconhecida.

## Implementação do parser

Utilizei a estratégia de análise descendente recursiva,
com escalonamento de precedência para as expressões.

Escolhi essa abordagem porque permite relacionar
as funções do analisador às construções da gramática,
facilitando a compreensão e a manutenção do código.

O parser recebe os tokens do scanner e verifica
se sua organização corresponde à gramática definida.

Quando existem erros léxicos, a análise sintática
não é executada, evitando diagnósticos adicionais
provocados por tokens ausentes ou inválidos.

## Construção da AST

Implementei a Árvore Sintática Abstrata para representar
a estrutura hierárquica do programa.

Os nós possuem informações sobre o tipo da construção,
seus atributos, seus filhos e as posições correspondentes
no código-fonte.

Por exemplo, na expressão 10 + 5 * 2, a AST mostra
a multiplicação como uma operação subordinada à adição,
demonstrando a precedência dos operadores.

Essa representação será utilizada como base para
a análise semântica na próxima etapa.

## Melhorias na interface

Atualizei a interface para apresentar os resultados
da análise léxica e sintática de maneira separada.

A árvore pode ser visualizada de forma hierárquica,
com controles de expansão e recolhimento dos nós.

Também foram acrescentadas informações sobre as
posições dos nós e as regras gramaticais relacionadas
às operações binárias.

Além dos exemplos válidos, disponibilizei exemplos
com erros léxicos e sintáticos, permitindo que o
estudante observe a diferença entre esses diagnósticos.

## Correções e robustez

Durante os testes, identifiquei situações em que
o analisador aceitava construções fora da gramática,
como comandos na mesma linha e blocos sem indentação.

Realizei correções para garantir a delimitação dos
comandos, a organização dos blocos condicionais
e a identificação de expressões incompletas.

Também estabeleci limites de caracteres, tokens
e profundidade da árvore para reduzir problemas
de processamento excessivo.

## Testes e validação

A versão inicial da Etapa 4 possuía 34 testes
automatizados. Após as correções e a ampliação
dos casos testados, o registro final passou a
contemplar 93 testes automatizados aprovados.

Também foram aprovados cinco testes de integração
HTTP, verificando códigos válidos, erros léxicos,
erros sintáticos e estruturas condicionais.

A aplicação foi executada com Docker Compose
e validada por meio do navegador.

As evidências visuais e os resultados dos testes
foram organizados no repositório.

## Decisões e limitações

Mantive o projeto restrito a um subconjunto de Python
para evitar que a implementação se tornasse ampla
demais para os objetivos da disciplina.

A integração opcional com modelos de linguagem
não foi implementada nesta etapa, pois priorizei
o funcionamento independente do scanner, do parser
e da construção da AST.

Os testes realizados demonstram o funcionamento
técnico das funcionalidades implementadas, mas não
representam uma avaliação formal de aprendizagem.

## Considerações finais

A quarta etapa representa a evolução do reconhecimento
individual dos tokens para a identificação da estrutura
gramatical do programa.

Com a implementação do parser e da AST, o software
passou a demonstrar duas fases fundamentais de um
compilador: a análise léxica e a análise sintática.

A próxima etapa será dedicada à análise semântica,
incluindo a utilização das informações presentes
na AST para verificar propriedades do programa.
