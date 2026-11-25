# Registro de testes — Trabalho 4

## 1. Objetivo

Validar o funcionamento do scanner, do parser, da AST,
da API e da interface, preservando as funcionalidades
implementadas nas etapas anteriores.

## 2. Ambiente de validação

- Windows 10, 64 bits;
- Python 3.13.15 no ambiente local;
- Python 3.12 no contêiner;
- Flask 3.0.3;
- Node.js 24.20.0;
- Docker Desktop 29.8.2;
- Docker Compose 5.5.1;
- Nginx para disponibilização do frontend.

## 3. Testes automatizados

| Grupo | Aprovados | Falhas |
|---|---:|---:|
| API do backend | 11 | 0 |
| Scanner | 6 | 0 |
| Parser | 7 | 0 |
| Robustez e limites | 21 | 0 |
| Gramática e AST | 26 | 0 |
| Lógica JavaScript do frontend | 10 | 0 |
| Contrato estático da interface | 12 | 0 |
| Total | 93 | 0 |

Todos os 93 testes automatizados foram aprovados.

## 4. Evolução da cobertura de testes

| Versão | Testes aprovados |
|---|---:|
| Versão inicial da Etapa 4 | 34 |
| Após correções de robustez | 55 |
| Após melhorias do frontend | 67 |
| Após testes permanentes da gramática | 93 |

Foram acrescentados 59 testes automatizados.

O aumento representa a ampliação da quantidade de
casos testados, não uma medição percentual de cobertura
de linhas do código-fonte.

## 5. Comandos de reprodução

Executar na raiz do projeto:

```powershell
python -m pip install -r backend\requirements.txt

python -m unittest discover -s backend -p "test*.py" -v

node --test frontend\test_app_core.js

python frontend\test_interface.py -v

python -m py_compile backend\app.py backend\scanner.py backend\parser.py backend\syntax_ast.py

node --check frontend\app.js

node --check frontend\app-core.js
```

Em ambientes Linux, pode ser necessário utilizar python3
e substituir as barras invertidas dos caminhos.

## 6. Casos cobertos

- Reconhecimento de tokens e lexemas;
- Preservação de linha e coluna;
- Atribuições e chamadas de print;
- Estruturas condicionais e blocos aninhados;
- Indentação válida e inválida;
- Precedência aritmética e lógica;
- Associatividade dos operadores;
- Agrupamento por parênteses;
- Literais booleanos e nulos;
- Estrutura e posições dos nós da AST;
- Expressões incompletas;
- Comparações encadeadas não suportadas;
- Tratamento de erros léxicos e sintáticos;
- Limites de entrada e complexidade;
- Contrato da API;
- Regressão das funcionalidades anteriores;
- Elementos e controles da interface.

Os testes de contrato da interface verificam seus
arquivos estáticos. Eles não substituem os testes
de interação realizados no navegador.

## 7. Validação no Docker

A construção das imagens do frontend e do backend
foi concluída com sucesso.

Durante a inicialização, foi identificado um conflito
entre nomes fixos de contêineres das etapas anteriores.

A configuração foi corrigida removendo container_name
do Docker Compose, permitindo a geração automática
dos nomes de cada projeto.

Após a correção, os dois serviços foram iniciados,
com o backend aprovado no healthcheck.

Foram verificados os endpoints:

- GET /api/hello
- GET /api/health
- POST /api/analyze

A interface foi acessada em http://localhost:8080.

## 8. Testes de integração HTTP

| Caso | Tokens | Erros léxicos | Erros sintáticos | AST | Resultado |
|---|---:|---:|---:|---|---|
| Código válido | 7 | 0 | 0 | Sim | Aprovado |
| Erro léxico | 4 | 1 | 0 | Não | Aprovado |
| Erro sintático | 4 | 0 | 1 | Não | Aprovado |
| Condicional válido | 12 | 0 | 0 | Sim | Aprovado |
| Indentação inválida | 8 | 0 | 1 | Não | Aprovado |

Resultado: 5 de 5 testes de integração aprovados.

## 9. Validação visual

Foram verificadas as seguintes situações por meio
da execução no navegador e de capturas de tela:

| Cenário | Resultado |
|---|---|
| Interface principal | Aprovado |
| Análise aritmética e AST | Aprovado |
| Estrutura condicional | Aprovado |
| Apresentação de erro léxico | Aprovado |
| Apresentação de erro sintático | Aprovado |

As evidências demonstram a apresentação dos tokens,
a hierarquia da AST, as posições dos nós, as regras
gramaticais e a diferenciação dos diagnósticos.

As imagens estão armazenadas em evidencias/etapa-4/.

Os controles de expansão e recolhimento estão presentes
na interface. A confirmação de sua interação manual
deve ser registrada após a execução dos respectivos testes.

## 10. Resultado consolidado

- 93 testes automatizados aprovados;
- 5 testes de integração aprovados;
- 98 aprovações nessas duas categorias;
- Nenhuma falha nas baterias finais executadas;
- Interface e quatro cenários de análise demonstrados
  por evidências visuais;
- Execução bem-sucedida com Docker Compose.

## 11. Limitações

Os resultados são referentes ao subconjunto implementado.

Não foi realizada uma avaliação formal de aprendizagem
com estudantes, nem uma medição de cobertura de código
ou de desempenho sob carga.

A análise semântica e a integração opcional com modelos
de linguagem não fazem parte da versão validada.
