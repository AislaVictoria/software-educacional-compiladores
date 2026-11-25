# Gramática do subconjunto Python — Etapa 4

## 1. Objetivo e escopo

O software educacional Laboratório de Linguagens utiliza um
subconjunto da linguagem Python para demonstrar os conceitos
de análise léxica, análise sintática e construção da Árvore
Sintática Abstrata (AST).

O objetivo não é implementar um compilador Python completo,
mas permitir que o estudante compreenda como os tokens são
reconhecidos e organizados segundo uma gramática formal.

O subconjunto contempla:

- Atribuições de variáveis;
- Literais inteiros, reais, textuais, booleanos e nulos;
- Identificadores;
- Operadores aritméticos, relacionais e lógicos;
- Chamadas de print com zero ou mais argumentos;
- Estruturas condicionais if e else;
- Estruturas condicionais aninhadas;
- Expressões agrupadas por parênteses;
- Blocos delimitados por indentação.

## 2. Estratégia de análise sintática

O parser foi implementado manualmente utilizando a estratégia
descendente recursiva, combinada com escalonamento de
precedência (precedence climbing) para as expressões.

A escolha permite associar funções do analisador às
construções gramaticais, facilitando a compreensão,
a manutenção e a geração da AST.

O parser recebe diretamente os tokens produzidos pelo
scanner, preservando seus tipos, lexemas, linhas e colunas.

Não é utilizado um gerador automático de parsers.

## 3. Gramática formal em EBNF

O símbolo inicial da gramática é programa.

Convenções:

- Aspas representam terminais literais.
- Letras maiúsculas representam categorias de tokens
  ou marcadores estruturais.
- Colchetes representam elementos opcionais.
- Chaves representam zero ou mais repetições.
- A barra vertical representa alternativas.

```ebnf
programa       = { comando } ;

comando        = comando_simples, FIM_LINHA
               | condicional ;

comando_simples = atribuicao
                | chamada_print
                | expressao ;

atribuicao     = IDENTIFICADOR, "=", expressao ;

chamada_print  = "print", "(",
                 [ expressao, { ",", expressao } ],
                 ")" ;

condicional    = "if", expressao, ":", FIM_LINHA,
                 bloco,
                 [ "else", ":", FIM_LINHA, bloco ] ;

bloco          = INDENT, comando, { comando }, DEDENT ;

expressao      = logica_or ;

logica_or      = logica_and, { "or", logica_and } ;

logica_and     = comparacao, { "and", comparacao } ;

comparacao     = soma,
                 [ operador_relacional, soma ] ;

operador_relacional = "==" | "!=" | "<" | ">"
                    | "<=" | ">=" ;

soma           = multiplicacao,
                 { ("+" | "-"), multiplicacao } ;

multiplicacao  = potencia,
                 { ("*" | "/" | "//" | "%"), potencia } ;

potencia       = primaria, [ "**", potencia ] ;

primaria       = IDENTIFICADOR
               | LITERAL_INTEIRO
               | LITERAL_REAL
               | LITERAL_TEXTO
               | "True"
               | "False"
               | "None"
               | "(", expressao, ")" ;
```

## 4. Símbolos não terminais

Os não terminais são:

programa, comando, comando_simples, atribuicao,
chamada_print, condicional, bloco, expressao, logica_or,
logica_and, comparacao, operador_relacional, soma,
multiplicacao, potencia e primaria.

## 5. Terminais e correspondência com o scanner

| Terminal | Categoria léxica |
|---|---|
| if, else, print | PALAVRA_RESERVADA |
| and, or | PALAVRA_RESERVADA |
| True, False, None | PALAVRA_RESERVADA |
| Nomes de variáveis | IDENTIFICADOR |
| Números inteiros | LITERAL_INTEIRO |
| Números reais | LITERAL_REAL |
| Textos entre aspas | LITERAL_TEXTO |
| =, +, -, *, /, //, %, ** | OPERADOR |
| ==, !=, <, >, <=, >= | OPERADOR |
| (, ), vírgula e dois-pontos | DELIMITADOR |

FIM_LINHA, INDENT e DEDENT são marcadores conceituais
utilizados na documentação da gramática.

Esses marcadores não são tokens emitidos pelo scanner.
O parser identifica as mudanças de linha e de indentação
por meio das posições dos tokens.

O fim do código também pode encerrar o último comando.

O reconhecimento léxico de uma palavra reservada ou
operador não significa que sua utilização seja aceita
pela gramática sintática desta etapa.

## 6. Regras de indentação

- Os comandos do nível principal começam na coluna 1.
- Cada comando simples ocupa uma única linha física.
- O corpo de um if ou else deve começar em outra linha.
- O corpo deve possuir indentação superior à do cabeçalho.
- Comandos pertencentes ao mesmo bloco devem manter
  uma indentação consistente.
- O else deve estar alinhado com seu if correspondente.
- Blocos vazios não são permitidos.
- Tabulações na indentação são rejeitadas.
- Linhas vazias e comentários são desconsiderados.
- Condicionais aninhados são permitidos.

Recomenda-se utilizar quatro espaços por nível de
indentação, embora o parser não exija exatamente
quatro espaços.

## 7. Precedência e associatividade

| Prioridade | Operadores | Associatividade |
|---|---|---|
| 6 - Maior | ** | Direita |
| 5 | *, /, //, % | Esquerda |
| 4 | +, - | Esquerda |
| 3 | ==, !=, <, >, <=, >= | Comparação simples |
| 2 | and | Esquerda |
| 1 - Menor | or | Esquerda |

