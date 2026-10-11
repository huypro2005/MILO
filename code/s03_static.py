"""Bước 3: POLS / FE / RE cho M1 (dummy năm / hiệu ứng thời gian) + kiểm định Hausman FE vs RE."""
import numpy as np
import pandas as pd
from scipy import stats

import common
import est
from common import TABLES, save_summary
from linearmodels.panel import PanelOLS, RandomEffects


def hausman(d, xs):
    dd = d.set_index(["Country", "Year"])
    fe = PanelOLS(dd["lnCO2"], dd[xs], entity_effects=True, time_effects=True).fit()
    yd = pd.get_dummies(dd.index.get_level_values("Year"), prefix="Year", drop_first=True, dtype=float)
    yd.index = dd.index
    X = pd.concat([dd[xs], yd], axis=1)
    X.insert(0, "const", 1.0)
    re = RandomEffects(dd["lnCO2"], X).fit()
    diff = fe.params[xs] - re.params[xs]
    V = fe.cov.loc[xs, xs] - re.cov.loc[xs, xs]
    stat = float(diff.values @ np.linalg.pinv(V.values) @ diff.values)
    eig_min = float(np.linalg.eigvalsh((V.values + V.values.T) / 2).min())
    return stat, len(xs), float(stats.chi2.sf(stat, len(xs))), eig_min


def mundlak(d, xs):
    """[A4 vòng 2] Hausman bền vững kiểu Mundlak: RE + dummy năm + trung bình nhóm của X; Wald H0: hệ số trung bình nhóm = 0,
    ma trận phương sai cụm theo nước (hợp lệ khi có phương sai thay đổi/tự tương quan)."""
    dd = d.set_index(["Country", "Year"]).copy()
    bars = [f"{v}_bar" for v in xs]
    for v, b in zip(xs, bars):
        dd[b] = dd.groupby(level=0)[v].transform("mean")
    yd = pd.get_dummies(dd.index.get_level_values("Year"), prefix="Year", drop_first=True, dtype=float)
    yd.index = dd.index
    X = pd.concat([dd[xs + bars], yd], axis=1)
    X.insert(0, "const", 1.0)
    res = RandomEffects(dd["lnCO2"], X).fit(cov_type="clustered", cluster_entity=True)
    g, V = res.params[bars].values, res.cov.loc[bars, bars].values
    stat = float(g @ np.linalg.solve(V, g))
    return stat, len(bars), float(stats.chi2.sf(stat, len(bars))), res.params[bars].to_dict()


def run():
    df = est.panel()
    d, x = est.spec(df, "H1")
    models = [est.static_fit(d, x, e, f"H1_{e}_NONE", "H1", "NONE") for e in ["POLS", "FE", "RE"]]
    stat, dof, p, eig = hausman(d, x)
    mstat, mdf, mp, mg = mundlak(d, x)
    rows = [{"model": m["id"], "var": n, **c, "nobs": m["nobs"]} for m in models for n, c in m["coef"].items()]
    pd.DataFrame(rows).to_csv(TABLES / "static_H1.csv", index=False)
    lines = ["# s03 POLS/FE/RE (M1, dummy năm; SE cụm theo nước)",
             "| model | FDI b | se | p | lnY b | p |", "|---|---|---|---|---|---|"]
    for m in models:
        f, y = m["coef"]["FDI"], m["coef"]["lnY"]
        lines.append(f"| {m['id']} | {f['b']:+.4f} | {f['se']:.4f} | {f['p']:.3f} | {y['b']:+.3f} | {y['p']:.3f} |")
    lines.append(f"- Hausman (FE 2 chiều vs RE+dummy năm; V = V_FE − V_RE, SE phi-robust): chi2({dof}) = {stat:.2f}, "
                 f"p = {p:.4g}; eigen min của V = {eig:.2e}"
                 + (" (V không xác định dương → dùng nghịch đảo giả)" if eig < 0 else ""))
    lines.append(f"- Hausman bền vững (Mundlak: RE + dummy năm + trung bình nhóm của X; Wald cụm theo nước): chi2({mdf}) = {mstat:.2f}, p = {mp:.4g} "
                 f"→ {'bác bỏ RE (dùng FE)' if mp < .05 else 'không bác bỏ RE'}; cổ điển p = {p:.4g} (không hợp lệ khi có khuyết tật, s04)")
    lines.append("- Bảng: results/tables/static_H1.csv")
    save_summary("s03", "\n".join(lines) + "\n")
    return models, {"hausman_p": p, "hausman_chi2": stat, "hausman_df": dof, "hausman_V_min_eig": eig,
                    "hausman_robust_p": mp, "hausman_robust_chi2": mstat, "hausman_robust_df": mdf}


if __name__ == "__main__":
    print(run()[1])
