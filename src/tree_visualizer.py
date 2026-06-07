"""
Visualização textual da Árvore Rubro-Negra.
"""

from __future__ import annotations

from typing import List

from src.red_black_tree import BLACK, RedBlackNode, RedBlackTree


def _color_label(node: RedBlackNode) -> str:
    """Retorna a abreviação da cor do nó para a visualização."""
    return "B" if node.color == BLACK else "R"


def _format_node(node: RedBlackNode) -> str:
    """Formata um nó real da árvore para exibição textual."""
    total_values = len(node.values)
    lote_label = "lote" if total_values == 1 else "lotes"
    return f"{node.key}({_color_label(node)}, {total_values} {lote_label})"


def render_tree(tree: RedBlackTree, max_depth: int = 4, show_nil: bool = False) -> str:
    """Gera uma representação textual da Árvore Rubro-Negra.

    Args:
        tree: árvore rubro-negra que será visualizada.
        max_depth: profundidade máxima exibida (esse limite evita uma saída muito grande quando a árvore tem muitos nós).
        show_nil: quando True, exibe os nós NIL pretos nas folhas.

    Returns:
        Uma string com a estrutura da árvore em formato textual.
    """
    if tree.is_empty():
        return "Árvore vazia."

    if max_depth < 0:
        raise ValueError("A profundidade máxima não pode ser negativa.")

    lines: List[str] = [_format_node(tree.root)]
    _render_children(
        tree=tree,
        node=tree.root,
        prefix="",
        depth=1,
        max_depth=max_depth,
        show_nil=show_nil,
        lines=lines,
    )
    return "\n".join(lines)


def _render_children(
    tree: RedBlackTree,
    node: RedBlackNode,
    prefix: str,
    depth: int,
    max_depth: int,
    show_nil: bool,
    lines: List[str],
) -> None:
    """Adiciona os filhos de um nó à lista de linhas da visualização."""
    children = []

    if node.left is not tree.nil:
        children.append(("E", node.left))
    elif show_nil:
        children.append(("E", tree.nil))

    if node.right is not tree.nil:
        children.append(("D", node.right))
    elif show_nil:
        children.append(("D", tree.nil))

    for index, (side, child) in enumerate(children):
        is_last = index == len(children) - 1
        connector = "└── " if is_last else "├── "
        next_prefix = prefix + ("    " if is_last else "│   ")

        if child is tree.nil:
            lines.append(f"{prefix}{connector}{side}: NIL(B)")
            continue

        if depth > max_depth:
            lines.append(f"{prefix}{connector}{side}: ...")
            continue

        lines.append(f"{prefix}{connector}{side}: {_format_node(child)}")
        _render_children(
            tree=tree,
            node=child,
            prefix=next_prefix,
            depth=depth + 1,
            max_depth=max_depth,
            show_nil=show_nil,
            lines=lines,
        )
