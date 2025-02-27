import numpy as np
import pandas as pd
import requests

def alma(series, window=9, sigma=6, offset=0.85):
    """Calculate Arnaud Legoux Moving Average (ALMA) and ensure correct output length."""
    series = series.dropna().values  # Remove NaN values before applying ALMA
    n = len(series)

    if n < window:
        return pd.Series(np.full(n, np.nan))  # Return full NaNs if too short

    m = offset * (window - 1)
    s = window / sigma
    weight = np.exp(-0.5 * ((np.arange(window) - m) / s) ** 2)
    weight /= weight.sum()  # Normalize weights

    alma_values = np.convolve(series, weight, mode="valid")  # Apply ALMA filter
    
    # ✅ **Ensure ALMA matches DataFrame length**
    alma_full = np.full(n, np.nan)  # Create full NaN array
    alma_full[window-1:] = alma_values  # Insert computed values at correct position

    return pd.Series(alma_full)  # Return series with correct index length

def fetch_moving_average_data():
    """Fetch hourly OHLCV data and calculate moving averages."""
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "7"}  # No interval to avoid Enterprise restriction

    response = requests.get(url, params=params)
    data = response.json()

    if "prices" in data:
        df = pd.DataFrame(data["prices"], columns=["timestamp", "close"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        # ✅ Fix SMA window sizes
        df["SMA_10"] = df["close"].rolling(window=10, min_periods=1).mean()
        df["SMA_30"] = df["close"].rolling(window=30, min_periods=1).mean()

        # ✅ Calculate ALMA with correct length
        df["ALMA_9"] = alma(df["close"], window=9, sigma=6, offset=0.85)

        # ✅ Fix NaN issue by replacing NaN with None for JSON serialization
        df.fillna(method="bfill", inplace=True)  # Backward fill for missing values
        df.fillna(method="ffill", inplace=True)  # Forward fill for missing values

        df["SMA_10"] = df["SMA_10"].apply(lambda x: None if pd.isna(x) else x)
        df["SMA_30"] = df["SMA_30"].apply(lambda x: None if pd.isna(x) else x)
        df["ALMA_9"] = df["ALMA_9"].apply(lambda x: None if pd.isna(x) else x)

        result = df.to_dict(orient="records")
        return result

    return []
