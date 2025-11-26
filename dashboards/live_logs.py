# live_logs.py
import psutil
import pandas as pd
import random

def fetch_live_logs(n_samples=50):
    logs = []
    processes = list(psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']))
    
    for i in range(n_samples):
        proc = random.choice(processes)
        cpu = proc.info['cpu_percent'] if proc.info['cpu_percent'] is not None else random.uniform(0, 50)
        mem = proc.info['memory_info'].rss / (1024*1024) if proc.info['memory_info'] else random.uniform(50, 500)
        logs.append({
            "file_access_count": random.randint(1, 50),
            "cpu_usage": cpu,
            "memory_usage": mem,
            "network_packets": random.randint(0, 1000),
            "network_ports": random.randint(0, 5),
            "privilege_escalation_attempt": random.randint(0, 2),
            "file_entropy": random.uniform(0, 8)
        })
    return pd.DataFrame(logs)
