# Dasbor E-commerce dengan Streamlit

Ini adalah aplikasi Streamlit sederhana yang menyediakan dasbor e-commerce interaktif. Aplikasi ini memvisualisasikan berbagai metrik dan statistik yang terkait dengan platform e-commerce menggunakan data dari file CSV.

## Fitur

- Menampilkan pratinjau dataset.
- Menampilkan statistik ringkasan dari dataset.
- Menyediakan visualisasi seperti:
  - Distribusi status pesanan.
  - Rata-rata skor ulasan berdasarkan kategori produk.
  - Distribusi tipe pembayaran.
  - Rata-rata waktu pengiriman berdasarkan kategori produk.
- Memungkinkan pengguna untuk memfilter data berdasarkan kota pelanggan.

## Dependensi

Untuk menjalankan aplikasi ini secara lokal, Anda memerlukan hal-hal berikut:

- Python 3.7 atau lebih tinggi.
- Pengelola paket `pip`.

## Instalasi dan proses running

1. **clone repositori** ke mesin lokal Anda:
   ```bash
   git clone https://github.com/srlnapr/Submission_serlin-aprilia
   cd nama-repositori-anda

2. **install dependensi** 
   pip install -r requirements.txt

3. **menjalankan dashboard**
   streamlit run dashboard/dashboard.py
