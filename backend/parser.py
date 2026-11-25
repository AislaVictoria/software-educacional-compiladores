"""Parser descendente recursivo para o subconjunto documentado do projeto."""

from typing import Any

from syntax_ast import ASTNode, node


class ParseError(Exception):
    def __init__(self, token: dict[str, Any], esperado: str, mensagem: str):
        self.token = token
        self.esperado = esperado
        self.mensagem = mensagem
        super().__init__(mensagem)


class Parser:
    PRECEDENCIA = {"or": 1, "and": 2, "==": 3, "!=": 3, "<": 3, ">": 3, "<=": 3, ">=": 3, "+": 4, "-": 4, "*": 5, "/": 5, "//": 5, "%": 5, "**": 6}

    def __init__(self, tokens: list[dict[str, Any]]):
        self.tokens = tokens
        self.index = 0
        self.erros: list[dict[str, Any]] = []

    @property
    def atual(self) -> dict[str, Any] | None:
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def parse(self) -> tuple[ASTNode | None, list[dict[str, Any]]]:
        if not self.tokens:
            return ASTNode("PROGRAMA", 1, 1, filhos=[]), []
        filhos: list[ASTNode] = []
        while self.atual is not None:
            inicio = self.index

            try:
                if self.atual["coluna"] != 1:
                    token = self.atual

                    raise ParseError(
                        token,
                        "comando sem indentação",
                        f"Erro sintático na linha {token['linha']}, "
                        f"coluna {token['coluna']}: "
                        "indentação inesperada no nível principal."
                    )

                filhos.append(self.declaracao_ou_comando())
            except ParseError as erro:
                self.erros.append({
                    "tipo": "ERRO_SINTATICO",
                    "linha": erro.token["linha"], "coluna": erro.token["coluna"],
                    "encontrado": erro.token["lexema"], "esperado": [erro.esperado],
                    "mensagem": erro.mensagem,
                })
                self.sincronizar(inicio)
        primeiro = self.tokens[0]
        ultimo = self.tokens[-1]
        return (None if self.erros else node("PROGRAMA", primeiro, filhos=filhos, ultimo=ultimo)), self.erros


    def declaracao_ou_comando(self) -> ASTNode:
        inicio = self.atual

        if self.eh("PALAVRA_RESERVADA", "if"):
            return self.condicional()

        if self.eh("PALAVRA_RESERVADA", "return"):
            resultado = self.retorno()

        elif self.eh("PALAVRA_RESERVADA", "print"):
            resultado = self.chamada_print()

        elif self.eh("IDENTIFICADOR") and self.peek_lexema() == "=":
            resultado = self.atribuicao()

        else:
            expr = self.expressao()
            resultado = node(
                "EXPRESSAO",
                inicio,
                filhos=[expr],
                ultimo=self.tokens[self.index - 1]
            )

        if self.atual is not None and self.atual["linha"] == inicio["linha"]:
            token = self.atual
            raise ParseError(
                token,
                "fim da linha",
                f"Erro sintático na linha {token['linha']}, "
                f"coluna {token['coluna']}: era esperado o fim do comando."
            )

        return resultado

    def atribuicao(self) -> ASTNode:
        nome = self.consumir("IDENTIFICADOR", "identificador")
        self.consumir_lexema("=", "'='")
        valor = self.expressao()
        return node("ATRIBUICAO", nome, {"nome": nome["lexema"]}, [valor], self.tokens[self.index - 1])


    def chamada_print(self) -> ASTNode:
        inicio = self.consumir(
            "PALAVRA_RESERVADA", "'print'"
        )

        self.consumir_lexema("(", "'('")

        argumentos: list[ASTNode] = []

        if not self.eh_lexema(")"):
            argumentos.append(self.expressao())

            while self.eh_lexema(","):
                self.consumir_lexema(",", "','")
                argumentos.append(self.expressao())

        fim = self.consumir_lexema(")", "')'")

        return node(
            "CHAMADA_FUNCAO",
            inicio,
            {"nome": "print"},
            argumentos,
            fim
        )



    def retorno(self) -> ASTNode:
        token = self.atual

        raise ParseError(
            token,
            "comando suportado",
            f"Erro sintático na linha {token['linha']}, "
            f"coluna {token['coluna']}: "
            "'return' não é suportado nesta etapa, "
            "pois a declaração de funções ainda não foi implementada."
        )



    def condicional(self) -> ASTNode:
        inicio = self.consumir("PALAVRA_RESERVADA", "'if'")
        condicao = self.expressao()

        dois_pontos = self.consumir_lexema(
            ":", "':' após a condição"
        )

        corpo = self.bloco(inicio, dois_pontos)
        filhos = [condicao, corpo]

        if (
            self.eh("PALAVRA_RESERVADA", "else")
            and self.atual["coluna"] == inicio["coluna"]
        ):
            inicio_else = self.avancar()

            dois_pontos_else = self.consumir_lexema(
                ":", "':' após 'else'"
            )

            alternativo = self.bloco(
                inicio_else, dois_pontos_else
            )

            filhos.append(alternativo)

        return node(
            "CONDICIONAL",
            inicio,
            filhos=filhos,
            ultimo=self.tokens[self.index - 1]
        )

    def bloco(self, cabecalho, dois_pontos) -> ASTNode:
        primeiro = self.atual

        if (
            primeiro is None
            or primeiro["linha"] <= dois_pontos["linha"]
            or primeiro["coluna"] <= cabecalho["coluna"]
        ):
            token = primeiro or self.token_fim()

            raise ParseError(
                token,
                "bloco indentado",
                f"Erro sintático na linha {token['linha']}, "
                f"coluna {token['coluna']}: "
                "era esperado um bloco indentado após ':'."
            )

        indentacao = primeiro["coluna"]
        filhos = []

        while self.atual is not None:
            token = self.atual

            if token["coluna"] < indentacao:
                break

            if token["coluna"] > indentacao:
                raise ParseError(
                    token,
                    "indentação consistente",
                    f"Erro sintático na linha {token['linha']}, "
                    f"coluna {token['coluna']}: "
                    "indentação inesperada."
                )

            filhos.append(self.declaracao_ou_comando())

        return node(
            "BLOCO",
            primeiro,
            filhos=filhos,
            ultimo=self.tokens[self.index - 1]
        )


    def expressao(self, minimo: int = 0) -> ASTNode:
        inicio = self.atual
        esquerda = self.primaria()

        comparadores = {
            "==", "!=", "<", ">", "<=", ">="
        }

        comparacao_realizada = False

        while (
            self.atual is not None
            and self.atual["lexema"] in self.PRECEDENCIA
            and self.atual["linha"] == inicio["linha"]
        ):
            operador = self.atual["lexema"]
            precedencia = self.PRECEDENCIA[operador]

            if precedencia < minimo:
                break

            if operador in comparadores:
                if comparacao_realizada:
                    token = self.atual

                    raise ParseError(
                        token,
                        "comparação simples",
                        f"Erro sintático na linha {token['linha']}, "
                        f"coluna {token['coluna']}: "
                        "comparações encadeadas não são suportadas."
                    )

                comparacao_realizada = True

            elif operador in ("and", "or"):
                comparacao_realizada = False

            self.avancar()

            direita = self.expressao(
                precedencia if operador == "**"
                else precedencia + 1
            )

            esquerda = node(
                "OPERACAO_BINARIA",
                inicio,
                {
                    "operador": operador,
                    "regra": self.regra_operador(operador)
                },
                [esquerda, direita],
                self.tokens[self.index - 1]
            )

        return esquerda



    def primaria(self) -> ASTNode:
        token = self.atual

        if token is None:
            anterior = self.token_fim()

            raise ParseError(
                anterior,
                "expressão",
                f"Erro sintático na linha {anterior['linha']}, "
                f"coluna {anterior['coluna']}: "
                "o código terminou antes de completar uma expressão."
            )

        if self.index > 0:
            anterior = self.tokens[self.index - 1]

            continuadores = set(self.PRECEDENCIA) | {
                "=", "(", ",", "if"
            }

            if (
                anterior["lexema"] in continuadores
                and token["linha"] != anterior["linha"]
            ):
                raise ParseError(
                    token,
                    "expressão na mesma linha",
                    f"Erro sintático na linha {token['linha']}, "
                    f"coluna {token['coluna']}: "
                    "a expressão anterior está incompleta."
                )

        if token["tipo"] in ("LITERAL_INTEIRO", "LITERAL_REAL"):
            self.avancar()

            return node(
                token["tipo"],
                token,
                {"valor": token["lexema"]}
            )

        if token["tipo"] == "LITERAL_TEXTO":
            self.avancar()

            return node(
                "LITERAL_TEXTO",
                token,
                {"valor": token["lexema"]}
            )

        if token["tipo"] == "IDENTIFICADOR":
            self.avancar()

            return node(
                "IDENTIFICADOR",
                token,
                {"nome": token["lexema"]}
            )

        if token["tipo"] == "PALAVRA_RESERVADA":
            if token["lexema"] in ("True", "False"):
                self.avancar()

                return node(
                    "LITERAL_BOOLEANO",
                    token,
                    {"valor": token["lexema"]}
                )

            if token["lexema"] == "None":
                self.avancar()

                return node(
                    "LITERAL_NULO",
                    token,
                    {"valor": token["lexema"]}
                )

        if token["lexema"] == "(":
            self.avancar()

            expr = self.expressao()

            fim = self.consumir_lexema(
                ")", "')' para fechar a expressão"
            )

            return node(
                "AGRUPAMENTO",
                token,
                filhos=[expr],
                ultimo=fim
            )

        raise ParseError(
            token,
            "expressão",
            f"Erro sintático na linha {token['linha']}, "
            f"coluna {token['coluna']}: "
            "era esperada uma expressão, mas foi encontrado "
            f"'{token['lexema']}'."
        )


    def sincronizar(self, inicio: int) -> None:
        if self.index == inicio and self.atual is not None:
            linha = self.atual["linha"]
            while self.atual is not None and self.atual["linha"] == linha:
                self.avancar()
        while self.atual is not None and self.atual["linha"] == self.tokens[max(0, self.index - 1)]["linha"]:
            self.avancar()


    def consumir(self, tipo: str, esperado: str) -> dict[str, Any]:
        if self.atual is not None and self.atual["tipo"] == tipo:
            return self.avancar()

        token = self.atual or self.token_fim()

        raise ParseError(
            token,
            esperado,
            f"Erro sintático na linha {token['linha']}, "
            f"coluna {token['coluna']}: era esperado "
            f"{esperado}, mas foi encontrado '{token['lexema']}'."
        )



    def consumir_lexema(self, lexema: str, esperado: str) -> dict[str, Any]:
        if self.eh_lexema(lexema):
            token = self.atual

            if self.index > 0:
                anterior = self.tokens[self.index - 1]

                if token["linha"] != anterior["linha"]:
                    raise ParseError(
                        token,
                        esperado,
                        f"Erro sintático na linha {token['linha']}, "
                        f"coluna {token['coluna']}: "
                        f"{esperado} deve estar na mesma linha do comando."
                    )

            return self.avancar()

        token = self.atual or self.token_fim()

        raise ParseError(
            token,
            esperado,
            f"Erro sintático na linha {token['linha']}, "
            f"coluna {token['coluna']}: era esperado "
            f"{esperado}, mas foi encontrado '{token['lexema']}'."
        )


    def eh(self, tipo: str, lexema: str | None = None) -> bool:
        return self.atual is not None and self.atual["tipo"] == tipo and (lexema is None or self.atual["lexema"] == lexema)

    def eh_lexema(self, lexema: str) -> bool:
        return self.atual is not None and self.atual["lexema"] == lexema

    def peek_lexema(self) -> str | None:
        return self.tokens[self.index + 1]["lexema"] if self.index + 1 < len(self.tokens) else None


    def avancar(self) -> dict[str, Any]:
        token = self.atual
        self.index += 1
        return token


    def token_fim(self) -> dict[str, Any]:
        if not self.tokens:
            return {"lexema": "fim do código", "linha": 1, "coluna": 1}
        ultimo = self.tokens[-1]
        return {"lexema": "fim do código", "linha": ultimo["linha"], "coluna": ultimo["coluna"] + len(ultimo["lexema"])}

    @staticmethod
    def regra_operador(operador: str) -> str:
        if operador == "**":
            return "potencia → primaria ** potencia"

        if operador in ("*", "/", "//", "%"):
            return f"multiplicacao → multiplicacao {operador} potencia"

        if operador in ("+", "-"):
            return f"soma → soma {operador} multiplicacao"

        if operador == "and":
            return "logica_and → logica_and and comparacao"

        if operador == "or":
            return "logica_or → logica_or or logica_and"

        return f"comparacao → soma {operador} soma"




