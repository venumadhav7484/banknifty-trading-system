import pandas as pd
import plotly.graph_objects as go

def plot_equity_curve(log_path="logs/virtual_trading_log.csv", output_path="reports/equity_curve.html"):
    df = pd.read_csv(log_path)
    if df.empty:
        print("⚠️ No data to plot. Generating placeholder chart.")
        import plotly.express as px
        fig = px.line(x=[0], y=[0], title="No Data Available")
        fig.write_html(output_path)
        fig.write_image("reports/equity_curve.png")
        return


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['Equity'], mode='lines', name='Equity Curve'))

    fig.update_layout(title='Equity Curve', xaxis_title='Date', yaxis_title='Equity Value')
    fig.write_html(output_path)
    fig.write_image("reports/equity_curve.png")
    print(f"✅ Equity curve saved to {output_path} and reports/equity_curve.png")

if __name__ == "__main__":
    plot_equity_curve()
