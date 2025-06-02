
import streamlit as st
import pandas as pd

st.set_page_config(page_title="📦 Análise de Estoque para Produção", layout="wide")

st.title("📦 Análise de Estoque para Produção")

st.sidebar.header("Parâmetros da Análise")
qtd_equip = st.sidebar.number_input("Quantidade de Equipamentos a Produzir", min_value=1, value=1, step=1)
tp_destino = st.sidebar.selectbox("Prefixo de Código de Destino (TP)", ["PL", "PV"])

st.markdown("### 📥 Envie a planilha de Estrutura do Produto")
file_estrutura = st.file_uploader("Drag and drop file here", type="xlsx", key="estrutura")

st.markdown("### 📥 Envie a planilha de Estoque Atual")
file_estoque = st.file_uploader("Drag and drop file here", type="xlsx", key="estoque")

if file_estrutura and file_estoque:
    estrutura = pd.read_excel(file_estrutura)
    estoque = pd.read_excel(file_estoque)

    estrutura["Total Necessário"] = estrutura["Quantidade"] * qtd_equip
    resultado = []

    for _, row in estrutura.iterrows():
        cod = row["Código do Item"]
        qtd_necessaria = row["Total Necessário"]

        saldo_total = estoque[estoque["Código"] == cod]["Saldo"].sum()
        origem_saldos = estoque[estoque["Código"] == cod].set_index("Prefixo")["Saldo"].to_dict()

        falta = max(0, qtd_necessaria - saldo_total)
        situacao = "OK" if falta == 0 else "Faltando"
        transposicao = "-"

        if falta > 0:
            if tp_destino == "PL":
                usar = 0
                for prefixo in ["MP", "AA", "PV"]:
                    if prefixo in origem_saldos and origem_saldos[prefixo] > 0:
                        usar = min(falta, origem_saldos[prefixo])
                        falta -= usar
                        transposicao = f"{usar} unid de {prefixo} → {tp_destino}\n"
                        if falta == 0:
                            break
                if falta > 0 and "RP" in origem_saldos and origem_saldos["RP"] > 0:
                    usar_rp = min(falta, origem_saldos["RP"])
                    falta -= usar_rp
                    if transposicao == "-":
                        transposicao = ""
                    transposicao += f"{usar_rp} unid do RP (uso direto)\n"
            elif tp_destino == "PV":
                usar = 0
                for prefixo in ["MP", "AA", "PL"]:
                    if prefixo in origem_saldos and origem_saldos[prefixo] > 0:
                        usar = min(falta, origem_saldos[prefixo])
                        falta -= usar
                        transposicao = f"{usar} unid de {prefixo} → {tp_destino}\n"
                        if falta == 0:
                            break

        resultado.append({
            "Componente": cod,
            "Situação": "OK" if falta == 0 else "Faltando mesmo com transposição",
            "Qtd Faltante": falta,
            "Transposição Sugerida": transposicao
        })

    df_resultado = pd.DataFrame(resultado)

    st.dataframe(df_resultado)

    st.download_button(
        "📥 Baixar Resultado em Excel",
        data=df_resultado.to_excel(index=False, engine="openpyxl"),
        file_name="resultado_estoque.xlsx"
    )
