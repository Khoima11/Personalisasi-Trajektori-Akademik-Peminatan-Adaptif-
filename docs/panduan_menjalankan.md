# Panduan Menjalankan dan Deploy NAVIKA

## A. Menjalankan di komputer sendiri (Windows, CMD)

1. Masuk ke folder repositori:
   ```cmd
   cd /d "C:\Users\User\Project_DSS\Personalisasi-Trajektori-Akademik-Peminatan-Adaptif-"
   ```
2. Pasang pustaka yang dibutuhkan (cukup sekali):
   ```cmd
   python -m pip install -r requirements.txt
   ```
3. Jalankan aplikasi:
   ```cmd
   python -m streamlit run app/streamlit_app.py
   ```
   Browser akan terbuka otomatis di `http://localhost:8501`. Untuk menghentikan, tekan `Ctrl + C` di CMD.

Jika langkah 2 gagal karena versi Python terlalu baru, pasang Python 3.12 dari python.org, lalu ganti
`python` dengan `py -3.12` pada langkah 2 dan 3.

## B. Deploy ke Streamlit Community Cloud (agar bisa dibuka lewat tautan)

1. Pastikan seluruh kode sudah di-push ke GitHub.
2. Buka share.streamlit.io, lalu masuk dengan akun GitHub.
3. Pilih **Create app**, lalu pilih opsi deploy dari repositori GitHub.
4. Isi:
   - Repository: `Khoima11/Personalisasi-Trajektori-Akademik-Peminatan-Adaptif-`
   - Branch: `main`
   - Main file path: `app/streamlit_app.py`
   - App URL: misalnya `navika-si` (opsional)
5. Buka **Advanced settings**, pilih Python **3.12**, lalu simpan.
6. Pilih **Deploy**. Proses pertama memakan waktu beberapa menit.
7. Salin tautan aplikasi untuk dibagikan ke responden SUS.

Catatan: jika repositori bersifat privat, Streamlit akan meminta izin akses tambahan ke repositori tersebut.
Aplikasi gratis di Streamlit Community Cloud akan "tertidur" jika lama tidak dibuka; pengunjung cukup menekan
tombol untuk membangunkannya kembali.
