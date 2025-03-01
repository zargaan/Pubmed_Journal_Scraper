# PubMed Journal Scraper 🔥📚

[![Scrapy](https://img.shields.io/badge/Scrapy-2.11%2B-red)](https://scrapy.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)

Proyek ini bertujuan untuk mengumpulkan data judul Artikel dari situs web PubMed dengan teknik menggunakan teknik scrapy dan manajemen halaman otomatis.

**Nama Kelompok :**
1. Agato Uria Oidamar Prawira
2. Ndaniel Mahulae
3. Aracel Nestova Aprilyanto

## 📌 Daftar Isi
- [Sumber_Data](#-sumber_data)
- [Struktur Direktori](#-struktur-direktori-pubmed_journal_scraper)
- [Fitur](#-fitur)
- [Instalasi](#-instalasi)
- [Penggunaan](#-penggunaan)
- [Konfigurasi](#-konfigurasi)
- [Output](#-output)
- [Troubleshooting](#-troubleshooting)
- [Etika](#-etika)
- [Lisensi](#-lisensi)

---

## Sumber_data
Website : [PubMed](https://pubmed.ncbi.nlm.nih.gov/)

---

## Struktur-direktori-pubmed_journal_scraper

```plaintext
📦.scrapy
 ┗ 📂httpcache
 ┃ ┗ 📂pubmed
 ┃ ┃ ┣ 📂13
 ┃ ┃ ┃ ┗ 📂13a154ffd71c93895a679f8f50ea428c140958af
 ┃ ┃ ┃ ┃ ┣ 📜meta
 ┃ ┃ ┃ ┃ ┣ 📜pickled_meta
 ┃ ┃ ┃ ┃ ┣ 📜request_body
 ┃ ┃ ┃ ┃ ┣ 📜request_headers
 ┃ ┃ ┃ ┃ ┣ 📜response_body
 ┃ ┃ ┃ ┃ ┗ 📜response_headers
 ┃ ┃ ┣ 📂26
 ┃ ┃ ┃ ┗ 📂26bfa22f4171e6f75c0561e84ccc0b840e50188d
 ┃ ┃ ┃ ┃ ┣ 📜meta
 ┃ ┃ ┃ ┃ ┣ 📜pickled_meta
 ┃ ┃ ┃ ┃ ┣ 📜request_body
 ┃ ┃ ┃ ┃ ┣ 📜request_headers
 ┃ ┃ ┃ ┃ ┣ 📜response_body
 ┃ ┃ ┃ ┃ ┗ 📜response_headers
 ┃ ┃ ┣ 📂30
 ┃ ┃ ┃ ┗ 📂30834863ccc621103b7ac34a8827fa456d99564c
 ┃ ┃ ┃ ┃ ┣ 📜meta
 ┃ ┃ ┃ ┃ ┣ 📜pickled_meta
 ┃ ┃ ┃ ┃ ┣ 📜request_body
 ┃ ┃ ┃ ┃ ┣ 📜request_headers
 ┃ ┃ ┃ ┃ ┣ 📜response_body
 ┃ ┃ ┃ ┃ ┗ 📜response_headers
 ┃ ┃ ┣ 📂46
 ┃ ┃ ┃ ┗ 📂46c368416c4e727a076a7b465a9c4394247006ec
 ┃ ┃ ┃ ┃ ┣ 📜meta
 ┃ ┃ ┃ ┃ ┣ 📜pickled_meta
 ┃ ┃ ┃ ┃ ┣ 📜request_body
 ┃ ┃ ┃ ┃ ┣ 📜request_headers
 ┃ ┃ ┃ ┃ ┣ 📜response_body
 ┃ ┃ ┃ ┃ ┗ 📜response_headers
 ┃ ┃ ┣ 📂52
 ┃ ┃ ┃ ┗ 📂522cb827f0b18deb30c7b40ff9786edda1aa2552
 ┃ ┃ ┃ ┃ ┣ 📜meta
 ┃ ┃ ┃ ┃ ┣ 📜pickled_meta
 ┃ ┃ ┃ ┃ ┣ 📜request_body
 ┃ ┃ ┃ ┃ ┣ 📜request_headers
 ┃ ┃ ┃ ┃ ┣ 📜response_body
 ┃ ┃ ┃ ┃ ┗ 📜response_headers
 ┃ ┃ ┗ 📂e8
 ┃ ┃ ┃ ┗ 📂e8fcbc4cf8a8a53f568674cb09615f94b1df8f42
 ┃ ┃ ┃ ┃ ┣ 📜meta
 ┃ ┃ ┃ ┃ ┣ 📜pickled_meta
 ┃ ┃ ┃ ┃ ┣ 📜request_body
 ┃ ┃ ┃ ┃ ┣ 📜request_headers
 ┃ ┃ ┃ ┃ ┣ 📜response_body
 ┃ ┃ ┃ ┃ ┗ 📜response_headers
📦journal_scraper
 ┣ 📂spiders
 ┃ ┣ 📂__pycache__
 ┃ ┃ ┣ 📜pubmed.cpython-313.pyc
 ┃ ┃ ┗ 📜__init__.cpython-313.pyc
 ┃ ┣ 📜pubmed.py
 ┃ ┗ 📜__init__.py
 ┣ 📂__pycache__
 ┃ ┣ 📜pipelines.cpython-313.pyc
 ┃ ┣ 📜settings.cpython-313.pyc
 ┃ ┗ 📜__init__.cpython-313.pyc
 ┣ 📜items.py
 ┣ 📜middlewares.py
 ┣ 📜pipelines.py
 ┣ 📜settings.py
 ┗ 📜__init__.py
 📦.gitattributes
 📦ai_hasil.csv
 📦cysec_hasil.csv
 📦is_hasil.csv
 📦ml_hasil.csv
 📦scrapy.cfg
```

---

## 🚀 Fitur
- **Auto-pagination** hingga 1000 halaman
- **Sistem anti-blokir:**
  - Delay acak (3-10 detik) ⏱️
  - Rotasi header request 🌀
  - Retry otomatis saat error ♻️
- **Ekstraksi data:**
  - Judul + abstrak 📑
  - Daftar penulis + afiliasi 👨💻
  - Info jurnal + tahun publikasi 📅
  - Link artikel + PMID 🔗

---

## ⚙️ Instalasi

### 1️⃣ Clone Repo
```bash
git clone https://github.com/username/pubmed-scraper.git
cd pubmed-scraper
```

### 2️⃣ Setup Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🛠️ Penggunaan

### Scrape Default (5 Halaman)
```bash
scrapy crawl pubmed -o hasil.json
```

### Scrape dengan Parameter Kustom
```bash
# Scrape 10 halaman dengan delay 5 detik
scrapy crawl pubmed -s MAX_PAGES=10 -s DOWNLOAD_DELAY=5 -o hasil.json
```

### Modifikasi Kata Kunci
Edit `pubmed_spider.py`:
```python
start_urls = ['https://pubmed.ncbi.nlm.nih.gov/?term=your_keyword_here']
```

---

## ⚡ Konfigurasi
| Parameter        | Deskripsi                     | Default | Contoh             |
|-----------------|-----------------------------|---------|--------------------|
| `MAX_PAGES`     | Maksimum halaman             | 5       | `-s MAX_PAGES=20`  |
| `DOWNLOAD_DELAY`| Jeda antar request (detik)   | 3       | `-s DELAY=10`      |
| `RETRY_TIMES`   | Percobaan ulang saat gagal  | 2       | `-s RETRY=5`       |

---

## 📄 Contoh Output
```json
{
  "title": "AI in Cancer Diagnosis: A Systematic Review",
  "authors": "Zhang L, Smith J, Lee K, et al",
  "journal": {
    "name": "Nature Medicine",
    "year": 2023,
    "citation": "Nat Med. 2023 Jan;29(1):45-53. doi: 10.1038/s41591-022-02145-y."
  },
  "pmid": "36624315",
  "page": 7,
  "url": "https://pubmed.ncbi.nlm.nih.gov/36624315/"
}
```

---

## 🚨 Troubleshooting

### ❌ Problem: Artikel Tidak Terekstrak
✅ **Solusi:**
```python
# Cek selector terbaru
documents = response.css('.docsum-content').getall()
print(documents)
```

### ❌ Problem: Paginasi Error
✅ **Debug URL:**
```bash
scrapy shell 'https://pubmed.ncbi.nlm.nih.gov/?term=test'
```
Di shell:
```python
fetch(response.url)
print(f"Page: {response.meta['page_number']}")
```

### ❌ Problem: IP Terblokir
✅ **Mitigasi:**
Tambah proxy di `settings.py`:
```python
ROTATING_PROXY_LIST = [
    'http://proxy1:port',
    'http://proxy2:port'
]
```

---

## ⚠️ Etika
- **Patuhi** `robots.txt` PubMed
- **Cache hasil secara lokal** untuk mengurangi request
- **Hindari scraping data pribadi**

---

## 📜 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
