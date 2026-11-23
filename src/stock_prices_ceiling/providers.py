from __future__ import annotations

import yfinance as yf


class YFinanceProvider:
    """Busca dividendos pagos por acao no Yahoo Finance."""

    def dividends(self, ticker: str):
        dividends = yf.Ticker(ticker).dividends
        if dividends is None:
            raise ValueError(f"Nenhum dado de dividendos retornado para {ticker}")
        return dividends
