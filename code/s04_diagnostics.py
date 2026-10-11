"""Bước 4: khuyết tật mô hình tĩnh M1 (phương sai thay đổi nhóm, Wooldridge AR(1), Pesaran CD)
-> FE Driscoll–Kraay (FEDK) cho H1, H2 (6 WGI), H3 (6 WGI)."""
import numpy as np
import pandas as pd
from scipy import stats

import common
import est
import s09_unitroot
from common import IQ, IQ_ALL, TABLES, save_summary
from linearmodels.panel import PanelOLS

CASES = [(1, False), (0, False), (1, True), (0, True)]  # (trễ ADF, xu thế); trường hợp chính (1, False) — D21
MAIN_CASE = (1, False)


def fe_resid(d, xs, twoway=False):
    dd = d.set_index(["Country", "Year"])
    r = PanelOLS(dd["lnCO2"], dd[xs], entity_effects=True, time_effects=twoway).fit()
    return r.resids.unstack("Year")  # nước x năm


def modified_wald(e):
    """Greene: H0 phương sai sai số bằng nhau giữa các nước (FE một chiều)."""
    N, T = e.shape
    s2i = (e ** 2).sum(axis=1) / T
    s2 = s2i.mean()
    vi = ((e ** 2).sub(s2i, axis=0) ** 2).sum(axis=1) / (T * (T - 1))
    W = float((((s2i - s2) ** 2) / vi).sum())
    return W, N, float(stats.chi2.sf(W, N))


def wooldridge(d, xs):
    """Wooldridge (2002): hồi quy sai phân không hằng số, phần dư e_t theo e_{t-1}, H0: b = -0,5."""
    dd = d.sort_values(["Country", "Year"])
    dif = dd.groupby("Country")[["lnCO2"] + xs].diff().dropna()
    ctry = dd.loc[dif.index, "Country"].values
    Y, X = dif["lnCO2"].values, dif[xs].values
    b = np.linalg.lstsq(X, Y, rcond=None)[0]
    z = pd.DataFrame({"e": Y - X @ b, "c": ctry})
    z["el"] = z.groupby("c")["e"].shift(1)
    z = z.dropna()
    x, y = z["el"].values, z["e"].values
    g = float((x * y).sum() / (x * x).sum())
    u = y - g * x
    cl = pd.Series(x * u).groupby(z["c"].values).sum()
    n = len(cl)
    se = float(np.sqrt(n / (n - 1) * (cl ** 2).sum()) / (x * x).sum())
    F = ((g + 0.5) / se) ** 2
    return g, float(F), float(stats.f.sf(F, 1, n - 1))


def pesaran_cd(e):
    N, T = e.shape
    rho = np.corrcoef(e.values)[np.triu_indices(N, 1)]
    cd = float(np.sqrt(2 * T / (N * (N - 1))) * rho.sum())
    return cd, float(2 * stats.norm.sf(abs(cd))), float(rho.mean()), float(np.abs(rho).mean())


def level_resid(d, xs, params):
    """u_it = y_it - x_it·b (giữ hiệu ứng nước & năm) dạng ma trận nước x năm (D21)."""
    dd = d.dropna(subset=xs + ["lnCO2"]).set_index(["Country", "Year"])
    return (dd["lnCO2"] - dd[xs] @ params[xs]).unstack("Year").values


def resid_cips(items, rng):
    """items: [(id, hyp_nhãn, k_hồi_quy, ma_trận_u, loại)] loại ∈ static|dynamic. MC theo D21. Trả DataFrame."""
    rows, cache = [], {}
    for mid, kind, k, U in items:
        N, T = U.shape
        key = ("static", k, T) if kind == "static" else ("unitroot", T)
        if key not in cache:
            if kind == "static":
                cache[key] = s09_unitroot.mc_null_resid(N, T, k, s09_unitroot.MC_REPS, rng, CASES)
            else:
                cache[key] = {c: s09_unitroot.mc_null(N, T, c[0], c[1], True, s09_unitroot.MC_REPS, rng) for c in CASES}
        for c in CASES:
            null, obs = cache[key][c], s09_unitroot.cadf_t(U, c[0], c[1], True).mean()
            rows.append({"model": mid, "kind": kind, "k_reg": k, "lags": c[0], "trend": c[1], "value": obs,
                         "crit5": float(np.quantile(null, 0.05)), "crit10": float(np.quantile(null, 0.10)),
                         "p_mc": (1 + (null <= obs).sum()) / (1 + len(null)), "main_case": c == MAIN_CASE})
    return pd.DataFrame(rows)


