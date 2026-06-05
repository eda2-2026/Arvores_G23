# Especificação do Sistema de Gerenciamento de Estoque de Água

## 1. Problema

Empresas distribuidoras de água precisam controlar com precisão os lotes em estoque, garantindo que:

- Lotes mais próximos do vencimento sejam expedidos primeiro (princípio FEFO — *First Expired, First Out*);
- Seja possível localizar rapidamente um lote específico por data de validade;
- Alertas sejam emitidos quando lotes estiverem prestes a vencer;
- Novas entradas sejam inseridas mantendo o estoque sempre ordenado por validade.

Com volumes de estoque que podem chegar a dezenas de milhares de lotes, soluções ingênuas (listas não ordenadas, varredura linear) tornam-se inaceitáveis em termos de desempenho.

---

## 2. Por que Árvore Rubro-Negra?

A **árvore rubro-negra** é uma árvore binária de busca balanceada que garante altura O(log n), o que assegura:

| Operação | Complexidade |
|----------|-------------|
| Inserção | O(log n) |
| Busca | O(log n) |
| Mínimo / máximo | O(log n) |
| Percurso em ordem | O(n) |
| Remoção | O(log n) |

Comparação com alternativas:

| Estrutura | Busca | Inserção | Ordem |
|-----------|-------|----------|-------|
| Lista não ordenada | O(n) | O(1) | O(n log n) |
| Lista ordenada | O(log n)* | O(n) | O(n) |
| Árvore BST simples | O(n) pior caso | O(n) pior caso | O(n) |
| **Árvore Rubro-Negra** | **O(log n)** | **O(log n)** | **O(n)** |

> *busca binária — mas inserção ordenada em lista é O(n) devido ao deslocamento de elementos.

A árvore rubro-negra é a estrutura mais adequada porque mantém o desempenho garantido em O(log n) para todas as operações principais, mesmo no pior caso.

---

## 3. Chave escolhida

```
chave da árvore = data de validade (string ISO 8601: YYYY-MM-DD)
```

**Justificativa:** a data de validade é a informação mais crítica para a gestão de estoque de alimentos e bebidas. Indexar por validade permite:

- Recuperar imediatamente o lote mais próximo do vencimento (`min` da árvore);
- Listar todos os lotes em ordem FEFO com percurso em ordem (`in_order`);
- Buscar se existe algum lote com determinada validade em O(log n).

Como pode haver múltiplos lotes com a mesma data de validade, cada nó da árvore armazenará uma **lista de StockItems** com aquela chave.

---

## 4. Operações do sistema

### 4.1 Inserir lote
Recebe um `StockItem` e o insere na árvore usando `validade` como chave. Se já existir um nó com aquela data, o item é adicionado à lista do nó.

### 4.2 Buscar por validade
Dado uma data de validade, retorna todos os lotes com aquela data.

### 4.3 Listar em ordem de validade
Percurso em ordem na árvore retorna todos os lotes do mais antigo ao mais recente (ordem FEFO).

### 4.4 Lote mais próximo do vencimento
Retorna o elemento mínimo da árvore — o lote que vence primeiro.

### 4.5 Alertar lotes próximos do vencimento
Lista todos os lotes cuja validade está dentro de um intervalo de N dias a partir de hoje.

### 4.6 Remover lote
Remove um lote específico do estoque. Se for o último lote de uma data, o nó é removido da árvore.

---

## 5. Modelo de dados

```python
@dataclass
class StockItem:
    id: int
    nome: str          # ex: "Garrafa de água 500ml"
    lote: str          # ex: "L00042"
    quantidade: int    # unidades em estoque
    validade: str      # "YYYY-MM-DD"
    fornecedor: str    # ex: "Fornecedor A"
```

---

## 6. Divisão de responsabilidades

| Membro | Componentes |
|--------|-------------|
| **Euller** | `data/mock_stock.json` · `src/models.py` · `src/inventory_service.py` · `tests/test_inventory_service.py` · `app.py` · `docs/roteiro_video.md` |
| **Davi** | `src/red_black_tree.py` · `src/tree_visualizer.py` · `tests/test_red_black_tree.py` · `docs/complexidade.md` |
| **Ambos** | `README.md` · `docs/especificacao.md` · `docs/divisoes.md` |

---

## 7. Fluxo da aplicação

```
mock_stock.json
      │
      ▼
 StockItem (models.py)
      │
      ▼
 InventoryService (inventory_service.py)
      │  carrega, insere, busca, lista
      ▼
 RedBlackTree (red_black_tree.py)
      │  indexada por validade
      ▼
 Interface Streamlit (app.py)
```
