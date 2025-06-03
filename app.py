
import streamlit as st
import pandas as pd
from io import BytesIO
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "utils"))
from analise import analisar_estoque

st.set_page_config(page_title="Análise de Estoque para Produção", layout="centered")
st.title("🔎 Análise de Estoque para Produção")

with st.sidebar:
    st.markdown("### 🛠 Parâmetros da Análise")
    qtd = st.number_input("Quantidade de Equipamentos a Produzir", min_value=1, value=1, step=1)
    codigo_destino = st.selectbox("Código de Destino", options=["PL", "PV", "MP", "AA", "RP"])
    estrutura_file = st.file_uploader("📥 Estrutura do Produto (.xlsx)", type=["xlsx"])
    estoque_file = st.file_uploader("📥 Estoque Atual (.xlsx)", type=["xlsx"])
    executar = st.button("▶️ Executar Análise")
    nova_analise = st.button("♻️ Nova Análise")

if executar and estrutura_file and estoque_file:
    estrutura_df = pd.read_excel(estrutura_file)
    estoque_df = pd.read_excel(estoque_file)

    resultado = analisar_estoque(estrutura_df, estoque_df, qtd, codigo_destino)

    st.subheader("📊 Resultado da Análise")
    st.dataframe(resultado)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        resultado.to_excel(writer, index=False, sheet_name="Resultado")

    st.download_button(
        label="📤 Baixar Análise (.xlsx)",
        data=output.getvalue(),
        file_name="relatorio_estoque_producao.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