def run():
    df = est.panel()
    d, x = est.spec(df, "H1")
    e = fe_resid(d, x)
    W, N, p_het = modified_wald(e)
    rho, F, p_ar = wooldridge(d, x)
    cd, p_cd, rbar, absr = pesaran_cd(e)
    cd2, p_cd2, _, _ = pesaran_cd(fe_resid(d, x, twoway=True))
    tests = {"het_p": p_het, "het_chi2": W, "wooldridge_ar1_p": p_ar, "wooldridge_F": F, "wooldridge_rho": rho,
             "pesaran_cd_p": p_cd, "pesaran_cd": cd, "pesaran_avg_rho": rbar, "pesaran_avg_abs_rho": absr,
             "pesaran_cd_twoway_p": p_cd2, "pesaran_cd_twoway": cd2}
    m1, r1 = est.static_fit(d, x, "FEDK", "H1_FEDK_NONE", "H1", "NONE", return_res=True)
    models = [m1]
    items = [("H1_FEDK_NONE", "static", len(x), level_resid(d, x, r1.params))]
    for k in IQ_ALL:  # [C2] H2_k (7 IQ): FEDK chính cho 6 WGI đã có; IQ_PCA do s07 ước lượng, ở đây chỉ lấy phần dư
        d2, x2 = est.spec(df, "H2", k)
        if k in IQ:
            mk, rk = est.static_fit(d2, x2, "FEDK", f"H2_FEDK_{k}", "H2", k, return_res=True)
            models.append(mk)
        else:
            rk = PanelOLS(d2.set_index(["Country", "Year"])["lnCO2"], d2.set_index(["Country", "Year"])[x2],
                          entity_effects=True, time_effects=True).fit()
        items.append((f"H2_FEDK_{k}", "static", len(x2), level_resid(d2, x2, rk.params)))
        if k not in IQ:
            continue
        d3, x3 = est.spec(df, "H3", k)
        m, res = est.static_fit(d3, x3, "FEDK", f"H3_FEDK_{k}", "H3", k, return_res=True)
        m["vcov_pair"] = est.fedk_pair(res, "FDI", f"FDIx{k}")
        models.append(m)
    pd.DataFrame([{"model": m["id"], "var": n, **c, "nobs": m["nobs"]}
                  for m in models for n, c in m["coef"].items()]).to_csv(TABLES / "fedk_IQ6.csv", index=False)
    # [C2, D21] phần dư FE động (H1 và H2_k): null nghiệm đơn vị thường, chỉ để thông tin
    dyn_items = []
    for hyp, ks in (("H1", ["NONE"]), ("H2", IQ_ALL)):
        for k in ks:
            dk, xk = est.spec(df, hyp, None if k == "NONE" else k)
            _, rk = est.static_fit(dk, xk, "FE", "tmp", hyp, k, dynamic=True, return_res=True)
            dyn_items.append((f"{hyp}_FEDYN_{k}", "dynamic", len(xk) + 1, level_resid(dk, [est.LAG] + xk, rk.params)))
    ru = resid_cips(items + dyn_items, np.random.default_rng(s09_unitroot.SEED + 3))
    ru.to_csv(TABLES / "resid_unit_root.csv", index=False)
    mn = ru[ru.main_case].set_index("model")
    tests["resid_cips_p"] = float(mn.loc["H1_FEDK_NONE", "p_mc"])
    tests["resid_cips_value"] = float(mn.loc["H1_FEDK_NONE", "value"])
    tests["resid_cips_h2_max_p"] = float(mn.loc[[f"H2_FEDK_{k}" for k in IQ_ALL], "p_mc"].max())
    tests["resid_cips_fedyn_h1_p"] = float(mn.loc["H1_FEDYN_NONE", "p_mc"])
    present = [n for n, pv in [("phương sai thay đổi", p_het), ("tự tương quan", p_ar), ("phụ thuộc chéo (CD)", p_cd)] if pv < .05]
    lines = ["# s04 Chẩn đoán M1 + FE Driscoll–Kraay",
             f"- Phương sai thay đổi theo nước (Modified Wald, FE 1 chiều): chi2({N}) = {W:.1f}, p = {p_het:.4g}",
             f"- Wooldridge AR(1) (H0: rho=-0,5): rho = {rho:.3f}, F(1,{N-1}) = {F:.1f}, p = {p_ar:.4g}",
             f"- Pesaran CD (FE 1 chiều): CD = {cd:.1f}, p = {p_cd:.4g}; rho TB = {rbar:.3f}, |rho| TB = {absr:.3f}",
             f"- Pesaran CD (FE 2 chiều, đã khử hiệu ứng năm): CD = {cd2:.1f}, p = {p_cd2:.4g}",
             "- Khuyết tật có mặt (p<0,05): " + (", ".join(present) if present else "không có")
             + ("; CD không bác bỏ nhưng |rho| TB cao -> CD kém hiệu lực khi tương quan hai dấu (Pesaran 2015)" if p_cd >= .05 and absr > .3 else ""),
             "- FEDK = PanelOLS(entity+time effects, cov kernel, băng thông mặc định linearmodels)",
             "- [C2/D21] CIPS phần dư u=y−Xb (hằng số, 1 trễ; MC 1000 lần, null không đồng liên kết N=73,T=21; H0: không dừng):",
             f"  H1 FEDK: CIPS={mn.loc['H1_FEDK_NONE', 'value']:.2f} (tới hạn 5%={mn.loc['H1_FEDK_NONE', 'crit5']:.2f}), p_mc={mn.loc['H1_FEDK_NONE', 'p_mc']:.3f}",
             f"  H2 FEDK (7 IQ): p_mc {mn.loc[[f'H2_FEDK_{k}' for k in IQ_ALL], 'p_mc'].min():.3f}–{tests['resid_cips_h2_max_p']:.3f}",
             f"  FEDYN H1: CIPS={mn.loc['H1_FEDYN_NONE', 'value']:.2f}, p_mc={tests['resid_cips_fedyn_h1_p']:.3f}; FEDYN H2: p_mc "
             f"{mn.loc[[f'H2_FEDYN_{k}' for k in IQ_ALL], 'p_mc'].min():.3f}–{mn.loc[[f'H2_FEDYN_{k}' for k in IQ_ALL], 'p_mc'].max():.3f} (null thường, thông tin)",
             "  → " + ("phần dư tĩnh DỪNG (p_mc<0,05): FEDK tĩnh không bị giả mạo theo tiêu chí này" if tests["resid_cips_p"] < .05 and tests["resid_cips_h2_max_p"] < .05
                      else "phần dư tĩnh KHÔNG (hoặc không đủ) bác bỏ nghiệm đơn vị -> FEDK tĩnh chỉ là tham chiếu (D21); bảng: resid_unit_root.csv"),
             "| model | FDI b (p) | k b (p) | FDIxk b (p) |", "|---|---|---|---|"]
    for m in models:
        k = m["iq"]

        def g(n):
            return f"{m['coef'][n]['b']:+.4f} ({m['coef'][n]['p']:.3f})" if n in m["coef"] else ""
        lines.append(f"| {m['id']} | {g('FDI')} | {g(k) if k != 'NONE' else ''} | {g('FDIx' + k) if k != 'NONE' else ''} |")
    save_summary("s04", "\n".join(lines) + "\n")
    return models, tests


if __name__ == "__main__":
    print(run()[1])
