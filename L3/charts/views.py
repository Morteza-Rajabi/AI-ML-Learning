
from django.shortcuts import render
import requests
import pandas as pd
from django.http import JsonResponse


def fetch_hourly_ohlcv():
    """Fetch the last 7 days of OHLCV data (without specifying interval)."""
    url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    params = {
        "vs_currency": "usd",
        "days": "7"  # Fetch last 7 days (CoinGecko auto-returns hourly data)
    }

    response = requests.get(url, params=params)
    data = response.json()

    print("DEBUG: API Response =", data)  # Check raw API response

    if "prices" in data and "total_volumes" in data:
        df_price = pd.DataFrame(data["prices"], columns=["timestamp", "close"])
        df_volume = pd.DataFrame(data["total_volumes"], columns=["timestamp", "volume"])

        df = pd.merge(df_price, df_volume, on="timestamp")
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        df.columns = ["timestamp", "close", "volume"]

        result = df.to_dict(orient="records")
        print("DEBUG: Processed Data =", result)  # Debug processed data
        return result

    print("ERROR: No 'prices' key found in API response")
    return []  # Return empty list if data is missing

def get_chart_data(request):
    """Returns JSON response of hourly OHLCV data."""
    data = fetch_hourly_ohlcv()
    return JsonResponse({"ohlcv": data})

def crypto_chart(request):
    """Renders the chart page."""
    return render(request, "chart.html")

