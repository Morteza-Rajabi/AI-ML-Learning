import joblib
import numpy as np

# Load the trained model
model = joblib.load("models/linear_regression_model.pkl")

# Get user input for today's Bitcoin price
new_price = float(input("Enter today's Bitcoin price (USD): "))

# Predict the next day's price
predicted_price = model.predict(np.array([[new_price]]))[0]

print(f"Predicted Next Day Price: ${predicted_price:.2f}")
