# PubMed Journal Scraper 🔥📚

[![Scrapy](https://img.shields.io/badge/Scrapy-2.11%2B-red)](https://scrapy.org/)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)

Proyek ini bertujuan untuk mengumpulkan data judul Artikel dari situs web PubMed dengan teknik menggunakan teknik scrapy dan manajemen halaman otomatis.

**Anggota Kelompok :**
1. Agato Uria Oidamar Prawira - 225150407111062
2. Ndaniel Mahulae	-	225150300111016
3. Aracel Nestova Aprilyanto	- 225150200111054

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
- [Preprocessing](#-preprocessing)
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
scrapy crawl pubmed -o hasil.json # Output JSON
scrapy crawl pubmed -o hasil.csv # Output CSV
```

### Scrape dengan Parameter Kustom
```bash
# Scrape 10 halaman dengan delay 5 detik
scrapy crawl pubmed -s MAX_PAGES=10 -s DOWNLOAD_DELAY=5 -o hasil.json
```

### Modifikasi Kata Kunci
Edit `pubmed.py`:
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
# JSON
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
```csv
# CSV
title,authors,journal,pmid,page,url
A guide to machine learning for biologists.,"Greener JG, Kandathil SM, Moffat L, Jones DT.","{'name': 'Nat Rev Mol Cell Biol', 'year': 2022, 'citation': 'Nat Rev Mol Cell Biol. 2022 Jan;23(1):40-55. doi: 10.1038/s41580-021-00407-0. Epub 2021 Sep 13.'}",34518686,1,https://pubmed.ncbi.nlm.nih.gov/34518686/
"Introduction to Machine Learning, Neural Networks, and Deep Learning.","Choi RY, Coyner AS, Kalpathy-Cramer J, Chiang MF, Campbell JP.","{'name': 'Transl Vis Sci Technol', 'year': 2020, 'citation': 'Transl Vis Sci Technol. 2020 Feb 27;9(2):14. doi: 10.1167/tvst.9.2.14.'}",32704420,1,https://pubmed.ncbi.nlm.nih.gov/32704420/
Machine Learning in Medicine.,Deo RC.,"{'name': 'Circulation', 'year': 2015, 'citation': 'Circulation. 2015 Nov 17;132(20):1920-30. doi: 10.1161/CIRCULATIONAHA.115.001593.'}",26572668,1,https://pubmed.ncbi.nlm.nih.gov/26572668/
eDoctor: machine learning and the future of medicine.,"Handelman GS, Kok HK, Chandra RV, Razavi AH, Lee MJ, Asadi H.","{'name': 'J Intern Med', 'year': 2018, 'citation': 'J Intern Med. 2018 Dec;284(6):603-619. doi: 10.1111/joim.12822. Epub 2018 Sep 3.'}",30102808,1,https://pubmed.ncbi.nlm.nih.gov/30102808/
Supervised Machine Learning: A Brief Primer.,"Jiang T, Gradus JL, Rosellini AJ.","{'name': 'Behav Ther', 'year': 2020, 'citation': 'Behav Ther. 2020 Sep;51(5):675-687. doi: 10.1016/j.beth.2020.05.002. Epub 2020 May 16.'}",32800297,1,https://pubmed.ncbi.nlm.nih.gov/32800297/
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

## 🔍 Preprocessing
Proses pembersihan data dilakukan sebelum data disimpan:
- **Clean Text:** Menghapus spasi berlebih, newline, dan karakter tidak relevan pada judul.
- **Clean Authors:** Menghapus tanda "et al.", ellipsis, dan pemisah seperti titik koma pada daftar penulis.
- **Parse Journal:** Memisahkan nama jurnal, tahun publikasi, dan kutipan lengkap menggunakan regex.

---

## 📜 Lisensi
Proyek ini dilisensikan di bawah [MIT License](LICENSE).
