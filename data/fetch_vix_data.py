import pandas as pd

def fetch_vix_data(start_date="2023-01-01", end_date="2023-12-31"):
    """
    Fetch India VIX data (mock for now).
    """
    try:
        vix_df = pd.read_csv("data/dummy_data/vix_dummy.csv", parse_dates=['date'])
        vix_df = vix_df[(vix_df['date'] >= start_date) & (vix_df['date'] <= end_date)]
        vix_df.reset_index(drop=True, inplace=True)
        return vix_df
    except FileNotFoundError:
        print("❌ VIX data file not found.")
        return pd.DataFrame()

def normalize_vix(vix_value, base=15):
    """
    Normalize VIX to adjust strategy parameters dynamically.
    """
    return vix_value / base
