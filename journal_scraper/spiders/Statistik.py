import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
import re
from collections import Counter

dataAI = pd.read_json('Hasil Scraping\scraping_hasil.json')

print(dataAI.info()) # pengecekan MisVal
print(dataAI.describe()) #pengecekan statistik dasar

# Mengunduh stopwords dari NLTK
nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

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
stop_words = set(stopwords.words('english'))  # Bisa diubah ke bahasa lain jika perlu

# Menghapus stopwords
filtered_words = [word for word in words if word not in stop_words]

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

