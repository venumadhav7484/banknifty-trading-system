import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from data.fetch_futures_data import fetch_futures_data
from data.fetch_vix_data import fetch_vix_data

# Test fetching Bank Nifty data
bnf_data = fetch_futures_data(symbol="BANKNIFTY", start_date="2023-01-10", end_date="2023-01-20")
print(" Bank Nifty Data Sample:")
print(bnf_data.head())

# Test fetching VIX data
vix_data = fetch_vix_data(start_date="2023-01-10", end_date="2023-01-20")
print("\nVIX Data Sample:")
print(vix_data.head())

# Test VIX Normalization
from data.fetch_vix_data import normalize_vix
vix_today = vix_data['vix'].iloc[0]
adjusted_multiplier = normalize_vix(vix_today)
print(f"\n Normalized Multiplier for VIX {vix_today}: {adjusted_multiplier:.2f}")
