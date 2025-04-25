import numpy as np
from fpdf import FPDF

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



def generate_pdf_report(metrics_path="reports/benchmarks/backtest_metrics.csv", output_pdf="reports/Backtest_Summary.pdf"):
    metrics = pd.read_csv(metrics_path, index_col=0)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Note: No trades were executed during this period.", ln=True)

    pdf.cell(200, 10, txt="Bank Nifty Backtest Summary", ln=True, align='C')
    pdf.ln(10)

    for index, row in metrics.iterrows():
        pdf.cell(200, 10, txt=f"{index}: {row.values[0]:.2f}", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, txt="Equity Curve:", ln=True)
    pdf.image("reports/equity_curve.png", x=10, y=None, w=180)

    pdf.output(output_pdf)
    print(f"✅ PDF report generated: {output_pdf}")
