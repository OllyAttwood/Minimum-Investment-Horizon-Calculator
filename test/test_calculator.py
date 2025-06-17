"""Tests for the calculator.py functions.

If the command "pytest" doesn't work (as it didn't for me), use
"python -m pytest" instead.

See https://www.tutorialspoint.com/pytest/index.htm for more help
"""

import pytest
from pytest import approx
import pandas as pd
import numpy as np
import sys
from pathlib import Path
#the next couple of lines are needed to be able to import modules from the parent directory
parent_dir = Path(__file__).resolve().parent.parent #get the parent directory
sys.path.append(str(parent_dir)) #add parent directory to sys.path
import calculator
import data_locations

@pytest.mark.parametrize(
    "index_name, minimum_profit_percentage_threshold, inflation, output",
    [
        ("S&P 500", 0, 0, 73.73737373737373),
        ("MSCI World", 20, 0, 32.608695652173914),
        ("FTSE All World", 0, 2.5, 75.0),
        ("MSCI Emerging Markets", 100, 3, 0)
    ]
)
def test_get_profit_chances(index_name, minimum_profit_percentage_threshold, inflation, output):
    profit_chances = calculator.get_profit_chances(index_name, minimum_profit_percentage_threshold, inflation)["profit_chances"][0]
    #use approx() as we are doing float comparison
    assert profit_chances == approx(output)

@pytest.mark.parametrize(
    "index_name, inflation, output",
    [
        ("S&P 500", 0, 1.2502),
        ("MSCI World", 10, 0.9690898083358964),
        ("FTSE All World", 20, 0.874031041270934),
        ("MSCI Emerging Markets", 50, 1.0003067021276597)
    ]
)
def test_process_annual_returns_from_file_path(index_name, inflation, output):
    file_path = data_locations.get_data_info()[index_name]
    annual_return = calculator.process_annual_returns_from_file_path(file_path, inflation)["Return"][0]
    assert annual_return == approx(output)

@pytest.mark.parametrize("window_size, annual_returns, output",
    [
        (3, [1.5, 1.1, 0.9, 1, 1.4], [1.485, 0.99, 1.26]),
        (1, [0.99, 1.3, 1.05], [0.99, 1.3, 1.05]),
        (4, [1.01, 2, 0.8, 1.1], [1.7776])
    ]
)
def test_calculate_rolling_window_returns(window_size, annual_returns, output):
    annual_returns = pd.DataFrame(data=annual_returns, columns=["Return"])
    window_returns = calculator.calculate_rolling_window_returns(window_size, annual_returns)
    assert np.all(np.isclose(window_returns, output))

@pytest.mark.parametrize(
    "window_returns, minimum_profit_percentage_threshold, output",
    [
        ([1.6, 1.1, 1.00001, 0.9999], 0, 75), #probabilities are in percentage form
        ([3.4, 2.9], 200, 50),
        ([1.05, 1.3, 0.9], 100, 0),
        ([2.006, 3.1, 2.5], 100, 100)
    ]
)
def test_calculate_chance_of_profit(window_returns, minimum_profit_percentage_threshold, output):
    window_returns = pd.Series(window_returns)
    chance = calculator.calculate_chance_of_profit(window_returns, minimum_profit_percentage_threshold)
    assert chance == approx(output)
