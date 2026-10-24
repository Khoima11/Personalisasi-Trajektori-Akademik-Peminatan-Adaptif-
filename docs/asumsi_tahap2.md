# Daftar Periksa Tahap 2: Asumsi yang Perlu Divalidasi Peneliti

Dokumen ini merangkum semua keputusan dan asumsi pada Tahap 2. Periksa setiap bagian, lalu tandai yang perlu diubah.

## A. Koreksi terhadap dokumen kurikulum

| No | Temuan | Keputusan |
|---|---|---|
| 1 | Prasyarat Statistika Terapan tertulis SIN2044, sedangkan Statistik dan Probabilitas berkode SIN2042 | Dianggap salah ketik, dipakai SIN2042 |
| 2 | Nilai minimal prasyarat Tata Kelola TI kosong | Diasumsikan D sesuai aturan mayoritas |
| 3 | Capstone Projek tidak memiliki kode | Memakai nomor MK45 sebagai kode |
| 4 | Ejaan "Pemrograan" pada MK pilihan PSI | Dirapikan menjadi "Pemrograman" |
| 5 | Aturan peminatan tidak tertulis | Mahasiswa hanya boleh mengambil MK pilihan dari satu peminatan (keputusan peneliti) |

## B. Prasyarat mata kuliah pilihan (asumsi berbasis materi)

Semua memakai nilai minimal D.

| Mata kuliah pilihan | Semester | Prasyarat | Alasan |
|---|---|---|---|
| Perencanaan Strategis SI (SIA) | 5 | Sistem Informasi Manajemen | Perencanaan strategis SI membutuhkan pemahaman peran SI dalam organisasi |
| Manajemen Layanan Teknologi Informasi (SIA) | 6 | Perencanaan Strategis SI | Manajemen layanan TI diturunkan dari rencana strategis SI |
| Manajemen Risiko & Keamanan IT (SIA) | 6 | Keamanan Sistem Informasi | Manajemen risiko keamanan dibangun di atas konsep keamanan SI |
| Enterprise Resource Planning (ERP) (SIA) | 6 | Manajemen Proses Bisnis | ERP mengintegrasikan proses bisnis organisasi |
| IS/IT Audit (SIA) | 7 | Manajemen Risiko & Keamanan IT | Audit SI/TI menilai pengendalian risiko dan keamanan |
| IS/IT Audit (SIA) | 7 | Tata Kelola Teknologi Informasi | Audit SI/TI berpedoman pada kerangka tata kelola TI |
| Knowledge Management System (SIA) | 7 | Sistem Informasi Manajemen | Sistem manajemen pengetahuan berbasis konsep SI organisasi |
| Supply Chain Management (SCM) (SIA) | 7 | Enterprise Resource Planning (ERP) | SCM berjalan di atas sistem ERP |
| Pemrograman Web Lanjutan (PSI) | 5 | Perancangan dan Pemrograman Web | Lanjutan langsung dari Perancangan dan Pemrograman Web |
| Pemrograman Mobile (PSI) | 6 | Pemrograman Berorientasi Obyek | Pengembangan aplikasi mobile berbasis paradigma berorientasi objek |
| Testing dan Implementasi (PSI) | 6 | Rekayasa Perangkat Lunak | Pengujian perangkat lunak bagian dari siklus rekayasa perangkat lunak |
| Sistem Komputasi Awan (PSI) | 6 | Jaringan dan Komunikasi Data | Komputasi awan membutuhkan dasar jaringan dan komunikasi data |
| Sistem Informasi Geografis (PSI) | 7 | Basis Data Lanjut | SIG mengelola basis data spasial |
| Teknologi Keuangan Syariah (PSI) | 7 | SI Akuntansi Keuangan Syariah | Teknologi keuangan syariah melanjutkan SI akuntansi keuangan syariah |
| Enterprise Application Integration (PSI) | 7 | Pemrograman Web Lanjutan | Integrasi aplikasi enterprise memakai web service dan API dari pemrograman web lanjutan |
| Pemodelan Data (DTA) | 5 | Basis Data Lanjut | Pemodelan data melanjutkan basis data lanjut |
| Artificial Intelligence & Sistem Data (DTA) | 6 | Algoritma & Struktur Data | AI membutuhkan dasar algoritma dan struktur data |
| Bisnis Intelijen (DTA) | 6 | Data Warehouse & Mining | Bisnis intelijen dibangun di atas data warehouse |
| Machine Learning (DTA) | 6 | Statistika Terapan | Machine learning membutuhkan dasar statistika |
| Machine Learning (DTA) | 6 | Aljabar Linier | Machine learning membutuhkan dasar aljabar linier |
| Sistem Pengambil Keputusan (DTA) | 7 | Statistika Terapan | Metode pengambilan keputusan memakai dasar statistika |
| Analisis dan Visualisasi Data (DTA) | 7 | Statistika Terapan | Analisis data membutuhkan dasar statistika terapan |
| Pengelolaan Big Data (DTA) | 7 | Pemodelan Data | Pengelolaan big data melanjutkan pemodelan data |

