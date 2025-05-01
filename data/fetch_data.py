# data/fetch_data.py
import os
import yfinance as yf
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from data.get_tickers import get_all_tickers
import threading
import queue

def timeout_handler(ticker, q):
    q.put(None)  # Signal timeout

def fetch_single_ticker(ticker):
    q = queue.Queue()
    timer = threading.Timer(5, timeout_handler, args=(ticker, q))
    timer.start()
    try:
        print(f"Fetching: {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        result = {
            'Ticker': ticker,
            'Market Cap': info.get('marketCap', 0),
            'PE Ratio': info.get('trailingPE', None),
            'EBITDA': info.get('ebitda', None),
            'Revenue Growth 1Y': info.get('revenueGrowth', None),
            'Revenue Growth 3Y': None,
            'EPS': info.get('trailingEps', None),
            'ROE': info.get('returnOnEquity', None),
            'Debt/Equity': info.get('debtToEquity', None),
            'Current Ratio': info.get('currentRatio', None),
            'Dividend Yield': info.get('dividendYield', None)
        }
        q.put(result)
    except Exception as e:
        print(f"Error with {ticker}: {e}")
        q.put(None)
    finally:
        timer.cancel()

    result = q.get()
    if result is None:
        print(f"Timeout or error fetching: {ticker}")
        return None
    return result

def get_stock_data(limit=1000, max_threads=20, use_cache=True):
    cache_file = "cached_results.csv"
    numeric_columns = [
        'Market Cap', 'PE Ratio', 'EBITDA', 'Revenue Growth 1Y',
        'EPS', 'ROE', 'Debt/Equity', 'Current Ratio', 'Dividend Yield'
    ]

    if use_cache and os.path.exists(cache_file):
        print("Loading data from cache...")
        try:
            df = pd.read_csv(cache_file)
            if df.empty or not df.columns.any():
                print("Warning: Cache file is empty or invalid, fetching fresh data...")
            else:
                for col in numeric_columns:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')
                print("Cache DataFrame types:", df.dtypes)
                print("Cache DataFrame shape:", df.shape)
                return df
        except Exception as e:
            print(f"Error loading cache: {e}, fetching fresh data...")

    tickers = get_all_tickers()[:limit]
    if not tickers:
        print("Error: No tickers available, returning empty DataFrame")
        return pd.DataFrame(columns=['Ticker'] + numeric_columns)

    # Filter out tickers with special characters (e.g., .U, .W, $)
    valid_tickers = [t for t in tickers if not any(c in t for c in ['.', '$'])]
    print(f"Filtered {len(tickers) - len(valid_tickers)} invalid tickers. Valid count: {len(valid_tickers)}")
    tickers = valid_tickers

    results = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = {executor.submit(fetch_single_ticker, t): t for t in tickers}
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                print(f"Thread error for {futures[future]}: {e}")

    df = pd.DataFrame(results)
    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    print("Fresh DataFrame types:", df.dtypes)

    if use_cache and not df.empty:
        try:
            df.to_csv(cache_file, index=False)
            print("Saved data to cache. Shape:", df.shape)
        except Exception as e:
            print(f"Error saving cache: {e}")

    return df