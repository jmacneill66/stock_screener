# data/get_tickers.py
import pandas as pd
import requests
from io import StringIO

def get_nasdaq_nyse_tickers():
    nasdaq_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt"
    other_url = "ftp://ftp.nasdaqtrader.com/SymbolDirectory/otherlisted.txt"

    def find_symbol_column(df, source_name):
        possible_columns = ['Symbol', 'Ticker', 'ACT Symbol', 'Security Name']
        for col in possible_columns:
            if col in df.columns:
                return col
        print(f"Error: No symbol column found in {source_name}. Columns: {df.columns.tolist()}")
        return None

    try:
        nasdaq_data = pd.read_csv(nasdaq_url, sep='|')
        print("Nasdaq columns:", nasdaq_data.columns.tolist())
        nasdaq_col = find_symbol_column(nasdaq_data, "Nasdaq data")

        other_data = pd.read_csv(other_url, sep='|')
        print("Other columns:", other_data.columns.tolist())
        other_col = find_symbol_column(other_data, "Other data")

        if nasdaq_col is None or other_col is None:
            return []

        nasdaq_tickers = [str(t) for t in nasdaq_data[nasdaq_col].dropna().tolist() if isinstance(t, str)]
        other_tickers = [str(t) for t in other_data[other_col].dropna().tolist() if isinstance(t, str)]

        tickers = list(set(nasdaq_tickers + other_tickers))
        print("Nasdaq/NYSE tickers sample:", tickers[:5])
        return tickers
    except Exception as e:
        print("Error fetching NASDAQ/NYSE:", e)
        return []

def get_tsx_tickers():
    # Replace with a valid TSX ticker CSV source
    tsx_url = "https://example.com/tsx_tickers.csv"  # Placeholder: find a real URL
    try:
        response = requests.get(tsx_url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        print("TSX columns:", df.columns.tolist())
        possible_columns = ['Symbol', 'Ticker', 'Code']
        for col in possible_columns:
            if col in df.columns:
                tickers = [str(t) for t in df[col].dropna().tolist() if isinstance(t, str)]
                print("TSX tickers sample:", tickers[:5])
                return tickers
        print("Error: No symbol column found in TSX data. Columns:", df.columns.tolist())
        return []
    except Exception as e:
        print("Error fetching TSX tickers:", e)
        return []

def get_all_tickers():
    tickers = get_nasdaq_nyse_tickers()
    tickers += get_tsx_tickers()
    non_strings = [t for t in tickers if not isinstance(t, str)]
    if non_strings:
        print("Warning: Non-string tickers found:", non_strings)
    tickers = [str(t) for t in tickers]
    return sorted(list(set(tickers)))