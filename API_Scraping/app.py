# API_scraping.py
from flask import Flask, jsonify, request
import subprocess
import os
import threading
import time
from datetime import datetime
import json

app = Flask(__name__)

# Status scraping
scraping_status = {
    'is_running': False,
    'start_time': None,
    'end_time': None,
    'progress': 0,
    'current_page': 0,
    'total_pages': 5  # Default value, bisa diubah via API
}

# Path ke file hasil scraping
SCRAPING_RESULT_PATH = os.path.join('shared_data', 'scraping_hasil.json')

def run_scrapy_spider(total_pages):
    """Fungsi untuk menjalankan spider Scrapy di background"""
    try:
        # Update status
        scraping_status.update({
            'is_running': True,
            'start_time': datetime.now().isoformat(),
            'end_time': None,
            'progress': 0,
            'current_page': 0,
            'total_pages': total_pages
        })
        
        # Jalankan spider Scrapy
        command = f'scrapy crawl pubmed -a max_pages={total_pages} -O {SCRAPING_RESULT_PATH}'
        process = subprocess.Popen(command, shell=True, cwd=os.getcwd())
        
        # Simulasikan update progress (dalam implementasi nyata, bisa dari log atau callback)
        while process.poll() is None:
            time.sleep(1)
            if scraping_status['current_page'] < scraping_status['total_pages']:
                scraping_status['current_page'] += 1
                scraping_status['progress'] = int((scraping_status['current_page'] / scraping_status['total_pages']) * 100)
        
        # Update status setelah selesai
        scraping_status.update({
            'is_running': False,
            'end_time': datetime.now().isoformat(),
            'progress': 100
        })
        
    except Exception as e:
        scraping_status.update({
            'is_running': False,
            'error': str(e)
        })

@app.route('/api/scrape/start', methods=['POST'])
def start_scraping():
    """Endpoint untuk memulai proses scraping"""
    if scraping_status['is_running']:
        return jsonify({'status': 'error', 'message': 'Scraping is already running'}), 400
    
    # Ambil parameter dari request
    data = request.get_json()
    total_pages = data.get('total_pages', 5)  # Default 5 halaman
    
    # Jalankan spider di thread terpisah
    thread = threading.Thread(target=run_scrapy_spider, args=(total_pages,))
    thread.start()
    
    return jsonify({
        'status': 'success',
        'message': 'Scraping started',
        'total_pages': total_pages
    })

@app.route('/api/scrape/status', methods=['GET'])
def get_scraping_status():
    """Endpoint untuk mendapatkan status scraping"""
    return jsonify(scraping_status)

@app.route('/api/scrape/results', methods=['GET'])
def get_scraping_results():
    """Endpoint untuk mendapatkan hasil scraping"""
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

if __name__ == '__main__':
    # Buat folder hasil scraping jika belum ada
    os.makedirs('shared_data', exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)