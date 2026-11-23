# Stock Prices Ceiling

Calcula o preco teto de acoes brasileiras usando dividendos historicos obtidos pelo `yfinance`.

## Regra

Para cada ticker, o programa:

1. Busca os dividendos pagos por acao.
2. Soma os dividendos por ano.
3. Considera os ultimos `N` anos completos, excluindo o ano corrente.
4. Calcula a media anual.
5. Calcula `preco_teto = media_anual / (percentual_desejado / 100)`.

Anos sem dividendos entram como zero na media. O resultado `.xlsx` contem as abas `Resumo`, `Dividendos anuais` e `Erros`.

## Instalar

```powershell
py -m pip install -e ".[test]"
```

## Executar

```powershell
py -m stock_prices_ceiling.cli PSSA3 BBSE3 TAEE4 --years 5 --profit 6 --output output/preco_teto.xlsx
```

Para uma saida simples em CSV:

```powershell
py -m stock_prices_ceiling.cli PSSA3 BBSE3 --years 5 --profit 6 --output output/preco_teto.csv
```

Tickers sem bolsa recebem automaticamente o sufixo `.SA`. A coleta depende de acesso a internet e dos dados disponibilizados pelo Yahoo Finance.

## Testar

```powershell
py -m pytest
```

## Debug no VS Code

O projeto possui uma configuracao de debug em `.vscode/launch.json`.

### Preparar o debug

1. Instale a extensao **Python** da Microsoft no VS Code.
2. Abra a pasta raiz do projeto.
3. Selecione o mesmo interpretador Python usado na instalacao das dependencias.
4. Abra um arquivo Python, por exemplo `src/stock_prices_ceiling/calculator.py`.
5. Clique na margem esquerda de uma linha para criar um breakpoint.

### Iniciar

Pressione `F5` e selecione **Preco teto: executar em debug**.

A configuracao executa o equivalente a:

```powershell
py -m stock_prices_ceiling.cli KLBN4 --years 5 --profit 6 --output output/preco_teto-DEBUG.xlsx
```

O resultado sera salvo em `output/preco_teto-DEBUG.xlsx`. Para depurar outros tickers ou parametros, altere o campo `args` em `.vscode/launch.json`.

### Atalhos durante o debug

- `F5`: continuar a execucao.
- `F10`: executar a proxima linha sem entrar na funcao.
- `F11`: entrar na funcao chamada.
- `Shift+F11`: sair da funcao atual.
- **Variables**: consultar valores de variaveis, como `config`, `results` e `errors`.

Tambem e possivel iniciar a aplicacao diretamente pelo terminal, sem breakpoints:

```powershell
py -m stock_prices_ceiling.cli PSSA3 --years 5 --profit 6 --output output/preco_teto.xlsx
```
