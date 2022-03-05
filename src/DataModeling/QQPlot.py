import pandas as pd
import matplotlib.pyplot as plt
from numpy import log as ln


def plot(filename="", title="", base_location=""):
    if (filename == "") or (base_location == ""):
        raise Exception("Incorrect File Name")

    qq_plot_df = pd.read_csv(filename, header=None)

    qq_plot_df = qq_plot_df.rename(columns={0: title})

    qq_plot_df.sort_values(by=[title], ascending=True, inplace=True, ignore_index=True, kind='quicksort')

    qq_plot_len = len(qq_plot_df)

    qq_plot_df["ranking"] = qq_plot_df.index + 1

    qq_plot_df["quantile"] = (qq_plot_df["ranking"] - 0.5) / qq_plot_len

    mean = qq_plot_df[title].mean()
    max_value = qq_plot_df[title].max()

    def inverse_exponential_cdf(row):
        return -1 * ln(1 - row["quantile"]) * mean

    qq_plot_df["y"] = qq_plot_df.apply(inverse_exponential_cdf, axis=1)

    point_color = (0.5, 0.5, 0.7, 0.8)

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    ax.scatter(x=qq_plot_df[title], y=qq_plot_df['y'], marker="2", c=point_color)
    ax.plot([0, max_value], [0, max_value], c='orange')

    ax.set_title(title + " QQ Plot")
    ax.set_xlabel(title + " data")
    ax.set_ylabel("Quantities of Exponential distribution")

    plt.savefig(base_location + "QQ_Plot " + title)
    plt.close(fig)

