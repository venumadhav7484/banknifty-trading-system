def detect_rollover(current_contract, next_contract):
    """
    Detect rollover based on volume shift.
    """
    return next_contract["volume"].iloc[-1] > current_contract["volume"].iloc[-1]

def adjust_rollover(old_contract_df, new_contract_df):
    """
    Adjust prices to ensure smooth rollover between futures contracts.
    """
    price_diff = new_contract_df.iloc[0]['open'] - old_contract_df.iloc[-1]['close']
    old_contract_df['close'] += price_diff
    return pd.concat([old_contract_df, new_contract_df], ignore_index=True)