def parse_tokens(
    tokens: list[dict[str, Any]]
) -> tuple[dict[str, Any] | None, list[dict[str, Any]]]:

    LIMITE_TOKENS = 2000
    LIMITE_PROFUNDIDADE = 100

    def erro_complexidade(token, mensagem):
        return None, [{
            "tipo": "ERRO_SINTATICO",
            "linha": token["linha"],
            "coluna": token["coluna"],
            "encontrado": token["lexema"],
            "esperado": ["código de menor complexidade"],
            "mensagem": mensagem
        }]

    if len(tokens) > LIMITE_TOKENS:
        return erro_complexidade(
            tokens[LIMITE_TOKENS],
            f"O código excede o limite de {LIMITE_TOKENS} tokens."
        )

    profundidade = 0

    for token in tokens:
        if token["tipo"] != "DELIMITADOR":
            continue

        if token["lexema"] == "(":
            profundidade += 1

            if profundidade > LIMITE_PROFUNDIDADE:
                return erro_complexidade(
                    token,
                    "Limite de agrupamentos aninhados excedido."
                )

        elif token["lexema"] == ")":
            profundidade = max(0, profundidade - 1)

    parser = Parser(tokens)

    try:
        ast, erros = parser.parse()

        if ast is None:
            return None, erros

        pilha = [(ast, 1)]

        while pilha:
            no, nivel = pilha.pop()

            if nivel > LIMITE_PROFUNDIDADE:
                return erro_complexidade(
                    {
                        "linha": no.linha,
                        "coluna": no.coluna,
                        "lexema": no.tipo
                    },
                    "A árvore sintática excede o limite "
                    "de profundidade permitido."
                )

            for filho in no.filhos:
                pilha.append((filho, nivel + 1))

        return ast.to_dict(), erros

    except RecursionError:
        token = parser.atual or parser.token_fim()

        return erro_complexidade(
            token,
            "O código possui uma estrutura muito complexa "
            "para o analisador sintático."
        )
