# pip
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator
from mplcursors import cursor as mplcursor
from matplotlib.axis import Tick
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# local
import trudge.display
import trudge.util

# only psychopaths use white backgrounds
plt.style.use("dark_background")


def plot_orm(record: pd.DataFrame, set_orms: pd.Series, desc: str) -> None:
    """ """
    COLS = ["orm", "weight", "reps", "effort", "orig_idx"]
    if record.shape[0] != set_orms.shape[0]:
        raise RuntimeError(f"size mismatch {record.size} != {set_orms.size}")
    if not np.all(record.index == set_orms.index):
        raise RuntimeError("indices don't match")

    # before we blow everything out of the water reindexing, store the original indexes for each row
    orig_idxs = pd.DataFrame({"orig_idx": record.index}, index=record.index)
    # merge the 2 data frames and reindex to speed up cluster finding
    data = record.join(set_orms).join(orig_idxs).reset_index()
    # get indices for new rows before first set of each session
    new_row_idxs = np.array([s[0] for s in trudge.util.session_clusters(data)]) - 0.5
    # remove unnecessary columns now that we've used "time" to find clusters
    data = data.drop([c for c in data.columns if c not in COLS], axis="columns")
    # insert empty rows where we want breaks
    for new_row_idx in new_row_idxs:
        data.loc[new_row_idx] = {c: np.nan for c in COLS}
    # sort and redo the indexing so the new rows aren't at the end
    data = data.sort_index().reset_index(drop=True)

    # dataframe of just labels at the breaks, but indices need to match
    sessions = pd.DataFrame(columns=["label"])
    for idx in data.index[np.isnan(data["reps"])]:
        orig_idx = data.loc[idx + 1]["orig_idx"]
        sessions.loc[idx] = {"label": record.loc[orig_idx]["time"].date().isoformat()}

    plt.figure()
    axes = [plt.subplot(gs) for gs in gridspec.GridSpec(2, 1, height_ratios=[2, 1])]

    # top plot: lifted weight and equivalent 1rm
    axes[0].bar(data.index, data["orm"], label="1RM", color="r")
    axes[0].bar(data.index, data["weight"], label="Lift", color="c")
    # sns.barplot(data, x=data.index, y="orm", color="r", ax=axes[0])
    # sns.barplot(data, x=data.index, y="weight", color="c", ax=axes[0])
    axes[0].grid(alpha=0.3)
    axes[0].legend()
    axes[0].set(
        title=f"1RM History\n{desc}",
        ylabel=trudge.display.get_header("weight"),
        xticks=sessions.index,
        xticklabels=[],
    )

    # bottom plot: number of reps
    effort_cmap = sns.color_palette("blend:green,darkred", as_cmap=True)
    effort_norm = Normalize(vmin=trudge.csv.MIN_EFFORT, vmax=trudge.csv.MAX_EFFORT)
    effort_clrs = effort_cmap(effort_norm(data["effort"]))
    # effort_palette = sns.color_palette("blend:darkred,green", n_colors=5)

    axes[1].bar(data.index, data["reps"], color=effort_clrs)
    # sns.barplot(data, x=data.index, y="reps", hue="effort", ax=axes[1], palette=effort_palette)
    axes[1].grid(alpha=0.3)
    axes[1].set(ylabel=f"{trudge.display.get_header('reps')}\nColored by Effort")
    # y ticks only on integers
    axes[1].yaxis.set_major_locator(MaxNLocator(integer=True))

    # plot interaction

    # FIXME: figure out how to do this automatically by using `gridspec` alongside `subplots`
    #        instead of in place of it.
    axes[1].sharex(axes[0])
    # tick only the first set of each workout
    # for some reason the only way to get ticks to show up on the bottom is to have the same ticks
    # on the top but just not show them??. something about sharex probably.
    axes[0].set_xticks(sessions.index, labels=sessions["label"], rotation=60)
    axes[1].set_xticks(sessions.index, labels=sessions["label"], rotation=60)
    axes[0].tick_params(labelbottom=False)

    # clicking on the top plot makes stuff happen
    cursor = mplcursor(
        axes[0],
        annotation_kwargs={
            "arrowprops": {"arrowstyle": "->", "color": "y"},
            "bbox": {"color": "y"},
            "color": "k",
        },
    )

    @cursor.connect("add")
    def onclick(sel):
        record_idx = data.loc[sel.index]["orig_idx"]
        # import ipdb
        # ipdb.set_trace()
        res = record.loc[record_idx].to_frame().transpose()
        trudge.display.print_df(res)

    plt.tight_layout()
    plt.show()
