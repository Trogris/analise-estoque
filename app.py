
import streamlit as st
import pandas as pd
from utils.analise import analisar_estoque
from io import BytesIO

st.set_page_config(page_title="Análise de Estoque para Produção", layout="centered")
st.title("🔎 Análise de Estoque para Produção")

st.markdown("## 🧮 Parâmetros da Análise")
qtd = st.number_input("Quantidade de Equipamentos a Produzir", min_value=1, value=1, step=1)
codigo_destino = st.selectbox("Código de Destino da Produção", options=["PL", "PV", "MP", "AA", "RP"])

st.markdown("## 📁 Upload dos Arquivos")
estrutura_file = st.file_uploader("Importar Estrutura do Produto (.xlsx)", type=["xlsx"])
estoque_file = st.file_uploader("Importar Estoque Atual (.xlsx)", type=["xlsx"])

executar = st.button("🔍 Executar Análise")

if executar and estrutura_file and estoque_file:
    estrutura_df = pd.read_excel(estrutura_file)
    estoque_df = pd.read_excel(estoque_file)

    resultado = analisar_estoque(estrutura_df, estoque_df, qtd, codigo_destino)

    st.markdown("## 📋 Resultado da Análise")
    st.dataframe(resultado)

    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        resultado.to_excel(writer, index=False, sheet_name="Resultado")
        writer.save()
    st.download_button(
        label="📥 Baixar Relatório Completo (.xlsx)",
        data=output.getvalue(),
        file_name="relatorio_estoque_producao.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
