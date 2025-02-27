import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def preprocess_crypto_data():
    df = pd.read_csv("data/bitcoin_prices.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Check for missing values
    df.dropna(inplace=True)

    # Normalize prices
    scaler = MinMaxScaler()
    df["normalized_price"] = scaler.fit_transform(df[["price"]])

    df.to_csv("data/bitcoin_prices_cleaned.csv", index=False)
    print("Cleaned data saved to data/bitcoin_prices_cleaned.csv")

if __name__ == "__main__":
    preprocess_crypto_data()
