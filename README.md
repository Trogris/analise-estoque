# 📦 Análise de Estoque para Produção

Aplicativo Web desenvolvido com **Streamlit** para realizar análise inteligente de estoque, baseado em regras de consumo e transposição de componentes entre diferentes códigos de uso (PL, PV, MP, AA, RP).

## 🎯 Funcionalidades

- 📥 Upload dos arquivos de **estrutura do produto** e **estoque** (em Excel ou CSV)
- 🔢 Input de quantidade de equipamentos a produzir
- 🏷️ Escolha do código de destino (PL ou PV)
- ✅ Verificação de estoque por código
- 🔁 Análise automática de transposição entre códigos (respeitando regras)
- 🛒 Identificação de necessidade de compra
- 📊 Geração de relatório em Excel para download

## 🔄 Regras de Consumo e Transposição

### ▶️ Quando o destino for **PL**:
1. Consome estoque do próprio PL
2. Se faltar, permite transposição de MP, AA, PV
3. Se ainda faltar, usa RP **diretamente**
4. Se ainda faltar, indica compra

### ▶️ Quando o destino for **PV**:
1. Consome estoque do próprio PV
2. Se faltar, permite transposição de MP, AA, PL
3. **Nunca usa** componentes RP
4. Se ainda faltar, indica compra

## ⚙️ Tecnologias Utilizadas

- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [OpenPyXL](https://openpyxl.readthedocs.io/)

## 🧪 Como Usar Localmente

1. Instale o Python (https://python.org)
2. Instale os pacotes com:
   ```
   pip install -r requirements.txt
   ```
3. Rode o app:
   ```
   streamlit run app.py
   ```

## 🌐 Como Usar na Web (via Streamlit Cloud)

1. Crie uma conta em [streamlit.io](https://streamlit.io/cloud)
2. Crie um repositório no GitHub e envie os arquivos
3. Conecte o GitHub ao Streamlit Cloud
4. Publique o app 100% online

---

## 📝 Histórico de Versões

**R11.5**
- Correção na barra de rolagem
- Organização dos botões (Executar Análise / Nova Análise)
- Compatibilidade com arquivos CSV e Excel
- Melhorias de layout e título
