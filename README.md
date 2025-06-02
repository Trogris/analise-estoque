# 📘 Análise de Estoque para Produção

## 1. Objetivo
Registrar a lógica atualizada e regras aplicadas na análise de estoque para produção de equipamentos voltados à **locação (PL)** e **venda (PV)**, contemplando:
- Transposições permitidas
- Uso direto de componentes reparados (RP)
- Critérios de priorização de consumo de estoque

## 2. Prefixos e Significados

| Prefixo | Significado |
|--------|-------------|
| 🔹 PL  | Produto para **Locação** – Manutenção por conta da empresa |
| 🔹 PV  | Produto para **Venda** – Deve usar componentes novos ou homologados |
| 🔹 MP  | Matéria-Prima |
| 🔹 AA  | Almoxarifado Auxiliar |
| 🔹 RP  | Componentes Reparados – Uso **limitado**, com exceções |

## 3. Regras de Transposição

| Origem | Destino | Permitido? |
|--------|---------|------------|
| PV     | PL      | ✅         |
| PV     | MP      | ✅         |
| AA     | PV      | ✅         |
| AA     | MP      | ✅         |
| MP     | PL      | ✅         |
| MP     | PV      | ✅         |
| PL     | MP      | ✅         |
| PL     | PV      | ✅         |
| RP     | Qualquer| ❌ **Proibido em transposição** |

> ⚠️ **RP nunca pode ser origem ou destino de transposição.**

## 4. 🔁 Lógica de Consumo para Produção de Equipamentos **PL**

1. ✅ Verifica **saldo no prefixo PL**
2. 🔄 Tenta **transpor** de: **MP**, **PV**, **AA** → PL *(respeitando regras)*
3. 🔧 Verifica saldo no **RP** → *uso direto permitido, sem transposição*
4. 🛒 Se ainda faltar → **saldo faltante é sinalizado para compra**

## 5. 🔁 Lógica de Consumo para Produção de Equipamentos **PV**

1. ✅ Verifica **saldo no prefixo PV**
2. 🔄 Tenta **transpor** de: **MP**, **PL**, **AA** → PV *(respeitando regras)*
3. ❌ Nunca utiliza componentes do **RP**
4. 🛒 Se ainda faltar → **saldo faltante é sinalizado para compra**
