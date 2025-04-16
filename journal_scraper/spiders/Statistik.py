import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
from collections import Counter
from transformers import BertTokenizer, BertModel
import torch
from io import BytesIO
import base64
import os


# Download NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

class DataProcessor:
    def __init__(self, data_path=None):
        
        self.data_path = data_path or 'shared_data/scraping_hasil.json'
        self.data = None
        self.filtered_words = []
        self.keyword_counts = {}
        self.embedding = None
        
    def is_processed(self):
        """Check if data has been processed"""
        return len(self.filtered_words) > 0
        
    def load_data(self):
        """Load JSON data"""
        if os.path.exists(self.data_path):
            self.data = pd.read_json(self.data_path)
        else:
            raise FileNotFoundError(f"Scraping data not found at {self.data_path}")
    
    def extract_titles(self):
        """Extract and clean titles from the data"""
        titles = []
        for entry in self.data['title']:
            if isinstance(entry, str):
                match = re.search(r'\[(.*?)\]', entry)
                if match:
                    titles.append(match.group(1))
            elif isinstance(entry, list):
                titles.extend(entry)
        return titles
    
    def preprocess_text(self, text):
        """Clean and tokenize text"""
        translator = str.maketrans('', '', string.punctuation)
        cleaned_text = text.translate(translator)
        words = word_tokenize(cleaned_text.lower())
        stop_words = set(stopwords.words('english'))
        return [word for word in words if word not in stop_words]
    
    def generate_wordcloud(self):
        """Generate wordcloud image as base64"""
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(self.filtered_words))
        
        img_buffer = BytesIO()
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(img_buffer, format='png', bbox_inches='tight')
        plt.close()
        img_buffer.seek(0)
        return base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    
    def count_keywords(self):
        """Count specific keywords frequency"""
        keywords = [
            'ai', 'artificial intelligence', 
            'is', 'information system', 
            'ml', 'machine learning', 
            'cysec', 'cyber security'
        ]
        text = ' '.join(self.filtered_words)
        return {keyword: text.count(keyword) for keyword in keywords}
    
    def generate_embeddings(self):
        """Generate BERT embeddings"""
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        model = BertModel.from_pretrained('bert-base-uncased')
        
        inputs = tokenizer(' '.join(self.filtered_words), 
                         return_tensors='pt', 
                         truncation=True, 
                         padding=True)
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        self.embedding = outputs.last_hidden_state[0][0].numpy()
        return self.embedding
    
    def process_all(self):
        """Run all processing steps"""
        self.load_data()
        titles = self.extract_titles()
        self.filtered_words = self.preprocess_text(" ".join(titles))
        self.keyword_counts = self.count_keywords()
        self.generate_embeddings()
        
        # Save embedding to file
        if self.embedding is not None:
            np.savetxt('../Hasil_embed.txt', self.embedding)
        
        return {
            'status': 'success',
            'word_count': len(self.filtered_words),
            'unique_words': len(set(self.filtered_words)),
            'embedding_shape': self.embedding.shape if self.embedding is not None else None,
            'filtered_text': " ".join(self.filtered_words) 
        }


    def get_basic_stats(self):
        """Return basic statistics"""
        if self.data is None:
            self.load_data()
            
        titles = self.extract_titles()
        years = self.data['journal'].apply(lambda x: x.get('year', None)).dropna()
        
        return {
            'total_articles': len(self.data),
            'earliest_year': int(years.min()) if not years.empty else None,
            'latest_year': int(years.max()) if not years.empty else None,
            'unique_journals': self.data['journal'].apply(lambda x: x.get('name', '')).nunique()
        }
    
    def get_keyword_counts(self):
        """Return filtered keyword counts (remove zero counts)"""
        return {k: v for k, v in self.keyword_counts.items() if v > 0}
    
    def get_top_words(self, n=10):
        """Return top n frequent words"""
        if not self.filtered_words:
            self.process_all()  # Pastikan data sudah diproses
        
        word_counts = Counter(self.filtered_words)
        return dict(word_counts.most_common(n))

if __name__ == '__main__':
    try:
        
        processor = DataProcessor()
        result = processor.process_all()
        
        print(f"- Total kata unik: {result['unique_words']}")
        print(f"- Dimensi embedding: {result['embedding_shape']}")
        
        # Tampilkan statistik dasar
        stats = processor.get_basic_stats()
       
        print(f"- Total artikel: {stats['total_articles']}")
        print(f"- Rentang tahun: {stats['earliest_year']} - {stats['latest_year']}")
        print(f"- Jurnal unik: {stats['unique_journals']}")
        
    except Exception as e:
        print(f" Error: {str(e)}")