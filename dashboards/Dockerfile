# Dockerfile for Live Cyber Threat Monitor
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psutil
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dashboard script
COPY live_threat_monitor.py .

# Install Python dependencies
RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    numpy \
    scikit-learn \
    joblib \
    psutil \
    plotly

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "live_threat_monitor.py", "--server.port=8501", "--server.address=0.0.0.0"]