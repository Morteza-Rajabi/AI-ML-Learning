import requests
import pandas as pd

# CoinGecko API for historical Bitcoin data (last 7 days)
url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
params = {
    "vs_currency": "usd",
    "days": "7",
    "interval": "daily" # "hourly": Change to "hourly" and "minutely" Fetch minute data
}

# Fetch data
response = requests.get(url, params=params)
data = response.json()

# Convert prices to Pandas DataFrame
prices = data["prices"]  # List of [timestamp, price]

# Create DataFrame
df = pd.DataFrame(prices, columns=["timestamp", "price"])

# Convert timestamp to readable date
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

# Display the DataFrame
print(df)
