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

# only psychopaths use white backgrounds
plt.style.use("dark_background")


def plot_orm(record: pd.DataFrame, set_orms: pd.Series, desc: str) -> None:
    """ """
    if record.shape[0] != set_orms.shape[0]:
        raise RuntimeError(f"size mismatch {record.size} != {set_orms.size}")

    N = record.shape[0]

    zero_idx = record.index[0]
    # what gets plotted
    data = pd.DataFrame(columns=["orm", "weight", "reps", "effort"])
    data.loc[0] = {
        "orm": 0,
        "weight": 0,
        "reps": 0,
        "effort": 0,
    }
    data.loc[1] = {
        "orm": set_orms[zero_idx],
        "weight": record["weight"][zero_idx],
        "reps": record["reps"][zero_idx],
        "effort": record["effort"][zero_idx],
    }
    # label the date for the first set of each workout
    dividers = pd.DataFrame(columns=["label"])
    dividers.loc[0] = record["time"][zero_idx].date().isoformat()
    # mask means indexes are no longer a range, so we have to use the index property
    # FIXME: could probably do this inline somehow
    for zero_idx, (i1, i2) in enumerate(zip(record.index[:-1], record.index[1:])):
        t1 = record["time"][i1]
        t2 = record["time"][i2]
        if t1 != t2:
            dividers.loc[len(data)] = t2.date().isoformat()
            data.loc[len(data)] = {
                "orm": np.nan,
                "weight": np.nan,
                "reps": np.nan,
                "effort": np.nan,
            }
        data.loc[len(data)] = {
            "orm": set_orms[i2],
            "weight": record["weight"][i2],
            "reps": record["reps"][i2],
            "effort": record["effort"][i2],
        }

    # FIXME: alternative to all this is just to insert a new row everytime the date changes?? idk
    #        this is very inelegant but whatever it works.

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
        xticks=dividers.index,
        xticklabels=[],
    )
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
        print(sel)
        print(sel.index)

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
    axes[0].set_xticks(dividers.index, labels=dividers["label"], rotation=60)
    axes[1].set_xticks(dividers.index, labels=dividers["label"], rotation=60)
    axes[0].tick_params(labelbottom=False)

    plt.tight_layout()
    plt.show()
