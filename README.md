## Introduction
A Python program to view the probabilities of making a profit investing in various stock market indices over different timescales, based on historical data. It allows the user to specify what profit percentage they are aiming for and adjust for inflation. The software is built using Pandas, NumPy, SciPy and Matplotlib, as well as unit testing with Pytest.

## Features
- **Index Comparison**: Compare multiple market indices simultaneously.
- **Dynamic Adjustments**: Update the graph instantly for modified inflation and profit thresholds.
- **Historical Popups**: View best, worst, and median performance metrics for different investment timeframes.

## How To Run
### External Libraries Needed
- Matplotlib
- NumPy
- SciPy
- Pandas

### Command
```bash
python3 main.py
```

## Demo Gifs

### Ability To Compare Different Stock Market Indices
![Indices Demo Gif](https://s13.gifyu.com/images/b7MBl.gif)

### Graph Changes Animation
When changes are made to the graph via the minimum profit threshold textbox or the inflation textbox, the lines are smoothly updated to aid interpretability.
![Animation Demo Gif](https://s13.gifyu.com/images/b7MBu.gif)

### Index Data Popups
These popups show the best-performing, worst-performing, and median periods of the selected period size and index (values are adjusted for the provided inflation value). The popups are colour-coded for easy recognition with the corresponding index.
![Popup Demo Gif](https://s13.gifyu.com/images/b7MBn.gif)
