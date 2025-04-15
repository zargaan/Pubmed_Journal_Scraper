FROM python:3.9-slim
WORKDIR /app
COPY API_Scraping/ .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY journal_scraper ./journal_scraper
RUN mkdir -p /app/data
RUN ls -la /app
CMD ["python", "app.py"]