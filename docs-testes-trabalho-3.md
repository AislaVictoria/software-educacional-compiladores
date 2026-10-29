\# Registro de testes — Trabalho 3



\## 1. Objetivo



Este documento registra os testes realizados na terceira etapa do software educacional de compiladores, dedicada à implementação da análise léxica (scanner) para um subconjunto didático da linguagem Python.



Foram verificados o reconhecimento de tokens, a integração com o backend, a apresentação dos resultados na interface, o tratamento de erros léxicos e a preservação das funcionalidades desenvolvidas nas Etapas 1 e 2.



\## 2. Testes automatizados



Os testes foram executados em 29/10/2026, utilizando Python e Node.js.



| Componente | Comando | Resultado |

|---|---|---|

| Backend Flask e scanner | `python -m unittest discover -s backend -p "test\*.py" -v` | 15 aprovados |

| Frontend JavaScript | `node --test frontend\\test\_app\_core.js` | 4 aprovados |

| Interface | `python frontend\\test\_interface.py` | 5 aprovados |

| \*\*Total\*\* | | \*\*24 aprovados, 0 falhas\*\* |



\### 2.1. Testes do backend e scanner



Os 15 testes verificaram:



\- Reconhecimento de palavras reservadas, identificadores, números, strings, operadores e delimitadores.

\- Tratamento de espaços em branco e comentários.

\- Identificação da linha e coluna dos tokens.

\- Reconhecimento de caracteres inválidos e literais malformados.

\- Acúmulo de erros léxicos.

\- Validação de entradas vazias e requisições inválidas.

\- Respostas do endpoint `/api/analyze`.

\- Funcionamento das rotas anteriores `/api/hello` e `/api/health`.



\*\*Resultado:\*\* 15 testes aprovados, sem falhas.



\### 2.2. Testes do frontend JavaScript



Foram verificados:



\- Disponibilidade de pelo menos três exemplos de programas.

\- Presença de título, descrição e código editável nos exemplos.

\- Validação de entradas vazias ou compostas apenas por espaços.

\- Aceitação de códigos válidos e caracteres especiais.



\*\*Resultado:\*\* 4 testes aprovados, sem falhas.



\### 2.3. Testes da interface



Foram executados cinco testes relacionados à estrutura da interface e à apresentação segura dos resultados da análise léxica.



\*\*Resultado:\*\* 5 testes aprovados, sem falhas.



\## 3. Validação funcional da API



A aplicação foi executada com Docker Compose e testada por meio de requisições HTTP.



\### 3.1. Código válido



Código utilizado:



```python

numero = 10

```



Resultado:



\- Requisição processada com sucesso.

\- `success: true`.

\- Três tokens identificados.

\- Nenhum erro léxico.



| Tipo | Lexema | Linha | Coluna |

|---|---|---|---|

| IDENTIFICADOR | numero | 1 | 1 |

| OPERADOR | = | 1 | 8 |

| LITERAL\_INTEIRO | 10 | 1 | 10 |



\### 3.2. Código com erro léxico



Código utilizado:



```python

numero = 10

resultado = numero @ 2

print(resultado)

```



Resultado:



\- `success: false`.

\- Um erro léxico identificado.

\- Caractere inválido: `@`.

\- Localização: linha 2, coluna 20.

\- Os tokens anteriores e posteriores ao erro foram reconhecidos.



O scanner continuou o processamento após encontrar o caractere inválido, permitindo a apresentação dos demais tokens.



\## 4. Validação com Docker Compose



A validação inicial, realizada em um ambiente sem o executável Docker, não pôde iniciar os contêineres.



Posteriormente, em 29/10/2026, a aplicação foi validada com sucesso no Windows, utilizando Docker Desktop e Docker Compose.



\### 4.1. Comandos executados



```powershell

docker compose up --build -d

docker compose ps

docker compose logs backend --tail=30

```



\### 4.2. Resultados



\- As imagens do backend e frontend foram construídas.

\- O contêiner `trabalho1-backend` iniciou com status `healthy`.

\- O contêiner `trabalho1-frontend` iniciou corretamente.

\- A interface ficou acessível em `http://localhost:8080`.

\- O endpoint `/api/analyze` recebeu o código e retornou os tokens e erros léxicos esperados.

\- Não foram identificados erros de inicialização do scanner.



Foi necessário encerrar os contêineres antigos da Etapa 2 para resolver um conflito de nomes.



Também foi confirmada a inclusão de `scanner.py` no Dockerfile:



```dockerfile

COPY app.py scanner.py .

```



\## 5. Validação visual da interface



A aplicação foi acessada pelo navegador.



Foi verificado que a interface apresenta:



\- Área de edição de código Python.

\- Seleção de exemplos.

\- Botão para solicitar análise.

\- Mensagem de conclusão da análise léxica.

\- Tabela com tipo, lexema, linha e coluna.

\- Quantidade total de tokens.

\- Contagem de tokens por categoria.

\- Explicações didáticas sobre tokens e lexemas.



Também foi verificado, por meio de requisição HTTP, que o backend retorna mensagens de erro léxico com localização.



\## 6. Correções realizadas



Durante o desenvolvimento e a validação, foram realizados os seguintes ajustes:



\- Preservação dos estilos anteriores da interface.

\- Inclusão dos elementos de apresentação dos tokens.

\- Correção do Dockerfile para copiar `scanner.py`.

\- Encerramento dos contêineres antigos para resolver o conflito de nomes.

\- Instalação do Flask no ambiente Python do Windows para permitir a execução dos testes locais.



Após a instalação do Flask, os testes do backend foram executados novamente e passaram.



\## 7. Limitações conhecidas



O scanner implementa um subconjunto didático de Python e não reconhece todas as construções da linguagem.



Entre as limitações estão:



\- Análise sintática e semântica ainda não implementadas.

\- Indentação sem tratamento como tokens específicos.

\- Strings multilinha e f-strings sem suporte completo.

\- Notação científica e determinados formatos numéricos sem suporte completo.

\- Decorators e operadores de bit fora do subconjunto previsto.



Algumas sequências fora do subconjunto podem ser divididas em tokens reconhecidos, sem gerar um erro específico. Esse comportamento deverá ser aprimorado nas próximas revisões.



A implementação atual não executa o código informado pelo usuário. Seu objetivo é identificar e classificar unidades léxicas.



\## 8. Resultado consolidado



\*\*Data:\*\* 29/10/2026



| Verificação | Resultado |

|---|---|

| Testes automatizados | 24 aprovados, 0 falhas |

| Docker Compose | Funcionando |

| Backend | Saudável |

| Frontend | Acessível |

| Tokenização de código válido | Aprovada |

| Identificação de erro léxico | Aprovada |

| Continuidade após erro | Aprovada |

| Exibição de tokens na interface | Verificada |

| Instalação limpa em outra máquina | Não realizada |

| Testes automatizados de ponta a ponta no navegador | Não realizados |



\## 9. Conclusão



A terceira etapa implementou a análise léxica para o subconjunto definido de Python, integrada à interface e ao backend.



Os 24 testes automatizados existentes foram executados com sucesso. O ambiente Docker Compose foi inicializado, e a comunicação entre os componentes foi verificada por requisições HTTP.



A aplicação reconhece tokens, informa suas categorias e posições e identifica erros léxicos com mensagens localizadas.



As limitações do subconjunto permanecem documentadas, e a análise sintática e semântica será desenvolvida nas próximas etapas.

