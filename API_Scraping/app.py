from flask import Flask, jsonify, request
import subprocess
import os
import threading
import time
from datetime import datetime
import json

# Prometheus
from prometheus_client import Counter, Summary, make_wsgi_app, Gauge
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# ===== Prometheus Metrics =====
REQUEST_COUNT = Counter('http_requests_total', 'Jumlah total HTTP request')
REQUEST_LATENCY = Summary('request_latency_seconds', 'Waktu proses setiap request')
SCRAPING_RUNNING = Gauge('scraping_is_running', 'Status scraping: 1 jika berjalan, 0 jika tidak')
SCRAPING_PROGRESS = Gauge('scraping_progress_percent', 'Progress scraping dalam persen')

# ======= Scraping Status Global =======
scraping_status = {
    'is_running': False,
    'start_time': None,
    'end_time': None,
    'progress': 0,
    'current_page': 0,
    'total_pages': 5
}

SCRAPING_RESULT_PATH = os.path.join('shared_data', 'scraping_hasil.json')

def run_scrapy_spider(total_pages):
    try:
        scraping_status.update({
            'is_running': True,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'progress': 0,
            'current_page': 0,
            'total_pages': total_pages
        })
        SCRAPING_RUNNING.set(1)

        command = f'scrapy crawl pubmed -a max_pages={total_pages} -O {SCRAPING_RESULT_PATH}'
        process = subprocess.Popen(command, shell=True, cwd=os.getcwd())

        while process.poll() is None:
            time.sleep(1)
            if scraping_status['current_page'] < scraping_status['total_pages']:
                scraping_status['current_page'] += 1
                scraping_status['progress'] = int(
                    (scraping_status['current_page'] / scraping_status['total_pages']) * 100
                )
                SCRAPING_PROGRESS.set(scraping_status['progress'])

        scraping_status.update({
            'is_running': False,
            'end_time': datetime.now().isoformat(),
            'progress': 100
        })
        SCRAPING_RUNNING.set(0)
        SCRAPING_PROGRESS.set(100)

    except Exception as e:
        scraping_status.update({
            'is_running': False,
            'error': str(e)
        })
        SCRAPING_RUNNING.set(0)

# === Flask Endpoints ===

@app.route('/api/scrape/start', methods=['POST'])
@REQUEST_LATENCY.time()
def start_scraping():
    REQUEST_COUNT.inc()

    if scraping_status['is_running']:
        return jsonify({'status': 'error', 'message': 'Scraping is already running'}), 400

    data = request.get_json()
    total_pages = data.get('total_pages', 5)

    thread = threading.Thread(target=run_scrapy_spider, args=(total_pages,))
    thread.start()

    return jsonify({
        'status': 'success',
        'message': 'Scraping started',
        'total_pages': total_pages
    })

@app.route('/api/scrape/status', methods=['GET'])
@REQUEST_LATENCY.time()
def get_scraping_status():
    REQUEST_COUNT.inc()
    return jsonify(scraping_status)

@app.route('/api/scrape/results', methods=['GET'])
@REQUEST_LATENCY.time()
def get_scraping_results():
    REQUEST_COUNT.inc()

    if not os.path.exists(SCRAPING_RESULT_PATH):
        return jsonify({'status': 'error', 'message': 'No scraping results found'}), 404

    try:
        with open(SCRAPING_RESULT_PATH, 'r') as f:
            results = json.load(f)
        return jsonify({
            'status': 'success',
            'count': len(results),
            'results': results
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Gabungkan dengan Prometheus metrics endpoint
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == '__main__':
    os.makedirs('shared_data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)
