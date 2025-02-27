import requests
import pandas as pd

# CoinGecko API for historical Bitcoin data
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "7"  # Between 2 to 90 days gives hourly data automatically
}

# Fetch data
response = requests.get(url, params=params)
data = response.json()

# Extract prices
if "prices" in data:
    prices = data["prices"]
    df = pd.DataFrame(prices, columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # Convert timestamp
    print(df)
else:
    print("Error: 'prices' key not found in API response.")
