import math

import pytest

from src.red_black_tree import BLACK, RED, RedBlackTree


def assert_red_black_properties(tree: RedBlackTree):
    assert tree.validate_properties(), "A árvore violou uma propriedade rubro-negra."


def test_arvore_inicia_vazia():
    tree = RedBlackTree()

    assert tree.is_empty()
    assert tree.node_count == 0
    assert tree.value_count == 0
    assert tree.in_order() == []
    assert tree.min() is None
    assert tree.max() is None
    assert_red_black_properties(tree)


def test_primeira_insercao_cria_raiz_preta():
    tree = RedBlackTree()

    node = tree.insert("2026-06-20", "L001")

    assert tree.root is node
    assert tree.root.color == BLACK
    assert tree.root.key == "2026-06-20"
    assert tree.search("2026-06-20") == ["L001"]
    assert_red_black_properties(tree)


def test_insercao_mantem_chaves_em_ordem():
    tree = RedBlackTree()
    keys = [
        "2026-08-10",
        "2026-06-20",
        "2026-07-01",
        "2026-05-15",
        "2026-09-30",
    ]

    for key in keys:
        tree.insert(key, f"lote-{key}")

    assert tree.keys() == sorted(keys)
    assert tree.in_order_values() == [f"lote-{key}" for key in sorted(keys)]
    assert_red_black_properties(tree)


def test_busca_retorna_lista_vazia_para_chave_inexistente():
    tree = RedBlackTree()
    tree.insert("2026-06-20", "L001")

    assert tree.search("2026-01-01") == []
    assert not tree.contains("2026-01-01")
    assert_red_black_properties(tree)


def test_chaves_duplicadas_sao_armazenadas_no_mesmo_no():
    tree = RedBlackTree()

    tree.insert("2026-06-20", "L001")
    tree.insert("2026-06-20", "L002")
    tree.insert("2026-06-20", "L003")

    assert tree.node_count == 1
    assert tree.value_count == 3
    assert tree.search("2026-06-20") == ["L001", "L002", "L003"]
    assert_red_black_properties(tree)


def test_min_e_max_retornam_lotes_com_menor_e_maior_validade():
    tree = RedBlackTree()
    tree.insert("2026-08-10", "L003")
    tree.insert("2026-06-20", "L001")
    tree.insert("2026-12-01", "L004")
    tree.insert("2026-07-01", "L002")

    assert tree.min() == ("2026-06-20", ["L001"])
    assert tree.max() == ("2026-12-01", ["L004"])
    assert_red_black_properties(tree)


def test_rotacao_esquerda_atualiza_raiz_e_pais_corretamente():
    tree = RedBlackTree()
    root = tree.insert(10, "raiz")
    right = tree.insert(20, "direita")

    tree.left_rotate(root)

    assert tree.root is right
    assert right.left is root
    assert root.parent is right
    assert tree.root.parent is tree.nil


def test_rotacao_direita_atualiza_raiz_e_pais_corretamente():
    tree = RedBlackTree()
    root = tree.insert(20, "raiz")
    left = tree.insert(10, "esquerda")

    tree.right_rotate(root)

    assert tree.root is left
    assert left.right is root
    assert root.parent is left
    assert tree.root.parent is tree.nil


def test_rotacao_invalida_lanca_erro():
    tree = RedBlackTree()
    root = tree.insert(10, "raiz")

    with pytest.raises(ValueError):
        tree.left_rotate(root)

    with pytest.raises(ValueError):
        tree.right_rotate(root)


def test_insercao_com_muitos_elementos_mantem_propriedades_rubro_negras():
    tree = RedBlackTree()
    keys = [41, 38, 31, 12, 19, 8, 55, 60, 1, 5, 30, 32, 70, 65]

    for key in keys:
        tree.insert(key, f"valor-{key}")
        assert tree.root.color == BLACK
        assert_red_black_properties(tree)

    assert tree.keys() == sorted(keys)


def test_altura_permanece_logaritmica_para_insercoes_ordenadas():
    tree = RedBlackTree()
    total = 100

    for key in range(1, total + 1):
        tree.insert(key, f"valor-{key}")

    # Uma árvore rubro-negra com n nós possui altura limitada por 2*log(n+1).
    limite_teorico = 2 * math.log2(total + 1)

    assert tree.height() <= math.ceil(limite_teorico)
    assert tree.keys() == list(range(1, total + 1))
    assert_red_black_properties(tree)
