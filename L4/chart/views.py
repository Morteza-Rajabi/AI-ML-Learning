import numpy as np
import pandas as pd
import requests
from django.http import JsonResponse
from django.shortcuts import render

import numpy as np
import pandas as pd

def alma(series, window=9, sigma=6, offset=0.85):
    """
    Calculate the Arnaud Legoux Moving Average (ALMA).

    Parameters:
        series (pd.Series): The price data.
        window (int): The lookback period for ALMA.
        sigma (int): Controls the smoothness of the curve.
        offset (float): Determines the central weight position.

    Returns:
        pd.Series: ALMA values aligned with the original series.
    """
    series = series.dropna().values  # Remove NaN values before applying ALMA
    n = len(series)

    if n < window:
        return pd.Series(np.full(n, np.nan))  # Return full NaNs if too short

    m = offset * (window - 1)  # Calculate the offset (center of the window)
    s = window / sigma  # Standard deviation for the Gaussian weight function

    # ✅ Create Gaussian Weights
    weight = np.exp(-0.5 * ((np.arange(window) - m) / s) ** 2)
    weight /= weight.sum()  # Normalize weights so they sum to 1

    # ✅ Apply Convolution (Weighted Sum)
    alma_values = np.convolve(series, weight, mode="valid")  

    # ✅ Ensure ALMA Matches DataFrame Length
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

        # ✅ Calculate SMA and ALMA with correct length
        df["SMA_10"] = df["close"].rolling(window=10, min_periods=10).mean()
        df["SMA_30"] = df["close"].rolling(window=30, min_periods=30).mean()
        df["ALMA_9"] = alma(df["close"], window=9, sigma=6, offset=0.85)

        # ✅ Remove rows where SMA-30 is NaN (Start chart from here)
        df.dropna(subset=["SMA_30"], inplace=True)

        # ✅ Convert NaN values to None for JSON serialization
        df["SMA_10"] = df["SMA_10"].apply(lambda x: None if pd.isna(x) else x)
        df["SMA_30"] = df["SMA_30"].apply(lambda x: None if pd.isna(x) else x)
        df["ALMA_9"] = df["ALMA_9"].apply(lambda x: None if pd.isna(x) else x)

        result = df.to_dict(orient="records")
        return result

    return []

def get_moving_average_chart_data(request):
    """Returns JSON response with moving averages."""
    try:
        data = fetch_moving_average_data()
        return JsonResponse({"ohlcv": data}, safe=False)
    except Exception as e:
        print("Error:", str(e))  # Print error in terminal
        return JsonResponse({"error": str(e)}, status=500)

def crypto_chart_sma(request):
    """Renders the chart page."""
    return render(request, "chart-sma.html")
