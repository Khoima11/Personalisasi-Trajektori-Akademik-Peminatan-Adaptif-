"""
Engine Inferensi Trajektori Kurikulum (Curriculum Prerequisite Network).

Alur:
  1. Kurikulum dimodelkan sebagai graf berarah asiklik (DAG):
     simpul = mata kuliah, sisi = prasyarat -> mata kuliah.
  2. Peran karir (keluaran C4.5) dipetakan ke peminatan dan prioritas mata kuliah pilihan.
  3. Semua kombinasi mata kuliah pilihan semester 5-7 dalam satu peminatan
     dienumerasi, lalu disaring dengan validasi rantai prasyarat
     (forward chaining: prasyarat harus sudah lulus di transkrip dengan nilai
     minimal, atau dijadwalkan di semester sebelumnya pada rencana).
  4. Rencana yang lolos validasi diberi skor berdasarkan prioritas karir;
     rencana dengan skor tertinggi menjadi rekomendasi.

Engine bersifat adaptif: setiap kali transkrip (nilai) atau target karir berubah,
rekomendasi dihitung ulang dari kondisi terbaru mahasiswa.
"""
from __future__ import annotations

import csv
import itertools
import json
import os

import networkx as nx

BASE = os.path.join(os.path.dirname(__file__), "..")
DIR_KUR = os.path.join(BASE, "data", "kurikulum")

SKALA_NILAI = {"A": 4.0, "A-": 3.75, "B+": 3.5, "B": 3.0, "B-": 2.75,
               "C+": 2.5, "C": 2.0, "D": 1.0, "E": 0.0}
SLOT_PILIHAN = {5: 1, 6: 2, 7: 2}
BOBOT_PRIORITAS = [3, 2, 1]  # peringkat 1, 2, 3 pada daftar prioritas karir


def lulus(nilai, minimal):
    return nilai in SKALA_NILAI and SKALA_NILAI[nilai] >= SKALA_NILAI[minimal]


