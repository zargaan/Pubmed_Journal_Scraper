import requests
import json

# Ganti ini dengan teks yang mau kamu prediksi topiknya
sample_texts = [
    "The research explores deep learning applications in medical imaging.",
    "COVID-19 has significantly impacted global health systems.",
]

# Format payload sesuai dengan format MLflow pyfunc
payload = {
    "columns": ["text"],  # Kolom harus sama dengan yang diproses di PyFuncModel kamu
    "data": [[text] for text in sample_texts]
}

# Kirim request POST ke model server
response = requests.post(
    url="http://127.0.0.1:5002/invocations",
    headers={"Content-Type": "application/json"},
    data=json.dumps(payload)
)

# Tampilkan hasil
print("Response dari model:")
print(response.json())
