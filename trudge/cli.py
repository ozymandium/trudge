#!/bin/env python3
from .csv_util import load_csv
from .metrics import orm_per_lift

import argparse

import ipdb
import pandas as pd
import tabulate


def orm_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    df = orm_per_lift(df)
    df = df.sort_values(args.sort, ascending=args.asc)
    disp = tabulate.tabulate(df, showindex=False, numalign="right", stralign="left", floatfmt=".1f")
    print(disp)


def show_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    mask = df["name"] == args.name
    print(df[mask])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    orm_parser = subparsers.add_parser("orm", help="Highest 1 rep max equivalent for each lift")
    orm_parser.add_argument("csv_path", help="Path to CSV tracking file")
    orm_parser.add_argument("--sort", help="How to sort 1RM (default 1RM)", default="orm")
    orm_parser.add_argument("--asc", action="store_true", help="Show in ascending order along requested column")
    orm_parser.set_defaults(func=orm_handler)

    show_parser = subparsers.add_parser("show", help="Show raw recorded data for a specific lift")
    show_parser.add_argument("csv_path", help="Path to CSV tracking file")
    show_parser.add_argument("name", help="Name of the lift to show recorded data for")
    show_parser.set_defaults(func=show_handler)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
