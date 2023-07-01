#!/bin/env python3
from .csv_util import load_csv
from .metrics import orm_per_lift

import argparse

import ipdb
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
TABULATE_KWARGS = {"showindex": False, "numalign": "right", "stralign": "left", "floatfmt": ".1f"}


def get_headers(columns: list[str]) -> list[str]:
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
    disp = tabulate.tabulate(df, headers=headers, **TABULATE_KWARGS)
    print(disp)


def show_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    mask = df["name"] == args.name
    df = df[mask]
    headers = get_headers(df.columns)
    disp = tabulate.tabulate(df, headers=headers, **TABULATE_KWARGS)
    print(disp)


def list_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    names = df["name"].unique()
    names.sort()
    disp = "\n".join(names)
    print(disp)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

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
