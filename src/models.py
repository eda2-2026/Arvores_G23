"""
Modelo de dados para itens do estoque de água.
"""

from dataclasses import dataclass


@dataclass
class StockItem:
    """Representa um lote de produto no estoque de água.

    Attributes:
        id: identificador único do item.
        nome: nome do produto (ex: "Garrafa de água 500ml").
        lote: código do lote (ex: "L000042").
        quantidade: número de unidades disponíveis.
        validade: data de validade no formato "YYYY-MM-DD".
        fornecedor: nome do fornecedor responsável pelo lote.
    """

    id: int
    nome: str
    lote: str
    quantidade: int
    validade: str
    fornecedor: str

    def __repr__(self) -> str:
        return (
            f"StockItem(id={self.id}, lote={self.lote!r}, "
            f"validade={self.validade!r}, qtd={self.quantidade})"
        )
