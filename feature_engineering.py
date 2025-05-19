import pandas as pd   
import ta
import os

def load_and_engineer_features(file_path):
    """
    Load OHLCV data from CSV and add technical indicators and features
    """
    df = pd.read_csv(file_path, sep='\t', parse_dates=['<DATE>'])

    # Drop rows with missing values (common after adding indicators)
    df = df.dropna().copy()

    # Momentum: percent change
    df['momentum_pct_change'] = df['<CLOSE>'].pct_change() * 100

    # RSI (14)
    df['sma_20'] = ta.trend.SMAIndicator(close=df['<CLOSE>'], window=20).sma_indicator()
    df['ema_20'] = ta.trend.EMAIndicator(close=df['<CLOSE>'], window=20).ema_indicator()

    # Bollinger Bands (Volatility)
    bb = ta.volatility.BollingerBands(close=df['<CLOSE>'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    df['bb_width'] = df['bb_upper'] - df['bb_lower']

    # Volume moving average
    df['volume_ma_20'] = df['<VOL>'].rolling(window=20).mean()

    # Candle body size
    df['candle_body'] = abs(df['<CLOSE>'] - df['<OPEN>'])
    df['candle_range'] = df['<HIGH>'] - df['<LOW>']

    # Drop NaN after calculations
    df = df.dropna().copy()

    return df

if __name__ == "__main__":
    test_file = os.path.join("data", "EURUSD_1d.csv")
    df_features = load_and_engineer_features(test_file)
    print(df_features.head())