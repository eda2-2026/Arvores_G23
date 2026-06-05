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

<!-- Preencher após Commit 3 -->

- Total de itens: _a definir_
- Produtos: _ex: Garrafa 500ml, Garrafa 1L, Galão 20L..._
- Período de validades: _a definir_
- Fornecedores: _a definir_

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

## 📝 Histórico de commits

| # | Commit | Autor | Status |
|---|--------|-------|--------|
| 1 | `chore: estrutura inicial do projeto` | Euller | ✅ |
| 2 | `docs: define proposta do sistema de estoque` | Euller | ⬜ |
| 3 | `feat: adiciona dados mock de estoque` | Euller | ⬜ |
| 4 | `feat: cria estrutura base da arvore rubro negra` | Davi | ⬜ |
| 5 | `feat: implementa rotacoes da arvore rubro negra` | Davi | ⬜ |
| 6 | `feat: implementa insercao e balanceamento` | Davi | ⬜ |
| 7 | `feat: adiciona busca e percurso em ordem` | Davi | ⬜ |
| 8 | `test: adiciona testes da arvore rubro negra` | Davi | ⬜ |
| 9 | `feat: cria modelo de item de estoque` | Euller | ⬜ |
| 10 | `feat: cria servico de inventario com dados mock` | Euller | ⬜ |
| 11 | `feat: integra estoque com arvore rubro negra` | Euller | ⬜ |
| 12 | `test: adiciona testes do servico de inventario` | Euller | ⬜ |
| 13 | `feat: adiciona interface streamlit de estoque` | Euller | ⬜ |
| 14 | `feat: adiciona visualizacao textual da arvore` | Davi | ⬜ |
| 15 | `docs: documenta complexidade e propriedades da arvore` | Ambos | ⬜ |
| 16 | `docs: adiciona roteiro da demonstracao em video` | Ambos | ⬜ |
