import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error

# Load data
df = pd.read_csv("data/bitcoin_prices_cleaned.csv")

# Prepare Features (X) and Target (y)
df["next_price"] = df["price"].shift(-1)  # Next day's price as target
df.dropna(inplace=True)  # Remove last row (no next day price)

X = df[["price"]].values  # Features (Current Price)
y = df["next_price"].values  # Target (Next Day Price)

# Split Data (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict and Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)

print(f"Model trained! Mean Absolute Error: {mae:.2f}")

# Save Model
import joblib
joblib.dump(model, "models/linear_regression_model.pkl")
print("Model saved!")
