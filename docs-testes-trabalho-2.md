\# Registro de testes — Trabalho 2



\## 1. Objetivo



Este documento registra os testes realizados no software educacional Laboratório de Linguagens, desenvolvido para receber códigos-fonte em Python e preparar a implementação futura das análises léxica, sintática e semântica.



Os testes tiveram como objetivo verificar o funcionamento das rotas da API, das validações, dos exemplos da interface e da comunicação entre frontend e backend.



\## 2. Testes automatizados



| Componente | Verificação | Resultado |

|---|---|---|

| Backend (Python/Flask) | Rotas, validações e regressão | 7 testes aprovados |

| Frontend (JavaScript) | Exemplos, validação e caracteres especiais | 4 testes aprovados |

| Interface (Python) | Elementos e contrato de comunicação | 4 testes aprovados |

| \*\*Total\*\* | | \*\*15 testes aprovados\*\* |



\### Comandos utilizados



\*\*Backend:\*\*



```powershell

.\\.venv\\Scripts\\python.exe -m unittest discover -s backend -p "test\_\*.py" -v

```



\*\*Lógica do frontend:\*\*



```powershell

node --test frontend\\test\_app\_core.js

```



\*\*Contrato da interface:\*\*



```powershell

.\\.venv\\Scripts\\python.exe -m unittest discover -s frontend -p "test\_\*.py" -v

```



\*\*Verificação de sintaxe Python:\*\*



```powershell

.\\.venv\\Scripts\\python.exe -m py\_compile backend\\app.py backend\\test\_app.py

```



Todos os testes automatizados foram executados com sucesso.



\## 3. Testes de integração



O projeto foi executado utilizando Docker Desktop e Docker Compose.



Comando utilizado:



```powershell

docker compose up --build -d

```



A construção das imagens foi concluída com sucesso.



O comando `docker compose ps` confirmou os seguintes estados:



\- Backend: `Up (healthy)`.

\- Frontend: `Up`.

\- Interface disponível em `http://localhost:8080`.



Também foram realizadas requisições HTTP para verificar a comunicação entre Nginx e Flask:



\- `GET /api/hello`: resposta HTTP 200 com a mensagem `Hello, World!`.

\- `POST /api/analyze`: resposta HTTP 200 confirmando o recebimento do código e retornando estatísticas de linhas e caracteres.



\## 4. Verificação visual



A interface foi acessada no navegador pela porta 8080.



Foram confirmados:



\- Carregamento da interface principal.

\- Exibição do editor de código Python.

\- Carregamento do exemplo de variáveis e tipos básicos.

\- Envio de código para o backend.

\- Apresentação da mensagem de sucesso.

\- Validação de campo vazio, com mensagem informativa ao usuário.



\## 5. Evidências



As capturas de tela estão disponíveis na pasta `evidencias`:



\- `interface-funcionando.png`: interface com código recebido.

\- `validacao-campo-vazio.png`: mensagem de validação.

\- `docker-containers.png`: execução dos serviços no Docker.



\## 6. Limitações conhecidas



Nesta etapa, o backend recebe e valida o código-fonte, além de calcular estatísticas básicas.



A análise léxica, sintática e semântica ainda não foi implementada. Essas funcionalidades fazem parte das próximas etapas de desenvolvimento do software educacional.



\## 7. Conclusão



Os 15 testes automatizados foram aprovados. A aplicação também foi construída e executada com Docker Compose, com frontend e backend funcionando e respondendo às requisições HTTP realizadas.



As evidências registradas demonstram o funcionamento da interface, da validação de entrada e da comunicação entre os serviços.
