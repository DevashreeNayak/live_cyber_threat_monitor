import pandas as pd
import joblib

# Paths
DATA_PATH = "../data/generated_behavior.csv"
MODEL_PATH = "../models/cyber_model.pkl"
SCALER_PATH = "../models/scaler.pkl"

#  Load dataset
df = pd.read_csv(DATA_PATH)
X = df.drop("label", axis=1)

#  Load model and scaler
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

#  Scale features
X_scaled = scaler.transform(X)

#  Predict
df["prediction"] = model.predict(X_scaled)

#  Save predictions
df.to_csv("../data/predicted_logs.csv", index=False)

# Summary
sus_count = df["prediction"].sum()
print(f"Total suspicious processes detected: {sus_count} / {len(df)}")
print("✅ Predictions saved to predicted_logs.csv")
