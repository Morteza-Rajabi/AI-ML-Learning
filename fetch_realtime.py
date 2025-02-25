import requests
import pandas as pd
import time

# Function to fetch current price and volume
def get_price_volume():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin",
        "vs_currencies": "usd",
        "include_market_cap": "false",
        "include_24hr_vol": "true",  # Get volume data
        "include_24hr_change": "false"
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Extract price and volume
    price = data["bitcoin"]["usd"]
    volume = data["bitcoin"]["usd_24h_vol"]
    timestamp = pd.Timestamp.now()

    return timestamp, price, volume

# Initialize OHLCV data storage
ohlcv_data = []

# Run for 5 minutes (as an example)
for i in range(5):
    timestamp, price, volume = get_price_volume()
    print(f"{timestamp} - Price: {price} - Volume: {volume}")

    # Store data
    ohlcv_data.append([timestamp, price, volume])

    time.sleep(60)  # Wait 1 minute before fetching again

# Convert to DataFrame
df = pd.DataFrame(ohlcv_data, columns=["timestamp", "close", "volume"])

# Calculate OHLCV values
df["open"] = df["close"].shift(1)  # Previous close as open
df["high"] = df["close"].rolling(2).max()  # Highest price in last 2 minutes
df["low"] = df["close"].rolling(2).min()   # Lowest price in last 2 minutes

# Print the final OHLCV DataFrame
print(df)
