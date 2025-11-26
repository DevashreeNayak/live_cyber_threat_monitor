import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

import src.generate_logs_real as gen_logs

gen_logs.collect_logs()  #w generated_behavior.csv


DATA_PATH = "/data"
MODELS_PATH = "/models"
os.makedirs(MODELS_PATH, exist_ok=True)

# Loading generated data
df = pd.read_csv(os.path.join(DATA_PATH, "generated_behavior.csv"))

#  Train model
X = df.drop("label", axis=1)
y = df["label"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=42)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall:", recall_score(y_test, y_pred))
print("F1 Score:", f1_score(y_test, y_pred))

#  Save model and scaler
joblib.dump(model, os.path.join(MODELS_PATH, "cyber_model.pkl"))
joblib.dump(scaler, os.path.join(MODELS_PATH, "scaler.pkl"))
print(f"✅ Model and scaler saved in {MODELS_PATH}")

#  Predict on full dataset
df["prediction"] = model.predict(X_scaled)
df.to_csv(os.path.join(DATA_PATH, "predicted_logs.csv"), index=False)
print(f"✅ predicted_logs.csv saved in {DATA_PATH}")
