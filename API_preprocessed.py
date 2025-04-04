from flask import Flask, jsonify, send_file
from journal_scraper.spiders.statistik import DataProcessor
import os
from io import BytesIO
import matplotlib.pyplot as plt
import base64
import sys
from os.path import dirname, join


# Tambahkan path ke sys.path
sys.path.append(join(dirname(__file__), 'journal_scraper'))


app = Flask(__name__)
processor = DataProcessor()

@app.route('/api/preprocessed/wordcloud', methods=['GET'])
def get_wordcloud():
    """Endpoint untuk wordcloud hasil preprocessing"""
    try:
        if not processor.is_processed():
            processor.process_all()
        
        img_data = base64.b64decode(processor.generate_wordcloud())
        return send_file(
            BytesIO(img_data),
            mimetype='image/png',
            as_attachment=False
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preprocessed/keywords', methods=['GET'])
def get_keywords():
    """Endpoint untuk distribusi keyword"""
    try:
        if not processor.is_processed():
            processor.process_all()
            
        return jsonify({
            'keywords': processor.get_keyword_counts(),
            'top_words': processor.get_top_words(10)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/preprocessed/stats', methods=['GET'])
def get_stats():
    """Endpoint untuk statistik dasar"""
    try:
        processor.load_data()
        return jsonify(processor.get_basic_stats())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)