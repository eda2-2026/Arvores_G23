"""
Gerador de massa de dados mock para o estoque de água.
Gera 50.000+ itens e salva em data/mock_stock.json
"""

import json
import random
from datetime import date, timedelta

random.seed(42)

PRODUTOS = [
    "Garrafa de água 200ml",
    "Garrafa de água 300ml",
    "Garrafa de água 500ml",
    "Garrafa de água 510ml",
    "Garrafa de água 750ml",
    "Garrafa de água 1L",
    "Garrafa de água 1.5L",
    "Garrafa de água 2L",
    "Galão de água 5L",
    "Galão de água 10L",
    "Galão de água 20L",
    "Caixa de água 1L",
    "Caixa de água 2L",
    "Água com gás 350ml",
    "Água com gás 500ml",
    "Água com gás 1L",
    "Água mineral com gás 300ml",
    "Água mineral sem gás 500ml",
    "Água alcalina 500ml",
    "Água alcalina 1.5L",
]

FORNECEDORES = [
    "Fornecedor A — Cristalina Ltda.",
    "Fornecedor B — Purágua S.A.",
    "Fornecedor C — NaturaFonte Distribuidora",
    "Fornecedor D — AquaPura Comércio",
    "Fornecedor E — Serra Verde Águas",
    "Fornecedor F — Fonte Pérola Industrial",
    "Fornecedor G — Hidroplus Ltda.",
    "Fornecedor H — BemSer Águas Minerais",
]

BASE_DATE = date(2025, 1, 1)
# Validades entre 2025-01-01 e 2027-12-31 (1095 dias)
TOTAL_DIAS = 1095
TOTAL_ITENS = 52000

items = []
for i in range(1, TOTAL_ITENS + 1):
    produto = random.choice(PRODUTOS)
    fornecedor = random.choice(FORNECEDORES)
    lote_num = f"L{i:06d}"
    quantidade = random.randint(1, 500)
    dias_offset = random.randint(0, TOTAL_DIAS)
    validade = (BASE_DATE + timedelta(days=dias_offset)).isoformat()

    items.append({
        "id": i,
        "nome": produto,
        "lote": lote_num,
        "quantidade": quantidade,
        "validade": validade,
        "fornecedor": fornecedor,
    })

output_path = "data/mock_stock.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

print(f"✅ Gerados {len(items):,} itens em '{output_path}'")
print(f"   Produtos distintos : {len(PRODUTOS)}")
print(f"   Fornecedores       : {len(FORNECEDORES)}")
print(f"   Período de validades: {BASE_DATE.isoformat()} → {(BASE_DATE + timedelta(days=TOTAL_DIAS)).isoformat()}")