Rantai berjenjang terpanjang: Dasar-dasar Pemrograman → Algoritma & Struktur Data → Perancangan dan Pemrograman Web → Pemrograman Web Lanjutan → Enterprise Application Integration (5 tingkat).

## C. Peta karir ke peminatan dan prioritas mata kuliah pilihan

| Karir | Peminatan | CPL | Prioritas semester 6 | Prioritas semester 7 | Dukungan kurikulum |
|---|---|---|---|---|---|
| Data Analyst | DTA | CPL04, CPL10, CPL03 | Bisnis Intelijen > Machine Learning > Artificial Intelligence & Sistem Data | Analisis dan Visualisasi Data > Sistem Pengambil Keputusan > Pengelolaan Big Data | kuat |
| Data Scientist | DTA | CPL04, CPL10, CPL11 | Machine Learning > Bisnis Intelijen > Artificial Intelligence & Sistem Data | Analisis dan Visualisasi Data > Pengelolaan Big Data > Sistem Pengambil Keputusan | kuat |
| Machine Learning Engineer | DTA | CPL04, CPL05, CPL10 | Machine Learning > Artificial Intelligence & Sistem Data > Bisnis Intelijen | Pengelolaan Big Data > Analisis dan Visualisasi Data > Sistem Pengambil Keputusan | kuat |
| AI Researcher | DTA | CPL04, CPL10, CPL11 | Artificial Intelligence & Sistem Data > Machine Learning > Bisnis Intelijen | Pengelolaan Big Data > Sistem Pengambil Keputusan > Analisis dan Visualisasi Data | sedang |
| NLP Research Scientist | DTA | CPL04, CPL10, CPL11 | Machine Learning > Artificial Intelligence & Sistem Data > Bisnis Intelijen | Pengelolaan Big Data > Analisis dan Visualisasi Data > Sistem Pengambil Keputusan | lemah |
| Database Administrator | DTA | CPL04, CPL06 | Bisnis Intelijen > Artificial Intelligence & Sistem Data > Machine Learning | Pengelolaan Big Data > Analisis dan Visualisasi Data > Sistem Pengambil Keputusan | kuat |
| Web Developer | PSI | CPL05, CPL04 | Testing dan Implementasi > Sistem Komputasi Awan > Pemrograman Mobile | Enterprise Application Integration > Sistem Informasi Geografis > Teknologi Keuangan Syariah | kuat |
| Mobile App Developer | PSI | CPL05, CPL04 | Pemrograman Mobile > Testing dan Implementasi > Sistem Komputasi Awan | Enterprise Application Integration > Sistem Informasi Geografis > Teknologi Keuangan Syariah | kuat |
| Software Engineer | PSI | CPL05, CPL09 | Testing dan Implementasi > Pemrograman Mobile > Sistem Komputasi Awan | Enterprise Application Integration > Teknologi Keuangan Syariah > Sistem Informasi Geografis | kuat |
| Cloud Solutions Architect | PSI | CPL06, CPL05, CPL08 | Sistem Komputasi Awan > Testing dan Implementasi > Pemrograman Mobile | Enterprise Application Integration > Sistem Informasi Geografis > Teknologi Keuangan Syariah | sedang |
| Information Security Analyst | SIA | CPL06, CPL07, CPL08 | Manajemen Risiko & Keamanan IT > Manajemen Layanan Teknologi Informasi > Enterprise Resource Planning (ERP) | IS/IT Audit > Knowledge Management System > Supply Chain Management (SCM) | sedang |
| Graphics Programmer | PSI | CPL05 | Pemrograman Mobile > Testing dan Implementasi > Sistem Komputasi Awan | Sistem Informasi Geografis > Enterprise Application Integration > Teknologi Keuangan Syariah | lemah |

