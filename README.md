# Stock Screener

A Python-based desktop application for screening stocks based on financial metrics such as Market Cap, PE Ratio, EBITDA, and more. The app fetches ticker data from Nasdaq and NYSE exchanges, retrieves financial data using the `yfinance` library, and allows users to apply custom filters via a PyQt5 GUI.

## Features

- **GUI Interface**: Built with PyQt5, featuring checkboxes and input fields for selecting and configuring filters.
- **Data Sources**: Fetches Nasdaq/NYSE tickers from `ftp.nasdaqtrader.com` and financial data from Yahoo Finance.
- **Custom Filters**: Filter stocks by metrics like PE Ratio (< threshold), Market Cap (> threshold), etc.
- **Caching**: Saves fetched data to `cached_results.csv` to speed up subsequent runs.
- **Multithreading**: Uses `ThreadPoolExecutor` for efficient data fetching.

## Requirements

- Python 3.12 or higher
- Ubuntu (or compatible Linux distribution; WSL supported but not tested)
- Virtual environment recommended
- Dependencies (listed in `requirements.txt`):
  - `pandas`
  - `yfinance`
  - `PyQt5`
  - `requests`

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/jmacneill66/stock_screener.git
   cd stock_screener
   ```

Using the GUI:
The app displays a window with checkboxes and input fields for financial metrics (e.g., Market Cap, PE Ratio).

Check the boxes for the metrics you want to filter.

Enter numeric threshold values (e.g., 20 for PE Ratio, 1000000000 for Market Cap).

Click Run Screener to fetch and filter stocks.

Results are displayed in a table, showing ticker symbols and metric values.

Example Filters:
PE Ratio: < 20 (stocks with PE Ratio less than 20)

Market Cap: > 1000000000 (stocks with Market Cap over 1 billion)

Dividend Yield: > 0.02 (stocks with Dividend Yield over 2%)

Notes:
If no values are entered for checked metrics, the app will display all fetched stocks without filtering.

The app currently fetches Nasdaq/NYSE tickers only (TSX support is disabled due to an invalid data source).

stock_screener/
├── data/
│   ├── fetch_data.py      # Fetches stock data using yfinance
│   ├── filter_logic.py    # Applies user-defined filters
│   ├── get_tickers.py     # Fetches ticker lists
├── ui/
│   ├── main_window.py     # PyQt5 GUI implementation
├── main.py                # Entry point for the application
├── requirements.txt       # List of dependencies
├── cached_results.csv     # Cache file (generated after running)
└── README.md              # Project documentation