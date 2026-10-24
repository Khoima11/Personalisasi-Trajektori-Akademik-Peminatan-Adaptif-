"""
NAVIKA: Navigasi Karir dan Akademik
Intelligent Decision Support System rekomendasi karir dan mata kuliah pilihan
untuk mahasiswa S1 Sistem Informasi.

Jalankan dari root repositori:  streamlit run app/streamlit_app.py
"""
import html
import os
import sys

import streamlit as st

sys.path.insert(0, os.path.dirname(__file__))
from logic import (KEMAMPUAN, MINAT, PEMINATAN, PILIHAN_NILAI, STATUS_LABEL,  # noqa: E402
                   Navika)

st.set_page_config(page_title="NAVIKA: Navigasi Karir dan Akademik", page_icon="🧭",
                   layout="wide", initial_sidebar_state="expanded")

WARNA_PEMINATAN = {"SIA": "#B7791F", "PSI": "#2F855A", "DTA": "#2B6CB0"}
LABEL_DUKUNGAN = {"kuat": "Didukung kuat oleh kurikulum", "sedang": "Didukung sebagian oleh kurikulum",
                  "lemah": "Dukungan kurikulum terbatas"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
:root { --ink:#102A43; --muted:#52667A; --paper:#FFFFFF; --rule:#D5E0E8; --teal:#0B6E8A; }
h1, h2, h3, h4, p, li, label, .stMarkdown, .nv { font-family:'Plus Jakarta Sans', system-ui, sans-serif; }
.nv-wordmark { font-weight:800; font-size:clamp(2.2rem, 5vw, 3.4rem); letter-spacing:0.14em; color:var(--ink);
  line-height:1; margin:0.2rem 0 0.35rem 0; }
.nv-tagline { color:var(--muted); font-size:1.02rem; margin-bottom:1.2rem; max-width:60ch; }
.nv-kecil { color:var(--muted); font-size:0.9rem; margin:0; }
.nv-karir { font-weight:800; font-size:clamp(1.9rem, 4.2vw, 2.9rem); color:var(--ink); line-height:1.08; margin:0.15rem 0 0.1rem 0; }
.nv-karir-id { font-size:1.1rem; color:var(--muted); margin-bottom:0.8rem; }
.nv-chip { display:inline-block; padding:0.28rem 0.7rem; margin:0 0.35rem 0.4rem 0; border-radius:999px;
  background:#EAF2F6; color:var(--ink); font-size:0.9rem; font-weight:600; border:1px solid #C9DCE6; }
.nv-plus { color:var(--muted); margin-right:0.35rem; font-weight:700; }
.nv-garis-pem { height:6px; border-radius:3px; margin:0.4rem 0 1rem 0; }
/* peta rute jalur studi */
.nv-rute { display:flex; gap:1.2rem; position:relative; padding-top:1.4rem; margin:0.6rem 0 1.4rem 0; }
.nv-rute::before { content:""; position:absolute; top:calc(1.4rem + 9px); left:9px; right:9px; height:6px;
  border-radius:3px; background:var(--warna); }
.nv-halte { flex:1 1 0; min-width:0; position:relative; }
.nv-titik { width:24px; height:24px; border-radius:50%; background:#fff; border:6px solid var(--warna);
  position:relative; z-index:1; margin-bottom:0.7rem; box-sizing:border-box; }
.nv-sem { font-weight:800; font-size:1.15rem; color:var(--ink); margin:0; }
.nv-sks { color:var(--muted); font-size:0.86rem; margin:0 0 0.7rem 0; }
.nv-mk { list-style:none; padding:0; margin:0; }
.nv-mk li { background:var(--paper); border:1px solid var(--rule); border-radius:10px; padding:0.55rem 0.7rem;
  margin-bottom:0.5rem; color:var(--ink); }
.nv-mk li.pil { border-left:6px solid var(--warna); }
.nv-mk li.wjb { background:#F6F9FB; font-size:0.88rem; padding:0.4rem 0.7rem; }
.nv-mk .nm { font-weight:700; display:block; }
.nv-mk .al { color:var(--muted); font-size:0.82rem; display:block; margin-top:0.15rem; }
.nv-st { display:inline-block; font-size:0.74rem; font-weight:700; border-radius:999px; padding:0.08rem 0.5rem;
  margin-top:0.3rem; }
.nv-st.LAYAK { background:#E3F3E8; color:#22543D; }
.nv-st.BERSYARAT { background:#FCF0D5; color:#7B4A0C; }
.nv-st.TIDAK_LAYAK { background:#FBE2E2; color:#822727; }
@media (max-width: 760px) {
  .nv-rute { flex-direction:column; padding-top:0; padding-left:2.2rem; }
  .nv-rute::before { top:9px; bottom:9px; left:9px; right:auto; width:6px; height:auto; }
  .nv-titik { position:absolute; left:-2.2rem; top:0; }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def lebar_penuh(fungsi, *args, **kwargs):
    """Kompatibel dengan Streamlit lama (use_container_width) dan baru (width="stretch")."""
    try:
        return fungsi(*args, width="stretch", **kwargs)
    except TypeError:
        return fungsi(*args, use_container_width=True, **kwargs)


@st.cache_resource
def muat():
    return Navika()


nv = muat()
e = html.escape

# ======================================================================
# Panel input
# ======================================================================
with st.sidebar:
    st.markdown("### Data Anda")
    semester = st.radio("Semester yang akan Anda tempuh", [5, 6, 7], horizontal=True,
                        format_func=lambda s: f"Semester {s}", key="semester")

    st.markdown("#### Minat dan kemampuan")
    minat = st.selectbox("Bidang yang paling Anda minati", list(MINAT.keys()),
                         format_func=lambda k: MINAT[k], key="minat")
    ipk = st.number_input("IPK saat ini", min_value=0.0, max_value=4.0, value=3.50, step=0.01,
                          format="%.2f", key="ipk")
    python_lv = st.select_slider("Kemampuan Python", options=[0, 1, 2], value=1,
                                 format_func=lambda v: KEMAMPUAN[v], key="python")
    sql_lv = st.select_slider("Kemampuan SQL", options=[0, 1, 2], value=1,
                              format_func=lambda v: KEMAMPUAN[v], key="sql")
    java_lv = st.select_slider("Kemampuan Java", options=[0, 1, 2], value=1,
                               format_func=lambda v: KEMAMPUAN[v], key="java")

    st.markdown("#### Nilai mata kuliah")
    st.caption("Hanya mata kuliah yang menjadi prasyarat atau pendukung karir yang ditanyakan. "
               "Mata kuliah wajib lain dianggap sudah lulus.")
    nilai_wajib = {}
    daftar = nv.mk_ringkas(semester)
    for s in sorted({nv.net.mk[k]["semester"] for k in daftar}):
        with st.expander(f"Semester {s}", expanded=False):
            for k in [k for k in daftar if nv.net.mk[k]["semester"] == s]:
                nilai_wajib[k] = st.selectbox(nv.net.mk[k]["nama"], PILIHAN_NILAI,
                                              index=PILIHAN_NILAI.index("B"), key=f"nilai_{k}")

    nilai_pilihan = {}
    if semester >= 6:
        st.markdown("#### Mata kuliah pilihan yang sudah diambil")
        opsi = ["-"] + list(PEMINATAN.keys())
        pem = st.selectbox("Peminatan yang sudah Anda jalani", opsi,
                           format_func=lambda k: "Belum mengambil mata kuliah pilihan" if k == "-" else PEMINATAN[k],
                           key="pem_diambil")
        if pem != "-":
            for k in nv.pilihan_semester(pem, 5):
                nilai_pilihan[k] = st.selectbox(f"{nv.net.mk[k]['nama']} (semester 5)", PILIHAN_NILAI,
                                                index=PILIHAN_NILAI.index("B"), key=f"pil_{k}")
            if semester == 7:
                sem6 = nv.pilihan_semester(pem, 6)
                dipilih = st.multiselect("Mata kuliah pilihan semester 6 yang diambil (maksimal 2)", sem6,
                                         format_func=lambda k: nv.net.mk[k]["nama"], max_selections=2,
                                         key=f"pil6_{pem}")
                for k in dipilih:
                    nilai_pilihan[k] = st.selectbox(f"Nilai {nv.net.mk[k]['nama']}", PILIHAN_NILAI[:-1],
                                                    index=PILIHAN_NILAI.index("B"), key=f"pil_{k}")

    st.divider()
    if lebar_penuh(st.button, "Susun rekomendasi", type="primary"):
        st.session_state["aktif"] = True
    if st.session_state.get("aktif"):
        st.caption("Rekomendasi diperbarui otomatis setiap kali Anda mengubah data di atas.")

# ======================================================================
# Area utama
# ======================================================================
st.markdown('<div class="nv nv-wordmark">NAVIKA</div>'
            '<div class="nv nv-tagline">Navigasi karir dan jalur studi untuk mahasiswa S1 Sistem Informasi: '
            'temukan karir yang sesuai, lalu lihat mata kuliah pilihan semester 5 sampai 7 yang aman diambil.</div>',
            unsafe_allow_html=True)

tab_rek, tab_rantai, tab_tentang = st.tabs(["Rekomendasi", "Rantai prasyarat", "Tentang NAVIKA"])

hasil = None
if st.session_state.get("aktif"):
    profil = {"minat": minat, "ipk": ipk, "python": python_lv, "sql": sql_lv, "java": java_lv}
    try:
        hasil = nv.rekomendasi(profil, semester, nilai_wajib, nilai_pilihan)
    except ValueError as err:
        st.error(f"Data belum dapat diproses: {err}")

with tab_rek:
    if hasil is None:
        st.markdown("#### Cara memakai NAVIKA")
        st.markdown(
            "1. Isi minat, IPK, dan kemampuan pemrograman di panel kiri.\n"
            "2. Periksa nilai mata kuliah yang ditanyakan. Nilai awal diisi B, ubah sesuai transkrip Anda.\n"
            "3. Pilih **Susun rekomendasi** untuk melihat karir yang sesuai dan jalur studi semester 5 sampai 7.")
        st.caption("Di perangkat seluler, buka panel input melalui tombol panah di kiri atas layar.")
    else:
        warna = WARNA_PEMINATAN[hasil["peminatan"]]
        kiri, kanan = st.columns([3, 2], gap="large")
        with kiri:
            st.markdown(
                f'<p class="nv nv-kecil">Karir yang paling sesuai dengan profil Anda</p>'
                f'<div class="nv nv-karir">{e(hasil["karir"])}</div>'
                f'<div class="nv nv-karir-id">{e(hasil["karir_id"])} &nbsp;|&nbsp; '
                f'{e(LABEL_DUKUNGAN[hasil["dukungan_kurikulum"]])}</div>',
                unsafe_allow_html=True)
            chips = '<span class="nv-plus">+</span>'.join(f'<span class="nv-chip">{e(a)}</span>' for a in hasil["aturan"])
            st.markdown(f'<p class="nv nv-kecil" style="margin-bottom:0.35rem">Aturan keputusan C4.5 yang terpenuhi</p>{chips}',
                        unsafe_allow_html=True)
            dist = hasil["daun"]["dist"]
            rincian = ", ".join(f"{v} {k}" for k, v in dist.items())
            st.caption(f"Dari {hasil['daun']['n']} data latih dengan pola yang sama: {rincian}.")
        with kanan:
            st.markdown(f"**Peminatan:** {PEMINATAN[hasil['peminatan']]}")
            st.markdown("**Kompetensi yang dibangun:** " + "; ".join(hasil["kompetensi"]))
            st.markdown("**CPL terkait:** " + ", ".join(hasil["cpl"]))
            idx = hasil["kesiapan_akademik"]["indeks"]
            if idx is not None:
                st.markdown(f"**Kesiapan akademik:** {idx:.2f} dari 4,00".replace(".", ",", 1)
                            + "  \n<span class='nv-kecil'>Rata-rata nilai mata kuliah wajib pendukung karir ini</span>",
                            unsafe_allow_html=True)
        if hasil["catatan_karir"]:
            st.info(hasil["catatan_karir"])
        if hasil["peminatan"] != hasil["peminatan_ideal"]:
            st.warning(f"Karir ini paling sesuai dengan peminatan {hasil['peminatan_ideal']}, "
                       f"tetapi peminatan Anda sudah {hasil['peminatan']}.")

        # ---- peta rute jalur studi ----
        st.markdown(f"#### Jalur studi semester {semester} sampai 7")
        halte = []
        for t in hasil["trajektori"]:
            item = []
            for m in t["mata_kuliah"]:
                kelas = "pil" if m["jenis"] == "pilihan" else "wjb"
                alasan = f'<span class="al">{e(m["alasan"])}</span>' if m.get("alasan") else ""
                item.append(f'<li class="{kelas}"><span class="nm">{e(m["nama"])}</span>{alasan}'
                            f'<span class="nv-st {m["status_prasyarat"]}">{STATUS_LABEL[m["status_prasyarat"]]}</span></li>')
            halte.append(f'<div class="nv-halte"><div class="nv-titik"></div>'
                         f'<p class="nv nv-sem">Semester {t["semester"]}</p>'
                         f'<p class="nv nv-sks">{t["total_sks"]} SKS</p><ul class="nv nv-mk">{"".join(item)}</ul></div>')
        st.markdown(f'<div class="nv-rute" style="--warna:{warna}">{"".join(halte)}</div>', unsafe_allow_html=True)
        st.caption("Kartu bergaris warna adalah mata kuliah pilihan yang direkomendasikan; kartu abu-abu adalah mata kuliah wajib. "
                   "Bersyarat berarti prasyaratnya dijadwalkan di semester sebelumnya dan harus lulus dengan nilai minimal.")

        if hasil["peringatan"]:
            st.markdown("#### Perlu perhatian")
            for w in hasil["peringatan"]:
                st.warning(w)

        st.markdown("#### Rincian prasyarat")
        for t in hasil["trajektori"]:
            with st.expander(f"Semester {t['semester']}"):
                for m in t["mata_kuliah"]:
                    st.markdown(f"**{m['nama']}** ({m['jenis']}, {m['sks']} SKS): {STATUS_LABEL[m['status_prasyarat']]}")
                    if m["detail_prasyarat"]:
                        for d in m["detail_prasyarat"]:
                            st.markdown(f"- {d['keterangan']}")
                    else:
                        st.markdown("- Tidak memiliki prasyarat")

        st.download_button("Unduh rencana studi (CSV)", data=nv.ke_csv(hasil),
                           file_name=f"rencana_studi_navika_semester{semester}.csv", mime="text/csv")

with tab_rantai:
    st.markdown("#### Telusuri rantai prasyarat")
    st.caption("Pilih mata kuliah untuk melihat seluruh mata kuliah yang harus lulus sebelumnya. "
               "Garis tegas berasal dari dokumen kurikulum; garis putus-putus adalah asumsi berbasis materi.")
    punya = sorted([k for k in nv.net.mk if nv.net.rantai(k)],
                   key=lambda k: (nv.net.mk[k]["semester"], nv.net.mk[k]["nama"]))
    awal = 0
    if hasil:
        rek = [m["kode"] for t in hasil["trajektori"] for m in t["mata_kuliah"] if m["jenis"] == "pilihan" and m["kode"] in punya]
        if rek:
            awal = punya.index(rek[-1])
    kode = st.selectbox("Mata kuliah", punya, index=awal,
                        format_func=lambda k: f"{nv.net.mk[k]['nama']} (semester {nv.net.mk[k]['semester']})")
    lebar_penuh(st.graphviz_chart, nv.rantai_dot(kode))
    n_rantai = len(nv.net.rantai(kode))
    st.caption(f"{nv.net.mk[kode]['nama']} memiliki {n_rantai} mata kuliah dalam rantai prasyaratnya.")

with tab_tentang:
    st.markdown("#### Apa yang dilakukan NAVIKA")
    st.markdown(
        "NAVIKA membantu mahasiswa S1 Sistem Informasi menentukan arah karir dan menyusun rencana mata kuliah "
        "pilihan semester 5 sampai 7. Sistem bekerja dalam dua langkah:\n\n"
        "1. **Prediksi karir** dengan algoritma pohon keputusan C4.5 berdasarkan minat, IPK, dan kemampuan pemrograman. "
        "Setiap prediksi disertai aturan keputusan yang dapat dibaca.\n"
        "2. **Penyusunan jalur studi** oleh engine trajektori yang memodelkan kurikulum sebagai jaringan prasyarat. "
        "Engine memilih kombinasi mata kuliah pilihan dalam satu peminatan yang paling relevan dengan karir, "
        "dan hanya merekomendasikan mata kuliah yang rantai prasyaratnya terpenuhi.")
    st.markdown("#### Kinerja dan pengujian")
    st.markdown(
        "- Model C4.5: akurasi 84,0% dan F1-macro 73,8% (stratified 5-fold cross validation, diulang 10 kali), "
        "dengan 14 aturan keputusan untuk 12 peran karir.\n"
        "- Engine trajektori: 14 dari 14 skenario uji sesuai harapan, dan 0 pelanggaran prasyarat pada uji 1.000 profil acak.")
    st.markdown("#### Keterbatasan")
    st.markdown(
        "- Model dilatih dengan data sekunder (Kaggle) berukuran kecil dan berlatar Computer Science, "
        "dengan rentang IPK data latih 3,20 sampai 3,90.\n"
        "- Peran khas Sistem Informasi seperti Business Analyst belum tercakup.\n"
        "- Prasyarat mata kuliah pilihan tidak tercantum di dokumen kurikulum, sehingga disusun berdasarkan keterkaitan materi.\n"
        "- Mata kuliah wajib yang tidak ditanyakan dianggap sudah lulus.\n\n"
        "Rekomendasi NAVIKA bersifat pendukung keputusan. Diskusikan rencana studi Anda dengan dosen pembimbing akademik.")
