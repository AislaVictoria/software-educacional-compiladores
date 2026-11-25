# Fluxograma do software educacional

## Fluxo de processamento — Etapa 4

```mermaid
flowchart TD
    A[Estudante insere ou seleciona código] --> B[Validação no frontend]
    B --> C{Entrada válida?}
    C -- Não --> D[Exibe mensagem de entrada inválida]
    C -- Sim --> E[POST /api/analyze]
    E --> F[Validação no backend]
    F --> G{Entrada e tamanho válidos?}
    G -- Não --> H[Retorna erro HTTP em JSON]
    G -- Sim --> I[Scanner léxico]
    I --> J{Existem erros léxicos?}
    J -- Sim --> K[Retorna tokens e erros léxicos]
    J -- Não --> L[Verifica limites e executa parser]
    L --> M{Análise sintática bem-sucedida?}
    M -- Não --> N[Retorna tokens e erros sintáticos]
    M -- Sim --> O[Serializa AST com posições]
    O --> P[Exibe tokens e AST hierárquica]
    K --> Q[Exibe tokens e diagnóstico léxico]
    N --> R[Exibe tokens e diagnóstico sintático]
    H --> S[Exibe mensagem de validação]
```

## Descrição

O frontend recebe o código-fonte, valida a entrada e
envia uma requisição HTTP ao backend.

O backend verifica novamente a entrada e os limites
de processamento.

O scanner identifica os tokens e registra os erros
léxicos. Caso existam erros léxicos, o parser não
é executado.

Na ausência de erros léxicos, os tokens são encaminhados
ao parser, que verifica as construções gramaticais
e constrói a Árvore Sintática Abstrata.

Quando existem erros sintáticos, a aplicação apresenta
os tokens e os diagnósticos, sem disponibilizar a AST.

Quando a análise é bem-sucedida, a interface apresenta
a tabela de tokens e a AST hierárquica, com posições,
regras gramaticais e controles de expansão e recolhimento.

## Arquitetura

```mermaid
flowchart LR
    A[Navegador] --> B[Frontend Nginx]
    B --> C[Backend Flask]
    C --> D[Scanner]
    D --> E[Parser]
    E --> F[AST]
    F --> C
    C --> B
    B --> A
```

O frontend e o backend são executados em contêineres
gerenciados pelo Docker Compose.

O processamento é determinístico e independente de
serviços externos de inteligência artificial.

A análise semântica será incorporada na Etapa 5.
