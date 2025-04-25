import pandas as pd
from data.fetch_futures_data import fetch_futures_data
from data.fetch_vix_data import fetch_vix_data
from backtrader.supertrend_adaptive import SupertrendAdaptiveStrategy
from reports.generate_reports import calculate_performance_metrics

def send_email_alert(subject, message):
    # Simulated email alert (placeholder for real SMTP integration)
    print(f"\n📧 EMAIL ALERT: {subject}\n{message}\n")

def run_forward_simulation():
    print("🚀 Starting Forward Simulation for 2024...")

    # === Load 2024 Data ===
    df = fetch_futures_data(start_date="2024-01-01", end_date="2024-12-31")
    vix_df = fetch_vix_data(start_date="2024-01-01", end_date="2024-12-31")

    # === Initialize Strategy ===
    strategy = SupertrendAdaptiveStrategy(config_path="config/banknifty_config.yaml", df=df, vix_df=vix_df)
    strategy.apply_strategy()

    # === Load Execution Logs ===
    trades = pd.read_csv("logs/margin_events.csv")
    print(f"Number of trades executed: {len(trades)}")
    print(trades.head())

    # === Daily P&L Tracking ===
    trades['date'] = pd.to_datetime(trades['date'])
    daily_pnl = trades.groupby(trades['date'].dt.date)['equity'].last().reset_index()
    daily_pnl.rename(columns={'equity': 'Equity'}, inplace=True)
    daily_pnl['Daily_Return'] = daily_pnl['Equity'].pct_change().fillna(0)

    # Save Virtual Trading Log
    daily_pnl.to_csv("logs/virtual_trading_log.csv", index=False)
    print("📄 Virtual trading log saved to logs/virtual_trading_log.csv")

    # === Performance Metrics ===
    metrics = calculate_performance_metrics(trades)

    # === Trigger Alerts ===
    if metrics["Max Drawdown (%)"] < -10:
        send_email_alert("⚠️ High Drawdown Alert", f"Max Drawdown reached {metrics['Max Drawdown (%)']:.2f}%")

    if metrics["Total Return (%)"] > 15:
        send_email_alert("🎉 Profit Milestone", f"Total Return crossed {metrics['Total Return (%)']:.2f}%")

    # === Save Summary ===
    pd.Series(metrics).to_csv("reports/benchmarks/forward_simulation_metrics.csv")
    print("\n✅ Forward Simulation completed. Metrics saved to reports/benchmarks/forward_simulation_metrics.csv")

if __name__ == "__main__":
    run_forward_simulation()
