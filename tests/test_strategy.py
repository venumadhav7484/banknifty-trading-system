import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from data.fetch_futures_data import fetch_futures_data
from data.fetch_vix_data import fetch_vix_data
from backtrader.supertrend_adaptive import SupertrendAdaptiveStrategy 

df = fetch_futures_data()
vix_df = fetch_vix_data()

strategy = SupertrendAdaptiveStrategy(config_path="config/banknifty_config.yaml", df=df, vix_df=vix_df)
strategy.apply_strategy()
print("✅ Strategy applied. Trades logged in logs/trade_logs.csv")
