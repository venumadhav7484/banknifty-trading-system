import pandas as pd
from data.fetch_futures_data import fetch_futures_data
from data.fetch_vix_data import fetch_vix_data
from backtrader.supertrend_adaptive import SupertrendAdaptiveStrategy
from reports.generate_reports import calculate_performance_metrics

def run_backtest():
    # === Load Data ===
    df = fetch_futures_data()
    vix_df = fetch_vix_data()

    # === Run Strategy ===
    strategy = SupertrendAdaptiveStrategy(config_path="config/banknifty_config.yaml", df=df, vix_df=vix_df)
    strategy.apply_strategy()

    # === Load Execution Logs ===
    trades = pd.read_csv("logs/margin_events.csv")

    # === Calculate Performance Metrics ===
    metrics = calculate_performance_metrics(trades)

    # === Benchmark: Buy & Hold ===
    bh_return = buy_and_hold_benchmark(df)

    # === Summary ===
    print("\n📊 Backtest Summary:")
    for k, v in metrics.items():
        print(f"{k}: {v:.2f}")

    print(f"Buy & Hold Return: {bh_return:.2f}%")

    # Save summary
    pd.Series(metrics).to_csv("reports/benchmarks/backtest_metrics.csv")
    print("\n✅ Backtest completed. Metrics saved to reports/benchmarks/backtest_metrics.csv")

def buy_and_hold_benchmark(df):
    start_price = df['close'].iloc[0]
    end_price = df['close'].iloc[-1]
    return ((end_price - start_price) / start_price) * 100

if __name__ == "__main__":
    run_backtest()
