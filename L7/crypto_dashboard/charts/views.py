from django.shortcuts import render
import pandas as pd
import numpy as np  # Import NumPy to handle NaN values

def bitcoin_chart(request):
    # Load cleaned data
    df = pd.read_csv("data/bitcoin_prices_cleaned.csv")

    # Convert data to JSON format for Chart.js
    chart_data = {
        "labels": df["timestamp"].tolist(),  # X-axis (dates)
        "prices": df["price"].tolist(),      # Y-axis (prices)
    }

    return render(request, "charts/bitcoin_chart.html", {"chart_data": chart_data})




def alma_chart(request):
    # Load the Bitcoin price data with ALMA values
    df = pd.read_csv("data/bitcoin_prices_with_alma_and_slope.csv")  # Ensure correct path

    # Ensure 'price' and 'ALMA' columns exist
    if "price" not in df.columns or "ALMA" not in df.columns:
        return render(request, 'charts/alma_chart.html', {'prices': [], 'alma_values': []})

    # Drop NaN values
    df = df.dropna(subset=["ALMA"])  # Remove rows where ALMA is NaN

    # Extract the last 100 data points
    prices = df["price"].tail(100).tolist()  
    alma_values = df["ALMA"].tail(100).tolist()  

    # Debugging - Print to console
    print("Filtered Prices:", prices)
    print("Filtered ALMA Values:", alma_values)

    # Pass data to template
    return render(request, 'charts/alma_chart.html', {'prices': prices, 'alma_values': alma_values})
