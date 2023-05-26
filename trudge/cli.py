#!/bin/env python3
from .csv_util import load_csv
from .metrics import orm_series

import argparse

import pandas as pd


def orm_handler(args: argparse.Namespace) -> None:
    df = load_csv(args.csv_path)
    orms = orm_series(df)
    names = df["name"].unique()
    data = []
    for name in names:
        mask = df["name"] == name
        these_orms = orms[mask]
        idx = these_orms.idxmax()
        data.append([
            name,
            df["time"][idx],
            orms[idx],
        ])
    res = pd.DataFrame(data, columns=("Name", "Time", "1RM"))
    print(res.sort_values(args.sort, ascending=args.asc))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    orm_parser = subparsers.add_parser("orm", help="1 rep max")
    orm_parser.add_argument("csv_path", help="Path to CSV tracking file")
    orm_parser.add_argument("--sort", help="How to sort 1RM (default 1RM)", default="1RM")
    orm_parser.add_argument("--asc", action="store_true", help="Show in ascending order along requested column")
    orm_parser.set_defaults(func=orm_handler)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
