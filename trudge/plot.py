# pip
from matplotlib.colors import Normalize
from matplotlib.ticker import MaxNLocator
from mplcursors import cursor
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
    count = 2
    orm_data = [0, set_orms[zero_idx]]
    weight_data = [0, record["weight"][zero_idx]]
    rep_data = [0, record["reps"][zero_idx]]
    effort_data = [0, record["effort"][zero_idx]]
    # label the date for the first set of each workout
    x_ticks = [0]
    x_labels = [record["time"][zero_idx].date().isoformat()]
    # mask means indexes are no longer a range, so we have to use the index property
    # FIXME: could probably do this inline somehow
    for zero_idx, (i1, i2) in enumerate(zip(record.index[:-1], record.index[1:])):
        t1 = record["time"][i1]
        t2 = record["time"][i2]

        if t1 != t2:
            x_ticks.append(count)
            x_labels.append(t2.date().isoformat())

            count += 1
            orm_data.append(np.nan)
            weight_data.append(np.nan)
            rep_data.append(np.nan)
            effort_data.append(np.nan)

        count += 1
        orm_data.append(set_orms[i2])
        weight_data.append(record["weight"][i2])
        rep_data.append(record["reps"][i2])
        effort_data.append(record["effort"][i2])

    # FIXME: alternative to all this is just to insert a new row everytime the date changes?? idk
    #        this is very inelegant but whatever it works.
    data = pd.DataFrame(
        {
            "orm": orm_data,
            "weight": weight_data,
            "reps": rep_data,
            "effort": effort_data,
        }
    )

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
        xticks=x_ticks,
        xticklabels=[],
    )
    cursor(
        axes[0],
        annotation_kwargs={
            "arrowprops": {"arrowstyle": "->", "color": "y"},
            "bbox": {"color": "y"},
            "color": "k",
        },
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
    axes[0].set_xticks(x_ticks, labels=x_labels, rotation=60)
    axes[1].set_xticks(x_ticks, labels=x_labels, rotation=60)
    axes[0].tick_params(labelbottom=False)

    plt.tight_layout()
    plt.show()
