"""
Testes do InventoryService.

Cobre:
- Carregamento dos dados mock
- Listagem em ordem de validade (FEFO)
- Busca por validade específica
- Lote mais próximo do vencimento
- Inserção de novo item
- Listagem de próximos vencimentos
"""

import sys
import os

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.inventory_service import InventoryService
from src.models import StockItem


# ---------------------------------------------------------------------------
# Fixture: serviço carregado com dados mock reais
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def svc_carregado():
    """Cria e carrega o InventoryService uma única vez por módulo."""
    service = InventoryService()
    service.load_from_file()
    return service


# ---------------------------------------------------------------------------
# Fixture: serviço vazio para testes de escrita isolados
# ---------------------------------------------------------------------------

@pytest.fixture()
def svc_vazio():
    return InventoryService()


# ---------------------------------------------------------------------------
# Testes de carregamento
# ---------------------------------------------------------------------------

class TestCarregamento:
    def test_carrega_todos_os_itens(self, svc_carregado):
        """O serviço deve carregar exatamente 52.000 itens do mock."""
        assert svc_carregado.total_lotes == 52_000

    def test_datas_distintas_dentro_do_esperado(self, svc_carregado):
        """O número de datas distintas deve ser <= total de itens e >= 1."""
        assert 1 <= svc_carregado.total_datas_distintas <= svc_carregado.total_lotes

    def test_arvore_nao_vazia_apos_carga(self, svc_carregado):
        assert not svc_carregado._tree.is_empty()

    def test_altura_arvore_logaritmica(self, svc_carregado):
        """Altura de uma RBT com n nós deve ser <= 2*log2(n+1)."""
        import math
        n = svc_carregado.total_datas_distintas
        altura_max = int(2 * math.log2(n + 1)) + 1
        assert svc_carregado.altura_arvore <= altura_max


# ---------------------------------------------------------------------------
# Testes de ordenação
# ---------------------------------------------------------------------------

class TestListagemPorValidade:
    def test_lista_em_ordem_crescente(self, svc_carregado):
        """listar_por_validade() deve retornar itens com validade não decrescente."""
        itens = svc_carregado.listar_por_validade()
        datas = [item.validade for item in itens]
        assert datas == sorted(datas)

    def test_lista_retorna_todos_os_itens(self, svc_carregado):
        itens = svc_carregado.listar_por_validade()
        assert len(itens) == svc_carregado.total_lotes

    def test_primeiro_item_e_o_de_menor_validade(self, svc_carregado):
        itens = svc_carregado.listar_por_validade()
        menor_validade, _ = svc_carregado.lote_mais_proximo_do_vencimento()
        assert itens[0].validade == menor_validade


# ---------------------------------------------------------------------------
# Testes de busca por validade
# ---------------------------------------------------------------------------

class TestBuscaPorValidade:
    def test_busca_validade_existente_retorna_lista(self, svc_carregado):
        # Pega a primeira validade real da árvore
        validade_min, _ = svc_carregado.lote_mais_proximo_do_vencimento()
        resultado = svc_carregado.buscar_por_validade(validade_min)
        assert isinstance(resultado, list)
        assert len(resultado) >= 1

    def test_todos_os_itens_tem_a_validade_buscada(self, svc_carregado):
        validade_min, _ = svc_carregado.lote_mais_proximo_do_vencimento()
        for item in svc_carregado.buscar_por_validade(validade_min):
            assert item.validade == validade_min

    def test_busca_validade_inexistente_retorna_vazio(self, svc_carregado):
        resultado = svc_carregado.buscar_por_validade("1900-01-01")
        assert resultado == []

    def test_todos_os_itens_sao_stock_item(self, svc_carregado):
        validade_min, _ = svc_carregado.lote_mais_proximo_do_vencimento()
        for item in svc_carregado.buscar_por_validade(validade_min):
            assert isinstance(item, StockItem)


# ---------------------------------------------------------------------------
# Testes do lote mais próximo do vencimento
# ---------------------------------------------------------------------------

class TestLoteMaisProximo:
    def test_retorna_tupla_nao_nula(self, svc_carregado):
        resultado = svc_carregado.lote_mais_proximo_do_vencimento()
        assert resultado is not None

    def test_retorna_menor_validade_da_arvore(self, svc_carregado):
        validade, itens = svc_carregado.lote_mais_proximo_do_vencimento()
        todas = svc_carregado.listar_por_validade()
        assert validade == todas[0].validade

    def test_retorna_none_em_estoque_vazio(self, svc_vazio):
        assert svc_vazio.lote_mais_proximo_do_vencimento() is None


# ---------------------------------------------------------------------------
# Testes de inserção
# ---------------------------------------------------------------------------

class TestInsercao:
    def test_insere_novo_item(self, svc_vazio):
        antes = svc_vazio.total_lotes
        svc_vazio.adicionar_item(
            nome="Garrafa de água 500ml",
            lote="L999999",
            quantidade=10,
            validade="2027-12-31",
            fornecedor="Fornecedor Teste",
        )
        assert svc_vazio.total_lotes == antes + 1

    def test_item_inserido_encontrado_por_busca(self, svc_vazio):
        svc_vazio.adicionar_item(
            nome="Galão 20L",
            lote="L888888",
            quantidade=5,
            validade="2027-06-15",
            fornecedor="Fornecedor Beta",
        )
        resultado = svc_vazio.buscar_por_validade("2027-06-15")
        lotes = [i.lote for i in resultado]
        assert "L888888" in lotes

    def test_insercao_mantem_ordem(self, svc_vazio):
        datas = ["2027-09-01", "2026-03-15", "2028-01-01", "2025-05-10"]
        for i, d in enumerate(datas):
            svc_vazio.adicionar_item("Produto", f"LX{i}", 1, d, "F")
        itens = svc_vazio.listar_por_validade()
        vals = [it.validade for it in itens]
        assert vals == sorted(vals)

    def test_item_inserido_tem_id_unico_crescente(self, svc_vazio):
        i1 = svc_vazio.adicionar_item("P1", "LA1", 1, "2027-01-01", "F")
        i2 = svc_vazio.adicionar_item("P2", "LA2", 1, "2027-01-02", "F")
        assert i2.id > i1.id

    def test_insercao_retorna_stock_item(self, svc_vazio):
        item = svc_vazio.adicionar_item("P", "LB", 1, "2027-03-01", "F")
        assert isinstance(item, StockItem)


# ---------------------------------------------------------------------------
# Testes de próximos vencimentos
# ---------------------------------------------------------------------------

class TestProximosVencimentos:
    def test_retorna_lista(self, svc_carregado):
        resultado = svc_carregado.listar_proximos_vencimentos(dias=30)
        assert isinstance(resultado, list)

    def test_todos_dentro_da_janela(self, svc_carregado):
        from datetime import date, timedelta
        hoje = date.today().isoformat()
        limite = (date.today() + timedelta(days=30)).isoformat()
        for item in svc_carregado.listar_proximos_vencimentos(dias=30):
            assert hoje <= item.validade <= limite

    def test_janela_zero_retorna_vazio_ou_hoje(self, svc_carregado):
        from datetime import date
        hoje = date.today().isoformat()
        resultado = svc_carregado.listar_proximos_vencimentos(dias=0)
        for item in resultado:
            assert item.validade == hoje
