"""Nós da Árvore Sintática Abstrata do subconjunto didático de Python."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ASTNode:
    tipo: str
    linha: int
    coluna: int
    atributos: dict[str, Any] = field(default_factory=dict)
    filhos: list["ASTNode"] = field(default_factory=list)
    linha_final: int | None = None
    coluna_final: int | None = None

    def to_dict(self) -> dict[str, Any]:
        resultado: dict[str, Any] = {
            "tipo": self.tipo,
            "linha": self.linha,
            "coluna": self.coluna,
            "atributos": self.atributos,
            "filhos": [filho.to_dict() for filho in self.filhos],
        }
        if self.linha_final is not None:
            resultado["linhaFinal"] = self.linha_final
        if self.coluna_final is not None:
            resultado["colunaFinal"] = self.coluna_final
        return resultado


def node(tipo: str, token, atributos=None, filhos=None, ultimo=None) -> ASTNode:
    fim = ultimo or token
    return ASTNode(
        tipo=tipo,
        linha=token["linha"],
        coluna=token["coluna"],
        atributos=atributos or {},
        filhos=filhos or [],
        linha_final=fim["linha"],
        coluna_final=fim["coluna"] + len(fim["lexema"]) - 1,
    )
