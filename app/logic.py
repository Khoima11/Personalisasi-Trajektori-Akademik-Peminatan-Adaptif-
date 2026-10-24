"""
Logika aplikasi NAVIKA yang terpisah dari tampilan Streamlit, sehingga dapat diuji tanpa antarmuka.
"""
from __future__ import annotations

import csv
import io
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

from c45 import C45  # noqa: E402
from engine import (NILAI_DIASUMSIKAN_LULUS, SKALA_NILAI, SLOT_PILIHAN,  # noqa: E402
                    CurriculumNetwork, TrajectoryEngine)

PATH_MODEL = os.path.join(ROOT, "models", "c45_karir.json")

MINAT = {
    "Data Science": "Sains Data",
    "Data Mining": "Penambangan Data",
    "Machine Learning": "Machine Learning",
    "Artificial Intelligence": "Kecerdasan Buatan (AI)",
    "Database Management": "Manajemen Basis Data",
    "Web Development": "Pengembangan Web",
    "Mobile App Development": "Pengembangan Aplikasi Mobile",
    "Software Development": "Pengembangan Perangkat Lunak",
    "Software Engineering": "Rekayasa Perangkat Lunak",
    "Cloud Computing": "Komputasi Awan (Cloud)",
    "Cybersecurity": "Keamanan Siber",
    "Computer Graphics": "Grafika Komputer",
}
KEMAMPUAN = {0: "Kurang", 1: "Cukup", 2: "Baik"}
PILIHAN_NILAI = ["A", "A-", "B+", "B", "B-", "C+", "C", "D", "E", "Belum diambil"]
# Deskripsi singkat peminatan (bukan nama resmi; ganti dengan nama resmi prodi bila tersedia)
PEMINATAN = {"SIA": "SIA: manajemen dan tata kelola SI",
             "PSI": "PSI: pengembangan sistem dan aplikasi",
             "DTA": "DTA: data dan analitik"}
STATUS_LABEL = {"LAYAK": "Layak", "BERSYARAT": "Bersyarat", "TIDAK_LAYAK": "Tidak layak"}


