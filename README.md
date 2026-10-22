# IDSS Rekomendasi Karir dan Mata Kuliah Pilihan Mahasiswa S1 Sistem Informasi

Intelligent Decision Support System (IDSS) yang mengintegrasikan klasifikasi peran karir berbasis
**Algoritma C4.5** dengan **Curriculum Prerequisite Network** untuk menghasilkan rekomendasi mata kuliah
pilihan semester 5, 6, dan 7 yang tervalidasi rantai prasyaratnya.

> Status: **Tahap 1 selesai** (praproses data dan pemodelan C4.5). Tahap berikutnya: kurikulum acuan,
> engine trajektori, aplikasi, dan evaluasi.

## Struktur repositori

```
data/raw/            dataset sumber (Kaggle: Computer Science Students Career Prediction)
data/processed/      dataset bersih hasil praproses
src/c45.py           implementasi C4.5 (gain ratio, split numerik & kategorikal, ekstraksi aturan)
src/experiment.py    praproses + eksperimen perbandingan fitur + pelatihan model final
src/figures.py       pembuatan grafik hasil
models/              model C4.5 (JSON) dan aturan IF-THEN
docs/                hasil eksperimen, metrik per kelas, confusion matrix, log praproses
docs/figures/        grafik untuk laporan
app/                 aplikasi DSS (tahap berikutnya)
```

## Cara menjalankan

```bash
pip install -r requirements.txt
python src/experiment.py
python src/figures.py
```

## Ringkasan tahap 1

- Data awal 180 baris, 33 karir. Dipakai 12 karir dengan minimal 6 data, lalu 80 baris duplikat
  dihapus sehingga tersisa 72 baris (evaluasi tanpa kebocoran data duplikat).
- Fitur: minat (kategorikal), IPK (numerik), kemampuan Python/SQL/Java (ordinal: Weak=0, Average=1, Strong=2).
- Evaluasi: stratified 5-fold cross validation, diulang 10 kali.

| Skenario | Accuracy | F1-macro |
|---|---|---|
| E1 Minat saja | 84,7% | 74,2% |
| E2 Skill ordinal + IPK | 15,6% | 12,9% |
| E3 Skill biner + minat | 84,4% | 74,7% |
| E4 Minat + skill ordinal + IPK | 79,6% | 70,1% |
| **E5 Model final (E4 + pre-pruning)** | **84,0%** | **73,8%** |

Model final memiliki kedalaman 2 dan 14 aturan IF-THEN (lihat `models/aturan_if_then.json`).

## Keterbatasan

Dataset bersifat sekunder dan fiktif, berukuran kecil, berlatar Computer Science, dan belum memuat
peran khas Sistem Informasi (misalnya Business Analyst, System Analyst). Penelitian ini diposisikan
sebagai *proof of concept*.

## Sumber data dan lisensi

Dataset: *Computer Science Students Career Prediction* (Kaggle, pengunggah: devildyno).
Periksa lisensi di halaman Kaggle sebelum menyertakan file mentah di repositori publik.
