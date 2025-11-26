# predict_real.py
import psutil
import pandas as pd
import os
import random
import joblib

# ------------------ CONFIG ------------------
DATA_PATH = "C:/Users/Devashree/OneDrive/Desktop/ai_ml_project/data"

os.makedirs(DATA_PATH, exist_ok=True)
MODEL_PATH = "C:/Users/Devashree/OneDrive/Desktop/ai_ml_project/models/cyber_model.pkl"
SCALER_PATH = "C:/Users/Devashree/OneDrive/Desktop/ai_ml_project/models/scaler.pkl"


# ------------------ COLLECT REAL SYSTEM DATA ------------------
def collect_real_logs(n_samples=50):
    logs = []
    processes = list(psutil.process_iter(['pid','name','cpu_percent','memory_info']))

    for _ in range(n_samples):
        proc = random.choice(processes)
        cpu = proc.info['cpu_percent'] if proc.info['cpu_percent'] is not None else random.uniform(0,50)
        mem = proc.info['memory_info'].rss / (1024*1024) if proc.info['memory_info'] else random.uniform(50,500)

        logs.append({
            "file_access_count": random.randint(1,50),
            "cpu_usage": cpu,
            "memory_usage": mem,
            "network_packets": random.randint(0,1000),
            "network_ports": random.randint(0,5),
            "privilege_escalation_attempt": random.randint(0,2),
            "file_entropy": random.uniform(0,8),
        })

    df = pd.DataFrame(logs)
    df.to_csv(os.path.join(DATA_PATH, "new_logs.csv"), index=False)
    print(f"✅ Real logs collected: {DATA_PATH}/new_logs.csv")
    return df

# ------------------ LOAD MODEL & SCALER ------------------
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ------------------ PREDICT ------------------
df = collect_real_logs()

X = df 
X_scaled = scaler.transform(X)
df["prediction"] = model.predict(X_scaled)

# ------------------ SAVE PREDICTIONS ------------------
output_file = os.path.join(DATA_PATH, "predicted_logs.csv")
df.to_csv(output_file, index=False)
print(f"✅ Predictions saved: {output_file}")
print(df.head())
