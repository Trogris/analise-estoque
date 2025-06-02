# 📘 Análise de Estoque para Produção

## Objetivo
Registrar a lógica atualizada e regras aplicadas na análise de estoque para produção de equipamentos voltados à locação (PL) e venda (PV), contemplando transposições, uso direto de componentes reparados (RP), e critérios de priorização de consumo de estoque.

## Prefixos e Significados
- PL – Produto para Locação: manutenção por conta da empresa.
- PV – Produto para Venda: deve usar componentes novos ou homologados.
- MP – Matéria-Prima.
- AA – Almoxarifado Auxiliar.
- RP – Componentes Reparados: uso limitado.

## Regras de Transposição
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
| RP     | Qualquer| ❌         |

## Lógica de Consumo – PL
1. Verifica saldo no próprio prefixo PL
2. Tenta transpor de MP, PV, AA para PL
3. Se ainda faltar, verifica saldo no RP (uso direto, sem transposição)
4. Se ainda faltar, sinaliza saldo a comprar

## Lógica de Consumo – PV
1. Verifica saldo no próprio prefixo PV
2. Tenta transpor de MP, PL, AA para PV
3. Nunca utiliza RP
4. Se ainda faltar, sinaliza saldo a comprar