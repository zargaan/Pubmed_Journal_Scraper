from flask import Flask, jsonify, send_file, request
import os
import io
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
import sys
import json
from os.path import dirname, join
from topic_model_trainer import train_model

sys.path.append("/app")

from journal_scraper.spiders.statistik import DataProcessor

app = Flask(__name__)

processor = DataProcessor()

EMBEDDING_PATH = 'Hasil_embed.txt'

@app.route('/api/preprocessed/wordcloud', methods=['GET'])
def get_wordcloud():
    """Endpoint untuk wordcloud hasil preprocessing"""
    try:
        result = processor.process_all()

        text = result.get("filtered_text", "")

        if not isinstance(text, str):
            return jsonify({'error': 'filtered_text bukan string'}), 500

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
        
        # Simpan ke buffer
        img_buffer = io.BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(img_buffer, format='png')
        plt.close()
        img_buffer.seek(0)
        
        return send_file(img_buffer, mimetype='image/png')

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

@app.route('/api/preprocessed/embeddings', methods=['GET'])
def get_embeddings():
    try:
        # Baca file embedding
        if os.path.exists(EMBEDDING_PATH):
            embeddings = np.loadtxt(EMBEDDING_PATH)
            return jsonify({'embeddings': embeddings.tolist()})
        else:
            return jsonify({'error': 'Embeddings not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/api/preprocessed/training', methods=['POST'])
def train_topic():
    try:
        with open("shared_data/scraping_hasil.json") as f:
            raw_data = json.load(f)

        # Ambil teks dari data (asumsi datanya list of dict dengan key 'text')
        documents = [entry['title'] for entry in raw_data]

        result = train_model(documents)

        return jsonify({
            "message": "Training selesai",
            "jumlah_topik": result["n_topics"],
            "coherence_score": result["coherence_score"]
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)