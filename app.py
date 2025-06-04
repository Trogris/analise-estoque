import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📘 Análise de Estoque para Produção", layout="centered")

st.title("📘 Análise de Estoque para Produção")

st.sidebar.header("📥 Parâmetros da Análise")
qtd_equip = st.sidebar.number_input("Quantidade de Equipamentos a Produzir", min_value=1, value=1)
codigo_destino = st.sidebar.selectbox("Código de Destino", ["PL", "PV"])

estrutura_file = st.sidebar.file_uploader("📥 Carregar Estrutura (Excel ou CSV)", type=["xlsx", "xls", "csv"])
estoque_file = st.sidebar.file_uploader("📥 Carregar Estoque (Excel ou CSV)", type=["xlsx", "xls", "csv"])

if estrutura_file and estoque_file:
    try:
        if estrutura_file.name.endswith(".csv"):
            estrutura = pd.read_csv(estrutura_file)
        else:
            estrutura = pd.read_excel(estrutura_file)

        if estoque_file.name.endswith(".csv"):
            estoque = pd.read_csv(estoque_file)
        else:
            estoque = pd.read_excel(estoque_file)

        estrutura["Qtd Total"] = estrutura["Quantidade por Equipamento"] * qtd_equip

        resultado = []

        for _, row in estrutura.iterrows():
            item = row["Código do Item"]
            qtd_necessaria = row["Qtd Total"]
            descricao = row["Descrição do Item"]

            saldo_total = 0
            origem_utilizada = ""
            transposicao = ""

            saldos = estoque[estoque["Código do Item"] == item]
            saldos_dict = dict(zip(saldos["Código"], saldos["Saldo"]))

            prioridade = []
            if codigo_destino == "PL":
                prioridade = ["PL", "MP", "AA", "PV"]
            elif codigo_destino == "PV":
                prioridade = ["PV", "MP", "AA", "PL"]

            for prefixo in prioridade:
                usar = min(saldos_dict.get(prefixo, 0), qtd_necessaria - saldo_total)
                saldo_total += usar
                if usar > 0 and prefixo != codigo_destino:
                    transposicao += f"{usar} unid de {prefixo} → {codigo_destino}; "

            if saldo_total < qtd_necessaria and codigo_destino == "PL":
                usar_rp = min(saldos_dict.get("RP", 0), qtd_necessaria - saldo_total)
                saldo_total += usar_rp
                if usar_rp > 0:
                    transposicao += f"{usar_rp} unid de RP (uso direto); "

            if saldo_total >= qtd_necessaria:
                status = "Ok"
            elif saldo_total > 0:
                status = "Solicitar Compra (parcial)"
            else:
                status = "Solicitar Compra"

            resultado.append({
                "Código do Item": item,
                "Descrição do Item": descricao,
                "Qtd Necessária": qtd_necessaria,
                "Qtd Atendida": saldo_total,
                "Status": status,
                "Transposição": transposicao
            })

        df_resultado = pd.DataFrame(resultado)
        st.dataframe(df_resultado)

        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df_resultado.to_excel(writer, index=False)
        st.download_button("📥 Baixar Resultado em Excel", data=buffer.getvalue(), file_name="resultado_estoque.xlsx")

    except Exception as e:
        st.error(f"Erro na análise: {e}")
