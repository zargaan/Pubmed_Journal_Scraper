from bertopic import BERTopic
import pandas as pd
import joblib

def train_model(documents):
    # Train model
    topic_model = BERTopic()
    topics, _ = topic_model.fit_transform(documents)

    # Evaluate (coherence score belum built-in, tapi bisa pakai alternatif)
    # Untuk simpel, kita pakai jumlah topik
    n_topics = len(set(topics))

    # Save model
    joblib.dump(topic_model, 'models/bertopic_model.pkl')

    return {"n_topics": n_topics}
