from datetime import date

import pandas as pd

from stock_prices_ceiling.calculator import CalculationConfig, calculate_stock, normalize_ticker


def test_calculates_annual_dividends_and_excludes_current_year():
    current_year = date.today().year
    index = pd.to_datetime(
        [
            f"{current_year - 2}-03-01",
            f"{current_year - 2}-09-01",
            f"{current_year - 1}-04-01",
            f"{current_year}-01-01",
        ]
    )
    dividends = pd.Series([1.0, 0.5, 2.0, 99.0], index=index)

    result = calculate_stock("TEST3", dividends, CalculationConfig(2, 10, current_year))

    assert result.ticker == "TEST3.SA"
    assert result.dividends_by_year == {current_year - 2: 1.5, current_year - 1: 2.0}
    assert result.dividend_total == 3.5
    assert result.annual_average == 1.75
    assert result.ceiling_price == 17.5


def test_normalize_ticker_preserves_explicit_exchange():
    assert normalize_ticker(" ita.sa ") == "ITA.SA"
    assert normalize_ticker("AAPL") == "AAPL.SA"
