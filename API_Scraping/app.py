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
SCRAPED_ARTICLE_COUNT = Gauge('scraped_article_count', 'Jumlah artikel hasil scraping')

# ======= Scraping Status Global =======
scraping_status = {
    'is_running': False,
    'start_time': None,
    'end_time': None,
    'progress': 0,
    'current_page': 0,
    'total_pages': 5
}

SCRAPING_RESULT_PATH = os.path.join('shared_data', 'seluruh_hasil.json')

@app.route('/api/scrape/results', methods=['GET'])
def get_scraping_results():

    if not os.path.exists(SCRAPING_RESULT_PATH):
        return jsonify({'status': 'error', 'message': 'No scraping results found'}), 404

    try:
        with open(SCRAPING_RESULT_PATH, 'r') as f:
            results = json.load(f)
            SCRAPED_ARTICLE_COUNT.set(len(results)) 
        return jsonify({
            'status': 'success',
            'jumlah_artikel': len(results),
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
