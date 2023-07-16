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


def get_header(name: str, newline: bool = False) -> str:
    desc = _DESCRIPTIONS[name]
    unit = _UNITS[name]
    sep = "\n" if newline else " "  # if you're on windows fuck you
    unit_add = f"{sep}({unit})" if unit else ""
    return f"{desc}{unit_add}"


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
    return get_header([get_header(col, newline) for col in df.cols])
