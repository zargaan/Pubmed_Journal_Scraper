# API_preprocessed/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Mount volume yang sama dengan API scraping
VOLUME /app/data

EXPOSE 5001

CMD ["python", "app.py"]