class Navika:
    def __init__(self):
        self.net = CurriculumNetwork()
        self.engine = TrajectoryEngine(self.net)
        self.model = C45.from_json(PATH_MODEL)
        pendukung = {k for v in self.engine.peta.values() for k in v["mk_wajib_pendukung"]}
        prasyarat_wajib = {r["prasyarat"] for rows in self.net.prasyarat.values() for r in rows
                           if self.net.mk[r["prasyarat"]]["jenis"] == "wajib"}
        self.mk_ditanyakan = pendukung | prasyarat_wajib

    # ---------- input ringkas ----------
    def mk_ringkas(self, semester_sekarang):
        """MK wajib yang ditanyakan nilainya: prasyarat atau pendukung karir yang sudah ditempuh."""
        daftar = [k for k in self.mk_ditanyakan if self.net.mk[k]["semester"] < semester_sekarang]
        return sorted(daftar, key=lambda k: (self.net.mk[k]["semester"], self.net.mk[k]["nama"]))

    def pilihan_semester(self, peminatan, semester):
        return sorted(self.net.pilihan(peminatan, semester), key=lambda k: self.net.mk[k]["nama"])

    def susun_transkrip(self, semester_sekarang, nilai_wajib, nilai_pilihan):
        """
        nilai_wajib: {kode: nilai atau 'Belum diambil'} untuk MK yang ditanyakan.
        nilai_pilihan: {kode: nilai} untuk MK pilihan yang sudah diambil.
        MK wajib lain yang sudah lewat semesternya diasumsikan lulus.
        """
        tr = {}
        for k, m in self.net.mk.items():
            if m["jenis"] == "wajib" and m["semester"] < semester_sekarang:
                if k in self.mk_ditanyakan:
                    v = nilai_wajib.get(k, "B")
                    if v != "Belum diambil":
                        tr[k] = v
                else:
                    tr[k] = NILAI_DIASUMSIKAN_LULUS
        for k, v in nilai_pilihan.items():
            if v != "Belum diambil":
                tr[k] = v
        return tr

    # ---------- proses utama ----------
    def rekomendasi(self, profil, semester_sekarang, nilai_wajib, nilai_pilihan):
        baris = {"minat": profil["minat"], "ipk": float(profil["ipk"]),
                 "python_ord": int(profil["python"]), "sql_ord": int(profil["sql"]),
                 "java_ord": int(profil["java"])}
        karir, jalur = self.model.predict_one(baris, return_path=True)
        daun = self.model.predict_leaf(baris)
        transkrip = self.susun_transkrip(semester_sekarang, nilai_wajib, nilai_pilihan)
        hasil = self.engine.rekomendasi(karir, transkrip, semester_sekarang)
        hasil["aturan"] = [self.terjemah_kondisi(c) for c in jalur]
        hasil["daun"] = {"n": daun["n"], "dist": dict(sorted(daun["dist"].items(), key=lambda x: -x[1]))}
        hasil["transkrip"] = transkrip
        return hasil

    # ---------- penjelasan ----------
    @staticmethod
    def terjemah_kondisi(c):
        m = re.match(r"(\w+) (<=|>|=) (.+)", c)
        if not m:
            return c
        attr, op, val = m.groups()
        if attr == "minat":
            v = val.split(" (")[0]
            return f"Minat: {MINAT.get(v, v)}"
        if attr == "ipk":
            angka = f"{float(val):.2f}".replace(".", ",")
            return f"IPK {'di atas' if op == '>' else 'paling tinggi'} {angka}"
        nama = {"python_ord": "Python", "sql_ord": "SQL", "java_ord": "Java"}.get(attr, attr)
        t = float(val)
        if op == "<=":
            lv = [KEMAMPUAN[i] for i in range(3) if i <= t]
        else:
            lv = [KEMAMPUAN[i] for i in range(3) if i > t]
        return f"Kemampuan {nama}: {' atau '.join(lv)}"

    def rantai_dot(self, kode):
        """Graf rantai prasyarat suatu MK dalam format DOT (untuk st.graphviz_chart)."""
        simpul = self.net.rantai(kode) | {kode}
        warna = {"wajib": "#E3EAF0", "SIA": "#F6D58E", "PSI": "#A8E0BC", "DTA": "#A9CDF0"}
        baris = ['digraph G {', 'rankdir=LR; bgcolor="transparent";',
                 'node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, color="#5B7083"];',
                 'edge [color="#5B7083"];']
        for n in sorted(simpul, key=lambda x: self.net.mk[x]["semester"]):
            m = self.net.mk[n]
            w = warna["wajib"] if m["jenis"] == "wajib" else warna[m["peminatan"]]
            tebal = ', penwidth=2.2' if n == kode else ''
            baris.append(f'"{n}" [label="{m["nama"]}\\nSemester {m["semester"]}", fillcolor="{w}"{tebal}];')
        for u, v, d in self.net.graf.edges(data=True):
            if u in simpul and v in simpul:
                gaya = "solid" if d["sumber"] == "dokumen" else "dashed"
                baris.append(f'"{u}" -> "{v}" [style={gaya}, label=" min. {d["nilai_minimal"]}", fontsize=9];')
        baris.append("}")
        return "\n".join(baris)

    @staticmethod
    def ke_csv(hasil):
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["semester", "kode", "mata_kuliah", "sks", "jenis", "status_prasyarat", "alasan"])
        for t in hasil["trajektori"]:
            for m in t["mata_kuliah"]:
                w.writerow([t["semester"], m["kode"], m["nama"], m["sks"], m["jenis"],
                            STATUS_LABEL[m["status_prasyarat"]], m.get("alasan", "")])
        return buf.getvalue().encode("utf-8-sig")


__all__ = ["Navika", "MINAT", "KEMAMPUAN", "PILIHAN_NILAI", "PEMINATAN", "STATUS_LABEL",
           "SKALA_NILAI", "SLOT_PILIHAN"]
