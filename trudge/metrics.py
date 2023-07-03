import enum
import math
import pandas as pd
import numpy as np
from typing import Any


class OrmFormula(enum.Enum):
    Brzycki = enum.auto()
    Epley = enum.auto()
    Lander = enum.auto()
    Lombardi = enum.auto()
    Mayhew = enum.auto()
    OConner = enum.auto()
    Wathan = enum.auto()


def orm(reps: Any, weight: Any, formula: OrmFormula = OrmFormula.Brzycki) -> Any:
    """https://www.athlegan.com/calculate-1rm

    Parameters
    ==========
    reps : int or pd.Series
    weight : float or pd.Series
        units don't matter
    formula
        Exactly what it says

    Returns
    =======
    one rep max, in whatever the type of `weight` is
    """
    if formula == OrmFormula.Brzycki:
        return weight * (36.0 / (37.0 - reps))
    if formula == OrmFormula.Epley:
        return weight * (1.0 + 0.0333 * reps)
    if formula == OrmFormula.Lander:
        return (100.0 * weight) / (101.3 - 2.67123 * reps)
    if formula == OrmFormula.Lombardi:
        return weight * reps**0.1
    if formula == OrmFormula.Mayhew:
        return (100.0 * weight) / (52.2 + (41.9 * math.e - 0.055 * reps))
    if formula == OrmFormula.OConner:
        return weight * (1 + 0.025 * reps)
    if formula == OrmFormula.Wathan:
        return (100.0 * weight) / (48.8 + (53.8 * math.e**-0.075 * reps))


def orm_series(df: pd.DataFrame) -> pd.Series:
    """
    Compute equivalent 1 rep max for every set in the record.

    Parameters
    ==========
    df : pd.DataFrame
        Presumed to be the raw parsed CSV with no extra information

    Returns
    =======
    pd.Series
        1 rep max for each set. Index into `df` is same as index into the return.
    """
    return pd.Series(orm(reps=df["reps"], weight=df["weight"]), name="orm")


def orm_per_lift(df: pd.DataFrame) -> pd.DataFrame:
    max_orm_per_set = pd.DataFrame(columns=("name", "time", "orm"))
    # equivalent ORM for each set
    set_orms = orm_series(df)
    # unique lift names
    max_orm_per_set["name"] = df["name"].unique()
    for out_idx, name in enumerate(max_orm_per_set["name"]):
        # find all set ORMs for this lift name
        mask = df["name"] == name
        these_orms = set_orms[mask]
        # where the max ORM
        in_idx = these_orms.idxmax()
        max_orm_per_set.at[out_idx, "time"] = df["time"][in_idx]
        max_orm_per_set.at[out_idx, "orm"] = set_orms[in_idx]
    return max_orm_per_set
