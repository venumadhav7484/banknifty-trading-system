import pandas as pd

def fetch_futures_data(symbol="BANKNIFTY", start_date="2023-01-01", end_date="2023-12-31"):
    """
    Fetch Bank Nifty futures data (mock for now).
    """
    try:
        df = pd.read_csv(f"data/dummy_data/{symbol.lower()}_dummy.csv", parse_dates=['date'])
        df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
        df.reset_index(drop=True, inplace=True)
        return df
    except FileNotFoundError:
        print(f"❌ Data file for {symbol} not found.")
        return pd.DataFrame()
