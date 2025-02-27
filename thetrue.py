import requests

# 🔹 Replace with TrueTrade's actual API URL
url = "https://api.truetrade.com/v1/ticker?symbol=BTC/USDT"

try:
    response = requests.get(url)
    data = response.json()  # Convert response to JSON

    # 🔹 Print full response for debugging
    print("Raw Response:", data)

    # Extract price (modify key based on API response structure)
    price = data.get("last_price")  # Adjust based on actual API format
    print(f"Bitcoin Price on TrueTrade: {price}")

except Exception as e:
    print("Error:", str(e))
