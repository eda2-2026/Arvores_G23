# Sistema de Gerenciamento de Estoque de Água

> Trabalho prático — Estruturas de Dados 2  
> Implementação de **Árvore Rubro-Negra** aplicada a um sistema de controle de estoque de lotes de água por data de validade.

---

## Alunos

| Membro | Responsabilidade principal |
|--------|---------------------------|
| Euller | Dados mock · Modelos · Serviço de inventário · Testes de serviço · Interface Streamlit |
| Davi   | Árvore rubro-negra · Rotações · Balanceamento · Testes da árvore · Visualizador |

---

## Estrutura do projeto

```
Arvores_G23/
├── README.md
├── .gitignore
├── app.py                        # interface Streamlit (Commit 13)
├── data/
│   └── mock_stock.json           # massa de dados mock   (Commit 3)
├── src/
│   ├── models.py                 # modelo StockItem      (Commit 9)
│   ├── red_black_tree.py         # árvore rubro-negra    (Commits 4-7)
│   ├── inventory_service.py      # serviço de estoque    (Commits 10-11)
│   └── tree_visualizer.py        # visualização textual  (Commit 14)
├── tests/
│   ├── test_red_black_tree.py    # testes da árvore      (Commit 8)
│   └── test_inventory_service.py # testes do serviço     (Commit 12)
├── docs/
│   ├── especificacao.md          # proposta do sistema   (Commit 2)
│   ├── complexidade.md           # análise de complexidade (Commit 15)
│   ├── divisoes.md
│   └── roteiro_video.md          # roteiro da demo       (Commit 16)
└── results/
    └── exemplos_execucao.md      # saídas de exemplo
```

---

## Como executar

```bash
# Instalar dependências
pip install streamlit

# Rodar a interface
streamlit run app.py

# Rodar os testes
python -m pytest tests/ -v
```

> **Pré-requisito:** Python 3.10+

---

## Por que Árvore Rubro-Negra?

A árvore rubro-negra é usada como **índice ordenado dos lotes** de água por data de validade.  
Isso permite responder em tempo O(log n):

- *"Quais lotes vencem primeiro?"*
- *"Existe algum lote com validade X em estoque?"*
- *"Qual o lote mais próximo do vencimento?"*

Sem essa estrutura, essas consultas exigiriam varredura linear O(n) em um estoque grande.

---

## Operações implementadas

| Operação | Complexidade | Status |
|----------|-------------|--------|
| Inserir lote | O(log n) | ⬜ pendente |
| Buscar por validade | O(log n) | ⬜ pendente |
| Listar em ordem de validade | O(n) | ⬜ pendente |
| Lote com vencimento mais próximo | O(log n) | ⬜ pendente |
| Remover lote | O(log n) | ⬜ pendente |
| Alertar itens próximos do vencimento | O(n) | ⬜ pendente |

---

## Dados mock

- **Total de itens:** 52.000
- **Produtos:** Garrafa 200ml / 300ml / 500ml / 750ml / 1L / 1.5L / 2L · Galão 5L / 10L / 20L · Caixa 1L / 2L · Água com gás 350ml / 500ml / 1L · Água alcalina 500ml / 1.5L · Água mineral (com e sem gás)
- **Período de validades:** 2025-01-01 → 2028-01-01
- **Fornecedores:** 8 (Cristalina Ltda., Purágua S.A., NaturaFonte, AquaPura, Serra Verde, Fonte Pérola, Hidroplus, BemSer)
- **Gerado por:** [`data/generate_mock.py`](data/generate_mock.py) com `random.seed(42)` (reproduzível)

---

## Testes

<!-- Preencher após Commits 8 e 12 -->

```
$ python -m pytest tests/ -v

(resultados serão adicionados aqui)
```

---

## Demonstração

<!-- Preencher após Commit 13 — adicionar prints da interface -->

---

## Documentação

- [`docs/especificacao.md`](docs/especificacao.md) — Proposta e justificativa do sistema
- [`docs/complexidade.md`](docs/complexidade.md) — Análise de complexidade da árvore
- [`docs/roteiro_video.md`](docs/roteiro_video.md) — Roteiro da demonstração em vídeo
- [`results/exemplos_execucao.md`](results/exemplos_execucao.md) — Saídas de exemplo

---