Semester 5 hanya memiliki satu MK pilihan per peminatan, sehingga otomatis mengikuti peminatan.

## D. Aturan engine

- Skala nilai: A, A-, B+, B, B-, C+, C, D, E. Lulus prasyarat jika nilai ≥ nilai minimal.
- Jatah MK pilihan: 1 (semester 5), 2 (semester 6), 2 (semester 7).
- Prasyarat dianggap terpenuhi jika sudah lulus di transkrip, atau dijadwalkan di semester sebelumnya pada rencana (status BERSYARAT).
- MK wajib terjadwal yang prasyaratnya tidak terpenuhi tidak dapat menjadi pemenuh prasyarat MK lain (validasi berantai).
- Jika mahasiswa sudah mengambil MK pilihan, peminatan terkunci ke peminatan tersebut.
- Pemilihan MK pilihan: enumerasi seluruh kombinasi dalam peminatan, saring dengan validasi prasyarat, pilih skor prioritas karir tertinggi (bobot 3/2/1).

## E. Penyesuaian berdasarkan kemampuan pemrograman (asumsi peneliti)

Aturan: mata kuliah pilihan mendapat tambahan skor 1,5 jika minimal satu kemampuan relevan bernilai Baik. Karena selisih skor antar peringkat prioritas adalah 1, tambahan ini dapat menaikkan mata kuliah satu peringkat, tetapi tidak melampaui dua peringkat. Penyesuaian hanya mengubah urutan di antara mata kuliah yang sudah lolos validasi prasyarat.

| Karir | Kemampuan relevan (untuk kesiapan teknis dan saran) |
|---|---|
| Data Analyst | SQL, Python |
| Data Scientist | Python, SQL |
| Machine Learning Engineer | Python |
| AI Researcher | Python |
| NLP Research Scientist | Python |
| Database Administrator | SQL |
| Web Developer | SQL |
| Mobile App Developer | Java |
| Software Engineer | Java, Python |
| Cloud Solutions Architect | Python |
| Information Security Analyst | Python |
| Graphics Programmer | Java |

| Mata kuliah pilihan | Kemampuan relevan |
|---|---|
| Pemodelan Data | SQL |
| Artificial Intelligence & Sistem Data | Python |
| Bisnis Intelijen | SQL |
| Machine Learning | Python |
| Analisis dan Visualisasi Data | Python |
| Pengelolaan Big Data | Python, SQL |
| Pemrograman Mobile | Java |
| Testing dan Implementasi | Java |
| Sistem Komputasi Awan | Python |
| Sistem Informasi Geografis | SQL |
| Teknologi Keuangan Syariah | SQL |
| Enterprise Application Integration | Java |
| Enterprise Resource Planning (ERP) | SQL |
| Supply Chain Management (SCM) | SQL |

Keterbatasan: dataset hanya memuat Python, SQL, dan Java, sehingga bahasa lain seperti JavaScript (Web Developer) atau C++ (Graphics Programmer) tidak terwakili.
