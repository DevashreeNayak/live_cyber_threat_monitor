import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

# Paths
DATA_PATH = "../data/generated_behavior.csv"
MODEL_PATH = "../models/cyber_model.pkl"
SCALER_PATH = "../models/scaler.pkl"

#  Load dataset
df = pd.read_csv(DATA_PATH)

#  Split features and label
X = df.drop("label", axis=1)
y = df["label"]

#  Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#  Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.25, random_state=42
)

#  Train Random Forest
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

#  Evaluate
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

#  Save model and scaler
os.makedirs("../models", exist_ok=True)
joblib.dump(model, MODEL_PATH)
joblib.dump(scaler, SCALER_PATH)

print("✅ Model and scaler saved successfully!")