Os parênteses permitem modificar a ordem estrutural
das operações.

Comparações encadeadas não são suportadas.

Exemplos:

- 10 + 5 * 2: multiplicação antes da adição.
- (10 + 5) * 2: adição agrupada antes da multiplicação.
- 20 - 5 - 3: associação à esquerda.
- 2 ** 3 ** 2: associação à direita.

A AST representa essas relações estruturais.
O software não calcula o resultado das expressões.

## 8. Árvore Sintática Abstrata

A AST é implementada em backend/syntax_ast.py.

Cada nó possui:

| Campo | Descrição |
|---|---|
| tipo | Categoria do nó |
| linha | Linha inicial |
| coluna | Coluna inicial |
| atributos | Informações específicas da construção |
| filhos | Lista de nós subordinados |
| linhaFinal | Linha final, quando disponível |
| colunaFinal | Coluna final, quando disponível |

As posições começam em 1. A coluna final representa
a posição inclusiva do último caractere do trecho.

Os principais tipos de nós são:

- PROGRAMA
- ATRIBUICAO
- CHAMADA_FUNCAO
- CONDICIONAL
- BLOCO
- EXPRESSAO
- OPERACAO_BINARIA
- AGRUPAMENTO
- IDENTIFICADOR
- LITERAL_INTEIRO
- LITERAL_REAL
- LITERAL_TEXTO
- LITERAL_BOOLEANO
- LITERAL_NULO

True e False são palavras reservadas no scanner e
originam nós LITERAL_BOOLEANO na AST.

None é uma palavra reservada no scanner e origina
um nó LITERAL_NULO na AST.

Os nós de operações binárias possuem atributos que
identificam o operador e sua regra gramatical.

As regras apresentadas na interface são representações
didáticas das produções correspondentes.

## 9. Exemplo de AST

Código:

```python
resultado = 10 + 5 * 2
print(resultado)
```

Representação simplificada:

```text
PROGRAMA
  ATRIBUICAO: resultado
    OPERACAO_BINARIA: +
      LITERAL_INTEIRO: 10
      OPERACAO_BINARIA: *
        LITERAL_INTEIRO: 5
        LITERAL_INTEIRO: 2
  CHAMADA_FUNCAO: print
    IDENTIFICADOR: resultado
```

A AST não é uma árvore de derivação concreta, pois
omite elementos gramaticais que não são necessários
para representar a estrutura do programa.

## 10. Exemplos válidos

### Variáveis e tipos básicos

```python
nome = "Ana"
idade = 20
estudante = True
valor = None
print(nome)
```

### Operações aritméticas

```python
resultado = (10 + 5) * 2
print(resultado)
```

### Estrutura condicional

```python
nota = 8

if nota >= 6:
    situacao = "Aprovada"
else:
    situacao = "Em recuperação"

print(situacao)
```

### Estrutura condicional aninhada

```python
x = 10
y = 5

if x > 0:
    if y > 0:
        print(x, y)
```

## 11. Exemplos inválidos

| Código ou situação | Motivo |
|---|---|
| resultado = 10 + | Expressão incompleta |
| print(resultado | Parêntese de fechamento ausente |
| x = 1 y = 2 | Dois comandos na mesma linha |
| x = 1 2 | Operador ausente |
| x = 1 < 2 < 3 | Comparação encadeada não suportada |
| if nota >= 6: sem corpo | Bloco vazio |
| Corpo de if sem indentação | Indentação inválida |
| else sem if | Estrutura condicional inválida |
| return 10 | Comando fora do subconjunto |
| numero = 10 @ 2 | Caractere não reconhecido pelo scanner |

## 12. Tratamento de erros

Quando existem erros léxicos, o parser não é executado.
Os tokens reconhecidos e os erros léxicos são retornados
ao frontend.

Quando existem erros sintáticos, são retornados
diagnósticos contendo:

- Tipo do erro;
- Linha e coluna;
- Elemento encontrado;
- Elemento esperado;
- Mensagem explicativa.

O parser utiliza sincronização por linha para tentar
continuar após encontrar um erro.

Quando existem erros sintáticos, a AST final não é
disponibilizada ao usuário.

## 13. Limites de processamento

Para reduzir problemas de processamento excessivo,
foram definidos os seguintes limites:

| Recurso | Limite |
|---|---:|
| Caracteres do código-fonte | 10000 |
| Tamanho do corpo HTTP | 128 KiB |
| Quantidade de tokens | 2000 |
| Profundidade de parênteses | 100 |
| Profundidade da AST | 100 níveis |

Os limites são independentes. Uma entrada pode atingir
o limite da AST antes do limite de parênteses.

Erros de recursão também são tratados para evitar
a apresentação de rastreamentos internos ao usuário.

## 14. Construções fora do escopo

Não são suportados nesta etapa:

- Toda a especificação da linguagem Python;
- Declaração de funções;
- Comando return;
- Laços for e while;
- Estruturas elif;
- Listas, tuplas e dicionários;
- Classes e importações;
- Tratamento de exceções;
- Operadores unários, incluindo not;
- Comparações encadeadas;
- Atribuições compostas;
- Expressões distribuídas em múltiplas linhas;
- Strings multilinha e f-strings;
- Execução e interpretação do código;
- Análise semântica;
- Tabela de símbolos e verificação de tipos.

A análise semântica será desenvolvida na Etapa 5.

A integração opcional com modelos de linguagem não
foi implementada. O scanner e o parser funcionam
independentemente de serviços de inteligência artificial.
