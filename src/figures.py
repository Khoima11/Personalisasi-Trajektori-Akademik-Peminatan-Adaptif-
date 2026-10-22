"""Membuat gambar hasil eksperimen untuk laporan. Jalankan: python src/figures.py"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

plt.style.use("seaborn-v0_8-whitegrid")

# 1. Perbandingan skenario fitur
t = pd.read_csv("docs/hasil_eksperimen.csv")
t["label"] = t["skenario"].str.replace(r" \(min_samples_split=8\)", "", regex=True)
fig, ax = plt.subplots(figsize=(10, 5))
y = range(len(t))
ax.barh([i + 0.2 for i in y], t["accuracy"] * 100, height=0.4, label="Accuracy", color="#2b6cb0")
ax.barh([i - 0.2 for i in y], t["f1_macro"] * 100, height=0.4, label="F1-macro", color="#9bbbe0")
for i, (a, f) in enumerate(zip(t["accuracy"], t["f1_macro"])):
    ax.text(a * 100 + 1, i + 0.2, f"{a*100:.1f}%", va="center", fontsize=9)
    ax.text(f * 100 + 1, i - 0.2, f"{f*100:.1f}%", va="center", fontsize=9)
ax.set_yticks(list(y)); ax.set_yticklabels(t["label"]); ax.invert_yaxis()
ax.set_xlim(0, 105); ax.set_xlabel("Persentase (5-fold CV, 10 kali ulang, data tanpa duplikat)")
ax.set_title("Minat menjadi penentu utama; skill dan IPK saja tidak cukup", fontsize=13, fontweight="bold")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)
for s in ["top", "right"]: ax.spines[s].set_visible(False)
plt.tight_layout(); plt.savefig("docs/figures/perbandingan_skenario_fitur.png", dpi=150, bbox_inches="tight")

# 2. Confusion matrix model final
cm = pd.read_csv("docs/confusion_matrix.csv", index_col=0)
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax, linewidths=0.5)
ax.set_xlabel("Prediksi"); ax.set_ylabel("Aktual")
ax.set_title("Confusion matrix C4.5 (model usulan): kesalahan terpusat pada pasangan karir dengan minat sama",
             fontsize=11, fontweight="bold")
plt.xticks(rotation=45, ha="right"); plt.tight_layout()
plt.savefig("docs/figures/confusion_matrix.png", dpi=150, bbox_inches="tight")
print("ok")
