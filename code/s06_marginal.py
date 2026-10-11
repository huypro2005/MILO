"""Bước 9: tác động biên của FDI theo chất lượng thể chế (H3), delta method.
ME(q) = b_FDI + b_FDIxk * (IQk(q) - mean IQk);  Var = V11 + x^2 V22 + 2 x V12.
Ma trận phương sai lấy từ: SGMM -> pydynpd mod.step_results[-1].vcov (đã hiệu chỉnh Windmeijer);
FEDK -> res.cov của linearmodels. Các phần tử (V11, V22, V12) được lưu trong models[i]['vcov_pair'].
Chạy SAU s07 (cần các mô hình H3 với IQ_PCA / winsorize)."""
import numpy as np
import pandas as pd
from scipy import stats

import common
import est
from common import IQ_ALL, TABLES, save_summary

PCTS = [10, 25, 50, 75, 90]


def me_rows(models, df, ids_prefix="H3", label="", use_jk=False):
    rows, notes = [], []
    for m in models:
        if m["hyp"] != "H3" or "vcov_pair" not in m or m["id"].split("_")[0] != ids_prefix:
            continue
        if use_jk and "jackknife" not in m:
            continue
        k = m["iq"]
        mean_k = df[k].mean()
        vp = m["vcov_pair"]
        cf = m["jackknife"] if use_jk else m["coef"]  # jackknife: hệ số đã hiệu chỉnh Nickell, phương sai DK mẫu đầy đủ
        b1, b2 = cf["FDI"]["b"], cf[f"FDIx{k}"]["b"]
        for q in PCTS:
            v = float(np.percentile(df[k], q))
            x = v - mean_k
            me = b1 + b2 * x
            var = vp["v11"] + x ** 2 * vp["v22"] + 2 * x * vp["v12"]
            se = float(np.sqrt(var))
            rows.append({"iq": k, "pct": q, "iq_value": v, "me": me, "se": se,
                         "p": float(2 * stats.norm.sf(abs(me / se))), "est": m["estimator"] + ("_JK" if use_jk else "")})
        thr = mean_k - b1 / b2 if b2 != 0 else np.nan
        notes.append((m["estimator"] + ("_JK" if use_jk else ""), k, thr, df[k].min() <= thr <= df[k].max()))
    return pd.DataFrame(rows), notes


def run(models=None):
    if models is None:
        raise ValueError("s06.run cần danh sách mô hình từ s04/s05/s07 (chạy qua run_all.py)")
    df = est.panel()
    tab, notes = me_rows(models, df, "H3")
    tab.to_csv(TABLES / "marginal_effects.csv", index=False)
    tjk, _ = me_rows(models, df, "H3", use_jk=True)  # ME với hệ số jackknife (FEDYNDK_JK)
    tjk.to_csv(TABLES / "marginal_effects_jk.csv", index=False)
    dfw = est.panel(winsor=True)
    tw, _ = me_rows(models, dfw, "H3w")
    tw.to_csv(TABLES / "marginal_effects_winsor.csv", index=False)
    lines = ["# s06 Tác động biên FDI theo IQ (delta method)",
             "ME = ∂lnCO2/∂FDI tại phân vị 10/25/50/75/90 của IQk (đơn vị: Δln CO2 trên 1 điểm % GDP FDI)",
             "| est | iq | ME p10 (p) | ME p50 (p) | ME p90 (p) | #pct p<0,05 | đổi dấu p10→p90? | IQ* trong mẫu? |",
             "|---|---|---|---|---|---|---|---|"]
    for (e, k), g in tab.groupby(["est", "iq"], sort=False):
        g = g.set_index("pct")
        sig = int((g["p"] < .05).sum())
        flip = "có" if g.loc[10, "me"] * g.loc[90, "me"] < 0 else "không"
        thr = [n for n in notes if n[0] == e and n[1] == k][0]
        f = lambda q: f"{g.loc[q, 'me']:+.4f} ({g.loc[q, 'p']:.3f})"
        lines.append(f"| {e} | {k} | {f(10)} | {f(50)} | {f(90)} | {sig}/5 | {flip} | "
                     f"{'có' if thr[3] else 'không'} (IQ*={thr[2]:.2f}) |")
    g = tjk.groupby("iq").apply(lambda x: int((x["p"] < .05).sum()), include_groups=False)
    lines.append("- ME jackknife (FEDYNDK_JK, marginal_effects_jk.csv): #pct p<0,05 theo IQ: " + ", ".join(f"{k} {v}/5" for k, v in g.items()))
    lines.append("- ME(P90)−ME(P10)=β(FDIxk)·(IQ90−IQ10) nên p của khác biệt trùng p của hệ số tương tác. Bảng: marginal_effects.csv, _winsor, _jk")
    save_summary("s06", "\n".join(lines) + "\n")
    return [], {}
