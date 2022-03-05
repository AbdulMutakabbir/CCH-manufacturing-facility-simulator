import pandas as pd
import math
import matplotlib.pyplot as plt

class Random:

    __seed = None
    __multiplier = 9
    __increment = 2**7 - 1
    __modulus = 2**48
    __last_rand = None

    # Constructor
    def __init__(self, seed=0):
        self.seed = seed
        self.last_rand = seed

    # Returns uniform distribution of random number
    def random_probability(self):
        self.last_rand = (self.__multiplier * self.last_rand + self.__increment) % self.__modulus
        return self.last_rand / self.__modulus

    def random_exponential(self, mean=None):
        if (mean is None) or (math.isnan(mean)):
            raise Exception("Mean Not Specified")
        uniform_rand = self.random_probability()
        return -1 * mean * math.log(uniform_rand, math.e)


def rand_test(base_location):
    rand_expo = []
    rand_uni = []
    r = Random(3**6 - 1)
    n = 9999
    bar_color = (0.5, 0.5, 0.7, 0.2)
    bar_border_color = (0.3, 0.3, 0.7, 0.8)

    for _ in range(n):
        rand_expo.append(r.random_exponential(8.75))
    expo_title = "Exponential Distribution Generator"
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(x=rand_expo,
            facecolor=bar_color,
            edgecolor=bar_border_color)
    ax.set_title(expo_title)
    ax.set_xlabel(expo_title + " Range")
    ax.set_ylabel("Frequency")
    plt.savefig(base_location + expo_title)
    plt.close(fig)
    # histogram = pd.cut(rand_expo, range(0, 100, 10)).value_counts().sort_index()
    # print(histogram)

    for _ in range(n):
        rand_uni.append(r.random_probability())
    uni_title = "Uniform Distribution Generator"
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.hist(x=rand_uni,
            facecolor=bar_color,
            edgecolor=bar_border_color)
    ax.set_title(uni_title)
    ax.set_xlabel(uni_title + " Range")
    ax.set_ylabel("Frequency")
    plt.savefig(base_location + uni_title)
    plt.close(fig)
    # histogram = pd.cut(rand_uni, [_/10 for _ in range(0, 100, 10)]).value_counts().sort_index()
    # print(histogram)