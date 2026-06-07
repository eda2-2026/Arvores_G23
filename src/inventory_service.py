"""
Serviço de inventário: carrega dados mock e oferece operações de estoque
usando a árvore rubro-negra como estrutura de índice por data de validade.
"""

from __future__ import annotations

import json
import os
from datetime import date, timedelta
from typing import List, Optional, Tuple

from src.models import StockItem
from src.red_black_tree import RedBlackTree


class InventoryService:
    """Gerencia o estoque de água indexado por data de validade.

    A árvore rubro-negra armazena os lotes com a data de validade
    como chave, permitindo busca e ordenação em O(log n).
    """

    # Caminho padrão para o arquivo mock
    DEFAULT_MOCK_PATH = os.path.join(
        os.path.dirname(__file__), "..", "data", "mock_stock.json"
    )

    def __init__(self) -> None:
        self._tree: RedBlackTree = RedBlackTree()
        self._next_id: int = 1

    # ------------------------------------------------------------------
    # Carregamento
    # ------------------------------------------------------------------

    def load_from_file(self, path: str | None = None) -> int:
        """Carrega itens de um arquivo JSON e os insere na árvore.

        Args:
            path: caminho para o JSON. Usa DEFAULT_MOCK_PATH se None.

        Returns:
            Número de itens carregados.
        """
        filepath = path or self.DEFAULT_MOCK_PATH
        with open(filepath, encoding="utf-8") as f:
            raw: list = json.load(f)

        for entry in raw:
            item = StockItem(
                id=entry["id"],
                nome=entry["nome"],
                lote=entry["lote"],
                quantidade=entry["quantidade"],
                validade=entry["validade"],
                fornecedor=entry["fornecedor"],
            )
            self._tree.insert(item.validade, item)
            if item.id >= self._next_id:
                self._next_id = item.id + 1

        return len(raw)

    # ------------------------------------------------------------------
    # Operações de escrita
    # ------------------------------------------------------------------

    def adicionar_item(
        self,
        nome: str,
        lote: str,
        quantidade: int,
        validade: str,
        fornecedor: str,
    ) -> StockItem:
        """Cria e insere um novo lote na árvore.

        Args:
            nome: nome do produto.
            lote: código do lote.
            quantidade: número de unidades.
            validade: data de validade no formato "YYYY-MM-DD".
            fornecedor: nome do fornecedor.

        Returns:
            O StockItem criado e inserido.
        """
        item = StockItem(
            id=self._next_id,
            nome=nome,
            lote=lote,
            quantidade=quantidade,
            validade=validade,
            fornecedor=fornecedor,
        )
        self._tree.insert(item.validade, item)
        self._next_id += 1
        return item

    # ------------------------------------------------------------------
    # Operações de leitura
    # ------------------------------------------------------------------

    def listar_por_validade(self) -> List[StockItem]:
        """Retorna todos os itens em ordem crescente de validade (FEFO).

        Complexidade: O(n).
        """
        return self._tree.in_order_values()

    def buscar_por_validade(self, validade: str) -> List[StockItem]:
        """Retorna todos os lotes com uma data de validade específica.

        Args:
            validade: data no formato "YYYY-MM-DD".

        Returns:
            Lista de StockItem com aquela data (pode ser vazia).

        Complexidade: O(log n).
        """
        return self._tree.search(validade)

    def lote_mais_proximo_do_vencimento(self) -> Optional[Tuple[str, List[StockItem]]]:
        """Retorna o lote com a data de validade mais próxima.

        Returns:
            Par (validade, [itens]) do nó mínimo, ou None se vazio.

        Complexidade: O(log n).
        """
        result = self._tree.min()
        if result is None:
            return None
        validade, items = result
        return validade, items

    def listar_proximos_vencimentos(self, dias: int = 30) -> List[StockItem]:
        """Lista todos os lotes que vencem nos próximos N dias.

        Args:
            dias: janela em dias a partir de hoje (padrão: 30).

        Returns:
            Lista de itens ordenada por validade crescente.

        Complexidade: O(n) — percurso em ordem com filtro.
        """
        hoje = date.today()
        limite = hoje + timedelta(days=dias)
        hoje_str = hoje.isoformat()
        limite_str = limite.isoformat()

        resultado: List[StockItem] = []
        for validade, items in self._tree.in_order():
            if validade > limite_str:
                break
            if validade >= hoje_str:
                resultado.extend(items)

        return resultado

    def listar_vencidos(self) -> List[StockItem]:
        """Retorna todos os lotes com validade anterior a hoje.

        Complexidade: O(n) — percurso em ordem com filtro.
        """
        hoje_str = date.today().isoformat()
        resultado: List[StockItem] = []
        for validade, items in self._tree.in_order():
            if validade >= hoje_str:
                break
            resultado.extend(items)
        return resultado

    # ------------------------------------------------------------------
    # Estatísticas
    # ------------------------------------------------------------------

    @property
    def total_lotes(self) -> int:
        """Número total de itens (lotes) no estoque."""
        return self._tree.value_count

    @property
    def total_datas_distintas(self) -> int:
        """Número de datas de validade distintas (nós na árvore)."""
        return self._tree.node_count

    @property
    def altura_arvore(self) -> int:
        """Altura atual da árvore rubro-negra."""
        return self._tree.height()