# ======================================================================
# 1. Curriculum Prerequisite Network
# ======================================================================
class CurriculumNetwork:
    def __init__(self, dir_kurikulum=DIR_KUR):
        self.mk = {}
        with open(os.path.join(dir_kurikulum, "kurikulum_acuan.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                r["sks"] = int(r["sks"]); r["semester"] = int(r["semester"])
                self.mk[r["kode"]] = r
        self.prasyarat = {}
        with open(os.path.join(dir_kurikulum, "prasyarat.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                self.prasyarat.setdefault(r["kode"], []).append(r)
        self.graf = nx.DiGraph()
        for k, m in self.mk.items():
            self.graf.add_node(k, **m)
        for k, rows in self.prasyarat.items():
            for r in rows:
                self.graf.add_edge(r["prasyarat"], k, nilai_minimal=r["nilai_minimal"], sumber=r["sumber"])
        self.validasi_integritas()

    def validasi_integritas(self):
        """Memastikan graf kurikulum konsisten sebelum dipakai."""
        masalah = []
        for k, rows in self.prasyarat.items():
            for r in rows:
                if k not in self.mk or r["prasyarat"] not in self.mk:
                    masalah.append(f"Kode tidak dikenal: {k} <- {r['prasyarat']}")
                elif self.mk[r["prasyarat"]]["semester"] >= self.mk[k]["semester"]:
                    masalah.append(f"Prasyarat {r['prasyarat']} tidak berada di semester lebih awal dari {k}")
        if not nx.is_directed_acyclic_graph(self.graf):
            masalah.append("Graf prasyarat mengandung siklus")
        if masalah:
            raise ValueError("Kurikulum tidak valid:\n" + "\n".join(masalah))
        return True

    def prasyarat_dari(self, kode):
        return self.prasyarat.get(kode, [])

    def rantai(self, kode):
        """Seluruh leluhur (rantai prasyarat berjenjang) suatu mata kuliah."""
        return nx.ancestors(self.graf, kode)

    def pilihan(self, peminatan, semester):
        return [k for k, m in self.mk.items()
                if m["jenis"] == "pilihan" and m["peminatan"] == peminatan and m["semester"] == semester]

    def wajib(self, semester):
        return [k for k, m in self.mk.items() if m["jenis"] == "wajib" and m["semester"] == semester]


# ======================================================================
# 2. Engine trajektori
# ======================================================================
class TrajectoryEngine:
    def __init__(self, net=None, path_peta=os.path.join(DIR_KUR, "peta_karir.json")):
        self.net = net or CurriculumNetwork()
        with open(path_peta, encoding="utf-8") as f:
            self.peta = json.load(f)["karir"]

    # ---- status prasyarat satu mata kuliah ----
    def _cek(self, kode, semester, transkrip, rencana_sem):
        """rencana_sem: {kode: semester} untuk mata kuliah yang dijadwalkan."""
        hasil = []
        for p in self.net.prasyarat_dari(kode):
            pk, minimal = p["prasyarat"], p["nilai_minimal"]
            nama = self.net.mk[pk]["nama"]
            if pk in transkrip and lulus(transkrip[pk], minimal):
                hasil.append({"prasyarat": pk, "nama": nama, "status": "lulus",
                              "keterangan": f"{nama} lulus dengan nilai {transkrip[pk]} (minimal {minimal})"})
            elif pk in rencana_sem and rencana_sem[pk] < semester:
                hasil.append({"prasyarat": pk, "nama": nama, "status": "direncanakan",
                              "keterangan": f"{nama} dijadwalkan di semester {rencana_sem[pk]}, harus lulus minimal {minimal}"})
            else:
                if pk in transkrip:
                    ket = f"{nama} bernilai {transkrip[pk]}, di bawah minimal {minimal}; perlu mengulang"
                else:
                    ket = f"{nama} belum ditempuh"
                hasil.append({"prasyarat": pk, "nama": nama, "status": "belum_terpenuhi", "keterangan": ket})
        if not hasil:
            status = "LAYAK"
        elif any(h["status"] == "belum_terpenuhi" for h in hasil):
            status = "TIDAK_LAYAK"
        elif any(h["status"] == "direncanakan" for h in hasil):
            status = "BERSYARAT"
        else:
            status = "LAYAK"
        return status, hasil

    def _peminatan_terkunci(self, transkrip):
        pem = {self.net.mk[k]["peminatan"] for k in transkrip
               if k in self.net.mk and self.net.mk[k]["jenis"] == "pilihan"}
        return pem

    # ---- rekomendasi utama ----
    def rekomendasi(self, karir, transkrip, semester_sekarang=5):
        if karir not in self.peta:
            raise ValueError(f"Karir tidak dikenal: {karir}")
        if semester_sekarang not in (5, 6, 7):
            raise ValueError("semester_sekarang harus 5, 6, atau 7")
        info = self.peta[karir]
        peringatan = []

        # 1) Tentukan peminatan (aturan: satu peminatan saja)
        pem_transkrip = self._peminatan_terkunci(transkrip)
        if len(pem_transkrip) > 1:
            raise ValueError(f"Transkrip berisi mata kuliah pilihan lintas peminatan: {sorted(pem_transkrip)}")
        if pem_transkrip:
            peminatan = pem_transkrip.pop()
            if peminatan != info["peminatan"]:
                peringatan.append(
                    f"Peminatan sudah terkunci ke {peminatan} karena mata kuliah pilihan yang telah diambil, "
                    f"sedangkan karir {karir} paling sesuai dengan peminatan {info['peminatan']}. "
                    "Rekomendasi tetap disusun di peminatan yang terkunci.")
        else:
            peminatan = info["peminatan"]
        prioritas = info["prioritas"] if peminatan == info["peminatan"] else {}

        semesters = list(range(semester_sekarang, 8))

        # 2) Mata kuliah wajib yang dijadwalkan + tunggakan semester sebelumnya
        rencana_wajib = {}
        for s in semesters:
            for k in self.net.wajib(s):
                if k not in transkrip:
                    rencana_wajib[k] = s
        for k, m in self.net.mk.items():
            if m["jenis"] == "wajib" and m["semester"] < semester_sekarang:
                if k not in transkrip:
                    peringatan.append(f"Mata kuliah wajib semester {m['semester']} belum tercatat: {m['nama']} ({k}).")
                elif transkrip[k] == "E":
                    peringatan.append(f"Mata kuliah wajib {m['nama']} ({k}) bernilai E; perlu diulang.")

        # 2b) Mata kuliah wajib terjadwal yang prasyaratnya tidak terpenuhi tidak boleh
        #     dihitung sebagai pemenuh prasyarat (validasi berantai)
        blok = set()
        for k, s in sorted(rencana_wajib.items(), key=lambda x: x[1]):
            valid = {kk: ss for kk, ss in rencana_wajib.items() if kk not in blok}
            if self._cek(k, s, transkrip, valid)[0] == "TIDAK_LAYAK":
                blok.add(k)

        # 3) Mata kuliah pilihan semester lalu yang seharusnya sudah diambil
        for s in range(5, semester_sekarang):
            diambil = [k for k in self.net.pilihan(peminatan, s) if k in transkrip]
            if len(diambil) < SLOT_PILIHAN[s]:
                peringatan.append(f"Jatah mata kuliah pilihan semester {s} belum terpenuhi "
                                  f"({len(diambil)} dari {SLOT_PILIHAN[s]}).")

        # 4) Enumerasi kombinasi pilihan per semester
        opsi_per_sem = []
        for s in semesters:
            kandidat = [k for k in self.net.pilihan(peminatan, s) if k not in transkrip]
            n = min(SLOT_PILIHAN[s], len(kandidat))
            kombinasi = [list(c) for c in itertools.combinations(kandidat, n)]
            # izinkan kombinasi lebih kecil jika kombinasi penuh tidak layak
            for kecil in range(n - 1, -1, -1):
                kombinasi += [list(c) for c in itertools.combinations(kandidat, kecil)]
            opsi_per_sem.append([(s, c) for c in kombinasi])

        def skor_mk(k, s):
            daftar = prioritas.get(str(s), [])
            return BOBOT_PRIORITAS[daftar.index(k)] if k in daftar else 1 if s == 5 else 0

        terbaik = None
        for plan in itertools.product(*opsi_per_sem):
            rencana_pilihan = {k: s for s, ks in plan for k in ks}
            rencana_sem = {**rencana_wajib, **rencana_pilihan}
            rencana_valid = {k: s for k, s in rencana_sem.items() if k not in blok}
            layak = all(self._cek(k, s, transkrip, rencana_valid)[0] != "TIDAK_LAYAK"
                        for k, s in rencana_pilihan.items())
            if not layak:
                continue
            jumlah = len(rencana_pilihan)
            skor = sum(skor_mk(k, s) for k, s in rencana_pilihan.items())
            kunci = (jumlah, skor, tuple(sorted(rencana_pilihan)))
            if terbaik is None or kunci[:2] > terbaik[0][:2]:
                terbaik = (kunci, rencana_pilihan, rencana_sem)

        _, rencana_pilihan, rencana_sem = terbaik
        rencana_valid = {k: s for k, s in rencana_sem.items() if k not in blok}

        # 5) Susun keluaran per semester
        trajektori = []
        for s in semesters:
            daftar = []
            for k in sorted([k for k, ss in rencana_sem.items() if ss == s],
                            key=lambda x: (self.net.mk[x]["jenis"] != "pilihan", x)):
                m = self.net.mk[k]
                status, detail = self._cek(k, s, transkrip, rencana_valid)
                item = {"kode": k, "nama": m["nama"], "sks": m["sks"], "jenis": m["jenis"],
                        "status_prasyarat": status, "detail_prasyarat": detail}
                if m["jenis"] == "pilihan":
                    daftar_p = prioritas.get(str(s), [])
                    item["alasan"] = (f"Prioritas ke-{daftar_p.index(k) + 1} untuk karir {karir}"
                                      if k in daftar_p else f"Mata kuliah pilihan peminatan {peminatan}")
                if status == "TIDAK_LAYAK":
                    peringatan.append(f"{m['nama']} (wajib, semester {s}) belum memenuhi prasyarat: "
                                      + "; ".join(d["keterangan"] for d in detail if d["status"] == "belum_terpenuhi"))
                daftar.append(item)
            n_pil = sum(1 for d in daftar if d["jenis"] == "pilihan")
            if n_pil < SLOT_PILIHAN[s]:
                peringatan.append(f"Semester {s}: hanya {n_pil} dari {SLOT_PILIHAN[s]} mata kuliah pilihan yang layak "
                                  "direkomendasikan karena prasyarat belum terpenuhi.")
            trajektori.append({"semester": s, "mata_kuliah": daftar,
                               "total_sks": sum(d["sks"] for d in daftar)})

        # 5b) Jelaskan mata kuliah prioritas karir yang terpaksa tidak direkomendasikan
        for s in semesters:
            for i, k in enumerate(prioritas.get(str(s), [])):
                if k in rencana_sem or k in transkrip:
                    continue
                status, detail = self._cek(k, s, transkrip, rencana_valid)
                if status == "TIDAK_LAYAK" and i < SLOT_PILIHAN[s]:
                    sebab = "; ".join(d["keterangan"] for d in detail if d["status"] == "belum_terpenuhi")
                    peringatan.append(f"{self.net.mk[k]['nama']} (prioritas ke-{i + 1} untuk {karir}, semester {s}) "
                                      f"tidak direkomendasikan karena prasyarat belum terpenuhi: {sebab}.")

        # 6) Kesiapan akademik dari nilai mata kuliah wajib pendukung karir
        nilai_pendukung = {k: transkrip[k] for k in info["mk_wajib_pendukung"]
                           if k in transkrip and transkrip[k] in SKALA_NILAI}
        kesiapan = (round(sum(SKALA_NILAI[v] for v in nilai_pendukung.values()) / len(nilai_pendukung), 2)
                    if nilai_pendukung else None)

        return {
            "karir": karir, "karir_id": info["nama_id"], "peminatan": peminatan,
            "peminatan_ideal": info["peminatan"], "dukungan_kurikulum": info["dukungan"],
            "catatan_karir": info["catatan"], "cpl": info["cpl"], "kompetensi": info["kompetensi"],
            "kesiapan_akademik": {"indeks": kesiapan, "dasar": {
                k: {"nama": self.net.mk[k]["nama"], "nilai": v} for k, v in nilai_pendukung.items()}},
            "trajektori": trajektori, "peringatan": peringatan,
        }


# ======================================================================
# 3. Verifikasi independen (dipakai untuk pengujian kepatuhan prasyarat)
# ======================================================================
def verifikasi(net, hasil, transkrip):
    """Mengembalikan daftar pelanggaran prasyarat pada mata kuliah PILIHAN yang direkomendasikan."""
    jadwal = {m["kode"]: t["semester"] for t in hasil["trajektori"] for m in t["mata_kuliah"]
              if m["status_prasyarat"] != "TIDAK_LAYAK"}
    pelanggaran = []
    pem = set()
    for t in hasil["trajektori"]:
        for m in t["mata_kuliah"]:
            if m["jenis"] != "pilihan":
                continue
            pem.add(net.mk[m["kode"]]["peminatan"])
            for p in net.prasyarat_dari(m["kode"]):
                ok_transkrip = p["prasyarat"] in transkrip and lulus(transkrip[p["prasyarat"]], p["nilai_minimal"])
                ok_rencana = p["prasyarat"] in jadwal and jadwal[p["prasyarat"]] < t["semester"]
                if not (ok_transkrip or ok_rencana):
                    pelanggaran.append((m["kode"], p["prasyarat"]))
    pem |= {net.mk[k]["peminatan"] for k in transkrip if k in net.mk and net.mk[k]["jenis"] == "pilihan"}
    if len(pem) > 1:
        pelanggaran.append(("lintas_peminatan", ",".join(sorted(pem))))
    return pelanggaran


# ======================================================================
# 4. Integrasi C4.5 -> engine (alur IDSS lengkap)
# ======================================================================
def rekomendasi_lengkap(profil, transkrip, semester_sekarang=5,
                        path_model=os.path.join(BASE, "models", "c45_karir.json")):
    """profil: {'minat': str, 'ipk': float, 'python_ord': 0-2, 'sql_ord': 0-2, 'java_ord': 0-2}"""
    import sys
    sys.path.insert(0, os.path.dirname(__file__))
    from c45 import C45
    model = C45.from_json(path_model)
    karir, jalur = model.predict_one(profil, return_path=True)
    hasil = TrajectoryEngine().rekomendasi(karir, transkrip, semester_sekarang)
    hasil["penjelasan_prediksi"] = "JIKA " + " DAN ".join(jalur) + f" MAKA {karir}"
    return hasil
