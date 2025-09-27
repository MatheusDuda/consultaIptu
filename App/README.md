# Documentação - Análise de Dados IPTU BH 2022

## 1. Origem dos Dados
- **Fonte:** Portal de Dados Abertos da Prefeitura de Belo Horizonte
- **URL:** https://ckan.pbh.gov.br/dataset/iptu-bairro
- **Dataset:** IPTU por Bairro - Exercício 2022

## 2. Formato dos Dados
- **Formato:** CSV (Valores separados por ponto e vírgula)
- **Encoding:** UTF-8
- **Colunas:**
  - `BAIRRO`: Nome do bairro (string)
  - `QDE_LANCAMENTOS`: Quantidade de lançamentos (inteiro)
  - `VALOR_TOTAL_LANCADO`: Valor total em Reais (decimal)

## 3. Periodicidade
- **Atualização:** Anual
- **Período de referência:** Exercício fiscal de 2022
- **Última atualização:** Dados referentes ao ano de 2022

## 4. Análise Exploratória
- **Total de registros:** 451 bairros
- **Valor total lançado:** Aproximadamente R$ 2 bilhões (em 2022)
- **Bairros com maior valor:** Savassi, Lourdes, Buritis
- **Formato numérico:** Valores em formato brasileiro (1.234,56)

## 5. Entidades Principais
### Bairro
- Atributos: id, nome
- Relacionamento: 1:N com AnoLancamento

### AnoLancamento  
- Atributos: id, ano, valor_total_lancado
- Relacionamento: Pertence a 1 Bairro, tem 1 QdeLancamento

### QdeLancamento
- Atributos: id, quantidade_lancamento
- Relacionamento: Pertence a 1 AnoLancamento