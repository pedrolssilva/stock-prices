from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class CalculationConfig:
    years_to_look: int
    desired_profit_percent: float
    reference_year: int | None = None

    @property
    def profit_rate(self) -> float:
        return self.desired_profit_percent / 100

    @property
    def years(self) -> list[int]:
        current_year = self.reference_year or date.today().year
        return list(range(current_year - self.years_to_look, current_year))


@dataclass(frozen=True)
class StockCalculation:
    requested_ticker: str
    ticker: str
    dividends_by_year: dict[int, float]
    dividend_total: float
    annual_average: float
    ceiling_price: float


def calculate_stock(
    ticker: str,
    dividends: pd.Series,
    config: CalculationConfig,
) -> StockCalculation:
    if config.years_to_look < 1:
        raise ValueError("years_to_look deve ser maior que zero")
    if config.profit_rate <= 0:
        raise ValueError("desired_profit_percent deve ser maior que zero")

    requested_ticker = ticker.upper().strip()
    normalized_ticker = normalize_ticker(requested_ticker)
    annual_dividends = _group_dividends_by_year(dividends)
    values = {year: round(float(annual_dividends.get(year, 0.0)), 8) for year in config.years}
    total = sum(values.values())
    average = total / config.years_to_look

    return StockCalculation(
        requested_ticker=requested_ticker,
        ticker=normalized_ticker,
        dividends_by_year=values,
        dividend_total=total,
        annual_average=average,
        ceiling_price=average / config.profit_rate,
    )


def calculate_many(
    tickers: Iterable[str],
    dividend_provider,
    config: CalculationConfig,
) -> tuple[list[StockCalculation], list[dict[str, str]]]:
    results = []
    errors = []
    for ticker in tickers:
        try:
            normalized = normalize_ticker(ticker)
            dividends = dividend_provider.dividends(normalized)
            results.append(calculate_stock(ticker, dividends, config))
        except Exception as error:
            errors.append({"ticker": ticker.strip().upper(), "error": str(error)})
    return results, errors


def normalize_ticker(ticker: str) -> str:
    clean_ticker = ticker.strip().upper()
    if not clean_ticker:
        raise ValueError("ticker vazio")
    return clean_ticker if "." in clean_ticker else f"{clean_ticker}.SA"


def _group_dividends_by_year(dividends: pd.Series) -> pd.Series:
    if dividends is None or dividends.empty:
        return pd.Series(dtype="float64")
    series = pd.to_numeric(dividends, errors="coerce").dropna()
    if series.empty:
        return pd.Series(dtype="float64")
    dates = pd.to_datetime(series.index)
    return series.groupby(dates.year).sum()
