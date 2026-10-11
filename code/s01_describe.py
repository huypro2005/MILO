"""Bước 1: thống kê mô tả (tổng thể, between/within, theo năm)."""
import pandas as pd

import common
from common import IQ, TABLES, load_panel, save_summary

VARS = ["lnCO2", "CO2", "FDI"] + IQ + ["IQ_PCA", "Y", "lnY", "URB", "TO", "Crdt"]


def run():
    df = load_panel()
    TABLES.mkdir(parents=True, exist_ok=True)
    rows = []
    for v in VARS:
        g = df.groupby("Country")[v]
        rows.append({"var": v, "n": df[v].count(), "mean": df[v].mean(), "sd": df[v].std(), "min": df[v].min(),
                     "p25": df[v].quantile(.25), "p50": df[v].median(), "p75": df[v].quantile(.75),
                     "max": df[v].max(), "skew": df[v].skew(), "sd_between": g.mean().std(),
                     "sd_within": (df[v] - g.transform("mean")).std()})
    t = pd.DataFrame(rows)
    t.to_csv(TABLES / "describe.csv", index=False)
    df.groupby("Year")[["lnCO2", "FDI", "IQ_PCA"]].mean().round(3).to_csv(TABLES / "describe_by_year.csv")
    q = df["FDI"].quantile([.01, .99])
    n_out = int(((df["FDI"] < q.iloc[0]) | (df["FDI"] > q.iloc[1])).sum())
    lines = ["# s01 Thống kê mô tả",
             f"- N={len(df)}, nước={df['Country'].nunique()}, năm {df['Year'].min()}–{df['Year'].max()}",
             "| var | mean | sd | min | max | sd_between | sd_within |", "|---|---|---|---|---|---|---|"]
    keep = ["lnCO2", "FDI", "lnY", "URB", "TO", "Crdt"] + IQ + ["IQ_PCA"]
    for _, r in t[t["var"].isin(keep)].iterrows():
        lines.append(f"| {r['var']} | {r['mean']:.3f} | {r['sd']:.3f} | {r['min']:.2f} | {r['max']:.2f} | "
                     f"{r['sd_between']:.3f} | {r['sd_within']:.3f} |")
    lines.append(f"- FDI winsorize 1%/99%: [{q.iloc[0]:.2f}, {q.iloc[1]:.2f}], {n_out} quan sát bị cắt")
    lines.append("- Bảng đầy đủ: results/tables/describe.csv, describe_by_year.csv")
    save_summary("s01", "\n".join(lines) + "\n")
    return [], {}


if __name__ == "__main__":
    run()
