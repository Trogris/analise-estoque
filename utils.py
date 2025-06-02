import pandas as pd
import streamlit as st

def carregar_arquivo(uploaded_file):
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    return pd.read_excel(uploaded_file)

def resetar_estado():
    for key in st.session_state.keys():
        del st.session_state[key]

def analisar_estoque(df_estoque, df_estrutura, qtd_equip, destino):
    df_estrutura['Qtd Total Necessária'] = df_estrutura['Quantidade'] * qtd_equip
    df_resultado = df_estrutura.copy()
    df_resultado['Saldo Disponível'] = 0
    df_resultado['Falta'] = 0
    df_resultado['Transposição Sugerida'] = ""
    df_resultado['🔧 Parâmetros da Análise'] = ""

    regras_permitidas = {
        "PL": ["MP", "PV", "AA"],
        "PV": ["MP", "PL", "AA"]
    }

    for i, row in df_resultado.iterrows():
        codigo = row['Código do Item']
        qtd_necessaria = row['Qtd Total Necessária']
        saldo_total = 0
        transposicao = ""
        falta = 0

        if destino == "PL":
            saldo_pl = df_estoque.query("Código == @codigo and Prefixo == 'PL'")["Saldo"].sum()
            saldo_total += saldo_pl
            transposicao += f"PL: {saldo_pl} "

            if saldo_total < qtd_necessaria:
                for prefixo in regras_permitidas["PL"]:
                    usar = min(
                        df_estoque.query("Código == @codigo and Prefixo == @prefixo")["Saldo"].sum(),
                        qtd_necessaria - saldo_total
                    )
                    if usar > 0:
                        saldo_total += usar
                        transposicao += f" | {usar} unid de {prefixo} → PL"

            if saldo_total < qtd_necessaria:
                saldo_rp = df_estoque.query("Código == @codigo and Prefixo == 'RP'")["Saldo"].sum()
                usar = min(saldo_rp, qtd_necessaria - saldo_total)
                if usar > 0:
                    saldo_total += usar
                    transposicao += f" | {usar} unid de RP (uso direto)"

        elif destino == "PV":
            saldo_pv = df_estoque.query("Código == @codigo and Prefixo == 'PV'")["Saldo"].sum()
            saldo_total += saldo_pv
            transposicao += f"PV: {saldo_pv} "

            if saldo_total < qtd_necessaria:
                for prefixo in regras_permitidas["PV"]:
                    usar = min(
                        df_estoque.query("Código == @codigo and Prefixo == @prefixo")["Saldo"].sum(),
                        qtd_necessaria - saldo_total
                    )
                    if usar > 0:
                        saldo_total += usar
                        transposicao += f" | {usar} unid de {prefixo} → PV"

        falta = max(0, qtd_necessaria - saldo_total)
        df_resultado.at[i, 'Saldo Disponível'] = saldo_total
        df_resultado.at[i, 'Falta'] = falta
        df_resultado.at[i, 'Transposição Sugerida'] = transposicao
        df_resultado.at[i, '🔧 Parâmetros da Análise'] = f"{qtd_necessaria} unid necessárias para {destino}"

    return df_resultado