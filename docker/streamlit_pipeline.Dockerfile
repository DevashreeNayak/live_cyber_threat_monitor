FROM python:3.10-slim

WORKDIR /app

COPY ../dashboards/dashboard.py .

RUN pip install streamlit pandas

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
