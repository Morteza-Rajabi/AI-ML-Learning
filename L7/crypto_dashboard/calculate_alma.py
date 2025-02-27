import pandas as pd
import numpy as np

# Load cleaned Bitcoin data
df = pd.read_csv("data/bitcoin_prices_cleaned.csv")

# Function to calculate ALMA
def calculate_alma(df, window_size=5, sigma=6, c=0.85):
    alma = []
    
    # Iterate through the dataframe to calculate ALMA
    for i in range(len(df)):
        if i + 1 < window_size:  # Skip until we have enough data for the window
            alma.append(np.nan)  # Append NaN for initial rows where ALMA can't be calculated
        else:
            # Calculate the weights (Gaussian distribution centered at 'c')
            weights = np.exp(-((np.arange(window_size) - c * window_size) ** 2) / (2 * sigma ** 2))
            weights /= weights.sum()  # Normalize weights
            
            # Calculate ALMA value by applying weights to the last 'window_size' prices
            alma_value = np.dot(weights, df["price"].iloc[i + 1 - window_size:i + 1])  # Adjusted for correct range
            alma.append(alma_value)
    
    return alma

# Apply the function to calculate ALMA with window_size=5
df["ALMA"] = calculate_alma(df, window_size=5)

# Calculate the slope (rate of change) of ALMA by subtracting consecutive ALMA values
df["ALMA_slope"] = df["ALMA"].diff()

# Print out the last few rows of ALMA and its slope to verify
print(df[["price", "ALMA", "ALMA_slope"]].tail(10))  # Print last 10 rows to confirm ALMA slope

# Save the updated dataframe with ALMA and its slope to a new CSV
df.to_csv("data/bitcoin_prices_with_alma_and_slope.csv", index=False)

print("ALMA and its slope calculated and added to dataframe. Saved to 'bitcoin_prices_with_alma_and_slope.csv'.")
