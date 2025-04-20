import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#calculates the compound returns for all periods (windows) of a given size in years
def calculate_rolling_window_returns(window_size, index_annual_return_file_name):
    annual_returns = pd.read_csv(index_annual_return_file_name)
    annual_returns["Return"] = (annual_returns["Return"] / 100) + 1
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


file_path = "/home/olly/Documents/programming/other/minimum_investment_horizon_calculator/data/sp500_annual_returns_slickcharts_com.csv"
window_sizes = range(1,30)
window_returns_list = [calculate_rolling_window_returns(window_size, file_path) for window_size in window_sizes]
chance_of_profit_list = [calculate_chance_of_profit(window_returns) for window_returns in window_returns_list]
print(chance_of_profit_list)
plt.plot(chance_of_profit_list)
plt.show()
print(window_returns_list)
