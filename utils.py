import pandas as pd

def analisar_estoque(estrutura, estoque, qtd_equip, destino):
    estrutura['Qtde Total'] = estrutura['Quantidade'] * qtd_equip
    resultado = estrutura.copy()
    resultado['Situação'] = "Ok"
    resultado['Transposição'] = ""

    for idx, row in resultado.iterrows():
        item = row['Código do Item']
        qtd_necessaria = row['Qtde Total']
        saldo_destino = estoque.loc[(estoque['Código'] == destino) & (estoque['Item'] == item), 'Saldo'].sum()

        if saldo_destino >= qtd_necessaria:
            continue

        falta = qtd_necessaria - saldo_destino

        if destino == "PL":
            origem_permitida = ["MP", "AA", "PV"]
        else:
            origem_permitida = ["MP", "AA", "PL"]

        transposto = 0
        for origem in origem_permitida:
            saldo_origem = estoque.loc[(estoque['Código'] == origem) & (estoque['Item'] == item), 'Saldo'].sum()
            usar = min(falta, saldo_origem)
            if usar > 0:
                transposto += usar
                falta -= usar
                resultado.at[idx, 'Transposição'] += f"{usar} unid de {origem} → {destino}; "
            if falta <= 0:
                break

        if destino == "PL" and falta > 0:
            saldo_rp = estoque.loc[(estoque['Código'] == "RP") & (estoque['Item'] == item), 'Saldo'].sum()
            if saldo_rp >= falta:
                resultado.at[idx, 'Transposição'] += f"Usar direto {falta} unid de RP"
                falta = 0

        if falta > 0:
            resultado.at[idx, 'Situação'] = "Solicitar Compra"
        elif transposto > 0:
            resultado.at[idx, 'Situação'] = "Necessário Transposição"

    return resultado[['Código do Item', 'Descrição do Item', 'Quantidade', 'Qtde Total', 'Situação', 'Transposição']]