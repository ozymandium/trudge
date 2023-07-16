import os
import pandas as pd


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
    "trainer": "Trainer",
    "unilateral": "Unilateral",
    "notes": "Notes",
    # secondary
    "orm": "1 Rep Max",
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
    "trainer": "Y/N",
    "unilateral": "Y/N",
    "notes": None,
    # secondary
    "orm": "lb",
}


def get_header(name: str, newline: bool = False) -> str:
    desc = _DESCRIPTIONS[name]
    unit = _UNITS[name]
    if unit is None:
        return desc
    sep = os.linesep if newline else " "
    return f"{desc}{sep}[{unit}]"


def get_headers(df: pd.DataFrame, newline: bool = False) -> list[str]:
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
    return [get_header(col, newline=newline) for col in df.columns]
