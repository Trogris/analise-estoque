import streamlit as st
import pandas as pd
from utils import analisar_estoque

st.set_page_config(page_title="📘 Análise de Estoque para Produção", layout="centered")

st.title("📘 Análise de Estoque para Produção")
st.write("Importe os arquivos e clique em 'Executar Análise' para verificar a disponibilidade de estoque.")

# Upload de arquivos
arquivo_estrutura = st.file_uploader("📥 Estrutura do Produto", type=["xlsx", "csv"])
arquivo_estoque = st.file_uploader("📥 Saldo de Estoque", type=["xlsx", "csv"])

# Parâmetros
col1, col2 = st.columns(2)
with col1:
    qtd_equipamentos = st.number_input("Quantidade de Equipamentos a Produzir", min_value=1, value=1)
with col2:
    codigo_destino = st.selectbox("Código de Destino", options=["PL", "PV"])

# Botões
executar = st.button("Executar Análise")
nova_analise = st.button("Nova Análise")

if executar and arquivo_estrutura and arquivo_estoque:
    estrutura = pd.read_excel(arquivo_estrutura) if arquivo_estrutura.name.endswith("xlsx") else pd.read_csv(arquivo_estrutura)
    estoque = pd.read_excel(arquivo_estoque) if arquivo_estoque.name.endswith("xlsx") else pd.read_csv(arquivo_estoque)

    resultado = analisar_estoque(estrutura, estoque, qtd_equipamentos, codigo_destino)
    st.dataframe(resultado)

    st.download_button("📥 Baixar Resultado em Excel", data=resultado.to_csv(index=False).encode(), file_name="resultado_estoque.csv")