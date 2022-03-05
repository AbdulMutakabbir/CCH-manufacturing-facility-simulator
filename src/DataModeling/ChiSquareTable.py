import pandas as pd
import math


def chi_square(filename="", title="", bin_bias=0, base_location=""):
    if (filename == "") or (base_location == ""):
        raise Exception("Incorrect File Name")

    df = pd.read_csv(filename, header=None)
    df = df.rename(columns={0: "frequency"})

    data_points_count = len(df)

    bins_count = math.sqrt(data_points_count)
    bins_count = math.floor(bins_count) - bin_bias

    max_data_value = df["frequency"].max()
    max_data_value = math.ceil(max_data_value)

    bin_step = max_data_value / bins_count
    bin_step = math.ceil(bin_step)

    bins = range(0, max_data_value + bin_step, bin_step)
    mean = df["frequency"].mean()

    histogram = pd.cut(df["frequency"], bins).value_counts().sort_index()
    histogram = pd.DataFrame(histogram)
    histogram = histogram.reset_index()
    histogram = histogram.rename(columns={"index": "range"})

    def exponential_cdf(row, n=data_points_count):
        lambda_val = 1 / mean
        power_left = -1 * lambda_val * row["range"].left
        power_right = -1 * lambda_val * row["range"].right
        return n * (math.pow(math.e, power_left) - math.pow(math.e, power_right))

    histogram["expected_frequency"] = histogram.apply(exponential_cdf, axis=1)
    histogram["O-E"] = histogram["frequency"] - histogram["expected_frequency"]
    histogram["(O-E)^2/E"] = (histogram["O-E"] ** 2) / histogram["expected_frequency"]
    histogram["range"] = histogram["range"].astype(str)

    histogram.to_csv(base_location + "ChiSquare " + title + ".csv")
