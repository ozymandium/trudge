#!/bin/env python3
# system
import argparse

# pip
import pandas as pd

# local
import trudge


def orm_list_handler(record: pd.DataFrame, args: argparse.Namespace) -> None:
    set_orms = trudge.metrics.orm_series(record)
    res = trudge.metrics.orm_per_lift(record, set_orms)
    res = res.sort_values(args.sort, ascending=args.asc)
    if args.output is not None:
        if args.output.endswith(".csv"):
            trudge.display.df_to_csv(res, args.output)
        else:
            raise ValueError(f"unknown output format {args.output}")
    else:
        trudge.display.print_df(res)


def orm_plot_handler(record: pd.DataFrame, args: argparse.Namespace) -> None:
    # FIXME: consolidate this call with `orm_list_handler`
    set_orms = trudge.metrics.orm_series(record)
    mask = trudge.util.name_mask(record, args.name)
    trudge.plot.plot_orm(record[mask], set_orms[mask], desc=args.name)


def show_handler(record: pd.DataFrame, args: argparse.Namespace) -> None:
    mask = trudge.util.name_mask(record, args.name)
    res = record[mask]
    trudge.display.print_df(res)


def list_handler(record: pd.DataFrame, args: argparse.Namespace) -> None:
    res = record["name"].unique().sort()
    print("\n".join(res))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    # trudge <...>
    sps = p.add_subparsers(required=True, dest="cmd", help="command to run")

    # trudge <...> /path/to/log.csv
    p.add_argument("csv_path", help="Path to CSV tracking file")

    # trudge orm <...> /path/to/log.csv
    orm_sp = sps.add_parser("orm", help="Highest 1 rep max equivalent for each lift")
    orm_sp.add_argument(
        "-f",
        "--formula",
        choices=[f.name for f in trudge.metrics.OrmFormula],
        help="Formula to use",
        default=trudge.metrics.OrmFormula.Brzycki,
    )
    # orm_sp.set_defaults(func=orm_handler)
    orm_ssps = orm_sp.add_subparsers(required=True, dest="orm_cmd", help="1RM command to run")

    # trudge orm list <...> /path/to/log.csv
    orm_list_ssp = orm_ssps.add_parser("list", help="List 1RM for all lifts")
    orm_list_ssp.add_argument(
        "--sort",
        help="How to sort 1RM (default 1RM)",
        default="orm",
        choices=trudge.metrics.ORM_PER_LIFT_COLS,
    )
    orm_list_ssp.add_argument(
        "--asc", action="store_true", help="Show in ascending order along requested column"
    )
    orm_list_ssp.add_argument(
        "-o", "--output", help="Output file to write to. Will infer format from extension."
    )
    orm_list_ssp.set_defaults(func=orm_list_handler)
    # FIXME: help for `trudge orm list -h` doesn't work
    # FIXME: shared upper function for orm, with split lower functions for subcommands somehow???

    # trudge orm plot <name> /path/to/log.csv
    orm_plot_ssp = orm_ssps.add_parser("plot", help="Plot 1RM history for specific lift.")
    orm_plot_ssp.add_argument("name", help="Lift to plot. To see options, `trudge list`")
    orm_plot_ssp.set_defaults(func=orm_plot_handler)

    # trudge show <name> /path/to/log.csv
    show_p = sps.add_parser("show", help="Show raw recorded data for a specific lift")
    show_p.add_argument("name", help="Name of the lift to show recorded data for")
    show_p.set_defaults(func=show_handler)

    # trudge list /path/to/log.csv
    list_p = sps.add_parser("list", help="List all tracked lifts")
    list_p.set_defaults(func=list_handler)

    return p.parse_args()


def main() -> None:
    args = parse_args()
    record = trudge.csv.load(args.csv_path)
    args.func(record, args)


if __name__ == "__main__":
    main()
