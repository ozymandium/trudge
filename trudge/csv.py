import datetime
import pandas as pd
from typing import Callable


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
    "heart",
    "trainer",
    "unilateral",
    "notes",
]
MIN_EFFORT = 1
MAX_EFFORT = 5


def _convert_effort(entry: str) -> int:
    val = int(entry)
    if val < MIN_EFFORT or MAX_EFFORT < val:
        raise Exception(f"invalid effort {entry}")
    return val


def _clean_whitespace(s: str) -> str:
    return s.lstrip(" ").rstrip(" ")


_CONVERTERS: dict[str, Callable] = {
    "time": lambda s: datetime.datetime.fromisoformat(s.replace(" ", "")),
    "name": _clean_whitespace,
    "reps": int,
    "weight": float,
    "rest": float,
    "positive": int,
    "hold": int,
    "negative": int,
    "effort": _convert_effort,
    "heart": lambda s: int(s) if s else None,
    "trainer": lambda s: {"Y": True, "N": False}[_clean_whitespace(s)],
    "unilateral": lambda s: {"Y": True, "N": False}[_clean_whitespace(s)],
    "notes": _clean_whitespace,
}


def load(path: str) -> pd.DataFrame:
    record = pd.read_csv(path, converters=_CONVERTERS)
    assert set(record.columns) == set(COLUMNS)
    return record
