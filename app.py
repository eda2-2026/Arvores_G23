"""
Interface Streamlit para o Gerenciador de Estoque de Água.
Execução: python -m streamlit run app.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st

from src.inventory_service import InventoryService
from src.models import StockItem

# ---------------------------------------------------------------------------
# Configuração da página
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Estoque de Água",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Carregamento do serviço (cache para não recarregar a cada interação)
# ---------------------------------------------------------------------------

@st.cache_resource(show_spinner="Carregando estoque...")
def carregar_servico() -> InventoryService:
    svc = InventoryService()
    svc.load_from_file()
    return svc


svc = carregar_servico()

# ---------------------------------------------------------------------------
# Sidebar — navegação
# ---------------------------------------------------------------------------

st.sidebar.title("💧 Estoque de Água")
st.sidebar.caption("Gerenciador indexado por Árvore Rubro-Negra")

pagina = st.sidebar.radio(
    "Menu",
    [
        "📦 Visualizar estoque",
        "➕ Inserir item",
        "🔍 Buscar por validade",
        "⚠️ Próximos vencimentos",
        "🌳 Percurso em ordem da árvore",
    ],
)

st.sidebar.divider()
st.sidebar.metric("Total de lotes", f"{svc.total_lotes:,}")
st.sidebar.metric("Datas distintas", f"{svc.total_datas_distintas:,}")
st.sidebar.metric("Altura da árvore", svc.altura_arvore)

# ---------------------------------------------------------------------------
# Página 1 — Visualizar estoque
# ---------------------------------------------------------------------------

if pagina == "📦 Visualizar estoque":
    st.title("📦 Estoque completo")
    st.caption("Itens exibidos em ordem crescente de validade (FEFO)")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de lotes", f"{svc.total_lotes:,}")
    col2.metric("Datas distintas na árvore", f"{svc.total_datas_distintas:,}")
    col3.metric("Altura da árvore rubro-negra", svc.altura_arvore)

    st.divider()

    limite = st.slider("Quantos itens exibir?", min_value=10, max_value=500, value=50, step=10)
    itens = svc.listar_por_validade()[:limite]

    dados = [
        {
            "ID": i.id,
            "Produto": i.nome,
            "Lote": i.lote,
            "Qtd.": i.quantidade,
            "Validade": i.validade,
            "Fornecedor": i.fornecedor,
        }
        for i in itens
    ]
    st.dataframe(dados, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Página 2 — Inserir item
# ---------------------------------------------------------------------------

elif pagina == "➕ Inserir item":
    st.title("➕ Inserir novo lote")

    with st.form("form_inserir"):
        col1, col2 = st.columns(2)

        nome = col1.selectbox(
            "Produto",
            [
                "Garrafa de água 200ml", "Garrafa de água 300ml",
                "Garrafa de água 500ml", "Garrafa de água 750ml",
                "Garrafa de água 1L", "Garrafa de água 1.5L",
                "Garrafa de água 2L", "Galão de água 5L",
                "Galão de água 10L", "Galão de água 20L",
                "Água com gás 350ml", "Água com gás 500ml",
                "Água alcalina 500ml", "Água alcalina 1.5L",
            ],
        )
        lote = col1.text_input("Código do lote", placeholder="ex: L999999")
        quantidade = col1.number_input("Quantidade", min_value=1, value=100)

        validade = col2.date_input("Data de validade")
        fornecedor = col2.selectbox(
            "Fornecedor",
            [
                "Fornecedor A — Cristalina Ltda.",
                "Fornecedor B — Purágua S.A.",
                "Fornecedor C — NaturaFonte Distribuidora",
                "Fornecedor D — AquaPura Comércio",
                "Fornecedor E — Serra Verde Águas",
                "Fornecedor F — Fonte Pérola Industrial",
                "Fornecedor G — Hidroplus Ltda.",
                "Fornecedor H — BemSer Águas Minerais",
            ],
        )

        enviado = st.form_submit_button("Inserir lote", type="primary")

    if enviado:
        if not lote.strip():
            st.error("Informe o código do lote.")
        else:
            item = svc.adicionar_item(
                nome=nome,
                lote=lote.strip(),
                quantidade=int(quantidade),
                validade=validade.isoformat(),
                fornecedor=fornecedor,
            )
            st.success(
                f"✅ Lote **{item.lote}** inserido com sucesso! "
                f"(ID {item.id} · validade {item.validade})"
            )

# ---------------------------------------------------------------------------
# Página 3 — Buscar por validade
# ---------------------------------------------------------------------------

elif pagina == "🔍 Buscar por validade":
    st.title("🔍 Buscar lotes por data de validade")

    data_busca = st.date_input("Selecione a data de validade")

    if st.button("Buscar", type="primary"):
        resultado = svc.buscar_por_validade(data_busca.isoformat())

        if not resultado:
            st.warning(f"Nenhum lote encontrado com validade **{data_busca}**.")
        else:
            st.success(f"Encontrados **{len(resultado)}** lote(s) com validade {data_busca}.")
            dados = [
                {
                    "ID": i.id,
                    "Produto": i.nome,
                    "Lote": i.lote,
                    "Qtd.": i.quantidade,
                    "Fornecedor": i.fornecedor,
                }
                for i in resultado
            ]
            st.dataframe(dados, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Página 4 — Próximos vencimentos
# ---------------------------------------------------------------------------

elif pagina == "⚠️ Próximos vencimentos":
    st.title("⚠️ Lotes próximos do vencimento")

    dias = st.slider("Janela de dias", min_value=1, max_value=365, value=30)

    proximos = svc.listar_proximos_vencimentos(dias=dias)
    vencidos = svc.listar_vencidos()

    col1, col2 = st.columns(2)
    col1.metric(f"Lotes nos próximos {dias} dias", len(proximos))
    col2.metric("Lotes vencidos", len(vencidos), delta=f"-{len(vencidos)}", delta_color="inverse")

    if proximos:
        st.subheader("Lotes próximos do vencimento")
        dados = [
            {
                "Produto": i.nome,
                "Lote": i.lote,
                "Qtd.": i.quantidade,
                "Validade": i.validade,
                "Fornecedor": i.fornecedor,
            }
            for i in proximos
        ]
        st.dataframe(dados, use_container_width=True, hide_index=True)
    else:
        st.info(f"Nenhum lote vence nos próximos {dias} dias.")

    if vencidos:
        with st.expander(f"🔴 Ver {len(vencidos)} lotes vencidos"):
            dados_v = [
                {
                    "Produto": i.nome,
                    "Lote": i.lote,
                    "Qtd.": i.quantidade,
                    "Validade": i.validade,
                    "Fornecedor": i.fornecedor,
                }
                for i in vencidos
            ]
            st.dataframe(dados_v, use_container_width=True, hide_index=True)

# ---------------------------------------------------------------------------
# Página 5 — Percurso em ordem
# ---------------------------------------------------------------------------

elif pagina == "🌳 Percurso em ordem da árvore":
    st.title("🌳 Percurso em ordem da árvore rubro-negra")
    st.caption(
        "Exibe as chaves (datas de validade) da árvore em ordem crescente, "
        "com a quantidade de lotes em cada data — resultado do in-order traversal."
    )

    pares = svc._tree.in_order()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de nós (datas distintas)", len(pares))
    col2.metric("Altura da árvore", svc.altura_arvore)

    limite_nos = st.slider("Quantos nós exibir?", 10, min(500, len(pares)), 50, 10)

    opcao = st.radio("Extremidade", ["Início (menores validades)", "Fim (maiores validades)"], horizontal=True)

    if opcao == "Início (menores validades)":
        exibir = pares[:limite_nos]
    else:
        exibir = pares[-limite_nos:]

    dados = [
        {"Data de validade": k, "Lotes nessa data": len(vs)}
        for k, vs in exibir
    ]
    st.dataframe(dados, use_container_width=True, hide_index=True)

    st.divider()

    if pares:
        min_val, min_itens = pares[0]
        max_val, max_itens = pares[-1]

        col1, col2 = st.columns(2)
        col1.info(f"**Mínimo (raiz mais à esquerda):** {min_val} — {len(min_itens)} lote(s)")
        col2.info(f"**Máximo (raiz mais à direita):** {max_val} — {len(max_itens)} lote(s)")
