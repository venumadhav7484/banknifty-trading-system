import numpy as np

def calculate_performance_metrics(trades_df):
    if trades_df.empty:
        print("⚠️ No trades executed. Cannot compute performance metrics.")
        return {
            "Total Return (%)": 0,
            "CAGR (%)": 0,
            "Sharpe Ratio": 0,
            "Max Drawdown (%)": 0,
            "Calmar Ratio": 0
        }

    equity_curve = trades_df['equity']
    
    if len(equity_curve) < 2:
        print("⚠️ Insufficient data points to compute meaningful metrics.")
        return {
            "Total Return (%)": 0,
            "CAGR (%)": 0,
            "Sharpe Ratio": 0,
            "Max Drawdown (%)": 0,
            "Calmar Ratio": 0
        }

    returns = equity_curve.pct_change().dropna()

    total_return = (equity_curve.iloc[-1] - equity_curve.iloc[0]) / equity_curve.iloc[0] * 100
    cagr = ((equity_curve.iloc[-1] / equity_curve.iloc[0]) ** (1/1)) - 1  # Assuming 1 year
    sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() != 0 else 0
    max_dd = max_drawdown(equity_curve)
    calmar = cagr / abs(max_dd) if max_dd != 0 else 0

    return {
        "Total Return (%)": total_return,
        "CAGR (%)": cagr * 100,
        "Sharpe Ratio": sharpe,
        "Max Drawdown (%)": max_dd * 100,
        "Calmar Ratio": calmar
    }

def max_drawdown(equity_curve):
    peak = equity_curve.expanding(min_periods=1).max()
    drawdown = (equity_curve - peak) / peak
    return drawdown.min()
