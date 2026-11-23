from __future__ import annotations

from pathlib import Path

import pandas as pd

from .calculator import StockCalculation


def export_results(
    results: list[StockCalculation],
    errors: list[dict[str, str]],
    output_path: str | Path,
) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    summary, details, error_rows = _dataframes(results, errors)

    if path.suffix.lower() == ".xlsx":
        with pd.ExcelWriter(path, engine="openpyxl") as writer:
            summary.to_excel(writer, sheet_name="Resumo", index=False)
            details.to_excel(writer, sheet_name="Dividendos anuais", index=False)
            error_rows.to_excel(writer, sheet_name="Erros", index=False)
    elif path.suffix.lower() == ".csv":
        summary.to_csv(path, index=False, sep=";", decimal=",")
    else:
        raise ValueError("O arquivo de saida deve terminar em .xlsx ou .csv")
    return path


def _dataframes(results: list[StockCalculation], errors: list[dict[str, str]]):
    summary_rows = []
    detail_rows = []
    for result in results:
        summary_rows.append(
            {
                "ticker": result.requested_ticker,
                "ticker_yfinance": result.ticker,
                "total_dividendos": result.dividend_total,
                "media_anual": result.annual_average,
                "preco_teto": result.ceiling_price,
            }
        )
        for year, dividend in result.dividends_by_year.items():
            detail_rows.append(
                {
                    "ticker": result.requested_ticker,
                    "ano": year,
                    "dividendos_por_acao": dividend,
                }
            )

    return (
        pd.DataFrame(summary_rows),
        pd.DataFrame(detail_rows),
        pd.DataFrame(errors, columns=["ticker", "error"]),
    )
