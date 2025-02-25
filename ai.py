import requests

# CoinGecko API endpoint for Bitcoin price
url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"

response = requests.get(url)
data = response.json()

print("Bitcoin Price (USD):", data["bitcoin"]["usd"])