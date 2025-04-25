import yaml

class BaseStrategy:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)
        self.logs = []

    def load_config(self, path):
        with open(path, 'r') as file:
            return yaml.safe_load(file)

    def log_trade(self, date, action, price):
        self.logs.append({'date': date, 'action': action, 'price': price})

    def save_logs(self, filepath):
        import pandas as pd
        pd.DataFrame(self.logs).to_csv(filepath, index=False)
