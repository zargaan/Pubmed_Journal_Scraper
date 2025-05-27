from bertopic import BERTopic
import pandas as pd
import joblib
import json
import mlflow
import mlflow.pyfunc
import os
from gensim.models import CoherenceModel
from gensim.corpora import Dictionary
from gensim.utils import simple_preprocess

# Wrapper supaya BERTopic bisa dilog sebagai pyfunc
class BERTopicWrapper(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        import joblib
        self.model = joblib.load(context.artifacts["bertopic_model"])

    def predict(self, context, model_input):
        texts = model_input["text"].tolist()
        topics, _ = self.model.transform(texts)
        topic_info = [self.model.get_topic(t) if t != -1 else [] for t in topics]
        return [{"topic_id": t, "keywords": [word for word, _ in info]} for t, info in zip(topics, topic_info)]


def train_model(documents):
    mlflow.set_tracking_uri("file:///C:/Users/danie/proyek/Pubmed_Journal_Scraper/mlruns")
    mlflow.set_experiment("my-local-exp")

    with mlflow.start_run() as run:
        mlflow.log_param("model", "BERTopic")
        mlflow.log_param("num_documents", len(documents))

        processed_docs = [simple_preprocess(doc) for doc in documents]
        dictionary = Dictionary(processed_docs)

        topic_model = BERTopic()
        topics, _ = topic_model.fit_transform(documents)

        topic_words = []
        for topic_id in range(len(set(topics)) - 1):  # Exclude outlier topic -1
            words = [word for word, _ in topic_model.get_topic(topic_id)]
            topic_words.append(words)

        coherence_model = CoherenceModel(
            topics=topic_words,
            texts=processed_docs,
            dictionary=dictionary,
            coherence='c_v'
        )
        coherence_score = coherence_model.get_coherence()
        n_topics = len([t for t in set(topics) if t != -1])

        mlflow.log_metric("coherence_score", coherence_score)
        mlflow.log_metric("n_topics", n_topics)

        os.makedirs("models", exist_ok=True)
        model_path = "models/bertopic_model.pkl"
        joblib.dump(topic_model, model_path)

        # Logging model as pyfunc
        mlflow.pyfunc.log_model(
            artifact_path="bertopic_model",
            python_model=BERTopicWrapper(),
            artifacts={"bertopic_model": model_path}
        )

        # Save metric as file (optional)
        metrics = {
            "jumlah_topik": n_topics,
            "coherence_score": coherence_score
        }
        with open("models/training_metrics.json", "w") as f:
            json.dump(metrics, f, indent=4)
        mlflow.log_artifact("models/training_metrics.json")

        print("Run ID:", run.info.run_id)
        return metrics

if __name__ == "__main__":
    data_path = os.path.join("shared_data", "seluruh_hasil.json")
    if not os.path.exists(data_path):
        exit(1)

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    documents = [entry["title"] for entry in data if "title" in entry]
    if not documents:
        exit(1)

    hasil = train_model(documents)
    print(json.dumps(hasil, indent=4))
