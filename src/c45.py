"""
Implementasi Algoritma C4.5 (Quinlan, 1993) untuk klasifikasi peran karir.

Fitur utama yang membedakannya dari CART (scikit-learn):
- Kriteria pemisahan: Gain Ratio = Information Gain / Split Information
- Atribut kategorikal dipecah multi-cabang (satu cabang per nilai)
- Atribut numerik/ordinal dipecah biner dengan ambang (threshold) terbaik
- Heuristik Quinlan: gain ratio hanya dipertimbangkan untuk atribut
  dengan information gain >= rata-rata information gain semua kandidat
- Ekstraksi aturan IF-THEN untuk explainability
"""
from __future__ import annotations

import json
import math
from collections import Counter


def entropy(labels):
    n = len(labels)
    if n == 0:
        return 0.0
    return -sum((c / n) * math.log2(c / n) for c in Counter(labels).values())


def split_info(sizes, n):
    return -sum((s / n) * math.log2(s / n) for s in sizes if s > 0)


class C45:
    def __init__(self, numeric_attrs, categorical_attrs, min_samples_split=2,
                 min_gain=1e-6, max_depth=None):
        self.numeric_attrs = list(numeric_attrs)
        self.categorical_attrs = list(categorical_attrs)
        self.min_samples_split = min_samples_split
        self.min_gain = min_gain
        self.max_depth = max_depth
        self.tree = None

    # ---------- pelatihan ----------
    def fit(self, rows, labels):
        """rows: list of dict {atribut: nilai}; labels: list kelas."""
        self.classes_ = sorted(set(labels))
        self.tree = self._build(rows, labels, depth=0,
                                attrs=self.numeric_attrs + self.categorical_attrs)
        return self

    def _leaf(self, labels):
        cnt = Counter(labels)
        return {"leaf": True, "label": cnt.most_common(1)[0][0],
                "n": len(labels), "dist": dict(cnt)}

    def _candidates(self, rows, labels, attrs):
        base = entropy(labels)
        n = len(labels)
        cands = []
        for a in attrs:
            if a in self.categorical_attrs:
                groups = {}
                for r, y in zip(rows, labels):
                    groups.setdefault(r[a], []).append(y)
                if len(groups) < 2:
                    continue
                rem = sum(len(g) / n * entropy(g) for g in groups.values())
                gain = base - rem
                si = split_info([len(g) for g in groups.values()], n)
                cands.append({"attr": a, "type": "cat", "gain": gain,
                              "gr": gain / si if si > 0 else 0.0})
            else:
                vals = sorted(set(r[a] for r in rows))
                best = None
                for lo, hi in zip(vals[:-1], vals[1:]):
                    t = (lo + hi) / 2
                    left = [y for r, y in zip(rows, labels) if r[a] <= t]
                    right = [y for r, y in zip(rows, labels) if r[a] > t]
                    rem = len(left) / n * entropy(left) + len(right) / n * entropy(right)
                    gain = base - rem
                    if best is None or gain > best["gain"]:
                        si = split_info([len(left), len(right)], n)
                        best = {"attr": a, "type": "num", "thr": t, "gain": gain,
                                "gr": gain / si if si > 0 else 0.0}
                if best:
                    cands.append(best)
        return cands

    def _build(self, rows, labels, depth, attrs):
        if (len(set(labels)) == 1 or len(labels) < self.min_samples_split
                or (self.max_depth is not None and depth >= self.max_depth)):
            return self._leaf(labels)
        cands = [c for c in self._candidates(rows, labels, attrs) if c["gain"] > self.min_gain]
        if not cands:
            return self._leaf(labels)
        avg_gain = sum(c["gain"] for c in cands) / len(cands)
        pool = [c for c in cands if c["gain"] >= avg_gain - 1e-12]
        best = max(pool, key=lambda c: (c["gr"], c["gain"]))
        node = {"leaf": False, "attr": best["attr"], "type": best["type"],
                "gain": round(best["gain"], 4), "gain_ratio": round(best["gr"], 4),
                "n": len(labels), "majority": Counter(labels).most_common(1)[0][0],
                "children": {}}
        if best["type"] == "cat":
            node["children"] = {}
            groups = {}
            for r, y in zip(rows, labels):
                groups.setdefault(r[best["attr"]], ([], []))
                groups[r[best["attr"]]][0].append(r)
                groups[r[best["attr"]]][1].append(y)
            rest = [a for a in attrs if a != best["attr"]]  # kategorikal tidak dipakai ulang
            for v, (rs, ys) in groups.items():
                node["children"][str(v)] = self._build(rs, ys, depth + 1, rest)
        else:
            t = best["thr"]
            node["thr"] = t
            L = [(r, y) for r, y in zip(rows, labels) if r[best["attr"]] <= t]
            R = [(r, y) for r, y in zip(rows, labels) if r[best["attr"]] > t]
            node["children"]["<="] = self._build([r for r, _ in L], [y for _, y in L], depth + 1, attrs)
            node["children"][">"] = self._build([r for r, _ in R], [y for _, y in R], depth + 1, attrs)
        return node

    # ---------- prediksi ----------
    def predict_one(self, row, return_path=False):
        node, path = self.tree, []
        while not node["leaf"]:
            a = node["attr"]
            if node["type"] == "cat":
                key = str(row[a])
                if key not in node["children"]:
                    path.append(f"{a} = {row[a]} (nilai baru, pakai mayoritas)")
                    return (node["majority"], path) if return_path else node["majority"]
                path.append(f"{a} = {row[a]}")
                node = node["children"][key]
            else:
                if row[a] <= node["thr"]:
                    path.append(f"{a} <= {node['thr']:.2f}")
                    node = node["children"]["<="]
                else:
                    path.append(f"{a} > {node['thr']:.2f}")
                    node = node["children"][">"]
        return (node["label"], path) if return_path else node["label"]

    def predict(self, rows):
        return [self.predict_one(r) for r in rows]

    # ---------- explainability ----------
    def rules(self):
        out = []

        def walk(node, conds):
            if node["leaf"]:
                out.append({"if": conds, "then": node["label"], "support": node["n"],
                            "confidence": round(node["dist"][node["label"]] / node["n"], 3)})
                return
            a = node["attr"]
            for k, child in node["children"].items():
                if node["type"] == "cat":
                    c = f"{a} = {k}"
                else:
                    c = f"{a} {k} {node['thr']:.2f}"
                walk(child, conds + [c])

        walk(self.tree, [])
        return out

    def depth(self, node=None):
        node = node or self.tree
        if node["leaf"]:
            return 0
        return 1 + max(self.depth(c) for c in node["children"].values())

    def n_leaves(self, node=None):
        node = node or self.tree
        if node["leaf"]:
            return 1
        return sum(self.n_leaves(c) for c in node["children"].values())

    def to_json(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump({"numeric_attrs": self.numeric_attrs,
                       "categorical_attrs": self.categorical_attrs,
                       "classes": self.classes_, "tree": self.tree}, f, indent=2, ensure_ascii=False)
