# pip
import matplotlib.pyplot as plt
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
    x_data = np.arange(N)
    x_ticks = [0]
    x_labels = [record["time"][record.index[0]].date().isoformat()]
    # mask means indexes are no longer a range, so we have to use the index property
    for i1, i2 in zip(record.index[:-1], record.index[1:]):
        t1 = record["time"][i1]
        t2 = record["time"][i2]
        if t1 != t2:
            x_ticks.append(list(record.index).index(i2))
            x_labels.append(t2.date().isoformat())

    fig, axes = plt.subplots(2, 1, sharex=True)

    axes[0].bar(
        x_data,
        set_orms,
        label="1RM",
        color="r",
    )
    axes[0].bar(
        x_data,
        record["weight"],
        label="Lift",
    )
    axes[0].set_ylabel(trudge.display.get_header("weight"))
    axes[0].grid(alpha=0.3)
    axes[0].set_title(f"1RM History:\n{name}")

    # tick only the first set of each workout
    axes[0].set_xticks(
        x_ticks,
        labels=x_labels,
    )

    axes[1].bar(
        x_data,
        record["reps"],
    )
    axes[1].grid(alpha=0.3)
    axes[1].set_ylabel(trudge.display.get_header("reps"))

    # axes[1].set_xlabel("Date")

    plt.show()
