import json

# Daftar file JSON yang ingin digabungkan
files = ['ai_hasil.json', 'ml_hasil.json', 'is_hasil.json', 'cysec_hasil.json']

# Daftar untuk menyimpan semua data dari file JSON
combined_data = []

# Membaca setiap file JSON dan menggabungkannya
for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        combined_data.extend(data)  # Gabungkan data dari file ke dalam list

# Menyimpan data yang telah digabungkan ke dalam file baru
with open('scraping_hasil.json', 'w') as f:
    json.dump(combined_data, f, indent=1)

print("File JSON berhasil digabungkan!")
