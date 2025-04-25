class ExecutionEngine:
    def __init__(self, initial_capital=1000000, max_leverage=3):
        self.equity = initial_capital
        self.max_leverage = max_leverage
        self.position = 0   # +1 for long, -1 for short, 0 for no position
        self.trade_log = []
        self.maintenance_margin = 0.12  # 12%

    def calculate_slippage(self, volume):
        return 0.1 if volume > 1e6 else 0.5  # % slippage

    def execute_trade(self, date, action, price, volume):
        slippage_pct = self.calculate_slippage(volume)
        cost_pct = 0.2  # STT + other charges in %

        effective_price = price * (1 + slippage_pct / 100 + cost_pct / 100)

        if action == "BUY":
            if self.position == 0:
                self.position = 1
                self.trade_log.append((date, action, effective_price, self.equity))
        elif action == "SELL":
            if self.position == 1:
                self.position = 0
                profit = 1000 * (price - effective_price)  # Assume 1 lot = 1000 units
                self.equity += profit
                self.trade_log.append((date, action, effective_price, self.equity))

        self.check_margin_call(date)

    def check_margin_call(self, date):
        if self.equity < self.maintenance_margin * 1000000:
            print(f"⚠️ Margin Call on {date}! Auto-liquidating position.")
            self.position = 0
            self.equity = self.maintenance_margin * 1000000
            self.trade_log.append((date, "LIQUIDATION", 0, self.equity))

    def save_execution_log(self):
        import pandas as pd
        df = pd.DataFrame(self.trade_log, columns=['date', 'action', 'price', 'equity'])
        df.to_csv("logs/margin_events.csv", index=False)
