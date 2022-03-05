from Histogram import plot_hist
from QQPlot import plot_QQ
from ChiSquareTable import chi_square
from RandomNumberGenerator import rand_test
import os

base_path = os.path.realpath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep + os.pardir + os.sep +\
            "dataset" + os.sep
base_output_plot_path = os.path.realpath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep + os.pardir +\
                        os.sep + "output" + os.sep + "plot" + os.sep
base_output_csv_path = os.path.realpath(__file__) + os.sep + os.pardir + os.sep + os.pardir + os.sep + os.pardir +\
                        os.sep + "output" + os.sep + "csv" + os.sep

WS1_TIME_DATA_FILE = base_path + "ws1.dat"
WS2_TIME_DATA_FILE = base_path + "ws2.dat"
WS3_TIME_DATA_FILE = base_path + "ws3.dat"
I11_TIME_DATA_FIlE = base_path + "servinsp1.dat"
I22_TIME_DATA_FIlE = base_path + "servinsp22.dat"
I23_TIME_DATA_FIlE = base_path + "servinsp23.dat"

WS1_NAME = "Workstation 1 Processing Time"
WS2_NAME = "Workstation 2 Processing Time"
WS3_NAME = "Workstation 3 Processing Time"
I11_NAME = "Inspector 1 Service Time for Component 1"
I22_NAME = "Inspector 2 Service Time for Component 2"
I23_NAME = "Inspector 2 Service Time for Component 3"


# main function for data modeling
def main():
    plot_hist(I11_TIME_DATA_FIlE, title=I11_NAME, bin_bias=10, base_location=base_output_plot_path)
    plot_hist(I22_TIME_DATA_FIlE, title=I22_NAME, bin_bias=10, base_location=base_output_plot_path)
    plot_hist(I23_TIME_DATA_FIlE, title=I23_NAME, bin_bias=10, base_location=base_output_plot_path)
    plot_hist(WS1_TIME_DATA_FILE, title=WS1_NAME, bin_bias=8, base_location=base_output_plot_path)
    plot_hist(WS2_TIME_DATA_FILE, title=WS2_NAME, bin_bias=8, base_location=base_output_plot_path)
    plot_hist(WS3_TIME_DATA_FILE, title=WS3_NAME, bin_bias=8, base_location=base_output_plot_path)

    plot_QQ(I11_TIME_DATA_FIlE, title=I11_NAME, base_location=base_output_plot_path)
    plot_QQ(I22_TIME_DATA_FIlE, title=I22_NAME, base_location=base_output_plot_path)
    plot_QQ(I23_TIME_DATA_FIlE, title=I23_NAME, base_location=base_output_plot_path)
    plot_QQ(WS1_TIME_DATA_FILE, title=WS1_NAME, base_location=base_output_plot_path)
    plot_QQ(WS2_TIME_DATA_FILE, title=WS2_NAME, base_location=base_output_plot_path)
    plot_QQ(WS3_TIME_DATA_FILE, title=WS3_NAME, base_location=base_output_plot_path)

    chi_square(I11_TIME_DATA_FIlE, title=I11_NAME, bin_bias=10, base_location=base_output_csv_path)
    chi_square(I22_TIME_DATA_FIlE, title=I22_NAME, bin_bias=10, base_location=base_output_csv_path)
    chi_square(I23_TIME_DATA_FIlE, title=I23_NAME, bin_bias=10, base_location=base_output_csv_path)
    chi_square(WS1_TIME_DATA_FILE, title=WS1_NAME, bin_bias=8, base_location=base_output_csv_path)
    chi_square(WS2_TIME_DATA_FILE, title=WS2_NAME, bin_bias=8, base_location=base_output_csv_path)
    chi_square(WS3_TIME_DATA_FILE, title=WS3_NAME, bin_bias=8, base_location=base_output_csv_path)

    rand_test(base_location=base_output_plot_path)


# run main function
if __name__ == "__main__":
    main()