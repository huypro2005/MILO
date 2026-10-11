"""Bước 2: ma trận tương quan + VIF (M1, M2 và M3 từng k; riêng 6 WGI đưa chung chỉ để minh hoạ D6)."""
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor

import common
import est
from common import CONTROLS, IQ, IQ_ALL, TABLES, save_summary


def vif(df, cols):
    X = df[cols].copy()
    X.insert(0, "const", 1.0)
    return {c: float(variance_inflation_factor(X.values, i)) for i, c in enumerate(X.columns) if c != "const"}


def run():
    df = est.panel()
    cols = ["lnCO2", "FDI"] + IQ + ["IQ_PCA"] + CONTROLS
    df[cols].corr().round(3).to_csv(TABLES / "corr.csv")
    rows = []
    for hyp, ks in [("H1", [None]), ("H2", IQ_ALL), ("H3", IQ_ALL)]:
        for k in ks:
            d, x = est.spec(df, hyp, k)
            for var, v in vif(d, x).items():
                rows.append({"hyp": hyp, "iq": k or "NONE", "var": var, "vif": v})
    joint = vif(df, ["FDI"] + IQ + CONTROLS)
    for var, v in joint.items():
        rows.append({"hyp": "ALL6_JOINT", "iq": "ALL6", "var": var, "vif": v})
    t = pd.DataFrame(rows)
    t.to_csv(TABLES / "vif.csv", index=False)
    main = t[t["hyp"] != "ALL6_JOINT"]
    vmax = float(main["vif"].max())
    top = main.loc[main["vif"].idxmax()]
    wgi = df[IQ].corr().values
    off = wgi[~(wgi == 1)]
    lines = ["# s02 Tương quan & VIF",
             f"- VIF max (M1, M2, M3, từng k riêng) = {vmax:.2f} tại {top['hyp']}/{top['iq']}/{top['var']}",
             f"- VIF max khi đưa chung 6 WGI = {max(joint.values()):.2f} (minh hoạ lý do D6: đưa riêng từng k)",
             f"- Tương quan giữa 6 WGI: min {off.min():.2f}, max {off.max():.2f}",
             f"- corr(lnCO2, FDI) = {df['lnCO2'].corr(df['FDI']):.3f}; corr(FDI, IQ_PCA) = {df['FDI'].corr(df['IQ_PCA']):.3f}",
             "- Bảng: results/tables/corr.csv, vif.csv"]
    save_summary("s02", "\n".join(lines) + "\n")
    return [], {"vif_max": vmax, "vif_max_all6_joint": float(max(joint.values()))}


if __name__ == "__main__":
    print(run()[1])
