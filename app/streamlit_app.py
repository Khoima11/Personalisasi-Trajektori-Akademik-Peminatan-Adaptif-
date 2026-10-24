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

WARNA_PEMINATAN = {"SIA": "#FF7EA2", "PSI": "#C5F04A", "DTA": "#6D4AFF"}
TEKS_PEMINATAN = {"SIA": "#111111", "PSI": "#111111", "DTA": "#FFFFFF"}
LABEL_DUKUNGAN = {"kuat": "Didukung kuat kurikulum", "sedang": "Didukung sebagian kurikulum",
                  "lemah": "Dukungan kurikulum terbatas"}
IKON_STATUS = {"LAYAK": "&#10003;", "BERSYARAT": "!", "TIDAK_LAYAK": "&#10005;"}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
:root { --hitam:#111111; --kertas:#F3F1EC; --putih:#FFFFFF; --lime:#C5F04A; --pink:#FF7EA2; --ungu:#6D4AFF;
  --abu:#5A5A5A; --garis-grid:#E2DED5; --bayang:4px 4px 0 #111111; }

/* ---------- tipografi dasar: satu keluarga sans + mono untuk kode ---------- */
html, body, p, li, label, input, textarea, button, h1, h2, h3, h4, h5, h6, summary,
.stMarkdown, [data-testid="stWidgetLabel"], [data-testid="stCaptionContainer"] {
  font-family:'Space Grotesk', 'Segoe UI', system-ui, sans-serif !important; }
.stMarkdown p, .stMarkdown li { font-size:1rem; line-height:1.6; color:var(--hitam); }
[data-testid="stCaptionContainer"] p { font-size:0.9rem !important; line-height:1.5; color:var(--abu) !important; }
[data-testid="stWidgetLabel"] p { font-weight:600 !important; font-size:0.95rem !important; color:var(--hitam) !important; }

/* ---------- latar kertas berpetak ---------- */
[data-testid="stAppViewContainer"] { background-color:var(--kertas);
  background-image:linear-gradient(var(--garis-grid) 1px, transparent 1px),
  linear-gradient(90deg, var(--garis-grid) 1px, transparent 1px); background-size:32px 32px; }
[data-testid="stHeader"] { background:transparent; }
.block-container { max-width:1180px; padding-top:2.2rem; }

/* ---------- panel samping ---------- */
[data-testid="stSidebar"] { background:var(--putih); border-right:3px solid var(--hitam); }
.nb-side-judul { background:var(--lime); border:3px solid var(--hitam); box-shadow:var(--bayang); padding:0.55rem 0.8rem;
  font-weight:700; font-size:1.05rem; margin:0.2rem 0 1rem 0; color:var(--hitam); }
.nb-side-sub { font-weight:700; font-size:1rem; color:var(--hitam); border-bottom:3px solid var(--hitam);
  padding-bottom:0.25rem; margin:1.4rem 0 0.7rem 0; }

/* ---------- komponen bawaan Streamlit ---------- */
div[data-baseweb="select"] > div, div[data-baseweb="input"], [data-testid="stNumberInput"] > div > div {
  border:2px solid var(--hitam) !important; border-radius:0 !important; background:var(--putih) !important; }
.stButton > button, .stDownloadButton > button {
  border:3px solid var(--hitam) !important; border-radius:0 !important; box-shadow:var(--bayang);
  background:var(--lime) !important; color:var(--hitam) !important; font-weight:700 !important;
  padding:0.6rem 1.1rem; transition:transform .08s ease, box-shadow .08s ease; }
.stButton > button p, .stDownloadButton > button p { font-weight:700 !important; font-size:1rem !important; }
.stButton > button:hover, .stDownloadButton > button:hover { transform:translate(2px,2px); box-shadow:2px 2px 0 var(--hitam); }
.stButton > button:focus-visible, .stDownloadButton > button:focus-visible { outline:3px solid var(--ungu); outline-offset:3px; }
[data-testid="stExpander"] details { border:2px solid var(--hitam) !important; border-radius:0 !important;
  background:var(--putih); box-shadow:3px 3px 0 var(--hitam); }
[data-testid="stExpander"] summary p { font-weight:600 !important; }
.stTabs [data-baseweb="tab-list"] { gap:0.6rem; border-bottom:none; }
.stTabs [data-baseweb="tab"] { border:3px solid var(--hitam); background:var(--putih); padding:0.5rem 1rem;
  border-radius:0; box-shadow:3px 3px 0 var(--hitam); height:auto; }
.stTabs [data-baseweb="tab"] p { font-weight:700 !important; font-size:0.98rem !important; }
.stTabs [aria-selected="true"] { background:var(--ungu) !important; }
.stTabs [aria-selected="true"] p { color:var(--putih) !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display:none; }

/* ---------- panel dan teks ---------- */
.nb-panel { background:var(--putih); border:3px solid var(--hitam); box-shadow:var(--bayang); padding:1.3rem 1.4rem; margin-bottom:1.4rem; }
.nb-h { font-weight:700; font-size:1.45rem; color:var(--hitam); margin:1.6rem 0 0.9rem 0; letter-spacing:0.01em; }
.nb-p { font-size:1rem; line-height:1.6; color:var(--hitam); margin:0 0 0.6rem 0; max-width:68ch; }
.nb-kecil { font-size:0.9rem; line-height:1.5; color:var(--abu); margin:0; }
.nb-badge { display:inline-block; font-weight:700; font-size:0.9rem; padding:0.3rem 0.65rem; border:2px solid var(--hitam); }

/* ---------- hero ---------- */
.nb-hero { display:grid; grid-template-columns:1.15fr 1fr; border:3px solid var(--hitam); box-shadow:6px 6px 0 var(--hitam);
  background:var(--putih); margin-bottom:1.6rem; }
.nb-hero-kiri { padding:2rem 1.8rem; background-color:var(--putih);
  background-image:linear-gradient(#ECE9E2 1px, transparent 1px), linear-gradient(90deg, #ECE9E2 1px, transparent 1px);
  background-size:22px 22px; }
.nb-hero-kanan { background:var(--pink); border-left:3px solid var(--hitam); padding:2rem 1.6rem; display:flex; align-items:center; }
.nb-wordmark { font-weight:700; font-size:clamp(2.8rem, 6vw, 4.4rem); line-height:0.95; color:var(--hitam); margin:0.9rem 0 0.7rem 0; }
.nb-karir { font-weight:700; font-size:clamp(2rem, 4.4vw, 3.1rem); line-height:1.02; color:var(--hitam); margin:0.9rem 0 0.35rem 0; }
.nb-sub { font-size:1.15rem; color:var(--hitam); margin:0 0 1rem 0; font-weight:500; }
.nb-kode { background:var(--ungu); color:var(--putih); border:3px solid var(--hitam); box-shadow:var(--bayang);
  padding:1.1rem 1.2rem; font-family:'Space Mono', Consolas, monospace; font-size:0.92rem; line-height:1.75; width:100%; }
.nb-kode .k { color:var(--lime); }
.nb-kode .s { color:#FFD3E0; }
.nb-kode .c { color:#CFC4FF; }

/* ---------- strip profil karir ---------- */
.nb-strip { display:grid; grid-template-columns:150px repeat(4, 1fr); border:3px solid var(--hitam); background:var(--putih);
  box-shadow:var(--bayang); margin-bottom:1.6rem; }
.nb-strip-label { background:var(--ungu); color:var(--putih); font-weight:700; font-size:1.1rem; padding:1rem; display:flex; align-items:center;
  border-right:3px solid var(--hitam); }
.nb-strip-sel { padding:0.9rem 1rem; border-right:2px solid var(--hitam); }
.nb-strip-sel:last-child { border-right:none; }
.nb-strip-sel .t { font-size:0.85rem; color:var(--abu); font-weight:600; margin:0 0 0.25rem 0; }
.nb-strip-sel .v { font-size:1rem; color:var(--hitam); font-weight:600; line-height:1.45; margin:0; }

/* ---------- peta jalur studi ---------- */
.nb-rute { display:grid; grid-template-columns:repeat(var(--kolom), 1fr); gap:1.3rem; position:relative; padding-top:2.2rem; }
.nb-rute::before { content:""; position:absolute; top:0.75rem; left:0.5rem; right:0.5rem; height:10px; background:var(--warna);
  border:3px solid var(--hitam); }
.nb-halte { position:relative; min-width:0; }
.nb-titik { position:absolute; top:-1.95rem; left:0; width:26px; height:26px; background:var(--putih); border:3px solid var(--hitam); z-index:1; }
.nb-sem { background:var(--hitam); color:var(--putih); padding:0.6rem 0.8rem; display:flex; justify-content:space-between; align-items:baseline; }
.nb-sem b { font-size:1.1rem; }
.nb-sem span { font-size:0.9rem; color:#DDDDDD; }
.nb-mk { list-style:none; padding:0; margin:0.8rem 0 0 0; }
.nb-mk li { border:2px solid var(--hitam); background:var(--kertas); padding:0.55rem 0.75rem; margin-bottom:0.6rem; }
.nb-mk li.pil { background:var(--putih); border-width:3px; box-shadow:var(--bayang); border-top:10px solid var(--warna); padding:0.75rem 0.85rem; margin-bottom:0.95rem; }
.nb-mk .nm { display:block; font-weight:600; font-size:0.97rem; line-height:1.35; color:var(--hitam); }
.nb-mk li.pil .nm { font-weight:700; font-size:1.05rem; }
.nb-mk .al { display:block; font-size:0.86rem; color:var(--abu); margin-top:0.25rem; line-height:1.4; }
.nb-st { display:inline-block; margin-top:0.45rem; font-size:0.8rem; font-weight:700; padding:0.1rem 0.5rem; border:2px solid var(--hitam); }
.nb-st.LAYAK { background:var(--lime); color:var(--hitam); }
.nb-st.BERSYARAT { background:var(--putih); color:var(--hitam); border-style:dashed; }
.nb-st.TIDAK_LAYAK { background:var(--hitam); color:var(--putih); }
.nb-legenda { display:flex; flex-wrap:wrap; gap:0.6rem 1.2rem; margin:0.4rem 0 0 0; align-items:center; }

/* ---------- catatan dan peringatan ---------- */
.nb-catatan { border:3px solid var(--hitam); background:var(--putih); box-shadow:var(--bayang); padding:1rem 1.2rem;
  border-left:12px solid var(--ungu); margin-bottom:1.4rem; }
.nb-awas { border:3px solid var(--hitam); background:var(--pink); box-shadow:var(--bayang); padding:1.1rem 1.3rem; margin:0.4rem 0 1.4rem 0; }
.nb-awas ul { margin:0.4rem 0 0 1.1rem; padding:0; }
.nb-awas li { margin-bottom:0.45rem; line-height:1.55; color:var(--hitam); }

/* ---------- langkah awal ---------- */
.nb-langkah { display:grid; grid-template-columns:repeat(3, 1fr); gap:1.2rem; margin-bottom:1.4rem; }
.nb-langkah div { background:var(--putih); border:3px solid var(--hitam); box-shadow:var(--bayang); padding:1rem 1.1rem; }
.nb-langkah .no { display:inline-block; background:var(--lime); border:2px solid var(--hitam); font-weight:700; padding:0 0.5rem; margin-bottom:0.5rem; }

.nb-kaki { background:var(--hitam); color:var(--putih); padding:0.8rem 1rem; margin-top:2rem; font-size:0.9rem; }

@media (max-width: 820px) {
  .nb-hero { grid-template-columns:1fr; }
  .nb-hero-kanan { border-left:none; border-top:3px solid var(--hitam); }
  .nb-strip { grid-template-columns:1fr; }
  .nb-strip-label, .nb-strip-sel { border-right:none; border-bottom:2px solid var(--hitam); }
  .nb-rute { grid-template-columns:1fr; padding-top:0; padding-left:2.4rem; }
  .nb-rute::before { top:0.3rem; bottom:0.3rem; left:0.4rem; right:auto; width:10px; height:auto; }
  .nb-titik { top:0.35rem; left:-2.4rem; }
  .nb-langkah { grid-template-columns:1fr; }
}
@media (prefers-reduced-motion: reduce) { .stButton > button { transition:none; } }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def lebar_penuh(fungsi, *args, **kwargs):
    """Kompatibel dengan Streamlit lama (use_container_width) dan baru (width="stretch")."""
    try:
        return fungsi(*args, width="stretch", **kwargs)
    except TypeError:
        return fungsi(*args, use_container_width=True, **kwargs)


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BERKAS_SISTEM = [os.path.join(ROOT, "src", "c45.py"), os.path.join(ROOT, "src", "engine.py"),
                 os.path.join(ROOT, "app", "logic.py"), os.path.join(ROOT, "models", "c45_karir.json")]
BERKAS_SISTEM += [os.path.join(ROOT, "data", "kurikulum", f) for f in sorted(os.listdir(os.path.join(ROOT, "data", "kurikulum")))]


def versi_sistem():
    """Penanda versi dari waktu ubah berkas inti; berubah setiap kali kode atau data diperbarui."""
    return tuple(round(os.path.getmtime(p), 3) for p in BERKAS_SISTEM if os.path.exists(p))


@st.cache_resource
def muat(versi):
    """Memuat ulang modul inti agar pembaruan engine atau data langsung terpakai tanpa reboot."""
    import importlib

    import c45
    import engine
    import logic
    for modul in (c45, engine, logic):
        importlib.reload(modul)
    return logic.Navika()


nv = muat(versi_sistem())
e = html.escape

# ======================================================================
# Panel input
# ======================================================================
with st.sidebar:
    st.markdown('<div class="nb-side-judul">&#129517; Data Anda</div>', unsafe_allow_html=True)
    semester = st.radio("Semester yang akan Anda tempuh", [5, 6, 7], horizontal=True,
                        format_func=lambda s: f"Semester {s}", key="semester")

    st.markdown('<div class="nb-side-sub">Minat dan kemampuan</div>', unsafe_allow_html=True)
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

    st.markdown('<div class="nb-side-sub">Nilai mata kuliah</div>', unsafe_allow_html=True)
    st.caption("Isi nilai mata kuliah yang menjadi prasyarat atau pendukung karir. "
               "Mata kuliah wajib lainnya dianggap sudah lulus.")
    nilai_wajib = {}
    daftar = nv.mk_ringkas(semester)
    for s in sorted({nv.net.mk[k]["semester"] for k in daftar}):
        with st.expander(f"Semester {s}", expanded=False):
            for k in [k for k in daftar if nv.net.mk[k]["semester"] == s]:
                nilai_wajib[k] = st.selectbox(nv.net.mk[k]["nama"], PILIHAN_NILAI,
                                              index=PILIHAN_NILAI.index("B"), key=f"nilai_{k}")

    nilai_pilihan = {}
    if semester >= 6:
        st.markdown('<div class="nb-side-sub">Mata kuliah pilihan yang sudah diambil</div>', unsafe_allow_html=True)
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
                dipilih = st.multiselect("Mata kuliah pilihan semester 6 (maksimal 2)", sem6,
                                         format_func=lambda k: nv.net.mk[k]["nama"], max_selections=2,
                                         key=f"pil6_{pem}")
                for k in dipilih:
                    nilai_pilihan[k] = st.selectbox(f"Nilai {nv.net.mk[k]['nama']}", PILIHAN_NILAI[:-1],
                                                    index=PILIHAN_NILAI.index("B"), key=f"pil_{k}")

    st.write("")
    if lebar_penuh(st.button, "Susun rekomendasi", type="primary"):
        st.session_state["aktif"] = True
    if st.session_state.get("aktif"):
        st.caption("Rekomendasi diperbarui otomatis setiap kali Anda mengubah data.")

# ======================================================================
# Proses
# ======================================================================
hasil, galat = None, None
if st.session_state.get("aktif"):
    profil = {"minat": minat, "ipk": ipk, "python": python_lv, "sql": sql_lv, "java": java_lv}
    try:
        hasil = nv.rekomendasi(profil, semester, nilai_wajib, nilai_pilihan)
    except ValueError as err:
        galat = str(err)


def kartu_kode(baris):
    """Kartu bergaya potongan kode (mengikuti tema referensi)."""
    return '<div class="nb-kode">' + "<br>".join(baris) + "</div>"


# ======================================================================
# Hero
# ======================================================================
if hasil is None:
    kode = kartu_kode([
        '<span class="k">&gt;</span> navika = {',
        '&nbsp;&nbsp;<span class="k">prediksi</span>: <span class="s">\'C4.5 pohon keputusan\'</span>,',
        '&nbsp;&nbsp;<span class="k">jalur</span>: <span class="s">\'semester 5 sampai 7\'</span>,',
        '&nbsp;&nbsp;<span class="k">validasi</span>: <span class="s">\'rantai prasyarat\'</span>,',
        '&nbsp;&nbsp;<span class="k">untuk</span>: <span class="s">\'mahasiswa S1 SI\'</span>',
        '}'])
    st.markdown(
        '<div class="nb-hero"><div class="nb-hero-kiri">'
        '<span class="nb-badge" style="background:var(--ungu);color:#fff">Halo, mahasiswa Sistem Informasi &#128075;</span>'
        '<div class="nb-wordmark">NAVIKA</div>'
        '<p class="nb-p" style="font-size:1.12rem;font-weight:500">Navigasi karir dan jalur studi. Temukan karir yang sesuai '
        'dengan minat dan kemampuan Anda, lalu lihat mata kuliah pilihan semester 5 sampai 7 yang aman diambil.</p>'
        f'</div><div class="nb-hero-kanan">{kode}</div></div>', unsafe_allow_html=True)
else:
    warna = WARNA_PEMINATAN[hasil["peminatan"]]
    baris = ['<span class="k">&gt;</span> jika {']
    for k, v in hasil["aturan_kv"]:
        baris.append(f'&nbsp;&nbsp;<span class="k">{e(k)}</span>: <span class="s">\'{e(v)}\'</span>,')
    baris.append(f'}} <span class="k">maka</span> <span class="s">\'{e(hasil["karir"])}\'</span>')
    rincian = ", ".join(f"{v} {k}" for k, v in hasil["daun"]["dist"].items())
    baris.append(f'<span class="c">// {hasil["daun"]["n"]} data latih serupa: {e(rincian)}</span>')
    st.markdown(
        '<div class="nb-hero"><div class="nb-hero-kiri">'
        '<span class="nb-badge" style="background:var(--ungu);color:#fff">Karir yang paling sesuai untuk Anda</span>'
        f'<div class="nb-karir">{e(hasil["karir"])}</div>'
        f'<p class="nb-sub">{e(hasil["karir_id"])}</p>'
        f'<span class="nb-badge" style="background:{warna};color:{TEKS_PEMINATAN[hasil["peminatan"]]}">Peminatan {hasil["peminatan"]}</span> '
        f'<span class="nb-badge" style="background:#fff">{e(LABEL_DUKUNGAN[hasil["dukungan_kurikulum"]])}</span>'
        '<p class="nb-p" style="margin-top:1rem;font-size:0.95rem"><b>Cara NAVIKA menentukan rekomendasi:</b> karir terutama ditentukan '
        'oleh minat Anda. Nilai mata kuliah menentukan mata kuliah yang aman diambil, dan kemampuan pemrograman ikut menentukan '
        'urutan prioritasnya. Kartu di samping menunjukkan aturan keputusan C4.5 untuk karir Anda.</p>'
        f'</div><div class="nb-hero-kanan">{kartu_kode(baris)}</div></div>', unsafe_allow_html=True)

if galat:
    st.markdown(f'<div class="nb-awas"><b>Data belum dapat diproses.</b><p class="nb-p">{e(galat)}</p></div>',
                unsafe_allow_html=True)

tab_rek, tab_rantai, tab_tentang = st.tabs(["Rekomendasi", "Rantai prasyarat", "Tentang NAVIKA"])

# ======================================================================
# Tab rekomendasi
# ======================================================================
with tab_rek:
    if hasil is None:
        st.markdown(
            '<div class="nb-h">Cara memakai NAVIKA</div><div class="nb-langkah">'
            '<div><span class="no">1</span><p class="nb-p">Isi minat, IPK, dan kemampuan pemrograman di panel kiri.</p></div>'
            '<div><span class="no">2</span><p class="nb-p">Periksa nilai mata kuliah. Nilai awal diisi B, sesuaikan dengan transkrip Anda.</p></div>'
            '<div><span class="no">3</span><p class="nb-p">Tekan <b>Susun rekomendasi</b> untuk melihat karir dan jalur studi Anda.</p></div>'
            '</div>', unsafe_allow_html=True)
        st.caption("Di ponsel, buka panel input lewat tombol panah di kiri atas layar.")
    else:
        warna = WARNA_PEMINATAN[hasil["peminatan"]]
        idx = hasil["kesiapan_akademik"]["indeks"]
        kesiapan = f"{idx:.2f} dari 4,00".replace(".", ",", 1) if idx is not None else "Belum ada nilai"
        tek = hasil.get("kesiapan_teknis")
        teknis_status = tek["status"] if tek else "-"
        teknis_rinci = ", ".join(f"{k}: {v}" for k, v in tek["rincian"].items()) if tek else ""
        st.markdown(
            '<div class="nb-strip"><div class="nb-strip-label">Profil karir</div>'
            f'<div class="nb-strip-sel"><p class="t">Peminatan</p><p class="v">{e(PEMINATAN[hasil["peminatan"]])}</p></div>'
            f'<div class="nb-strip-sel"><p class="t">Kompetensi yang dibangun</p><p class="v">{e("; ".join(hasil["kompetensi"]))}</p></div>'
            f'<div class="nb-strip-sel"><p class="t">Kesiapan akademik</p><p class="v">{kesiapan}</p>'
            f'<p class="nb-kecil">CPL terkait: {e(", ".join(hasil["cpl"]))}</p></div>'
            f'<div class="nb-strip-sel"><p class="t">Kesiapan teknis</p><p class="v">{e(teknis_status)}</p>'
            f'<p class="nb-kecil">{e(teknis_rinci)}</p></div></div>',
            unsafe_allow_html=True)

        if hasil.get("saran_pengembangan"):
            butir = "".join(f"<li>{e(x)}</li>" for x in hasil["saran_pengembangan"])
            st.markdown('<div class="nb-catatan" style="border-left-color:var(--lime)"><b>Saran pengembangan kemampuan</b>'
                        f'<ul style="margin:0.4rem 0 0 1.1rem;padding:0">{butir}</ul></div>', unsafe_allow_html=True)

        if hasil["catatan_karir"]:
            st.markdown(f'<div class="nb-catatan"><b>Catatan untuk karir ini</b><p class="nb-p">{e(hasil["catatan_karir"])}</p></div>',
                        unsafe_allow_html=True)
        if hasil["peminatan"] != hasil["peminatan_ideal"]:
            st.markdown(f'<div class="nb-catatan"><b>Peminatan berbeda</b><p class="nb-p">Karir ini paling sesuai dengan peminatan '
                        f'{hasil["peminatan_ideal"]}, tetapi peminatan Anda sudah {hasil["peminatan"]}. Rekomendasi tetap disusun '
                        'di peminatan Anda.</p></div>', unsafe_allow_html=True)

        # ---- peta jalur studi ----
        st.markdown(f'<div class="nb-h">Jalur studi semester {semester} sampai 7</div>', unsafe_allow_html=True)
        halte = []
        for t in hasil["trajektori"]:
            item = []
            for m in t["mata_kuliah"]:
                kelas = "pil" if m["jenis"] == "pilihan" else "wjb"
                alasan = f'<span class="al">{e(m["alasan"])}</span>' if m.get("alasan") else ""
                st_ = m["status_prasyarat"]
                item.append(f'<li class="{kelas}"><span class="nm">{e(m["nama"])}</span>{alasan}'
                            f'<span class="nb-st {st_}">{IKON_STATUS[st_]} {STATUS_LABEL[st_]}</span></li>')
            halte.append(f'<div class="nb-halte"><div class="nb-titik"></div>'
                         f'<div class="nb-sem"><b>Semester {t["semester"]}</b><span>{t["total_sks"]} SKS</span></div>'
                         f'<ul class="nb-mk">{"".join(item)}</ul></div>')
        st.markdown(f'<div class="nb-rute" style="--warna:{warna};--kolom:{len(halte)}">{"".join(halte)}</div>',
                    unsafe_allow_html=True)
        st.markdown(
            '<div class="nb-legenda">'
            f'<span class="nb-kecil"><b style="color:#111">Kartu bergaris warna</b>: mata kuliah pilihan yang direkomendasikan</span>'
            '<span class="nb-kecil"><b style="color:#111">Kartu polos</b>: mata kuliah wajib</span>'
            '<span class="nb-st BERSYARAT" style="margin:0">! Bersyarat</span>'
            '<span class="nb-kecil">prasyarat dijadwalkan di semester sebelumnya dan harus lulus</span></div>',
            unsafe_allow_html=True)

        if hasil["peringatan"]:
            butir = "".join(f"<li>{e(w)}</li>" for w in hasil["peringatan"])
            st.markdown(f'<div class="nb-h">Perlu perhatian</div><div class="nb-awas"><ul>{butir}</ul></div>',
                        unsafe_allow_html=True)

        st.markdown('<div class="nb-h">Rincian prasyarat</div>', unsafe_allow_html=True)
        for t in hasil["trajektori"]:
            with st.expander(f"Semester {t['semester']}"):
                for m in t["mata_kuliah"]:
                    st.markdown(f"**{m['nama']}** ({m['jenis']}, {m['sks']} SKS): {STATUS_LABEL[m['status_prasyarat']]}")
                    if m["detail_prasyarat"]:
                        for d in m["detail_prasyarat"]:
                            st.markdown(f"- {d['keterangan']}")
                    else:
                        st.markdown("- Tidak memiliki prasyarat")

        st.write("")
        st.download_button("Unduh rencana studi (CSV)", data=nv.ke_csv(hasil),
                           file_name=f"rencana_studi_navika_semester{semester}.csv", mime="text/csv")

# ======================================================================
# Tab rantai prasyarat
# ======================================================================
with tab_rantai:
    st.markdown('<div class="nb-h">Telusuri rantai prasyarat</div>', unsafe_allow_html=True)
    st.caption("Pilih mata kuliah untuk melihat semua mata kuliah yang harus lulus sebelumnya. "
               "Garis tegas berasal dari dokumen kurikulum, garis putus-putus adalah asumsi berbasis materi.")
    punya = sorted([k for k in nv.net.mk if nv.net.rantai(k)],
                   key=lambda k: (nv.net.mk[k]["semester"], nv.net.mk[k]["nama"]))
    awal = 0
    if hasil:
        rek = [m["kode"] for t in hasil["trajektori"] for m in t["mata_kuliah"]
               if m["jenis"] == "pilihan" and m["kode"] in punya]
        if rek:
            awal = punya.index(rek[-1])
    kode_mk = st.selectbox("Mata kuliah", punya, index=awal,
                           format_func=lambda k: f"{nv.net.mk[k]['nama']} (semester {nv.net.mk[k]['semester']})")
    lebar_penuh(st.graphviz_chart, nv.rantai_dot(kode_mk))
    st.caption(f"{nv.net.mk[kode_mk]['nama']} memiliki {len(nv.net.rantai(kode_mk))} mata kuliah dalam rantai prasyaratnya. "
               "Warna: putih wajib, pink SIA, hijau PSI, ungu DTA.")

# ======================================================================
# Tab tentang
# ======================================================================
with tab_tentang:
    st.markdown(
        '<div class="nb-h">Apa yang dilakukan NAVIKA</div><div class="nb-panel">'
        '<p class="nb-p">NAVIKA membantu mahasiswa S1 Sistem Informasi menentukan arah karir dan menyusun rencana '
        'mata kuliah pilihan semester 5 sampai 7. Sistem bekerja dalam dua langkah.</p>'
        '<p class="nb-p"><b>1. Prediksi karir.</b> Algoritma pohon keputusan C4.5 memprediksi karir dari minat, IPK, '
        'dan kemampuan pemrograman. Setiap prediksi disertai aturan keputusan yang dapat dibaca.</p>'
        '<p class="nb-p"><b>2. Penyusunan jalur studi.</b> Engine trajektori memodelkan kurikulum sebagai jaringan prasyarat, '
        'memilih kombinasi mata kuliah pilihan dalam satu peminatan yang paling relevan dengan karir, dan hanya '
        'merekomendasikan mata kuliah yang rantai prasyaratnya terpenuhi.</p>'
        '<p class="nb-p"><b>3. Penyesuaian kemampuan.</b> Jika kemampuan pemrograman yang relevan dengan suatu mata kuliah '
        'bernilai Baik, mata kuliah itu dapat naik satu peringkat prioritas. Kemampuan juga dipakai untuk menilai kesiapan teknis '
        'dan memberi saran pengembangan. Pemetaan kemampuan ke karir dan mata kuliah merupakan asumsi peneliti.</p></div>'
        '<div class="nb-h">Kinerja dan pengujian</div><div class="nb-panel">'
        '<p class="nb-p">Model C4.5 mencapai akurasi 84,0% dan F1-macro 73,8% (stratified 5-fold cross validation, '
        'diulang 10 kali) dengan 14 aturan keputusan untuk 12 peran karir.</p>'
        '<p class="nb-p">Engine trajektori lolos 18 dari 18 skenario uji dan tidak menghasilkan pelanggaran prasyarat '
        'pada uji 1.000 profil acak.</p></div>'
        '<div class="nb-h">Keterbatasan</div><div class="nb-panel">'
        '<p class="nb-p">Model dilatih dengan data sekunder (Kaggle) berukuran kecil dan berlatar Computer Science, '
        'dengan rentang IPK data latih 3,20 sampai 3,90. Peran khas Sistem Informasi seperti Business Analyst belum tercakup.</p>'
        '<p class="nb-p">Prasyarat mata kuliah pilihan tidak tercantum di dokumen kurikulum, sehingga disusun berdasarkan '
        'keterkaitan materi. Mata kuliah wajib yang tidak ditanyakan dianggap sudah lulus.</p>'
        '<p class="nb-p"><b>Rekomendasi NAVIKA bersifat pendukung keputusan.</b> Diskusikan rencana studi Anda dengan '
        'dosen pembimbing akademik.</p></div>', unsafe_allow_html=True)

st.markdown('<div class="nb-kaki">NAVIKA: sistem pendukung keputusan karir dan jalur studi mahasiswa S1 Sistem Informasi.</div>',
            unsafe_allow_html=True)
