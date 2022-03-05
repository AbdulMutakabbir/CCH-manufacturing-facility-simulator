import pandas as pd
import matplotlib.pyplot as plt
import math


def plot(filename="", title="", bin_bias=0, base_location=""):
    if (filename == "") or (base_location == ""):
        raise Exception("Incorrect File Name")

    plot_df = pd.read_csv(filename, header=None)
    plot_df = plot_df.rename(columns={0: title})

    data_points_count = len(plot_df)

    bins_count = math.sqrt(data_points_count)
    bins_count = math.floor(bins_count) - bin_bias

    max_data_value = plot_df[title].max()
    max_data_value = math.ceil(max_data_value)

    bin_step = max_data_value/bins_count
    bin_step = math.ceil(bin_step)

    x_ticks = range(0, max_data_value + bin_step, bin_step)

    bar_color = (0.5, 0.5, 0.7, 0.2)
    bar_border_color = (0.3, 0.3, 0.7, 0.8)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.hist(x=plot_df[title],
            bins=x_ticks,
            facecolor=bar_color,
            edgecolor=bar_border_color)

    ax.set_title(title)
    ax.set_xticks(x_ticks)
    ax.set_xlabel(title + " Range")
    ax.set_ylabel("Frequency")

    plt.savefig(base_location + "Histogram " + title)
    plt.close(fig)
