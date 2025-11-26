# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy main pipeline
COPY docker/full_pipeline.py .

# Copy src folder
COPY src/ ./src/

# Copy dashboards (optional)
COPY dashboards/ ./dashboards/

# Install dependencies
RUN pip install --no-cache-dir pandas numpy scikit-learn joblib psutil streamlit

# Default command
CMD ["python", "full_pipeline.py"]
