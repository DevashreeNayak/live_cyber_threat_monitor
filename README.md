# 🛡️ Live Cyber Threat Monitor
Live Cyber Threat Monitor: Real-time system process monitoring and threat detection using Python, Streamlit, and a trained Random Forest ML model. Includes visualizations, risk scoring, and downloadable snapshots of monitored processes



## 📌 Overview

This project monitors the running processes on a system and uses a trained Random Forest model to classify them as **Normal** or **Suspicious**. It refreshes automatically, shows detailed metrics, interactive charts, and allows exporting the current snapshot as CSV.

---


## ⚙️ Installation & Usage

### **1. Clone the repository**


git clone <repo_url>
cd live_cyber_monitor

2. Install the required packages
pip install -r requirements.txt

3. Run the Live Threat Monitoring App
python -m streamlit run live_threat_monitor.py


The dashboard will open automatically in your browser and begin monitoring processes.


# 🎛️ App Controls


Refresh Rate Slider: Choose 1–10 seconds refresh interval

Auto Refresh: Enable/disable automatic process scanning

Manual Refresh: Collects data instantly

Download CSV: Export the current scan results



# 🔍 Features

Real-time process monitoring

Streamlit-based live dashboard

Random Forest ML model for threat prediction

Calculates a custom Threat Score

Color-coded table:

🟢 Normal processes

🔴 Suspicious processes

Visualizations:

Pie chart of threat distribution

Bar chart of top CPU consumers

3D Scatter: CPU vs Memory vs Network

CSV export for reporting



# 🧠 How It Works

Collects system processes using psutil

Extracts features like CPU usage, memory usage, network packets, threads, etc.

Scales features using a pre-trained scaler

Runs the Random Forest model to classify each process

Calculates a threat score to help visualize severity

Displays results in a clean and interactive dashboard





-- > Docker was only used for training the ML model, not for running the dashboard.
During model training, Docker ensured:

A controlled environment

Consistent dependencies

No conflicts with system libraries

The live Streamlit dashboard does NOT require Docker and runs directly with Python.



# 🛠️ Technologies Used

Python 3

Streamlit

Psutil

Plotly

Pandas & NumPy

Scikit-learn (Random Forest)

Joblib


# 👩‍💻 Author

Devashree Nayak

Cyber Threat Intelligence & ML Dashboard Project


