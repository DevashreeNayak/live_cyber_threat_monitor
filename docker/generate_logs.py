import pandas as pd
import numpy as np
import os

os.makedirs("/data", exist_ok=True)

n_samples = 500

normal = pd.DataFrame({
    "file_access_count": np.random.randint(1, 10, n_samples),
    "cpu_usage": np.random.uniform(5, 30, n_samples),
    "memory_usage": np.random.uniform(100, 500, n_samples),
    "network_packets": np.random.randint(10, 100, n_samples),
    "network_ports": np.random.randint(0, 2, n_samples),
    "privilege_escalation_attempt": 0,
    "file_entropy": np.random.uniform(0, 3, n_samples),
    "label": 0
})

suspicious = pd.DataFrame({
    "file_access_count": np.random.randint(20, 100, n_samples),
    "cpu_usage": np.random.uniform(50, 95, n_samples),
    "memory_usage": np.random.uniform(500, 2000, n_samples),
    "network_packets": np.random.randint(200, 1000, n_samples),
    "network_ports": np.random.randint(1, 5, n_samples),
    "privilege_escalation_attempt": np.random.randint(0, 2, n_samples),
    "file_entropy": np.random.uniform(3, 8, n_samples),
    "label": 1
})

df = pd.concat([normal, suspicious], ignore_index=True).sample(frac=1).reset_index(drop=True)
df.to_csv("/data/generated_behavior.csv", index=False)
print("Logs generated successfully in /data/generated_behavior.csv")
