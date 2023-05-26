import enum
import math
import pandas as pd
import numpy as np


class OrmFormula(enum.Enum):
    Brzycki = enum.auto()
    Epley = enum.auto()
    Lander = enum.auto()
    Lombardi = enum.auto()
    Mayhew = enum.auto()
    OConner = enum.auto()
    Wathan  = enum.auto()


def orm(reps, weight, formula: OrmFormula = OrmFormula.Brzycki):
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
        return weight * (36. / (37. - reps))
    if formula == OrmFormula.Epley:
        return weight * (1. + 0.0333 * reps)
    if formula == OrmFormula.Lander:
        return (100. * weight) / (101.3 - 2.67123 * reps)
    if formula == OrmFormula.Lombardi:
        return weight * reps ** 0.1
    if formula == OrmFormula.Mayhew:
        return (100. * weight) / (52.2 + (41.9 * math.e - 0.055 * reps))
    if formula == OrmFormula.OConner:
        return weight * (1 + 0.025 * reps)
    if formula == OrmFormula.Wathan:
        return (100. * weight) / (48.8 + (53.8 * math.e ** -0.075 * reps))


def orm_series(df: pd.DataFrame) -> pd.Series:
    return pd.Series(orm(reps=df["reps"], weight=df["weight"]), name="orm")
