import pandas as pd
import numpy 
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
import json

# Mengunduh stopwords dari NLTK
nltk.download('punkt')
nltk.download('stopwords')

dataAI = pd.read_json('Hasil Scraping\scraping_hasil.json')

print(dataAI.info()) # pengecekan MisVal
print(dataAI.describe()) #pengecekan statistik dasar



# Menarik hanya teks dalam tanda kurung siku (title) dari setiap entri
titles = []
for entry in dataAI['title']:
    match = re.search(r'\[(.*?)\]', entry)
    if match:
        titles.append(match.group(1))  # Ambil teks yang ada di dalam []

# Gabungkan semua judul menjadi satu string
text = " ".join(titles)

# Preprocessing teks: menghapus tanda baca dan stopwords
# Menghapus tanda baca
translator = str.maketrans('', '', string.punctuation)
cleaned_text = text.translate(translator)

# Tokenisasi kata
words = word_tokenize(cleaned_text.lower())

# Mengambil stopwords
stop_words = set(stopwords.words('english')) 

# Menghapus stopwords
filtered_words = [word for word in words if word not in stop_words]

# Menghapus domain-specific stopwords
domain_stopwords = set(['approach', 'study', 'method', 'result', 'effect'])
filtered_words = [word for word in filtered_words if word not in domain_stopwords]

# Lemmatization
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()
filtered_words = [lemmatizer.lemmatize(word) for word in filtered_words]

# Membuat WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_words))

# Visualisasi WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')  # Menyembunyikan axis
plt.show()

# Distribusi Kata: Menghitung frekuensi kata
word_freq = Counter(filtered_words)

keywords = ['ai','artificial intelligence','is','information system', 'ml','machine learning', 'cysec','cyber security']
filtered_word_freq = {}


for keyword in keywords:
    keyword_count = 0
    if ' '.join(filtered_words).find(keyword) != -1:  # Cek jika frasa ada
        keyword_count = ' '.join(filtered_words).count(keyword)  # Menghitung frekuensi kemunculannya
    filtered_word_freq[keyword] = keyword_count

# Menampilkan distribusi kata dalam bentuk grafik batang
plt.figure(figsize=(10, 5))
if filtered_word_freq:
    filtered_word_freq = {key: value for key, value in filtered_word_freq.items() if value > 0}
    if filtered_word_freq:
        plt.bar(filtered_word_freq.keys(), filtered_word_freq.values(), color='blue')
        plt.xlabel('Kata')
        plt.ylabel('Frekuensi')
        plt.title('Distribusi Frekuensi Kata')
        plt.xticks(rotation=45)
        plt.show()
else:
    print("No Match")

# Simpan keyword-keyword terfilter ke top_keywords.json
with open('models/top_keywords.json', 'w') as f:
    json.dump(sorted(filtered_word_freq.items(), key=lambda x: x[1], reverse=True), f)

#Representasi teks

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Menyiapkan teks untuk BERT
inputs = tokenizer(' '.join(filtered_words), return_tensors='pt', truncation=True, padding=True)

# Mendapatkan embeddings dari BERT
with torch.no_grad():
    outputs = model(**inputs)

# Mendapatkan embeddings untuk token pertama (representasi [CLS])
embedding = outputs.last_hidden_state[0][0].numpy()

# Menyimpan embedding ke dalam file .txt
if __name__ == '__main__':
    numpy.savetxt('Hasil_embed.txt', embedding)