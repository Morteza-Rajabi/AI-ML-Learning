from scripts.fetch_data import fetch_crypto_data
from scripts.preprocess_data import preprocess_crypto_data

if __name__ == "__main__":
    fetch_crypto_data()
    preprocess_crypto_data()
    print("Data collection and preprocessing completed.")
