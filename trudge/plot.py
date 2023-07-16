# pip
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import MaxNLocator
import pandas as pd
import numpy as np

# local
import trudge.display

# only psychopaths use white backgrounds
plt.style.use("dark_background")


def plot_orm(record: pd.DataFrame, set_orms: pd.Series, name: str) -> None:
    """

    TODO: color bars by effort level from green to red
    """
    if record.shape[0] != set_orms.shape[0]:
        raise RuntimeError(f"size mismatch {record.size} != {set_orms.size}")

    mask = record["name"] == name

    record = record[mask]
    set_orms = set_orms[mask]
    N = record.shape[0]

    # TODO: break between workouts
    zero_idx = record.index[0]
    # what gets plotted
    x_data = [0, 1]
    orm_data = [0, set_orms[zero_idx]]
    weight_data = [0, record["weight"][zero_idx]]
    rep_data = [0, record["reps"][zero_idx]]
    # label the date for the first set of each workout
    x_ticks = [0]
    x_labels = [record["time"][zero_idx].date().isoformat()]
    # mask means indexes are no longer a range, so we have to use the index property
    # FIXME: could probably do this inline somehow
    for zero_idx, (i1, i2) in enumerate(zip(record.index[:-1], record.index[1:])):
        t1 = record["time"][i1]
        t2 = record["time"][i2]

        if t1 != t2:
            x_ticks.append(len(x_data))
            x_labels.append(t2.date().isoformat())

            x_data.append(x_data[-1] + 1)
            orm_data.append(0)
            weight_data.append(0)
            rep_data.append(0)

        x_data.append(x_data[-1] + 1)
        orm_data.append(set_orms[i2])
        weight_data.append(record["weight"][i2])
        rep_data.append(record["reps"][i2])

    plt.figure()
    axes = [plt.subplot(gs) for gs in gridspec.GridSpec(2, 1, height_ratios=[2, 1])]

    # top plot: lifted weight and equivalent 1rm
    axes[0].bar(
        x_data,
        orm_data,
        label="1RM",
        color="r",
    )
    axes[0].bar(
        x_data,
        weight_data,
        label="Lift",
    )
    axes[0].set_ylabel(trudge.display.get_header("weight"))
    axes[0].grid(alpha=0.3)
    axes[0].set_title(f"1RM History:\n{name}")
    axes[0].legend()
    axes[0].set(xticks=x_ticks, xticklabels=[])

    # bottom plot: number of reps
    axes[1].bar(
        x_data,
        rep_data,
    )
    axes[1].grid(alpha=0.3)
    axes[1].set_ylabel(trudge.display.get_header("reps"))
    # tick only the first set of each workout
    axes[1].set_xticks(x_ticks, labels=x_labels, rotation=60)
    # y ticks only on integers
    axes[1].yaxis.set_major_locator(MaxNLocator(integer=True))

    plt.tight_layout()
    plt.show()
