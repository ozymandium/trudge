import os
from typing import Any

import pandas as pd
import tabulate


_DESCRIPTIONS = {
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
    "heart": "Heart Rate",
    "trainer": "Trainer",
    "unilateral": "Unilateral",
    "notes": "Notes",
    # secondary
    "orm": "1 Rep Max",
}
_SHORT_DESCRIPTIONS = {
    # in the source data
    "time": "Date",
    "name": "Type",
    "reps": "Reps",
    "weight": "Weight",
    "rest": "Rest",
    "positive": "Conc",
    "hold": "Hold",
    "negative": "Ecc",
    "effort": "Effort",
    "heart": "Heart",
    "trainer": "Coach",
    "unilateral": "Unil",
    "notes": "Notes",
    # secondary
    "orm": "1RM",
}
_UNITS = {
    # in the source data
    "time": None,
    "name": None,
    "reps": None,
    "weight": "lb",
    "rest": "min",
    "positive": "sec",
    "hold": "sec",
    "negative": "sec",
    "effort": "1-5",
    "heart": "bpm",
    "trainer": "Y/N",
    "unilateral": "Y/N",
    "notes": None,
    # secondary
    "orm": "lb",
}
_WIDTHS = {
    # in the source data
    "time": None,
    "name": 24,
    "reps": None,
    "weight": None,
    "rest": None,
    "positive": None,
    "hold": None,
    "negative": None,
    "effort": None,
    "heart": None,
    "trainer": None,
    "unilateral": None,
    "notes": 30,
    # secondary
    "orm": None,
}


def prettify_name(obj: Any) -> Any:
    """
    "Press:Behind The Neck:Snatch Grip" -> "Snatch Grip Behind The Neck Press"

    recursive function that prettifies a string, the "name" field of a series, or the "name" column
    of a data frame.
    """
    if type(obj) is pd.DataFrame:
        if "name" in obj.columns:
            return obj.replace({name: prettify_name(name) for name in obj["name"].unique()})
        else:
            return obj
    elif type(obj) is str:
        ret = " ".join(obj.split(":")[-1::-1])
        return ret
    else:
        raise TypeError(f"unknown type {type(obj)}")


def get_header(name: str, newline: bool = False, short: bool = False) -> str:
    desc = _SHORT_DESCRIPTIONS[name] if short else _DESCRIPTIONS[name]
    unit = _UNITS[name]
    if unit is None:
        return desc
    sep = os.linesep if newline else " "
    return f"{desc}{sep}[{unit}]"


def get_headers(df: pd.DataFrame, newline: bool = False, short: bool = False) -> list[str]:
    """
    For an arbitrary pandas DataFrame with column names `columns` get the formatted headers for each
    column to print for human readable output.

    Parameters
    ==========
    df : pd.DataFrame
        dataframe whose columns need appropriate human readable headers

    Returns
    =======
    list[str]
        Order corresponds to input order. List of formatted (including newlines) column headers
    """
    return [get_header(col, newline=newline, short=short) for col in df.columns]


def print_df(df: pd.DataFrame, short: bool = False) -> None:
    """
    Print a pandas DataFrame with human readable headers and prettified names.

    Parameters
    ==========
    df : pd.DataFrame
        dataframe to print
    short : bool
        whether to use short headers (default False)
    """
    disp = tabulate.tabulate(
        prettify_name(df).to_numpy().tolist(),
        headers=get_headers(df, newline=True, short=short),
        showindex=False,
        numalign="right",
        stralign="left",
        floatfmt=".1f",
        tablefmt="fancy_grid",
        maxcolwidths=[_WIDTHS[c] for c in df.columns],
    )
    print(disp)


def df_to_csv(df: pd.DataFrame, path: str) -> None:
    """
    Write a dataframe to a csv file with human readable headers and prettified names.

    Parameters
    ==========
    df : pd.DataFrame
        dataframe to write
    path : str
        path to write to
    """
    df.to_csv(path, header=get_headers(df, newline=False), index=False, float_format="%.1f")
