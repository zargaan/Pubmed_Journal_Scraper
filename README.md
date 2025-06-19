# PubMed Journal Scraper

[![Scrapy](https://img.shields.io/badge/Scrapy-2.11%2B-red)](https://scrapy.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue)](https://docker.com)
[![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange)](https://prometheus.io)
[![Grafana](https://img.shields.io/badge/Grafana-Visualization-blue)](https://grafana.com)

Proyek ini bertujuan untuk mengumpulkan data judul Artikel dari situs web PubMed dengan teknik menggunakan teknik scrapy dan manajemen halaman otomatis. Proyek ini terdiri dari dua API utama: API Scraping untuk pengumpulan data dan API Preprocessing untuk pemrosesan data, dilengkapi dengan sistem monitoring menggunakan Prometheus dan Grafana.

**Anggota Kelompok :**
1. Agato Uria Oidamar Prawira - 225150407111062
2. Ndaniel Mahulae	-	225150300111016
3. Aracel Nestova Aprilyanto	- 225150200111054

## Daftar Isi
- [Sumber Data](#sumber-data)
- [Struktur Direktori](#struktur-direktori)
- [Fitur](#fitur)
- [Instalasi](#instalasi)
- [Penggunaan](#penggunaan)
- [Monitoring](#monitoring)
- [Preprocessing](#preprocessing)
- [Docker Deployment](#docker-deployment)
- [Etika](#etika)
- [Lisensi](#lisensi)

---

## Sumber Data
Website : [PubMed](https://pubmed.ncbi.nlm.nih.gov/)

---

## Struktur Direktori

```plaintext
📦journal_scraper/
 ┣ 📂.dvc/                      # Folder konfigurasi DVC
 ┃ ┣ 📜.gitignore               # Abaikan isi tertentu dari folder ini
 ┃ ┣ 📜config                   # Konfigurasi DVC utama
 ┣ 📂API_Scraping/        # API untuk scraping data
 ┃ ┣ 📜app.py             # Flask API endpoint
 ┃ ┣ 📜Dockerfile         # Konfigurasi Docker
 ┃ ┗ 📜requirements.txt   # Dependencies
 ┣ 📂API_preprocessed/    # API untuk preprocessing
 ┃ ┣ 📜app.py             # Flask API endpoint
 ┃ ┣ 📜Dockerfile         # Konfigurasi Docker
 ┃ ┣ 📜requirements.txt   # Dependencies
 ┃ ┗ 📜topic_model_trainer.py   # Model training
 ┣ 📂journal_scraper/           # Core scraper code
 ┃ ┣ 📂spiders/                 # Spider-spider Scrapy
 ┃ ┃ ┣ 📜preprop.py             # Spider preprocessing 
 ┃ ┃ ┣ 📜pubmed.py              # Spider untuk scraping dari PubMed
 ┃ ┃ ┣ 📜statistik.py           # Spider untuk statistik atau metrik tambahan
 ┃ ┃ ┗ 📜__init__.py            # Init file untuk modul spiders
 ┃ ┣ 📜items.py                 # Definisi struktur item hasil scraping
 ┃ ┣ 📜middlewares.py           # Middleware Scrapy untuk modifikasi request/response
 ┃ ┣ 📜pipelines.py             # Pipeline pemrosesan data hasil scraping
 ┃ ┣ 📜settings.py              # Konfigurasi utama Scrapy
 ┃ ┗ 📜__init__.py              # Init file untuk modul utama journal_scraper
 ┣ 📂models/                    # Model storage
 ┃ ┣ 📜bertopic_model.pkl.dvc   # Metadata tracking DVC untuk model
 ┃ ┣ 📜grafana_table.json       # Output dalam format JSON untuk dashboard Grafana
 ┃ ┣ 📜top_keywords.json        # Kata kunci utama dari hasil model
 ┃ ┗ 📜training_metrics.json    # Metrik hasil pelatihan model
 ┣ 📂monitoring/          # Monitoring configuration
 ┃ ┗ 📜prometheus.yml     # Prometheus config
 ┣ 📂shared/data/         # Shared utilities/ Folder untuk wordcloud hasil visualisasi topik
 ┃ ┗ 📜wordcloud.png      # Gambar wordcloud dalam ekstensi png
 ┣ 📂shared_data/         # Shared data storage
 ┃ ┣ 📜.gitignore               # Mengabaikan file tertentu dari Git
 ┃ ┣ 📜JlhScraping.py           # Script analisis untuk menggabungkan semua scraping
 ┃ ┣ 📜scraping_hasil_ai.json   # Hasil scraping untuk topik AI
 ┃ ┣ 📜scraping_hasil_cysec.json# Hasil scraping untuk topik Cyber Security
 ┃ ┣ 📜scraping_hasil_is.json   # Hasil scraping untuk topik Information System
 ┃ ┣ 📜scraping_hasil_ml.json   # Hasil scraping untuk topik Machine Learning
 ┃ ┗ 📜seluruh_hasil.json.dvc   # Tracking DVC untuk seluruh_hasil.json
 ┣ 📜.dockerignore              # File untuk mengabaikan file saat build Docker
 ┣ 📜.dvcignore                 # File untuk mengabaikan file dalam proses DVC
 ┣ 📜.gitignore                 # Mengabaikan file tertentu dari Git
 ┣ 📜.gitattributes             # Aturan atribut Git (misal, CRLF handling, merge, dll)
 ┣ 📜hasil_embed.txt           # Hasil embedding teks, kemungkinan dari model
 ┣ 📜LICENSE                   # Lisensi proyek
 ┣ 📜docker-compose.yml   # Docker services config
 ┣ 📜tracking_mlflow.py   # MLflow tracking
 ┣ 📜scrapy.cfg           # Scrapy configuration
 ┣ 📜penjadwalan.sh       # Scheduling script
 ┗ 📜README.md            # Dokumentasi proyek
```

## Fitur
- **API Scraping:**
  - Auto-pagination hingga 1000 halaman
  - Sistem anti-blokir dengan delay acak
  - Rotasi header request
  - Retry otomatis saat error
  - REST API endpoint untuk scraping

- **API Preprocessing:**
  - Pembersihan dan normalisasi data
  - Ekstraksi fitur teks
  - Topic modeling
  - REST API endpoint untuk preprocessing

- **Monitoring:**
  - Prometheus metrics collection
  - Grafana dashboards
  - Performance tracking

## Instalasi

### 1️⃣ Clone Repo
```bash
git clone https://github.com/username/pubmed-scraper.git
cd pubmed-scraper
```

### 2️⃣ Setup dengan Docker
```bash
# Build dan jalankan semua service
docker-compose up --build

# Jalankan di background
docker-compose up -d
```

### 3️⃣ Akses Services
- Scraping API: http://localhost:5000
- Preprocessing API: http://localhost:5001
- Grafana Dashboard: http://localhost:3000
- Prometheus: http://localhost:9090

## Penggunaan

### API Scraping
```bash
# Scrape artikel dengan keyword
curl -X POST http://localhost:5001/api/preprocessed/training
```

### API Preprocessing
```bash
# Preprocess data
curl -X POST http://localhost:5001/preprocess \
  -H "Content-Type: application/json" \
  -d '{"data": "path/to/data.csv"}'
```

## Monitoring
- **Prometheus Metrics:**
  - Request latency
  - Error rates
  - Resource usage
  - Scraping statistics

- **Grafana Dashboards:**
  - Performance metrics
  - System health
  - Custom visualizations

## Preprocessing
Proses pembersihan data dilakukan sebelum data disimpan:
- **Clean Text:** Menghapus spasi berlebih, newline, dan karakter tidak relevan pada judul
- **Clean Authors:** Menghapus tanda "et al.", ellipsis, dan pemisah seperti titik koma pada daftar penulis
- **Parse Journal:** Memisahkan nama jurnal, tahun publikasi, dan kutipan lengkap menggunakan regex
- **Topic Modeling:** Analisis topik dari artikel menggunakan BERTopic

## Docker Deployment
Proyek menggunakan Docker Compose untuk mengelola multiple services:
- **Scraping API:** Port 5000
- **Preprocessing API:** Port 5001
- **Prometheus:** Port 9090
- **Grafana:** Port 3000

Konfigurasi Docker dapat ditemukan di `docker-compose.yml`

## Etika
- **Patuhi** `robots.txt` PubMed
- **Cache hasil secara lokal** untuk mengurangi request
- **Hindari scraping data pribadi**
- **Gunakan rate limiting** untuk menghindari overload server

---

## Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE)
