import streamlit as st
import pandas as pd
import numpy as np
import psutil
import joblib
import os
import plotly.express as px
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ---------- AUTO REFRESH ----------
st_autorefresh(interval=5000, key="live_monitor")  # refresh every 5s
# ---------- CONFIG ----------
st.set_page_config(
    page_title="Live Cyber Threat Monitor🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- LOAD MODEL ----------
MODEL_PATH = "../models/cyber_model.pkl"
SCALER_PATH = "../models/scaler.pkl"

@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH) and os.path.exists(SCALER_PATH):
        model = joblib.load(MODEL_PATH)
        scaler = joblib.load(SCALER_PATH)
        return model, scaler
    else:
        st.error("❌ Model not found! Train the model first by running train_model.py")
        st.stop()

model, scaler = load_model()

# ---------- COLLECT LIVE DATA ----------
def collect_live_data():
    logs = []
    current_pid = os.getpid()  # Skip Streamlit

    # Initialize CPU percent
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            proc.cpu_percent(interval=None)
        except:
            continue
    time.sleep(0.1)

    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'num_threads']):
        if proc.info['pid'] == current_pid:
            continue
        try:
            cpu = proc.cpu_percent(interval=None)
            mem = proc.info['memory_info'].rss / (1024*1024) if proc.info['memory_info'] else 0
            threads = proc.info['num_threads'] or 1

            logs.append({
                "process_name": proc.info['name'] or "Unknown",
                "pid": proc.info['pid'],
                "file_access_count": threads * 2,  # simulated
                "cpu_usage": cpu,
                "memory_usage": mem,
                "network_packets": int(np.random.randint(0, 100) * (cpu/10)),  # simulated
                "network_ports": 1 if cpu > 20 else 0,
                "privilege_escalation_attempt": 1 if mem > 500 else 0,
                "file_entropy": np.random.uniform(0, 8),
                "timestamp": datetime.now().strftime("%H:%M:%S")
            })

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return pd.DataFrame(logs)

# ---------- PREDICT THREATS ----------
def predict_threats(df):
    if df.empty:
        return df

    feature_cols = ["file_access_count", "cpu_usage", "memory_usage",
                    "network_packets", "network_ports",
                    "privilege_escalation_attempt", "file_entropy"]
    X = df[feature_cols]
    X_scaled = scaler.transform(X)
    df["prediction"] = model.predict(X_scaled)
    df["threat_probability"] = model.predict_proba(X_scaled)[:, 1]

    df["threat_score"] = (
        df["cpu_usage"]/100 +
        (df["memory_usage"]/df["memory_usage"].max() if df["memory_usage"].max() > 0 else 0) +
        (df["network_packets"]/df["network_packets"].max() if df["network_packets"].max() > 0 else 0) +
        df["privilege_escalation_attempt"]
    )

    return df

# ---------- STYLE TABLE ----------
def style_table(df):
    def color_row(row):
        return ['background-color: #F44336; color: white' if row['prediction']==1 else 'background-color: #4CAF50; color: white' for _ in row]
    return df.style.apply(color_row, axis=1)

# ---------- MAIN APP ----------
st.title("🛡️ Live Cyber Threat Monitor")
st.markdown("**Real-time monitoring of your laptop's processes**")

# Sidebar
st.sidebar.header("⚙️ Controls")
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 10, 3)
auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)

# Collect data
with st.spinner("Collecting live data from your system..."):
    live_df = collect_live_data()
    if not live_df.empty:
        live_df = predict_threats(live_df)

        # ---------- METRICS ----------
        st.subheader("📊 Current System Status")
        normal = len(live_df[live_df["prediction"] == 0])
        suspicious = len(live_df[live_df["prediction"] == 1])

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🟢 Normal Processes", normal)
        col2.metric("🔴 Suspicious Processes", suspicious)
        col3.metric("📈 Total Monitored", len(live_df))
        col4.metric("⏰ Last Update", live_df['timestamp'].iloc[0])

        if suspicious > 0:
            st.error(f"⚠️ **ALERT**: {suspicious} suspicious processes detected!")

        # ---------- VISUALIZATIONS ----------
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🎯 Threat Distribution")
            fig_pie = px.pie(
                values=[normal, suspicious],
                names=["Normal", "Suspicious"],
                color_discrete_sequence=["#4CAF50", "#F44336"],
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        st.subheader("📋 All Monitored Processes")
        st.dataframe(style_table(live_df.sort_values("threat_score", ascending=False)))

        # 3D Scatter
        st.subheader("🌐 CPU vs Memory vs Network (3D)")
        fig_3d = px.scatter_3d(
            live_df,
            x="cpu_usage",
            y="memory_usage",
            z="network_packets",
            color="prediction",
            size="threat_score",
            hover_data=["process_name"],
            color_discrete_map={0: "#4CAF50", 1: "#F44336"},
            labels={"prediction": "Threat Status"}
        )
        st.plotly_chart(fig_3d, use_container_width=True)

        # ---------- DOWNLOAD ----------
        st.subheader("💾 Export Data")
        csv = live_df.to_csv(index=False)
        st.download_button(
            label="Download Current Snapshot as CSV",
            data=csv,
            file_name=f"threat_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )

        with col2:
            st.subheader("📊 Top CPU Consumers")
            top_cpu = live_df.nlargest(10, "cpu_usage")
            fig_bar = px.bar(
                top_cpu,
                x="process_name",
                y="cpu_usage",
                color="prediction",
                color_discrete_map={0: "#4CAF50", 1: "#F44336"}
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        
        # ---------- COLOR-CODED STREAMLIT TABLE ----------
      

    else:
        st.error("❌ No data collected. Check permissions.")

st.markdown("---")
st.caption("🛡️ Live Cyber Threat Monitor | Powered by Random Forest ML")
