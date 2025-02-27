import requests
import pandas as pd

# CoinGecko API for historical Bitcoin data
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "1"  # Only 1-day data provides minute-level resolution
}

# Fetch data
response = requests.get(url, params=params)
data = response.json()

# Check if "prices" key exists
if "prices" in data:
    prices = data["prices"]  # List of [timestamp, price]
    
    # Convert to DataFrame
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # Convert timestamp
    
    # Filter to keep only every 5th row (5-minute intervals)
    df_5min = df.iloc[::5, :]

    print(df_5min)  # Print 5-minute interval data
else:
    print("Error: 'prices' key not found in API response.")
