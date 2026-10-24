"""
Pengujian kepatuhan prasyarat engine trajektori.
Jalankan dari root repo:  python tests/uji_kepatuhan.py

Bagian A: skenario uji terencana (black-box) dengan hasil yang diharapkan, termasuk penyesuaian kemampuan.
Bagian B: uji acak 1.000 profil mahasiswa (nilai dan kemampuan acak); setiap rekomendasi diverifikasi
          ulang secara independen terhadap rantai prasyarat.
"""
import csv
import os
import random
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from engine import SLOT_PILIHAN, CurriculumNetwork, TrajectoryEngine, verifikasi  # noqa: E402

net = CurriculumNetwork()
eng = TrajectoryEngine(net)
OUT = os.path.join(os.path.dirname(__file__), "..", "docs")


def transkrip_dasar(sampai_semester=4, nilai="B"):
    return {k: nilai for k, m in net.mk.items() if m["jenis"] == "wajib" and m["semester"] <= sampai_semester}


def pilihan(hasil):
    return {m["kode"]: t["semester"] for t in hasil["trajektori"] for m in t["mata_kuliah"] if m["jenis"] == "pilihan"}


def status_wajib(hasil, kode):
    for t in hasil["trajektori"]:
        for m in t["mata_kuliah"]:
            if m["kode"] == kode:
                return m["status_prasyarat"]
    return None


