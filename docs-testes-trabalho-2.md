# Registro de testes — Trabalho 2

## Escopo

Foram implementados testes para a nova rota de recebimento de código, para as validações do backend, para a preservação das rotas da primeira etapa e para a lógica dos exemplos exibidos na interface.

## Execuções

| Funcionalidade | Tipo | Comando | Resultado |
|---|---|---|---|
| Rotas `/api/hello`, `/api/health` e `/api/analyze` | API / regressão | `python3 -m unittest discover -s backend -p "test_*.py"` | 7 testes aprovados |
| Exemplos, validação de entrada e caracteres especiais | Unitário de frontend | `node --test frontend/test_app_core.js` | 4 testes aprovados |
| Sintaxe dos arquivos Python | Verificação estática | `python3 -m py_compile backend/app.py backend/test_app.py` | Aprovada |

## Casos cobertos

- recebimento de código válido;
- cálculo de linhas e caracteres;
- campo `codigo` ausente;
- requisição sem JSON;
- texto vazio ou composto apenas por espaços;
- caracteres especiais e acentuação;
- manutenção das rotas `hello` e `health` da primeira etapa;
- existência e conteúdo dos três exemplos;
- validação utilizada antes do envio pela interface.

## Limitações conhecidas

A análise léxica, sintática e semântica ainda não foi implementada, pois pertence às próximas etapas do projeto. Também não foi possível executar a construção dos contêineres neste ambiente específico porque o comando Docker não está instalado. Os Dockerfiles e o `docker-compose.yml` foram mantidos e atualizados para a execução em um ambiente com Docker.


| Elementos e contrato da interface | Teste de contrato | `python3 -m unittest frontend.test_interface -v` | 4 testes aprovados |

No total, foram aprovados 15 testes automatizados nesta etapa: 7 da API, 4 da lógica dos exemplos e 4 do contrato da interface.
