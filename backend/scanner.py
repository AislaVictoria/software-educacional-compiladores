"""Scanner léxico para o subconjunto didático de Python do projeto."""

from dataclasses import dataclass, asdict
from typing import Any


KEYWORDS = {
    "and", "else", "False", "if", "in", "is", "None", "not", "or",
    "print", "return", "True", "while",
}

OPERATORS = (
    "**=", "//=", "+=", "-=", "*=", "/=", "%=", "**", "//",
    "==", "!=", "<=", ">=", "+", "-", "*", "/", "%", "=", "<", ">",
)
DELIMITERS = set("()[]{}.,:;")


@dataclass(frozen=True)
class Token:
    tipo: str
    lexema: str
    linha: int
    coluna: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LexicalError:
    tipo: str
    lexema: str
    linha: int
    coluna: int
    mensagem: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Scanner:
    """Percorre o código caractere a caractere e produz tokens e erros."""

    def __init__(self, source: str):
        self.source = source
        self.length = len(source)
        self.index = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []
        self.errors: list[LexicalError] = []

    def scan(self) -> tuple[list[Token], list[LexicalError]]:
        while not self.at_end:
            character = self.current
            if character in " \t\r":
                self.advance()
            elif character == "\n":
                self.advance_line()
            elif character == "#":
                self.skip_comment()
            elif character.isalpha() or character == "_":
                self.scan_identifier()
            elif character.isdigit():
                self.scan_number()
            elif character in "'\"":
                self.scan_string()
            elif self.scan_operator():
                pass
            elif character in DELIMITERS:
                self.add_token("DELIMITADOR", character)
                self.advance()
            else:
                self.add_error(character, "Caractere não reconhecido")
                self.advance()
        return self.tokens, self.errors

    @property
    def at_end(self) -> bool:
        return self.index >= self.length

    @property
    def current(self) -> str:
        return "" if self.at_end else self.source[self.index]

    def peek(self, offset: int = 1) -> str:
        position = self.index + offset
        return "" if position >= self.length else self.source[position]

    def advance(self) -> str:
        character = self.current
        self.index += 1
        self.column += 1
        return character

    def advance_line(self) -> None:
        self.index += 1
        self.line += 1
        self.column = 1

    def add_token(self, token_type: str, lexeme: str, line: int | None = None, column: int | None = None) -> None:
        self.tokens.append(Token(token_type, lexeme, line or self.line, column or self.column))

    def add_error(self, lexeme: str, reason: str, line: int | None = None, column: int | None = None) -> None:
        error_line = line or self.line
        error_column = column or self.column
        self.errors.append(LexicalError(
            "ERRO_LEXICO", lexeme, error_line, error_column,
            f"Erro léxico na linha {error_line}, coluna {error_column}: {reason} '{lexeme}'. "
            "Verifique se o trecho faz parte do subconjunto suportado.",
        ))

    def skip_comment(self) -> None:
        while not self.at_end and self.current != "\n":
            self.advance()

    def scan_identifier(self) -> None:
        start_line, start_column = self.line, self.column
        start = self.index
        while self.current.isalnum() or self.current == "_":
            self.advance()
        lexeme = self.source[start:self.index]
        token_type = "PALAVRA_RESERVADA" if lexeme in KEYWORDS else "IDENTIFICADOR"
        self.add_token(token_type, lexeme, start_line, start_column)

    def scan_number(self) -> None:
        start_line, start_column = self.line, self.column
        start = self.index
        while self.current.isdigit():
            self.advance()
        token_type = "LITERAL_INTEIRO"
        if self.current == ".":
            if self.peek().isdigit():
                token_type = "LITERAL_REAL"
                self.advance()
                while self.current.isdigit():
                    self.advance()
            else:
                lexeme = self.source[start:self.index + 1]
                self.add_error(lexeme, "Literal numérico malformado", start_line, start_column)
                self.advance()
                return
        self.add_token(token_type, self.source[start:self.index], start_line, start_column)

    def scan_string(self) -> None:
        start_line, start_column = self.line, self.column
        quote = self.current
        start = self.index
        self.advance()
        escaped = False
        while not self.at_end:
            character = self.current
            if character == "\n" and not escaped:
                lexeme = self.source[start:self.index]
                self.add_error(lexeme, "Literal de texto não fechado", start_line, start_column)
                self.advance_line()
                return
            if character == quote and not escaped:
                self.advance()
                self.add_token("LITERAL_TEXTO", self.source[start:self.index], start_line, start_column)
                return
            if character == "\\" and not escaped:
                escaped = True
            else:
                escaped = False
            self.advance()
        lexeme = self.source[start:self.index]
        self.add_error(lexeme, "Literal de texto não fechado", start_line, start_column)

    def scan_operator(self) -> bool:
        for operator in OPERATORS:
            if self.source.startswith(operator, self.index):
                start_line, start_column = self.line, self.column
                for _ in operator:
                    self.advance()
                self.add_token("OPERADOR", operator, start_line, start_column)
                return True
        return False


def tokenize(source: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    tokens, errors = Scanner(source).scan()
    return [token.to_dict() for token in tokens], [error.to_dict() for error in errors]