# ---------------- Bagian A: skenario terencana ----------------
def skenario():
    S = []

    tr = transkrip_dasar()
    h = eng.rekomendasi("Web Developer", tr, 5)
    p = pilihan(h)
    S.append(("S01", "Semua MK semester 1-4 lulus (B), karir Web Developer, awal semester 5",
              "Peminatan PSI; 5 MK pilihan; Enterprise Application Integration bersyarat lulus Pemrograman Web Lanjutan",
              h["peminatan"] == "PSI" and len(p) == 5 and "PSI7584" in p, h, tr))

    tr = transkrip_dasar(); tr["SIN3094"] = "E"
    h = eng.rekomendasi("Web Developer", tr, 5)
    p = pilihan(h)
    S.append(("S02", "Perancangan dan Pemrograman Web bernilai E, karir Web Developer",
              "Pemrograman Web Lanjutan dan Enterprise Application Integration tidak direkomendasikan",
              "PSI5514" not in p and "PSI7584" not in p, h, tr))

    tr = transkrip_dasar(); tr["SIN3054"] = "E"
    h = eng.rekomendasi("Data Scientist", tr, 5)
    p = pilihan(h)
    S.append(("S03", "Statistika Terapan bernilai E, karir Data Scientist",
              "Machine Learning, SPK, dan Analisis & Visualisasi Data tidak direkomendasikan",
              not {"DTA6624", "DTA7634", "DTA7644"} & set(p), h, tr))

    tr = transkrip_dasar(); tr["SIN3032"] = "E"
    h = eng.rekomendasi("Machine Learning Engineer", tr, 5)
    p = pilihan(h)
    S.append(("S04", "Aljabar Linier bernilai E, karir Machine Learning Engineer",
              "Machine Learning tidak direkomendasikan; diganti MK pilihan DTA lain",
              "DTA6624" not in p and sum(1 for s in p.values() if s == 6) == 2, h, tr))

    tr = transkrip_dasar(); tr["SIN4192"] = "E"
    h = eng.rekomendasi("Information Security Analyst", tr, 5)
    p = pilihan(h)
    S.append(("S05", "Keamanan Sistem Informasi bernilai E, karir Information Security Analyst",
              "Manajemen Risiko & Keamanan IT dan IS/IT Audit (rantai berjenjang) tidak direkomendasikan",
              "SIA6454" not in p and "SIA7474" not in p, h, tr))

    tr = transkrip_dasar(); tr["SIN3362"] = "D"
    h = eng.rekomendasi("Database Administrator", tr, 5)
    p = pilihan(h)
    S.append(("S06", "Basis Data Lanjut bernilai D (batas minimal), karir Database Administrator",
              "Pemodelan Data tetap layak karena nilai minimal D terpenuhi",
              "DTA5594" in p, h, tr))

    tr = transkrip_dasar(6)
    tr.update({"DTA5594": "B", "DTA6614": "B", "DTA6624": "A", "SIN5292": "D"})
    h = eng.rekomendasi("Data Analyst", tr, 7)
    S.append(("S07", "Awal semester 7, Metodologi Penelitian bernilai D",
              "Seminar Proposal ditandai TIDAK_LAYAK karena membutuhkan nilai minimal C",
              status_wajib(h, "SIN7342") == "TIDAK_LAYAK", h, tr))

    tr = transkrip_dasar(5); tr["DTA5594"] = "A"
    h = eng.rekomendasi("Data Analyst", tr, 6)
    p = pilihan(h)
    S.append(("S08", "Awal semester 6, sudah mengambil Pemodelan Data",
              "Melanjutkan peminatan DTA dengan 2 MK semester 6 dan 2 MK semester 7",
              h["peminatan"] == "DTA" and len(p) == 4, h, tr))

    tr = transkrip_dasar(5); tr["PSI5514"] = "B"
    h = eng.rekomendasi("Data Scientist", tr, 6)
    p = pilihan(h)
    S.append(("S09", "Sudah mengambil MK pilihan PSI, tetapi prediksi karir Data Scientist",
              "Peminatan tetap terkunci di PSI dan sistem memberi peringatan ketidaksesuaian",
              h["peminatan"] == "PSI" and all(k.startswith("PSI") for k in p)
              and any("terkunci" in w for w in h["peringatan"]), h, tr))

    tr = transkrip_dasar(6); tr.update({"SIA5434": "B", "SIA6444": "B", "SIA6464": "B"})
    h = eng.rekomendasi("Information Security Analyst", tr, 7)
    p = pilihan(h)
    S.append(("S10", "Awal semester 7 tanpa Manajemen Risiko & Keamanan IT, karir Information Security Analyst",
              "IS/IT Audit tidak direkomendasikan; diganti KMS dan SCM",
              "SIA7474" not in p and {"SIA7494", "SIA7504"} <= set(p), h, tr))

    tr = transkrip_dasar()
    h = eng.rekomendasi("Graphics Programmer", tr, 5)
    S.append(("S11", "Karir Graphics Programmer",
              "Rekomendasi tetap disusun dengan catatan dukungan kurikulum lemah",
              h["dukungan_kurikulum"] == "lemah" and h["catatan_karir"] != "", h, tr))

    tr = transkrip_dasar(5); tr.update({"SIN5372": "E", "SIA5434": "B"})
    h = eng.rekomendasi("Information Security Analyst", tr, 6)
    p = pilihan(h)
    S.append(("S12", "Enterprise Architecture bernilai E, awal semester 6, karir Information Security Analyst",
              "Tata Kelola TI tidak layak sehingga IS/IT Audit (berantai) juga tidak direkomendasikan",
              status_wajib(h, "SIN6404") == "TIDAK_LAYAK" and "SIA7474" not in p, h, tr))

    tr = transkrip_dasar(); tr["SIN2174"] = "E"; del tr["SIN3362"]
    h = eng.rekomendasi("Database Administrator", tr, 5)
    p = pilihan(h)
    S.append(("S13", "Basis Data bernilai E sehingga Basis Data Lanjut belum ditempuh (rantai 4 tingkat), karir Database Administrator",
              "Pemodelan Data dan Pengelolaan Big Data tidak direkomendasikan",
              "DTA5594" not in p and "DTA7654" not in p, h, tr))

    tr = transkrip_dasar()
    h = eng.rekomendasi("Cloud Solutions Architect", tr, 5)
    p = pilihan(h)
    S.append(("S14", "Karir Cloud Solutions Architect, semua lulus",
              "Sistem Komputasi Awan menjadi prioritas semester 6",
              "PSI6544" in p, h, tr))

    tr = transkrip_dasar()
    h = eng.rekomendasi("Data Analyst", tr, 5, {"python": 2, "sql": 1, "java": 1})
    p = pilihan(h)
    alasan = [m.get("alasan", "") for t in h["trajektori"] for m in t["mata_kuliah"] if m["kode"] == "DTA7654"]
    S.append(("S15", "Karir Data Analyst, kemampuan Python Baik",
              "Pengelolaan Big Data (relevan Python) naik satu peringkat menggantikan Sistem Pengambil Keputusan, disertai alasan",
              "DTA7654" in p and "DTA7634" not in p and alasan and "Python" in alasan[0], h, tr))

    tr = transkrip_dasar()
    h = eng.rekomendasi("Data Analyst", tr, 5, {"python": 1, "sql": 1, "java": 1})
    p = pilihan(h)
    S.append(("S16", "Karir Data Analyst, semua kemampuan Cukup",
              "Tidak ada penyesuaian; semester 7 tetap Analisis dan Visualisasi Data serta Sistem Pengambil Keputusan",
              {"DTA7644", "DTA7634"} <= set(p), h, tr))

    tr = transkrip_dasar()
    h = eng.rekomendasi("Information Security Analyst", tr, 5, {"python": 1, "sql": 2, "java": 1})
    sem6 = [m["kode"] for t in h["trajektori"] if t["semester"] == 6 for m in t["mata_kuliah"] if m["jenis"] == "pilihan"]
    S.append(("S17", "Karir Information Security Analyst, kemampuan SQL Baik",
              "ERP (relevan SQL) naik dari peringkat 3 ke 2, tetapi Manajemen Risiko & Keamanan IT tetap prioritas pertama",
              sem6[:1] == ["SIA6454"] and "SIA6464" in sem6, h, tr))

    tr = transkrip_dasar()
    h = eng.rekomendasi("Data Analyst", tr, 5, {"python": 0, "sql": 1, "java": 1})
    S.append(("S18", "Karir Data Analyst, kemampuan Python Kurang",
              "Kesiapan teknis berstatus Perlu penguatan dan muncul saran pengembangan Python",
              h["kesiapan_teknis"]["status"] == "Perlu penguatan" and any("Python" in x for x in h["saran_pengembangan"]), h, tr))

    return S


