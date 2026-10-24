# NAVIKA: Navigasi Karir dan Akademik

IDSS rekomendasi karir dan mata kuliah pilihan mahasiswa S1 Sistem Informasi.

Intelligent Decision Support System (IDSS) yang mengintegrasikan klasifikasi peran karir berbasis
**Algoritma C4.5** dengan **Curriculum Prerequisite Network** untuk menghasilkan rekomendasi mata kuliah
pilihan semester 5, 6, dan 7 yang tervalidasi rantai prasyaratnya.

> Status: **Tahap 3 selesai** (aplikasi NAVIKA berbasis Streamlit). Tahap berikutnya: evaluasi
> (black-box testing, SUS, validasi pakar).

## Struktur repositori

```
data/raw/            dataset sumber (Kaggle: Computer Science Students Career Prediction)
data/processed/      dataset bersih hasil praproses
data/kurikulum/      kurikulum acuan S1 SI, rantai prasyarat, CPL, peta karir ke mata kuliah
src/c45.py           implementasi C4.5 (gain ratio, split numerik & kategorikal, ekstraksi aturan)
src/experiment.py    praproses + eksperimen perbandingan fitur + pelatihan model final
src/figures.py       pembuatan grafik hasil
src/engine.py        Curriculum Prerequisite Network + engine trajektori + integrasi C4.5
src/gambar_graf.py   gambar graf prasyarat
tests/               skenario uji dan uji acak kepatuhan prasyarat
models/              model C4.5 (JSON) dan aturan IF-THEN
docs/                hasil eksperimen, metrik per kelas, confusion matrix, log praproses
docs/figures/        grafik untuk laporan
app/streamlit_app.py tampilan aplikasi NAVIKA (Streamlit)
app/logic.py         logika aplikasi: input ringkas, integrasi C4.5 + engine, penjelasan aturan
.streamlit/          tema aplikasi
```

## Menjalankan aplikasi NAVIKA

```bash
pip install -r requirements.txt
streamlit run app/streamlit_app.py
```

Panduan lengkap (Windows dan deploy ke Streamlit Community Cloud): `docs/panduan_menjalankan.md`.

## Menjalankan eksperimen dan pengujian

```bash
pip install -r requirements.txt
python src/experiment.py
python src/figures.py
python src/gambar_graf.py
python tests/uji_kepatuhan.py
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

## Ringkasan tahap 2

- Kurikulum acuan: 66 mata kuliah (45 wajib, 21 pilihan dalam 3 peminatan: SIA, PSI, DTA).
- Curriculum Prerequisite Network: graf berarah asiklik dengan 33 relasi prasyarat
  (10 dari dokumen kurikulum, 23 asumsi berbasis materi), rantai terpanjang 5 tingkat.
- Peta 12 karir ke peminatan, CPL (rujukan IS2020), dan prioritas mata kuliah pilihan.
- Engine: enumerasi kombinasi mata kuliah pilihan semester 5-7 dalam satu peminatan,
  validasi prasyarat berantai, pemilihan berdasarkan prioritas karir, dan penjelasan alasan.
- Pengujian: 18/18 skenario terencana sesuai harapan (termasuk penyesuaian kemampuan); uji acak
  1.000 profil mahasiswa dengan nilai dan kemampuan acak menghasilkan 0 pelanggaran prasyarat (kepatuhan 100%).
- Daftar asumsi untuk divalidasi: `docs/asumsi_tahap2.md`.

## Ringkasan tahap 3

Aplikasi NAVIKA (Streamlit) dengan alur: input profil (minat, IPK, kemampuan Python/SQL/Java) dan nilai
mata kuliah ringkas, prediksi karir C4.5 beserta aturan keputusan, peta jalur studi semester 5-7 dengan status
prasyarat, peringatan, rincian prasyarat, unduhan rencana studi (CSV), penelusuran rantai prasyarat, dan
pembaruan rekomendasi otomatis saat data diubah (simulasi adaptif). Kemampuan pemrograman yang relevan
dapat menaikkan prioritas mata kuliah pilihan satu peringkat, serta dipakai untuk kesiapan teknis dan saran
pengembangan (pemetaan di `data/kurikulum/kemampuan.json`, asumsi peneliti). Mata kuliah wajib yang tidak ditanyakan
diasumsikan lulus.

## Keterbatasan

Dataset bersifat sekunder dan fiktif, berukuran kecil, berlatar Computer Science, dan belum memuat
peran khas Sistem Informasi (misalnya Business Analyst, System Analyst). Penelitian ini diposisikan
sebagai *proof of concept*. Prasyarat mata kuliah pilihan tidak tercantum di dokumen kurikulum sehingga
disusun berdasarkan keterkaitan materi dan perlu divalidasi.

## Sumber data dan lisensi

Dataset: *Computer Science Students Career Prediction* (Kaggle, pengunggah: devildyno).
Periksa lisensi di halaman Kaggle sebelum menyertakan file mentah di repositori publik.
