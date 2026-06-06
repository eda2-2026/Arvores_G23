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

    def left_rotate(self, x: RedBlackNode) -> None:
        """Executa rotação à esquerda no nó informado."""
        y = x.right
        if y is self.nil:
            raise ValueError("Não é possível rotacionar à esquerda sem filho direito.")

        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, y: RedBlackNode) -> None:
        """Executa rotação à direita no nó informado."""
        x = y.left
        if x is self.nil:
            raise ValueError("Não é possível rotacionar à direita sem filho esquerdo.")

        y.left = x.right
        if x.right is not self.nil:
            x.right.parent = y

        x.parent = y.parent
        if y.parent is self.nil:
            self.root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x

        x.right = y
        y.parent = x

    def insert(self, key: Any, value: Any = None) -> RedBlackNode:
        """Insere uma chave/valor na árvore e retorna o nó afetado.

        Se a chave já existir, o valor é apenas anexado à lista do nó existente.
        Nesse caso não há alteração estrutural nem necessidade de balanceamento.
        """
        parent = self.nil
        current = self.root

        while current is not self.nil:
            parent = current
            if key == current.key:
                current.values.append(value)
                self._value_count += 1
                return current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = RedBlackNode(
            key=key,
            values=[value],
            color=RED,
            left=self.nil,
            right=self.nil,
            parent=parent,
        )

        if parent is self.nil:
            self.root = new_node
        elif key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        self._node_count += 1
        self._value_count += 1
        self._insert_fixup(new_node)
        return new_node

    def _insert_fixup(self, node: RedBlackNode) -> None:
        """Restaura as propriedades da árvore após uma inserção."""
        while node.parent.color == RED:
            grandparent = node.parent.parent

            if node.parent is grandparent.left:
                uncle = grandparent.right

                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    node = grandparent
                else:
                    if node is node.parent.right:
                        node = node.parent
                        self.left_rotate(node)

                    node.parent.color = BLACK
                    grandparent.color = RED
                    self.right_rotate(grandparent)
            else:
                uncle = grandparent.left

                if uncle.color == RED:
                    node.parent.color = BLACK
                    uncle.color = BLACK
                    grandparent.color = RED
                    node = grandparent
                else:
                    if node is node.parent.left:
                        node = node.parent
                        self.right_rotate(node)

                    node.parent.color = BLACK
                    grandparent.color = RED
                    self.left_rotate(grandparent)

        self.root.color = BLACK
        self.root.parent = self.nil
