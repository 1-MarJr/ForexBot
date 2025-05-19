import os
import glob
import pandas as pd
from feature_engineering import load_and_engineer_features

def merge_timeframes_for_symbol(symbol, timeframes):
    """
    Load and merge engineered features for all specified timeframes of a symbol.
    Returns a merged Dataframe aligned on timestamps.
    """
    dfs = []

    for tf in timeframes:
        file_path = f"data/{symbol}_{tf}.csv"
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        df = load_and_engineer_features(file_path)
        df = df.set_index("<DATE>")

        # Rename columns to reflect the timeframe (e.g., rsi_1h, bb_width_15m)
        df = df.add_suffix(f"_{tf}")

        # Keep the timestamp for merging
        dfs.append(df)

    # Merge on time index using inner join (only keep overlapping timestamps)
    if not dfs:
        return pd.DataFrame()
    
    merged_df = dfs[0]
    for df in dfs[1:]:
        merged_df = merged_df.join(df, how='inner')

    # Reset index to bring 'time' back as a column
    merged_df.reset_index(inplace=True)
    return merged_df


def merge_all_symbols(symbols, timeframes):
    """
    Process all symbols and save merged multi-timeframe data to merged_data/
    """
    os.makedirs("merged_data", exist_ok=True)
    for symbol in symbols:
        merged = merge_timeframes_for_symbol(symbol, timeframes)
        if not merged.empty:
            merged.to_csv(f"merged_data/{symbol}_merged.csv", index=False)
            print(f"✅ Merged data saved: {symbol}_merged.csv")
        else:
            print(f"⚠️ No data merged for {symbol}")


if __name__ == "__main__":
    # Customize the symbols and timeframes used
    symbols = ["GBPUSD", "EURUSD", "USDJPY"]
    timeframes = ["15m", "30m", "1h", "4h", "1d"]

    # Merge and save the data
    merge_all_symbols(symbols, timeframes)