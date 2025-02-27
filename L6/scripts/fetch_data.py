import requests
import pandas as pd

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {"vs_currency": "usd", "days": "30", "interval": "daily"}
    
    response = requests.get(url, params=params)
    data = response.json()
    
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    
    df.to_csv("data/bitcoin_prices.csv", index=False)
    print("Data saved to data/bitcoin_prices.csv")

if __name__ == "__main__":
    fetch_crypto_data()
