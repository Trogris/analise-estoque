
import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="📦 Análise de Estoque para Produção", layout="wide")

st.markdown("# 📦 Análise de Estoque para Produção")
st.write("")

with st.sidebar:
    st.markdown("### Parâmetros da Análise")
    qtd_equip = st.number_input("Quantidade de Equipamentos a Produzir", min_value=1, step=1, value=1)
    tp_destino = st.selectbox("Prefixo de Código de Destino (TP)", ["PL", "PV"])

estrutura_file = st.file_uploader("📥 Envie a planilha de Estrutura do Produto", type=["xlsx", "csv"])
estoque_file = st.file_uploader("📥 Envie a planilha de Estoque Atual", type=["xlsx", "csv"])

executar = st.button("🚀 Executar Análise")
nova = st.button("🔄 Nova Análise")

if executar and estrutura_file and estoque_file:
    if estrutura_file.name.endswith(".csv"):
        estrutura_df = pd.read_csv(estrutura_file)
    else:
        estrutura_df = pd.read_excel(estrutura_file)

    if estoque_file.name.endswith(".csv"):
        estoque_df = pd.read_csv(estoque_file)
    else:
        estoque_df = pd.read_excel(estoque_file)

    estrutura_df.columns = estrutura_df.columns.str.strip().str.lower()
    estoque_df.columns = estoque_df.columns.str.strip().str.lower()

    estrutura_df["qtd_total"] = estrutura_df["quantidade necessária"] * qtd_equip
    resultado = []

    for _, row in estrutura_df.iterrows():
        item = row["código do item"]
        qtd_necessaria = row["qtd_total"]

        saldo_pleno = estoque_df[estoque_df["código"] == item]
        saldo_total = saldo_pleno["saldo"].sum() if not saldo_pleno.empty else 0

        consumo = 0
        origem_usada = []

        def consumir(prefixo):
            nonlocal consumo
            filtro = estoque_df[(estoque_df["código"] == item) & (estoque_df["prefixo"] == prefixo)]
            saldo = filtro["saldo"].sum() if not filtro.empty else 0
            usar = min(saldo, qtd_necessaria - consumo)
            consumo += usar
            if usar > 0:
                origem_usada.append(f"{int(usar)} unid de {prefixo}")
            return usar

        if tp_destino == "PL":
            for origem in ["PL", "MP", "AA", "PV"]:
                consumir(origem)
            if consumo < qtd_necessaria:
                usar_rp = estoque_df[(estoque_df["código"] == item) & (estoque_df["prefixo"] == "RP")]["saldo"].sum()
                usar_rp = min(usar_rp, qtd_necessaria - consumo)
                consumo += usar_rp
                if usar_rp > 0:
                    origem_usada.append(f"{int(usar_rp)} unid de RP (uso direto)")

        if tp_destino == "PV":
            for origem in ["PV", "MP", "AA", "PL"]:
                consumir(origem)

        faltando = int(qtd_necessaria - consumo)

        if faltando <= 0:
            status = "✅ OK"
        elif consumo > 0:
            status = f"⚠️ Necessário Transposição ({' + '.join(origem_usada)})"
            if faltando > 0:
                status += f" + Solicitar Compra ({faltando})"
        else:
            status = f"🛒 Solicitar Compra ({faltando})"

        resultado.append({
            "Componente": item,
            "Descrição": row["descrição do item"],
            "Qtd Necessária": int(qtd_necessaria),
            "Qtd Atendida": int(consumo),
            "Qtd Faltante": faltando,
            "Situação": status
        })

    df_resultado = pd.DataFrame(resultado)
    st.dataframe(df_resultado, use_container_width=True)

    buffer = io.BytesIO()
    df_resultado.to_excel(buffer, index=False, engine='openpyxl')
    st.download_button("📥 Baixar Resultado em Excel", data=buffer.getvalue(), file_name="resultado_estoque.xlsx", mime="application/vnd.ms-excel")
