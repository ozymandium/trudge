import datetime
import pandas as pd

# Column ordering. These are the internal names that are used as column keys
COLUMNS = [
    "time",
    "name",
    "reps",
    "weight",
    "rest",
    "positive",
    "hold",
    "negative",
    "effort",
    "trainer",
    "unilateral",
    "notes",
]


def convert_effort(entry: str):
    val = int(entry)
    if val < 1 or 5 < val:
        raise Exception("effort {} must be on a 5 star scale".format(entry))
    return val


def clean_whitespace(s: str):
    return s.lstrip(" ").rstrip(" ")


CONVERTERS = {
    "time": lambda s: datetime.datetime.fromisoformat(s.replace(" ", "")),
    "name": clean_whitespace,
    "reps": int,
    "weight": float,
    "rest": float,
    "positive": int,
    "hold": int,
    "negative": int,
    "effort": convert_effort,
    "trainer": lambda s: {"Y": True, "N": False}[clean_whitespace(s)],
    "unilateral": lambda s: {"Y": True, "N": False}[clean_whitespace(s)],
    "notes": clean_whitespace,
}


def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(
        path, names=COLUMNS, header=0, converters=CONVERTERS  # to override header row
    )
