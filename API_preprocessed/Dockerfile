FROM python:3.9-slim
WORKDIR /app

COPY API_preprocessed/ ./
COPY Hasil_embed.txt ./Hasil_embed.txt
RUN pip install --no-cache-dir --timeout=1000 -r requirements.txt
RUN pip install flask-cors
RUN mkdir -p /app/models
CMD ["python", "app.py"]