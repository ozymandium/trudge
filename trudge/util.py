import pandas as pd


def name_mask(df: pd.DataFrame, prefix: str) -> pd.Series:
    """
    get a mask for all indexes into `df` where the column `"name"` starts with `prefix`
    """
    mask = pd.Series(index=df.index)
    for idx in df.index:
        mask[idx] = df["name"][idx].startswith(prefix)
    return mask
