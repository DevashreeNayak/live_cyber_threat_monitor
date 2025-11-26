FROM python:3.10-slim

WORKDIR /app

# Copy log generation script
COPY generate_logs.py .

# Install dependencies
RUN pip install numpy pandas

# Mount /data when running to save logs
CMD ["python", "generate_logs.py"]
