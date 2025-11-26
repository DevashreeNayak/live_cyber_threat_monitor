import pandas as pd
import numpy as np
import os

# Create data directory
os.makedirs("../data", exist_ok=True)

n_samples = 500

# ---------- REALISTIC NORMAL PROCESSES ----------
# More overlap with suspicious to avoid overfitting
normal = pd.DataFrame({
    "file_access_count": np.random.randint(1, 30, n_samples),  # Increased upper bound
    "cpu_usage": np.random.uniform(5, 60, n_samples),  # More overlap
    "memory_usage": np.random.uniform(100, 800, n_samples),  # More overlap
    "network_packets": np.random.randint(10, 300, n_samples),  # More overlap
    "network_ports": np.random.randint(0, 3, n_samples),  # Some normal can have ports
    "privilege_escalation_attempt": np.random.choice([0, 1], n_samples, p=[0.95, 0.05]),  # 5% false positives
    "file_entropy": np.random.uniform(0, 5, n_samples),  # More overlap
    "label": 0
})

# ---------- REALISTIC SUSPICIOUS PROCESSES ----------
# More overlap with normal to make it harder
suspicious = pd.DataFrame({
    "file_access_count": np.random.randint(15, 100, n_samples),  # Some overlap
    "cpu_usage": np.random.uniform(40, 95, n_samples),  # Overlap zone
    "memory_usage": np.random.uniform(400, 2000, n_samples),  # Overlap zone
    "network_packets": np.random.randint(150, 1000, n_samples),  # Overlap zone
    "network_ports": np.random.randint(1, 5, n_samples),
    "privilege_escalation_attempt": np.random.choice([0, 1, 2], n_samples, p=[0.1, 0.5, 0.4]),  # Some don't escalate
    "file_entropy": np.random.uniform(2, 8, n_samples),  # Overlap zone
    "label": 1
})

# ---------- ADD NOISE TO PREVENT OVERFITTING ----------
# Add some borderline cases
borderline_normal = pd.DataFrame({
    "file_access_count": np.random.randint(25, 40, 100),
    "cpu_usage": np.random.uniform(50, 70, 100),
    "memory_usage": np.random.uniform(600, 900, 100),
    "network_packets": np.random.randint(200, 400, 100),
    "network_ports": np.random.randint(1, 3, 100),
    "privilege_escalation_attempt": np.random.choice([0, 1], 100, p=[0.7, 0.3]),
    "file_entropy": np.random.uniform(3, 5, 100),
    "label": 0  # Actually normal but looks suspicious
})

borderline_suspicious = pd.DataFrame({
    "file_access_count": np.random.randint(10, 25, 100),
    "cpu_usage": np.random.uniform(35, 55, 100),
    "memory_usage": np.random.uniform(300, 700, 100),
    "network_packets": np.random.randint(100, 250, 100),
    "network_ports": np.random.randint(0, 2, 100),
    "privilege_escalation_attempt": np.random.choice([0, 1], 100, p=[0.5, 0.5]),
    "file_entropy": np.random.uniform(2, 4, 100),
    "label": 1  # Actually suspicious but looks normal
})

# Combine all data
df = pd.concat([normal, suspicious, borderline_normal, borderline_suspicious], 
               ignore_index=True)

# Shuffle thoroughly
df = df.sample(frac=1, random_state=None).reset_index(drop=True)  # No random_state = different each time

# Save
output_path = "../data/generated_behavior.csv"
df.to_csv(output_path, index=False)

print(f"✅ Realistic logs generated: {output_path}")
print(f"   Total samples: {len(df)}")
print(f"   Normal: {len(df[df['label']==0])}")
print(f"   Suspicious: {len(df[df['label']==1])}")
print(f"   → Model should now achieve 85-95% accuracy (realistic!)")