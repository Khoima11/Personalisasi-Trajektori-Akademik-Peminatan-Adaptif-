"""
Eksperimen klasifikasi peran karir dengan C4.5.
Jalankan dari root repo:  python src/experiment.py
"""
import json
import os
import sys
import warnings

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_recall_fscore_support)
from sklearn.model_selection import RepeatedStratifiedKFold, StratifiedKFold

sys.path.insert(0, os.path.dirname(__file__))
from c45 import C45  # noqa: E402

warnings.filterwarnings("ignore")
RAW = "data/raw/cs_students.csv"
OUT_DATA = "data/processed"
OUT_MODEL = "models"
OUT_DOCS = "docs"
LEVEL = {"Weak": 0, "Average": 1, "Strong": 2}
MIN_PER_CLASS = 6


# ---------------- 1. Praproses ----------------
def preprocess():
    raw = pd.read_csv(RAW)
    log = {"baris_awal": len(raw), "karir_awal": raw["Future Career"].nunique()}
    vc = raw["Future Career"].value_counts()
    keep = vc[vc >= MIN_PER_CLASS].index
    df = raw[raw["Future Career"].isin(keep)].copy()
    log["baris_setelah_filter_kelas"] = len(df)
    log["karir_dipakai"] = sorted(keep.tolist())

    # Seleksi fitur: atribut identitas & demografis dibuang (ID, Nama, Gender, Usia),
    # Major konstan, Projects teks bebas berkardinalitas tinggi.
    df = df[["Interested Domain", "GPA", "Python", "SQL", "Java", "Future Career"]].copy()
    df.columns = ["minat", "ipk", "python", "sql", "java", "karir"]
    for s in ["python", "sql", "java"]:
        df[s + "_ord"] = df[s].map(LEVEL)              # representasi ordinal (capaian)
        df[s + "_bin"] = (df[s] != "Weak").astype(int)  # representasi biner (pembanding)
    full = df.copy()
    dedup = df.drop_duplicates(subset=["minat", "ipk", "python", "sql", "java", "karir"])
    log["duplikat_dihapus"] = len(df) - len(dedup)
    log["baris_final"] = len(dedup)
    log["distribusi_kelas"] = dedup["karir"].value_counts().to_dict()
    os.makedirs(OUT_DATA, exist_ok=True)
    dedup.to_csv(f"{OUT_DATA}/dataset_bersih.csv", index=False)
    return full, dedup, log


SKENARIO = {
    "E1 Minat saja": ([], ["minat"]),
    "E2 Skill ordinal + IPK": (["ipk", "python_ord", "sql_ord", "java_ord"], []),
    "E3 Skill biner + minat": (["python_bin", "sql_bin", "java_bin"], ["minat"]),
    "E4 Usulan: minat + skill ordinal + IPK": (["ipk", "python_ord", "sql_ord", "java_ord"], ["minat"]),
    "E5 Usulan + pre-pruning (min_samples_split=8)": (["ipk", "python_ord", "sql_ord", "java_ord"], ["minat"]),
}
PRUNE = {"E5 Usulan + pre-pruning (min_samples_split=8)": 8}
FINAL = "E5 Usulan + pre-pruning (min_samples_split=8)"


def evaluate(df, num, cat, n_repeats=10, seed=42, mss=2):
    X = df[num + cat].to_dict("records")
    y = df["karir"].tolist()
    rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=n_repeats, random_state=seed)
    accs, ps, rs, fs = [], [], [], []
    for tr, te in rskf.split(np.zeros(len(y)), y):
        m = C45(num, cat, min_samples_split=mss).fit([X[i] for i in tr], [y[i] for i in tr])
        pred = m.predict([X[i] for i in te])
        true = [y[i] for i in te]
        accs.append(accuracy_score(true, pred))
        p, r, f, _ = precision_recall_fscore_support(true, pred, average="macro", zero_division=0)
        ps.append(p); rs.append(r); fs.append(f)
    return {"accuracy": np.mean(accs), "accuracy_sd": np.std(accs), "precision_macro": np.mean(ps),
            "recall_macro": np.mean(rs), "f1_macro": np.mean(fs)}


def main():
    full, df, log = preprocess()
    hasil = []
    for nama, (num, cat) in SKENARIO.items():
        mss = PRUNE.get(nama, 2)
        r = evaluate(df, num, cat, mss=mss)
        r_dup = evaluate(full, num, cat, n_repeats=3, mss=mss)
        hasil.append({"skenario": nama, **{k: round(v, 4) for k, v in r.items()},
                      "accuracy_dengan_duplikat": round(r_dup["accuracy"], 4)})
    tabel = pd.DataFrame(hasil)
    os.makedirs(OUT_DOCS, exist_ok=True)
    tabel.to_csv(f"{OUT_DOCS}/hasil_eksperimen.csv", index=False)

    # Confusion matrix & laporan per kelas untuk model usulan (5-fold, 1 kali)
    num, cat = SKENARIO[FINAL]
    mss = PRUNE[FINAL]
    X = df[num + cat].to_dict("records"); y = df["karir"].tolist()
    pred = [None] * len(y)
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=42).split(np.zeros(len(y)), y):
        m = C45(num, cat, min_samples_split=mss).fit([X[i] for i in tr], [y[i] for i in tr])
        for i, p in zip(te, m.predict([X[i] for i in te])):
            pred[i] = p
    labels = sorted(set(y))
    cm = pd.DataFrame(confusion_matrix(y, pred, labels=labels), index=labels, columns=labels)
    cm.to_csv(f"{OUT_DOCS}/confusion_matrix.csv")
    p, r, f, s = precision_recall_fscore_support(y, pred, labels=labels, zero_division=0)
    per_kelas = pd.DataFrame({"karir": labels, "precision": p.round(3), "recall": r.round(3),
                              "f1": f.round(3), "support": s})
    per_kelas.to_csv(f"{OUT_DOCS}/metrik_per_kelas.csv", index=False)

    # Model final dilatih dengan seluruh data bersih
    final = C45(num, cat, min_samples_split=mss).fit(X, y)
    os.makedirs(OUT_MODEL, exist_ok=True)
    final.to_json(f"{OUT_MODEL}/c45_karir.json")
    rules = final.rules()
    with open(f"{OUT_MODEL}/aturan_if_then.json", "w", encoding="utf-8") as fh:
        json.dump(rules, fh, indent=2, ensure_ascii=False)
    log["model_final"] = {"kedalaman": final.depth(), "jumlah_daun_aturan": final.n_leaves(),
                          "atribut_akar": final.tree.get("attr")}
    with open(f"{OUT_DOCS}/log_praproses.json", "w", encoding="utf-8") as fh:
        json.dump(log, fh, indent=2, ensure_ascii=False)

    print(json.dumps(log, indent=2, ensure_ascii=False))
    print(tabel.to_string(index=False))
    print(per_kelas.to_string(index=False))
    print(cm.to_string())


if __name__ == "__main__":
    main()
