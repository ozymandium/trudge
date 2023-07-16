#!/bin/env python3
# system
import argparse

# pip
import pandas as pd
import tabulate

# local
import trudge


def orm_handler(record: pd.DataFrame, args: argparse.Namespace) -> None:
    set_orms = trudge.metrics.orm_series(record)

    if args.list:
        res = trudge.metrics.orm_per_lift(record, set_orms)
        res = res.sort_values(args.sort, ascending=args.asc)
        headers = trudge.display.get_headers(res, newline=True)
        disp = tabulate.tabulate(
            res.to_numpy().tolist(),
            headers=headers,
            showindex=False,
            numalign="right",
            stralign="left",
            floatfmt=".1f",
        )
        print(disp)

    elif args.plot:
        trudge.plot.plot_orm(record, set_orms, args.plot)

    else:
        print("No ")


def show_handler(record: pd.DataFrame, args: argparse.Namespace) -> None:
    mask = record["name"] == args.name
    res = record[mask]
    headers = trudge.display.get_headers(res, newline=True)
    disp = tabulate.tabulate(
        res.to_numpy().tolist(),
        headers=headers,
        showindex=False,
        numalign="right",
        stralign="left",
        floatfmt=".1f",
    )
    print(disp)


def list_handler(record: pd.DataFrame, args: argparse.Namespace) -> None:
    res = record["name"].unique()
    res.sort()
    disp = "\n".join(res)
    print(disp)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(required=True, dest="cmd", help="command to run")

    parser.add_argument("csv_path", help="Path to CSV tracking file")

    orm_parser = subparsers.add_parser("orm", help="Highest 1 rep max equivalent for each lift")
    orm_parser.add_argument("-l", "--list", action="store_true", help="List 1RM for all lifts")
    orm_parser.add_argument(
        "-p",
        "--plot",
        type=str,
        help="Plot 1RM history for specific lift. To see options, `trudge list`",
    )
    orm_parser.add_argument(
        "--sort",
        help="How to sort 1RM (default 1RM)",
        default="orm",
        choices=["time", "name", "orm"],
    )
    orm_parser.add_argument(
        "--asc", action="store_true", help="Show in ascending order along requested column"
    )
    orm_parser.set_defaults(func=orm_handler)

    show_parser = subparsers.add_parser("show", help="Show raw recorded data for a specific lift")
    show_parser.add_argument("name", help="Name of the lift to show recorded data for")
    show_parser.set_defaults(func=show_handler)

    list_parser = subparsers.add_parser("list", help="List all tracked lifts")
    list_parser.set_defaults(func=list_handler)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    record = trudge.csv.load(args.csv_path)
    args.func(record, args)


if __name__ == "__main__":
    main()
