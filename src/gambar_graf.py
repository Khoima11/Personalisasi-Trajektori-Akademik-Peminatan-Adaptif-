"""Menggambar Curriculum Prerequisite Network. Jalankan: python src/gambar_graf.py"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

sys.path.insert(0, os.path.dirname(__file__))
from engine import CurriculumNetwork  # noqa: E402

net = CurriculumNetwork()
G = net.graf
terlibat = {n for e in G.edges for n in e} | {k for k, m in net.mk.items() if m["jenis"] == "pilihan"}
H = G.subgraph(terlibat).copy()

WARNA = {"wajib": "#cbd5e1", "SIA": "#f6ad55", "PSI": "#68d391", "DTA": "#63b3ed"}
urut_pem = {"": 0, "SIA": 1, "PSI": 2, "DTA": 3}
pos = {}
for s in range(1, 9):
    nodes = sorted([n for n in H if net.mk[n]["semester"] == s],
                   key=lambda n: (urut_pem[net.mk[n]["peminatan"]], n))
    for i, n in enumerate(nodes):
        pos[n] = (s * 3.2, -(i - (len(nodes) - 1) / 2) * 1.25)

fig, ax = plt.subplots(figsize=(20, 12))
dok = [(u, v) for u, v, d in H.edges(data=True) if d["sumber"] == "dokumen"]
asm = [(u, v) for u, v, d in H.edges(data=True) if d["sumber"] != "dokumen"]
nx.draw_networkx_edges(H, pos, edgelist=dok, ax=ax, edge_color="#334155", width=1.6, arrows=True,
                       arrowsize=14, node_size=2600, connectionstyle="arc3,rad=0.05")
nx.draw_networkx_edges(H, pos, edgelist=asm, ax=ax, edge_color="#64748b", width=1.2, style="dashed",
                       arrows=True, arrowsize=12, node_size=2600, connectionstyle="arc3,rad=0.05")
for n, (x, y) in pos.items():
    m = net.mk[n]
    warna = WARNA["wajib"] if m["jenis"] == "wajib" else WARNA[m["peminatan"]]
    ax.text(x, y, "\n".join(textwrap.wrap(m["nama"], 18)), ha="center", va="center", fontsize=7.5,
            bbox=dict(boxstyle="round,pad=0.35", fc=warna, ec="#475569", lw=0.8))
for s in range(1, 9):
    ax.text(s * 3.2, max(p[1] for p in pos.values()) + 1.4, f"Semester {s}", ha="center",
            fontsize=11, fontweight="bold")
ax.legend(handles=[Patch(fc=WARNA["wajib"], ec="#475569", label="Wajib"),
                   Patch(fc=WARNA["SIA"], ec="#475569", label="Pilihan SIA"),
                   Patch(fc=WARNA["PSI"], ec="#475569", label="Pilihan PSI"),
                   Patch(fc=WARNA["DTA"], ec="#475569", label="Pilihan DTA"),
                   Line2D([0], [0], color="#334155", lw=1.6, label="Prasyarat dari dokumen kurikulum"),
                   Line2D([0], [0], color="#64748b", lw=1.2, ls="--", label="Prasyarat asumsi berbasis materi")],
          loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=6, frameon=False, fontsize=10)
fig.suptitle("Curriculum Prerequisite Network S1 Sistem Informasi: rantai prasyarat hingga 5 tingkat", y=1.02,
                 fontsize=15, fontweight="bold")
ax.axis("off")
plt.tight_layout()
plt.savefig(os.path.join(os.path.dirname(__file__), "..", "docs", "figures", "graf_prasyarat.png"),
            dpi=150, bbox_inches="tight")
print("ok", H.number_of_nodes(), H.number_of_edges(), "rantai terpanjang", nx.dag_longest_path_length(G) + 1)
