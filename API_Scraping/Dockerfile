# API_scraping/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Buat volume untuk data scraping
RUN mkdir -p /app/data
VOLUME /app/data

EXPOSE 5000

CMD ["python", "app.py"]