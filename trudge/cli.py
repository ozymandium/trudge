#!/bin/env python3
from trudge.csv_util import load_csv
from trudge.metrics import orm_per_lift

import argparse

import pandas as pd
import tabulate


DESCRIPTIONS = {
    # in the source data
    "time": "Date",
    "name": "Type",
    "reps": "Reps",
    "weight": "Weight",
    "rest": "Rest",
    "positive": "Concentric",
    "hold": "Hold",
    "negative": "Eccentric",
    "effort": "Effort",
    "trainer": "Trainer",
    "unilateral": "Unilateral",
    "notes": "Notes",
    # secondary
    "orm": "1 Rep Max",
}
UNITS = {
    # in the source data
    "time": "",
    "name": "",
    "reps": "",
    "weight": "lb",
    "rest": "min",
    "positive": "sec",
    "hold": "sec",
    "negative": "sec",
    "effort": "1-5",
    "trainer": "Y/N",
    "unilateral": "Y/N",
    "notes": "",
    # secondary
    "orm": "lb",
}


def get_headers(columns: pd.Index) -> list[str]:
    """
    For an arbitrary pandas DataFrame with column names `columns` get the formatted headers for each
    column to print for human readable output.

    Parameters
    ==========
    columns : pd.Index
        list of column names, each of which must appear as a key in both DESCRIPTIONS and UNITS

    Returns
    =======
    list[str]
        Order corresponds to input order. List of formatted (including newlines) column headers
    """
    headers = []
    for col in columns:
        desc = DESCRIPTIONS[col]
        unit = UNITS[col]
        unit_add = f"\n({unit})" if unit else ""
        headers.append(f"{desc}{unit_add}")
    return headers


def orm_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    df = orm_per_lift(df)
    df = df.sort_values(args.sort, ascending=args.asc)
    headers = get_headers(df.columns)
    disp = tabulate.tabulate(
        df.to_numpy().tolist(),
        headers=headers,
        showindex=False,
        numalign="right",
        stralign="left",
        floatfmt=".1f",
    )
    print(disp)


def show_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    mask = df["name"] == args.name
    df = df[mask]
    headers = get_headers(df.columns)
    disp = tabulate.tabulate(
        df.to_numpy().tolist(),
        headers=headers,
        showindex=False,
        numalign="right",
        stralign="left",
        floatfmt=".1f",
    )
    print(disp)


def list_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    names = df["name"].unique()
    names.sort()
    disp = "\n".join(names)
    print(disp)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True, dest="cmd", help="command to run")

    orm_parser = subparsers.add_parser("orm", help="Highest 1 rep max equivalent for each lift")
    orm_parser.add_argument("csv_path", help="Path to CSV tracking file")
    orm_parser.add_argument("--sort", help="How to sort 1RM (default 1RM)", default="orm")
    orm_parser.add_argument(
        "--asc", action="store_true", help="Show in ascending order along requested column"
    )
    orm_parser.set_defaults(func=orm_handler)

    show_parser = subparsers.add_parser("show", help="Show raw recorded data for a specific lift")
    show_parser.add_argument("csv_path", help="Path to CSV tracking file")
    show_parser.add_argument("name", help="Name of the lift to show recorded data for")
    show_parser.set_defaults(func=show_handler)

    list_parser = subparsers.add_parser("list", help="List all tracked lifts")
    list_parser.add_argument("csv_path", help="Path to CSV tracking file")
    list_parser.set_defaults(func=list_handler)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
