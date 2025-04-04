from flask import Flask, jsonify
from .spiders.statistik import DataProcessor

app = Flask(__name__)
processor = DataProcessor()

@app.route('/preprocess', methods=['GET'])
def preprocess():
    try:
        result = processor.process_all()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)