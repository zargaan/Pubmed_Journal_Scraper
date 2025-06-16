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
 ┣ 📂API_Scraping/         # API untuk scraping data
 ┃ ┣ 📜app.py             # Flask API endpoint
 ┃ ┣ 📜Dockerfile         # Konfigurasi Docker
 ┃ ┗ 📜requirements.txt   # Dependencies
 ┣ 📂API_preprocessed/    # API untuk preprocessing
 ┃ ┣ 📜app.py             # Flask API endpoint
 ┃ ┣ 📜Dockerfile         # Konfigurasi Docker
 ┃ ┣ 📜requirements.txt   # Dependencies
 ┃ ┗ 📜topic_model_trainer.py # Model training
 ┣ 📂data/                # Data storage
 ┣ 📂models/              # Model storage
 ┣ 📂monitoring/          # Monitoring configuration
 ┃ ┗ 📜prometheus.yml     # Prometheus config
 ┣ 📂shared/              # Shared utilities
 ┣ 📂shared_data/         # Shared data storage
 ┣ 📂journal_scraper/     # Core scraper code
 ┃ ┣ 📂spiders/
 ┃ ┃ ┣ 📜pubmed.py
 ┃ ┃ ┗ 📜__init__.py
 ┃ ┣ 📜items.py
 ┃ ┣ 📜middlewares.py
 ┃ ┣ 📜pipelines.py
 ┃ ┣ 📜settings.py
 ┃ ┗ 📜__init__.py
 ┣ 📜docker-compose.yml   # Docker services config
 ┣ 📜tracking_mlflow.py   # MLflow tracking
 ┣ 📜scrapy.cfg           # Scrapy configuration
 ┣ 📜penjadwalan.sh       # Scheduling script
 ┗ 📜README.md
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
  - Real-time monitoring
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
curl -X POST http://localhost:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"keyword": "machine learning", "max_pages": 10}'
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
  - Real-time monitoring
  - Performance metrics
  - System health
  - Custom visualizations

## Preprocessing
Proses pembersihan data dilakukan sebelum data disimpan:
- **Clean Text:** Menghapus spasi berlebih, newline, dan karakter tidak relevan pada judul
- **Clean Authors:** Menghapus tanda "et al.", ellipsis, dan pemisah seperti titik koma pada daftar penulis
- **Parse Journal:** Memisahkan nama jurnal, tahun publikasi, dan kutipan lengkap menggunakan regex
- **Topic Modeling:** Analisis topik dari artikel menggunakan LDA

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
