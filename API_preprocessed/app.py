from flask import Flask, jsonify, send_file, request, Response
import os
import io
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import base64
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST, Summary, Counter
import sys
import json
from os.path import dirname, join
from topic_model_trainer import train_model
from flask import send_from_directory
from flask_cors import CORS

sys.path.append("/app")

from journal_scraper.spiders.statistik import DataProcessor

def convert_table_to_array_of_objects(table_json):
    columns = table_json.get("columns", [])
    rows = table_json.get("rows", [])

    col_names = [col['text'] for col in columns]
    result = []

    for row in rows:
        obj = {}
        for i, val in enumerate(row):
            obj[col_names[i]] = val
        result.append(obj)
    return result

app = Flask(__name__)
CORS(app)

processor = DataProcessor()

EMBEDDING_PATH = 'Hasil_embed.txt'

jumlah_topik_metric = Gauge('jumlah_topik', 'Jumlah topik yang ditemukan')  #nilai naik turun
coherence_score_metric = Gauge('coherence_score', 'Nilai coherence score model')
PREPROCESSING_TIME = Summary('preprocessing_duration_seconds',
                             'Waktu yang dibutuhkan untuk preprocessing',
                             ['type'] ) #durasi
REQUEST_LATENCY = Summary('request_latency_seconds', 'Waktu proses setiap request')
PREPROCESSING_ERRORS = Counter('preprocessing_errors_total', 'Jumlah error selama preprocessing') #nilai naik terus
KEYWORD_COUNT = Gauge('keyword_count', 'Frekuensi kemunculan keyword', ['keyword'])

@app.route('/api/preprocessed/wordcloud', methods=['GET'])
def get_wordcloud():
    with REQUEST_LATENCY.time():
        with PREPROCESSING_TIME.labels(type='wordcloud').time():
            try:
                result = processor.process_all()
                text = result.get("filtered_text", "")

                if not isinstance(text, str):
                    return jsonify({'error': 'filtered_text bukan string'}), 500

                wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

                # Simpan gambar WordCloud ke file statis di server
                output_folder = 'data'
                os.makedirs(output_folder, exist_ok=True)
                img_path = os.path.join(output_folder, 'wordcloud.png')
                
                # Menyimpan gambar WordCloud ke dalam file PNG
                wordcloud.to_file(img_path)

                return jsonify({'status': 'success', 'message': 'WordCloud saved successfully', 'image_url': f'/api/preprocessed/wordcloud.png'})

            except Exception as e:
                PREPROCESSING_ERRORS.inc()
                return jsonify({'error': str(e)}), 500

@app.route('/wordcloud')
def serve_wordcloud():
     with REQUEST_LATENCY.time():
        with PREPROCESSING_TIME.labels(type='wcl').time():
            return send_from_directory('data', 'wordcloud.png')

@app.route('/api/preprocessed/stats', methods=['GET'])
def get_stats():
    with REQUEST_LATENCY.time():
        with PREPROCESSING_TIME.labels(type='stats').time():
            try:
                processor.load_data()
                return jsonify(processor.get_basic_stats())
            except Exception as e:
                PREPROCESSING_ERRORS.inc()
                return jsonify({'error': str(e)}), 500

@app.route('/api/preprocessed/embeddings', methods=['GET'])
def get_embeddings():
    with REQUEST_LATENCY.time():
        with PREPROCESSING_TIME.labels(type='embeddings').time():
            try:
                if os.path.exists(EMBEDDING_PATH):
                    embeddings = np.loadtxt(EMBEDDING_PATH)
                    return jsonify({'embeddings': embeddings.tolist()})
                else:
                    return jsonify({'error': 'Embeddings not found'}), 404
            except Exception as e:
                PREPROCESSING_ERRORS.inc()
                return jsonify({'error': str(e)}), 500

@app.route('/api/preprocessed/training', methods=['POST'])
def train_topic():
    with REQUEST_LATENCY.time():
        with PREPROCESSING_TIME.labels(type='training').time():
            try:
                with open("shared_data/seluruh_hasil.json") as f:
                    raw_data = json.load(f)

                documents = [entry['title'] for entry in raw_data]
                result = train_model(documents)

                return jsonify({
                    "message": "Training selesai",
                    "n_topics": result["jumlah_topik"],
                    "coherence_score": result["coherence_score"]
                })

            except Exception as e:
                PREPROCESSING_ERRORS.inc()
                return jsonify({'error': str(e)}), 500

@app.route('/api/preprocessed/metrics', methods=['GET'])
def prometheus_metrics():
    with REQUEST_LATENCY.time():
        with PREPROCESSING_TIME.labels(type='metrics').time():
            try:
                with open('models/training_metrics.json') as f:
                    metrics = json.load(f)

                jumlah_topik_metric.set(metrics.get('jumlah_topik', 0))
                coherence_score_metric.set(metrics.get('coherence_score', 0.0))

                return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

            except Exception as e:
                return Response(f"# Error: {str(e)}", mimetype='text/plain'), 500

@app.route('/api/preprocessed/top_keywords', methods=['GET'])
def get_top_keywords():
    with REQUEST_LATENCY.time():
        with PREPROCESSING_TIME.labels(type='top_keywords').time():
            try:
                topic_labels = {
                    "0": "Health Information Systems",
                    "1": "Information Management & HR Planning",
                    "2": "BlockChain",
                    "3": "Information & Data Security",
                    "4": "Clinical & Patient Information Systems"
                }

                with open('models/grafana_table.json') as f:
                    keywords = json.load(f) 

                keywords_array = convert_table_to_array_of_objects(keywords)
                return jsonify(keywords_array)

            except Exception as e:
                PREPROCESSING_ERRORS.inc()
                return jsonify({'error': str(e)}), 500
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)