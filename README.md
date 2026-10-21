# Laboratório de Linguagens

## Trabalho 1 — Primeira etapa do projeto

Este repositório apresenta a primeira etapa do meu software educacional: um ambiente inicial para estudar como uma linguagem de programação é analisada. Nesta fase, o objetivo principal não é entregar um analisador completo, e sim construir uma base organizada, reproduzível e preparada para receber as próximas funcionalidades.

## 1\. Escolha da linguagem e do subconjunto inicial

Para o projeto, escolhi a linguagem **Python** como linguagem de programação a ser analisada nas próximas etapas. A escolha foi feita porque Python tem uma sintaxe relativamente simples e bastante legível, o que facilita a explicação dos conceitos de análise léxica, sintática e semântica. Além disso, é uma linguagem muito utilizada tanto no ensino quanto no mercado, tornando o projeto mais próximo de situações reais de aprendizagem.

O subconjunto inicial planejado será pequeno e progressivo. Primeiro, serão trabalhados:

* declaração e atribuição de variáveis;
* tipos básicos, como números, textos e valores booleanos;
* operadores aritméticos e relacionais;
* estruturas condicionais (`if` e `else`);
* comandos simples de saída, como `print()`.

Decidi começar dessa forma porque tentar analisar toda a linguagem Python logo no início deixaria o projeto muito amplo e difícil de validar. Com um subconjunto bem delimitado, será possível implementar cada etapa com mais cuidado e explicar os resultados de maneira compreensível para quem está aprendendo.

## 2\. Estrutura do repositório

```text
trabalho-1/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.js
│   ├── index.html
│   ├── nginx.conf
│   ├── styles.css
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

O **frontend** é responsável pela interface que o usuário acessa. O **backend** disponibiliza as rotas da aplicação e, nesta primeira versão, responde à mensagem de teste e a uma rota de saúde. A separação entre as duas partes foi feita desde o começo para deixar o projeto mais organizado e facilitar sua evolução.

## 3\. Tecnologias utilizadas

* Python 3.12;
* Flask, para a criação do backend;
* HTML, CSS e JavaScript, para a interface;
* Nginx, para servir o frontend e encaminhar as chamadas da API;
* Docker e Docker Compose, para padronizar o ambiente.

Não incluí banco de dados nesta etapa porque ainda não existe uma funcionalidade que precise armazenar informações. Essa decisão evita complexidade desnecessária e mantém o foco na estrutura inicial do sistema.

## 4\. Como executar o projeto

### Pré-requisitos

É necessário ter instalado:

* Docker 24 ou superior;
* Docker Compose v2 ou superior, normalmente disponível pelo comando `docker compose`;
* Git, caso o repositório seja clonado do GitHub.

### Inicialização

Na pasta raiz do projeto, execute:

```bash
docker compose up --build
```

Depois, abra no navegador:

```text
http://localhost:8080
```

Ao acessar http://localhost:8080, a aplicação apresenta a interface do Laboratório de Linguagens, com editor de código Python, exemplos e botão para solicitar análise. A comunicação entre frontend e backend pode ser verificada pela rota /api/hello, que retorna a mensagem “Hello, World!”, e pela rota /api/analyze, responsável por receber e validar o código-fonte enviado.

### Encerramento

Para parar os serviços sem remover os contêineres, use `Ctrl + C`. Para derrubar os contêineres criados pelo Compose, execute:

```bash
docker compose down
```

Se for necessário reconstruir as imagens depois de alguma alteração, use novamente:

```bash
docker compose up --build
```

## 5\. Rotas disponíveis no backend

* `GET /api/hello`: retorna a mensagem de teste da aplicação;
* `GET /api/health`: informa se o backend está funcionando corretamente.

## 6\. Validação da instalação limpa

A validação deve ser feita em uma máquina ou ambiente que não tenha dependências específicas deste projeto instaladas. O procedimento é:

1. clonar o repositório;
2. entrar na pasta do projeto;
3. executar `docker compose up --build`;
4. acessar `http://localhost:8080`;
5. confirmar a exibição de “Hello, World!”;
6. executar `docker compose down` ao finalizar.

A configuração foi preparada para que não seja necessário instalar Flask, Nginx ou outras dependências diretamente na máquina do usuário. Essas dependências são instaladas e executadas dentro dos contêineres, o que torna o processo mais previsível.

## 7\. Repositório e acompanhamento

O projeto deve ser publicado em um repositório do GitHub e compartilhado com o professor **rocha3runo**, conforme a orientação da disciplina. Depois da publicação, o link do repositório deve ser informado no local indicado pelo professor.

## Considerações finais

Esta primeira etapa representa a fundação do projeto. Mesmo que a aplicação ainda seja simples, ela já possui uma divisão clara entre frontend e backend, uma configuração reproduzível com Docker e uma documentação que explica como começar e como encerrar a execução. A partir dessa base, as próximas etapas poderão se concentrar na implementação do analisador educacional, sem que seja necessário reorganizar toda a estrutura do sistema.



# Trabalho 2 — Interface Web e entrada de código-fonte

## O que foi acrescentado

Nesta segunda etapa, a tela inicial foi transformada em uma interface de entrada para o analisador educacional. O usuário consegue escrever ou colar um programa em Python, editar o conteúdo, escolher um exemplo pronto e solicitar o recebimento do código pelo backend.

A proposta continua sendo trabalhar inicialmente com variáveis, tipos básicos, operadores aritméticos e estruturas condicionais. A análise léxica, sintática e semântica ainda não é executada: neste momento, o sistema valida a entrada, registra algumas informações simples e deixa o código preparado para as próximas etapas.

## Exemplos disponíveis

A interface oferece três exemplos:

1. **Variáveis e tipos básicos** — apresenta atribuições de texto, número e valor booleano.
2. **Operações aritméticas** — apresenta soma, multiplicação e armazenamento de um resultado.
3. **Estrutura condicional** — apresenta `if`, `else` e uma decisão baseada em uma nota.

Ao escolher um exemplo, seu conteúdo é carregado no editor, mas continua totalmente editável. Assim, o estudante pode observar o código, modificar alguma parte e só depois solicitar o processamento.

## Comunicação entre frontend e backend

O frontend envia o código para o backend por meio de uma requisição HTTP `POST` para `/api/analyze`, usando JSON:

```json
{
  "codigo": "numero = 10\\\\nprint(numero)"
}
```

Em caso de sucesso, o backend responde com:

```json
{
  "success": true,
  "message": "Código recebido com sucesso. A análise será implementada nas próximas etapas.",
  "recebido": true,
  "estatisticas": {
    "caracteres": 25,
    "linhas": 2
  }
}
```

A API também trata entrada ausente, corpo que não seja JSON e código vazio. O frontend repete a validação antes do envio para dar uma resposta mais rápida, mas o backend mantém sua própria validação para não depender apenas da interface.

## Mensagens para o usuário

As mensagens foram separadas por situação: aviso para código vazio ou inválido, sucesso para código recebido e erro de comunicação quando o servidor não pode ser acessado. As mensagens não exibem caminhos internos, rastreamentos ou informações técnicas desnecessárias para o estudante.

## Testes automatizados

Os testes podem ser executados na raiz do projeto com:

```bash
python3 -m unittest discover -s backend -p "test\_\*.py"
node --test frontend/test\_app\_core.js
```

O registro detalhado dos testes está em [`docs-testes-trabalho-2.md`](docs-testes-trabalho-2.md). Os testes cobrem o novo endpoint, os casos inválidos, os caracteres especiais, os exemplos e a regressão das rotas que já existiam na primeira etapa.
