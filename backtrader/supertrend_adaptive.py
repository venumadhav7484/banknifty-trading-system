from backtrader.base_strategy import BaseStrategy
from backtrader.utils_indicators import supertrend, calculate_ema, dynamic_supertrend_multiplier
from backtrader.margin_leverage_manager import ExecutionEngine

class SupertrendAdaptiveStrategy(BaseStrategy):
    def __init__(self, config_path, df, vix_df):
        super().__init__(config_path)
        self.df = df.copy()
        self.vix_df = vix_df
        self.executor = ExecutionEngine(
            initial_capital=self.config.get('initial_capital', 100000),
            max_leverage=self.config.get('max_leverage', 3)
        )

    def apply_strategy(self):
        mode = self.config['mode']
        atr_period = self.config['atr_period']
        base_multiplier = self.config['multiplier']

        for idx, row in self.vix_df.iterrows():
            date = row['date']
            vix_today = row['vix']
            multiplier = dynamic_supertrend_multiplier(vix_today, base=base_multiplier)
            
            daily_data = self.df[self.df['date'] == date].copy()
            if daily_data.empty:
                continue

            daily_data = supertrend(daily_data, atr_period=atr_period, multiplier=multiplier)

            if mode == "Low-Risk":
                daily_data = calculate_ema(daily_data, period=200)
                if daily_data['close'].iloc[0] < daily_data['EMA_200'].iloc[0]:
                    continue  # Skip trade if below EMA in Low-Risk mode

            signal = daily_data['Supertrend'].iloc[0]
            action = "BUY" if signal else "SELL"
            price = daily_data['close'].iloc[0]
            volume = daily_data['volume'].iloc[0]

            # Log trade signal
            self.log_trade(date, action, price)

            # Execute trade through risk-managed engine
            self.executor.execute_trade(date, action, price, volume)

        # Save logs
        self.save_logs("logs/trade_logs.csv")
        self.executor.save_execution_log()
