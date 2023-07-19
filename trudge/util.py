import pandas as pd


def name_mask(df: pd.DataFrame, prefix: str) -> pd.Series:
    """
    get a mask for all indexes into `df` where the column `"name"` starts with `prefix`
    """
    mask = pd.Series(index=df.index)
    for idx in df.index:
        mask[idx] = df["name"][idx].startswith(prefix)
    return mask


def session_clusters(df: pd.DataFrame, column="time") -> list[list[object]]:
    """
    cluster all the sets into clusters such that each cluster occurred at the same time and return
    indices to organize this way
    """
    if df.index.is_monotonic_increasing and df.index[0] == 0:
        # this works if the index is a range index.
        # FIXME: make it work for arbitrary indexing
        # FIXME: better way to detect would be df.index == df.reset_index() == df.index but that
        #        seems inefficient?
        # find where the time field changes and that is the first set of each session
        is_first_set = df[column].diff().astype(bool)
        begin = is_first_set.index[is_first_set].to_list()
        # now if i can be as deeply clever about populating the rest..
        end_idxs = begin[1:] + [len(df)]
        return [list(range(begin, end)) for begin, end in zip(begin, end_idxs)]
    else:
        # slow dumb way that works for anything
        clusters = [[df.index[0]]]
        for zero_idx in range(1, len(df)):
            idx0 = clusters[-1][-1]
            idx1 = df.index[zero_idx]
            val0 = df[column][idx0]
            val1 = df[column][idx1]
            if val0 == val1:
                clusters[-1].append(idx1)
            else:
                clusters.append([idx1])
        return clusters
