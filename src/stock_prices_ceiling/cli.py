from __future__ import annotations

import argparse

from .calculator import CalculationConfig, calculate_many
from .exporters import export_results
from .providers import YFinanceProvider


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calcula preco teto usando dividendos historicos do yfinance."
    )
    parser.add_argument("tickers", nargs="+", help="Tickers, com ou sem o sufixo .SA")
    parser.add_argument(
        "--years", type=int, default=5, help="Quantidade de anos completos a considerar (padrao: 5)"
    )
    parser.add_argument(
        "--profit",
        type=float,
        default=6.0,
        help="Taxa anual desejada em porcentagem (padrao: 6)",
    )
    parser.add_argument(
        "--output", default="output/preco_teto.xlsx", help="Saida .xlsx ou .csv"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = CalculationConfig(args.years, args.profit)
    results, errors = calculate_many(args.tickers, YFinanceProvider(), config)
    output = export_results(results, errors, args.output)

    print(f"Arquivo exportado: {output}")
    print(f"Acoes calculadas: {len(results)}")
    if errors:
        print(f"Acoes com erro: {len(errors)} (consulte a aba Erros)")
    return 0 if results else 1


if __name__ == "__main__":
    raise SystemExit(main())