def bagian_a():
    rows, lulus = [], 0
    for sid, kondisi, harapan, ok, h, tr in skenario():
        pel = verifikasi(net, h, tr)
        sesuai = ok and not pel
        lulus += sesuai
        rek = "; ".join(f"S{t['semester']}: " + ", ".join(m["nama"] for m in t["mata_kuliah"] if m["jenis"] == "pilihan")
                        for t in h["trajektori"])
        rows.append({"id": sid, "kondisi": kondisi, "hasil_diharapkan": harapan,
                     "rekomendasi_pilihan": rek, "pelanggaran_prasyarat": len(pel),
                     "hasil": "Sesuai" if sesuai else "Tidak sesuai"})
    with open(os.path.join(OUT, "skenario_uji_prasyarat.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)
    print(f"Bagian A: {lulus}/{len(rows)} skenario sesuai harapan")
    for r in rows:
        print(f"  {r['id']} {r['hasil']:<13} {r['kondisi']}")
    return lulus, len(rows)


# ---------------- Bagian B: uji acak ----------------
def bagian_b(n=1000, seed=7):
    rng = random.Random(seed)
    karir = list(eng.peta.keys())
    distribusi = ["A"] * 3 + ["A-", "B+"] * 2 + ["B"] * 3 + ["B-", "C+", "C"] * 2 + ["D"] * 2 + ["E"] * 2
    total_mk, total_pel, kasus_terblokir = 0, 0, 0
    for _ in range(n):
        sem = rng.choice([5, 6, 7])
        tr = {}
        for k, m in net.mk.items():
            if m["jenis"] == "wajib" and m["semester"] < sem and rng.random() > 0.03:
                tr[k] = rng.choice(distribusi)
        pem = rng.choice(["SIA", "PSI", "DTA"])
        for s in range(5, sem):
            for k in rng.sample(net.pilihan(pem, s), SLOT_PILIHAN[s]):
                tr[k] = rng.choice(distribusi[:-2])
        kem = {b: rng.choice([0, 1, 2]) for b in ("python", "sql", "java")}
        h = eng.rekomendasi(rng.choice(karir), tr, sem, kem)
        p = pilihan(h)
        total_mk += len(p)
        total_pel += len(verifikasi(net, h, tr))
        if any("prasyarat belum terpenuhi" in w for w in h["peringatan"]):
            kasus_terblokir += 1
    kepatuhan = 100 * (1 - total_pel / total_mk) if total_mk else 100
    print(f"Bagian B: {n} profil acak, {total_mk} MK pilihan direkomendasikan, "
          f"{total_pel} pelanggaran prasyarat, kepatuhan {kepatuhan:.2f}%; "
          f"{kasus_terblokir} profil memiliki MK prioritas yang terblokir prasyarat")
    with open(os.path.join(OUT, "hasil_uji_acak.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["jumlah_profil", "mk_pilihan_direkomendasikan", "pelanggaran_prasyarat",
                    "kepatuhan_persen", "profil_dengan_mk_prioritas_terblokir"])
        w.writerow([n, total_mk, total_pel, round(kepatuhan, 2), kasus_terblokir])
    return total_pel


if __name__ == "__main__":
    a_ok, a_n = bagian_a()
    pel = bagian_b()
    sys.exit(0 if (a_ok == a_n and pel == 0) else 1)
