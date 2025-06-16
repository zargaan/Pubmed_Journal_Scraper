from bertopic import BERTopic
import os
import json
import joblib
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess
from nltk.corpus import stopwords

def train_model(documents):
    # Preprocessing: tokenisasi + lowercase
    processed_docs = [simple_preprocess(doc) for doc in documents]
    dictionary = Dictionary(processed_docs)

    # Latih BERTopic (pakai default vectorizer)
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(documents)

    # Ambil frekuensi topik
    topic_freq = topic_model.get_topic_info()
    top_topics = topic_freq[topic_freq.Topic != -1].nlargest(5, "Count")

    # Mapping label topik
    topic_labels = {
        "0": "Health Information Systems",
        "1": "Information Management & HR Planning",
        "2": "Privacy-Preserving Electronic Health Records",
        "3": "Information & Data Security",
        "4": "Clinical & Patient Information Systems"
    }

    # Ambil top 3 keyword dari tiap topik
    top_keywords_3 = {}
    for _, row in top_topics.iterrows():
        topic_id = row['Topic']
        words = topic_model.get_topic(topic_id)
        top_keywords_3[str(topic_id)] = [
            {"keyword": word.replace("_", " "), "weight": float(weight)}
            for word, weight in words[:3]
        ]

    # Format ke tabel Grafana
    grafana_rows = []
    for topic_id_str, keywords in top_keywords_3.items():
        topic_label = topic_labels.get(topic_id_str, f"Topic {topic_id_str}")
        for i, kw in enumerate(keywords):
            grafana_rows.append([
                topic_label if i == 0 else "", 
                kw["keyword"],
                kw["weight"]
            ])

    grafana_table = {
        "columns": [
            {"text": "Topic", "type": "string"},
            {"text": "Keyword", "type": "string"},
            {"text": "Weight", "type": "number"}
        ],
        "rows": grafana_rows,
        "type": "table"
    }

    # Simpan file
    os.makedirs("models", exist_ok=True)

    with open("models/grafana_table.json", "w") as f:
        json.dump(grafana_table, f, indent=2)

    # Ambil semua topik untuk hitung coherence
    topic_words = []
    valid_topic_ids = topic_model.get_topic_info()
    valid_topic_ids = valid_topic_ids[valid_topic_ids.Topic != -1]["Topic"].tolist()

    for topic_id in valid_topic_ids:
        topic = topic_model.get_topic(topic_id)
        if topic is not None:
            words = [word for word, _ in topic]
            if words:
                topic_words.append(words)

    # Hitung coherence score
    if topic_words and processed_docs:
        coherence_model = CoherenceModel(
            topics=topic_words,
            texts=processed_docs,
            dictionary=dictionary,
            coherence='c_v'
        )
        coherence_score = coherence_model.get_coherence()
    else:
        coherence_score = 0.0

    # Simpan model dan metrik
    joblib.dump(topic_model, "models/bertopic_model.pkl")

    n_topics = len([t for t in set(topics) if t != -1])
    metrics = {
        "jumlah_topik": n_topics,
        "coherence_score": coherence_score
    }
    with open("models/training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    return metrics
