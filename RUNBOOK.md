# Runbook de Operacao

Este documento descreve como executar o calculo de preco teto usando dividendos historicos do Yahoo Finance por meio da biblioteca `yfinance`.

## 1. Pre-requisitos

- Windows com Python 3.10 ou superior.
- Acesso a internet durante a consulta dos dividendos.
- Terminal aberto na pasta do projeto.

Para confirmar o ambiente:

```powershell
py --version
```

Entre na pasta do projeto, caso necessario:

```powershell
cd D:\GitHubPedro\stock-prices\stock-prices-ceiling
```

## 2. Instalacao

Instale o projeto e as dependencias:

```powershell
py -m pip install -e ".[test]"
```

Use `py -m pip` no Windows para garantir que o pip pertence ao mesmo Python usado na execucao.

## 3. Execucao padrao

Informe um ou mais tickers, a quantidade de anos completos, o percentual de lucro desejado e o arquivo de saida:

```powershell
py -m stock_prices_ceiling.cli PSSA3 BBSE3 TAEE4 --years 5 --profit 6 --output output/preco_teto.xlsx
```

O programa:

1. Busca os dividendos pagos por acao no Yahoo Finance.
2. Adiciona `.SA` aos tickers que nao possuem bolsa informada. Por exemplo, `PSSA3` vira `PSSA3.SA`.
3. Soma os dividendos por ano.
4. Exclui o ano corrente.
5. Preenche com zero os anos sem dividendos.
6. Calcula a media anual.
7. Calcula o preco teto.
8. Exporta os resultados.

## 4. Parametros

| Parametro | Obrigatorio | Padrao | Descricao |
| --- | --- | --- | --- |
| `tickers` | sim | - | Um ou mais tickers separados por espaco. |
| `--years` | nao | `5` | Quantidade de anos completos considerados. Deve ser maior que zero. |
| `--profit` | nao | `6` | Taxa desejada em porcentagem. `6` significa 6%, e deve ser maior que zero. |
| `--output` | nao | `output/preco_teto.xlsx` | Arquivo `.xlsx` ou `.csv`. |

Para consultar todos os parametros:

```powershell
py -m stock_prices_ceiling.cli --help
```

## 5. Exemplos

### Carteira com cinco anos e taxa de 6%

```powershell
py -m stock_prices_ceiling.cli PSSA3 BBSE3 TAEE4 EGIE3 B3SA3 ITSA4 CSMG3 BBAS3 SANB4 KLBN4 --years 5 --profit 6 --output output/carteira.xlsx
```

### Analise dos ultimos tres anos com taxa de 8%

```powershell
py -m stock_prices_ceiling.cli ITSA4 VALE3 --years 3 --profit 8 --output output/analise_3_anos.xlsx
```

### Saida em CSV

```powershell
py -m stock_prices_ceiling.cli KLBN4 --years 5 --profit 6 --output output/klbn4.csv
```

O Excel e o formato recomendado quando for necessario consultar o detalhamento anual. O CSV contem o resumo consolidado.

## 6. Formula e interpretacao

A formula usada e:

```text
preco_teto = media_anual / (percentual_desejado / 100)
```

Exemplo: se a soma dos dividendos dos cinco anos for `10,00` e a taxa desejada for `6%`:

```text
media_anual = 10,00 / 5 = 2,00
preco_teto = 2,00 / 0,06 = 33,33
```

O resultado e uma referencia baseada nos dividendos historicos. Ele nao representa garantia de dividendos futuros nem recomendacao de investimento.

## 7. Arquivo Excel

O arquivo `.xlsx` possui tres abas:

### `Resumo`

Uma linha por ticker, contendo:

- `ticker`: ticker informado.
- `ticker_yfinance`: ticker usado na consulta.
- `total_dividendos`: soma dos dividendos no periodo.
- `media_anual`: soma dividida pela quantidade de anos.
- `preco_teto`: media anual dividida pela taxa desejada.

### `Dividendos anuais`

Mostra uma linha por ticker e ano, com o valor de dividendos por acao utilizado no calculo. Anos sem dividendos aparecem com valor zero.

### `Erros`

Lista tickers que nao puderam ser consultados ou calculados. A execucao continua para os demais tickers validos.

## 8. Validacao apos a execucao

Uma execucao bem-sucedida exibe mensagens semelhantes a estas:

```text
Arquivo exportado: output\preco_teto.xlsx
Acoes calculadas: 3
```

Quando houver falhas individuais:

```text
Acoes com erro: 1 (consulte a aba Erros)
```

Confirme se o arquivo existe:

```powershell
Get-Item output\preco_teto.xlsx
```

Para ler o resumo diretamente no terminal:

```powershell
py -c "import pandas as pd; print(pd.read_excel('output/preco_teto.xlsx', sheet_name='Resumo').to_string(index=False))"
```

## 9. Problemas comuns

### `No module named stock_prices_ceiling`

Execute o comando a partir da pasta do projeto e reinstale em modo editavel:

```powershell
py -m pip install -e ".[test]"
```

### `No module named openpyxl`

Instale as dependencias novamente:

```powershell
py -m pip install -e ".[test]"
```

### Ticker aparece na aba `Erros`

Verifique:

- se o ticker existe no Yahoo Finance;
- se o sufixo de bolsa esta correto, como `.SA` para acoes brasileiras;
- se o computador possui acesso a internet;
- se o Yahoo Finance esta respondendo no momento.

Para tickers internacionais, informe explicitamente a bolsa, por exemplo `AAPL.US` ou o simbolo aceito pelo Yahoo Finance.

### Nenhum arquivo foi gerado

O programa retorna codigo de erro quando nenhum ticker e calculado. Corrija os tickers ou a conexao e execute novamente.

### Falha ao gravar Excel

Verifique se o arquivo de destino nao esta aberto no Excel e se a pasta de saida permite gravacao.

## 10. Testes locais

Execute os testes automatizados:

```powershell
py -m pytest
```

Os testes usam dados simulados para validar a formula sem depender da rede ou de dados atuais do Yahoo Finance.
