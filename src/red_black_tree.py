"""
Implementação de Árvore Rubro-Negra para indexação de lotes de estoque.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

RED = "RED"
BLACK = "BLACK"


@dataclass
class RedBlackNode:
    """Nó da árvore rubro-negra.

    Attributes:
        key: chave usada para ordenar o nó na árvore.
        values: lista de valores associados à chave.
        color: cor do nó, RED (vermelho) ou BLACK (preto).
        left: filho esquerdo.
        right: filho direito.
        parent: nó pai.
    """

    key: Any
    values: List[Any] = field(default_factory=list)
    color: str = RED
    left: Optional["RedBlackNode"] = None
    right: Optional["RedBlackNode"] = None
    parent: Optional["RedBlackNode"] = None

    def __repr__(self) -> str:
        return f"RedBlackNode(key={self.key!r}, color={self.color}, values={len(self.values)})"


class RedBlackTree:
    """Árvore Rubro-Negra com suporte a valores duplicados por chave."""

    def __init__(self) -> None:
        self.nil = RedBlackNode(key=None, values=[], color=BLACK)
        self.nil.left = self.nil
        self.nil.right = self.nil
        self.nil.parent = self.nil

        self.root: RedBlackNode = self.nil
        self._node_count = 0
        self._value_count = 0

    def is_empty(self) -> bool:
        """Retorna True se a árvore não possui nós reais."""
        return self.root is self.nil

    @property
    def node_count(self) -> int:
        """Quantidade de chaves distintas armazenadas na árvore."""
        return self._node_count

    @property
    def value_count(self) -> int:
        """Quantidade total de valores armazenados, incluindo chaves repetidas."""
        return self._value_count
