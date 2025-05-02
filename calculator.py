import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline

#calculates the compound returns for all periods (windows) of a given size in years
def calculate_rolling_window_returns(window_size, annual_returns):
    windows =  annual_returns.rolling(window=window_size)

    return windows["Return"].apply(np.prod)[window_size-1:] #trim the first window_size-1 rows as they're empty

#calculates the overall chance of making a profit from all the compound returns of a single window size
def calculate_chance_of_profit(window_returns):
    profit_loss_counts = (window_returns > 1).value_counts()

    #handles the condition where all the windows result in profits or all windows result in losses
    if len(profit_loss_counts) == 1:
        if profit_loss_counts.keys()[0] == True: #explicitly included "== True" for clarity
            return 100
        else:
            return 0

    num_profit_windows = profit_loss_counts[True]
    num_loss_windows = profit_loss_counts[False]
    percentage_profit_windows = num_profit_windows / (num_profit_windows + num_loss_windows) * 100

    return percentage_profit_windows

#produce a smoothed version of the graph line
#see https://www.geeksforgeeks.org/how-to-plot-a-smooth-curve-in-matplotlib/
def smooth_line(original_line):
    x = np.array(range(len(original_line)))
    spline = make_interp_spline(x, original_line)
    x_increased_num_points = np.linspace(x.min(), x.max(), 500)

    return spline(x_increased_num_points)

#extracts the minimum, maximum and median values of a single window size
def min_max_median(window_returns):
    return {
        "min": window_returns.min(),
        "max": window_returns.max(),
        "median": window_returns.median()
    }

#gets the annual returns data from the CSV file, then processes the data so it is
#suitable for cumulatively multiplying to find the total return for a longer period
def process_annual_returns_from_file_path(annual_returns_path):
    annual_returns = pd.read_csv(annual_returns_path)
    annual_returns["Return"] = (annual_returns["Return"] / 100) + 1

    return annual_returns

#function for the presenter class to call
def get_profit_chances():
    file_path = "/home/olly/Documents/programming/other/minimum_investment_horizon_calculator/data/sp500_annual_returns_slickcharts_com.csv"
    annual_returns = process_annual_returns_from_file_path(file_path)
    window_sizes = range(1,30)
    window_returns_list = [calculate_rolling_window_returns(window_size, annual_returns) for window_size in window_sizes]
    chance_of_profit_list = [calculate_chance_of_profit(window_returns) for window_returns in window_returns_list]
    print(chance_of_profit_list)
    print(window_returns_list)
    min_max_medians = [min_max_median(window_returns) for window_returns in window_returns_list]
    print(min_max_medians)

    return chance_of_profit_list
