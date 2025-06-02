import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Análise de Estoque para Produção", layout="wide")
st.markdown("### 📦 Análise de Estoque para Produção")

st.sidebar.markdown("## ⚙️ Parâmetros da Análise")
qtd_equip = st.sidebar.number_input("Quantidade de Equipamentos a Produzir", min_value=1, step=1, value=1)
prefixo_destino = st.sidebar.selectbox("Prefixo de Código de Destino (TP)", ["PL", "PV"])

st.markdown("#### 📥 Envie a planilha de Estrutura do Produto")
file_estrutura = st.file_uploader("📥 Estrutura do Produto (.xlsx ou .csv)", type=["xlsx", "csv"], key="estrutura")

st.markdown("#### 📥 Envie a planilha de Estoque Atual")
file_estoque = st.file_uploader("📥 Estoque Atual (.xlsx ou .csv)", type=["xlsx", "csv"], key="estoque")

def carregar_arquivo(uploaded_file):
    if uploaded_file is not None:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    return None

df_estrutura = carregar_arquivo(file_estrutura)
df_estoque = carregar_arquivo(file_estoque)

def analisar_estoque(estrutura, estoque, qtd, tp_destino):
    estrutura.columns = estrutura.columns.str.strip()
    estoque.columns = estoque.columns.str.strip()
    resultado = []

    for _, row in estrutura.iterrows():
        cod = row["Código do Item"]
        desc = row.get("Descrição do Item", "")
        qtd_necessaria = row["Quantidade"] * qtd
        saldos = estoque[estoque["Código"] == cod]
        saldo_total = saldos["Saldo"].sum() if not saldos.empty else 0
        faltante = max(qtd_necessaria - saldo_total, 0)
        situacao = "OK" if faltante == 0 else "Faltando"
        transposicao = ""

        if faltante > 0:
            prefixos_validos = []
            if tp_destino == "PL":
                prefixos_validos = ["MP", "AA", "PV"]
            elif tp_destino == "PV":
                prefixos_validos = ["MP", "AA", "PL"]

            saldo_utilizado = 0
            for prefixo in prefixos_validos:
                saldo_origem = estoque[(estoque["Código"] == cod) & (estoque["Prefixo"] == prefixo)]
                disponivel = saldo_origem["Saldo"].sum()
                if disponivel > 0:
                    usar = min(disponivel, faltante - saldo_utilizado)
                    if usar > 0:
                        transposicao += f"{usar} unid de {prefixo} → {tp_destino}
"
                        saldo_utilizado += usar
                if saldo_utilizado >= faltante:
                    break

            if tp_destino == "PL":
                saldo_rp = estoque[(estoque["Código"] == cod) & (estoque["Prefixo"] == "RP")]["Saldo"].sum()
                if saldo_rp > 0 and saldo_utilizado < faltante:
                    usar_rp = min(faltante - saldo_utilizado, saldo_rp)
                    transposicao += f"{usar_rp} unid do RP (uso direto)
"
                    saldo_utilizado += usar_rp

            if saldo_utilizado >= faltante:
                situacao = "Resolvido com Transposição"
            else:
                situacao = "Faltando mesmo com transposição"

        resultado.append({
            "Componente": cod,
            "Descrição": desc,
            "Qtd Necessária": qtd_necessaria,
            "Qtd em Estoque": saldo_total,
            "Qtd Faltante": faltante,
            "Situação": situacao,
            "Transposição Sugerida": transposicao.strip()
        })

    return pd.DataFrame(resultado)

if st.button("🚀 Executar Análise"):
    if df_estrutura is not None and df_estoque is not None:
        df_resultado = analisar_estoque(df_estrutura, df_estoque, qtd_equip, prefixo_destino)
        st.success("✅ Análise concluída.")
        st.dataframe(df_resultado, use_container_width=True)
        buffer = io.BytesIO()
        df_resultado.to_excel(buffer, index=False, engine='openpyxl')
        st.download_button("📥 Baixar Resultado em Excel", data=buffer.getvalue(), file_name="resultado_estoque.xlsx")
    else:
        st.warning("⚠️ Por favor, envie os dois arquivos para iniciar a análise.")

if st.button("🔄 Nova Análise"):
    st.experimental_rerun()
