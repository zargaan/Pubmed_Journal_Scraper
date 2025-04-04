from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/scrape', methods=['POST'])
def run_scraper():
    try:
        # Jalankan spider Scrapy
        subprocess.run(['scrapy', 'crawl', 'pubmed'], cwd='journal_scraper')
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)