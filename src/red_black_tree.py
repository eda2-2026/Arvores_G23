"""
Implementação de Árvore Rubro-Negra para indexação de lotes de estoque.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional, Tuple

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

    def search_node(self, key: Any) -> Optional[RedBlackNode]:
        """Busca e retorna o nó de uma chave, ou None se não encontrar."""
        current = self.root

        while current is not self.nil:
            if key == current.key:
                return current
            if key < current.key:
                current = current.left
            else:
                current = current.right

        return None

    def search(self, key: Any) -> List[Any]:
        """Retorna todos os valores associados à chave informada."""
        node = self.search_node(key)
        if node is None:
            return []
        return list(node.values)

    def contains(self, key: Any) -> bool:
        """Retorna True se a chave existir na árvore."""
        return self.search_node(key) is not None

    def in_order(self) -> List[Tuple[Any, List[Any]]]:
        """Retorna uma lista de pares (chave, valores) em ordem crescente."""
        result: List[Tuple[Any, List[Any]]] = []
        self._in_order(self.root, result)
        return result

    def _in_order(self, node: RedBlackNode, result: List[Tuple[Any, List[Any]]]) -> None:
        if node is self.nil:
            return

        self._in_order(node.left, result)
        result.append((node.key, list(node.values)))
        self._in_order(node.right, result)

    def in_order_values(self) -> List[Any]:
        """Retorna todos os valores na ordem crescente das chaves."""
        values: List[Any] = []
        for _, node_values in self.in_order():
            values.extend(node_values)
        return values

    def keys(self) -> List[Any]:
        """Retorna todas as chaves distintas em ordem crescente."""
        return [key for key, _ in self.in_order()]

    def minimum_node(self, start: Optional[RedBlackNode] = None) -> Optional[RedBlackNode]:
        """Retorna o nó de menor chave a partir de start, ou da raiz."""
        current = self.root if start is None else start
        if current is self.nil:
            return None

        while current.left is not self.nil:
            current = current.left

        return current

    def maximum_node(self, start: Optional[RedBlackNode] = None) -> Optional[RedBlackNode]:
        """Retorna o nó de maior chave a partir de start, ou da raiz."""
        current = self.root if start is None else start
        if current is self.nil:
            return None

        while current.right is not self.nil:
            current = current.right

        return current

    def min(self) -> Optional[Tuple[Any, List[Any]]]:
        """Retorna o par (menor chave, valores), ou None se a árvore estiver vazia."""
        node = self.minimum_node()
        if node is None:
            return None
        return node.key, list(node.values)

    def max(self) -> Optional[Tuple[Any, List[Any]]]:
        """Retorna o par (maior chave, valores), ou None se a árvore estiver vazia."""
        node = self.maximum_node()
        if node is None:
            return None
        return node.key, list(node.values)

    def height(self) -> int:
        """Retorna a altura da árvore, onde uma árvore vazia possui altura 0,
        enquanto uma árvore apenas com a raiz possui altura 1."""
        return self._height(self.root)

    def _height(self, node: RedBlackNode) -> int:
        if node is self.nil:
            return 0
        return 1 + max(self._height(node.left), self._height(node.right))

    def validate_properties(self) -> bool:
        """Valida as propriedades de uma árvore rubro-negra:
        1. Todo nó é vermelho ou preto.
        2. A raiz é preta.
        3. Todo NIL é preto.
        4. Nó vermelho não possui filho vermelho.
        5. Todo caminho até NIL possui a mesma quantidade de nós pretos.
        """
        if self.nil.color != BLACK:
            return False

        if self.root is self.nil:
            return True

        if self.root.color != BLACK:
            return False

        try:
            self._validate_node(self.root, min_key=None, max_key=None)
        except AssertionError:
            return False

        return True

    def _validate_node(self, node: RedBlackNode, min_key: Any, max_key: Any) -> int:
        if node is self.nil:
            return 1

        assert node.color in (RED, BLACK)

        if min_key is not None:
            assert node.key > min_key
        if max_key is not None:
            assert node.key < max_key

        if node.color == RED:
            assert node.left.color == BLACK
            assert node.right.color == BLACK

        left_black_height = self._validate_node(node.left, min_key, node.key)
        right_black_height = self._validate_node(node.right, node.key, max_key)

        assert left_black_height == right_black_height

        return left_black_height + (1 if node.color == BLACK else 0)

    def bulk_insert(self, pairs: Iterable[Tuple[Any, Any]]) -> None:
        """Insere vários pares (chave, valor) na árvore."""
        for key, value in pairs:
            self.insert(key, value)
