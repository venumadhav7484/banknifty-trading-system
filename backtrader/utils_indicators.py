import pandas as pd
import numpy as np

def calculate_atr(df, period=10):
    df.loc[:, 'H-L'] = df['high'] - df['low']
    df.loc[:, 'H-PC'] = abs(df['high'] - df['close'].shift(1))
    df.loc[:, 'L-PC'] = abs(df['low'] - df['close'].shift(1))
    df.loc[:, 'TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1)
    df.loc[:, 'ATR'] = df['TR'].rolling(window=period).mean()
    return df

def supertrend(df, atr_period=10, multiplier=3):
    assert atr_period >= 5, "ATR period must be ≥5 for stability"
    
    df = calculate_atr(df, period=atr_period)
    hl2 = (df['high'] + df['low']) / 2
    df.loc[:, 'UpperBand'] = hl2 + (multiplier * df['ATR'])
    df.loc[:, 'LowerBand'] = hl2 - (multiplier * df['ATR'])
    df.loc[:, 'Supertrend'] = True

    # Simple trend flip logic
    for i in range(1, len(df)):
        if df['close'][i] > df['UpperBand'][i-1]:
            df['Supertrend'][i] = True
        elif df['close'][i] < df['LowerBand'][i-1]:
            df['Supertrend'][i] = False
        else:
            df['Supertrend'][i] = df['Supertrend'][i-1]
    
    return df

def calculate_ema(df, period=200):
    df.loc[:, f'EMA_{period}'] = df['close'].ewm(span=period, adjust=False).mean()
    return df

def calculate_volume_ma(df, period=20):
    df.loc[:, f'Vol_MA_{period}'] = df['volume'].rolling(window=period).mean()
    return df

def dynamic_supertrend_multiplier(vix, base=3.0):
    return base * (vix / 15)
