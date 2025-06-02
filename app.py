import streamlit as st
import pandas as pd
from utils import (
    carregar_arquivo,
    analisar_estoque,
    resetar_estado
)

st.set_page_config(page_title="📘 Análise de Estoque para Produção", layout="wide")

st.title("📘 Análise de Estoque para Produção")

if "analisado" not in st.session_state:
    st.session_state.analisado = False

col1, col2 = st.columns([3, 2])
with col1:
    quantidade = st.number_input("Quantidade de Equipamentos a Produzir", min_value=1, value=1)
with col2:
    destino = st.selectbox("Código de Destino", ["PL", "PV"])

with st.expander("📥 Carregar Arquivos", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        estoque_file = st.file_uploader("📥 Estoque (Excel ou CSV)", type=["xlsx", "xls", "csv"], key="estoque")
    with col2:
        estrutura_file = st.file_uploader("📥 Estrutura do Produto (Excel ou CSV)", type=["xlsx", "xls", "csv"], key="estrutura")

executar = st.button("🚀 Executar Análise")

if executar and estoque_file and estrutura_file:
    df_estoque = carregar_arquivo(estoque_file)
    df_estrutura = carregar_arquivo(estrutura_file)
    df_resultado = analisar_estoque(df_estoque, df_estrutura, quantidade, destino)
    st.session_state.analisado = True
    st.session_state.df_resultado = df_resultado

if st.session_state.analisado:
    st.dataframe(st.session_state.df_resultado.style.set_properties(subset=["🔧 Parâmetros da Análise"], **{"width": "200px"}), use_container_width=True)
    buffer = pd.ExcelWriter("/mnt/data/resultado_estoque.xlsx", engine='openpyxl')
    st.session_state.df_resultado.to_excel(buffer, index=False)
    buffer.close()
    with open("/mnt/data/resultado_estoque.xlsx", "rb") as file:
        st.download_button("📥 Baixar Resultado em Excel", data=file, file_name="resultado_estoque.xlsx")

    if st.button("🔄 Nova Análise"):
        resetar_estado()
        st.experimental_rerun()