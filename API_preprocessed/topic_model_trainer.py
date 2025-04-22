from bertopic import BERTopic
import pandas as pd
import joblib
import json
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess  # Untuk preprocessing dasar

def train_model(documents):
    # Preprocessing untuk gensim
    processed_docs = [simple_preprocess(doc) for doc in documents]  # Tokenisasi + lowercase
    dictionary = Dictionary(processed_docs)
    
    # Train model BERTopic
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(documents)

    # Persiapkan topik untuk coherence score
    topic_words = []
    for topic_id in range(len(set(topics))-1):  # Exclude outlier topic (-1)
        words = [word for word, _ in topic_model.get_topic(topic_id)]
        topic_words.append(words)

    # Hitung coherence score
    coherence_model = CoherenceModel(
        topics=topic_words,
        texts=processed_docs,  # Gunakan texts yang sudah diproses
        dictionary=dictionary,
        coherence='c_v'
    )
    coherence_score = coherence_model.get_coherence()

    # Simpan model
    joblib.dump(topic_model, 'models/bertopic_model.pkl')

    n_topics = len([t for t in set(topics) if t != -1])

    metrics = {
        "jumlah_topik": n_topics,
        "coherence_score": coherence_score
    }
    with open("models/training_metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    return metrics