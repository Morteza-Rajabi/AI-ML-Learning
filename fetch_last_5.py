import requests
import pandas as pd

# CoinGecko API for historical minute-level data
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "1"  # Only 1-day data provides minute-level resolution
}

# Fetch data
response = requests.get(url, params=params)
data = response.json()

# Check if "prices" and "total_volumes" exist
if "prices" in data and "total_volumes" in data:
    prices = data["prices"]  # List of [timestamp, price]
    volumes = data["total_volumes"]  # List of [timestamp, volume]

    # Convert to DataFrame
    df_price = pd.DataFrame(prices, columns=["timestamp", "price"])
    df_volume = pd.DataFrame(volumes, columns=["timestamp", "volume"])

    # Merge price & volume data
    df = pd.merge(df_price, df_volume, on="timestamp")

    # Convert timestamp to datetime
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    # Resample into 5-minute intervals
    df.set_index("timestamp", inplace=True)
    df_5min = df.resample("5T").agg({
        "price": ["first", "max", "min", "last"],  # Open, High, Low, Close
        "volume": "sum"  # Total volume
    })

    # Rename columns
    df_5min.columns = ["open", "high", "low", "close", "volume"]
    df_5min.reset_index(inplace=True)

    # Get last 5-minute OHLCV data
    last_5min_ohlcv = df_5min.iloc[-1]
    print("Last 5-Min OHLCV:")
    print(last_5min_ohlcv)

else:
    print("Error: 'prices' or 'total_volumes' key not found in API response.")
