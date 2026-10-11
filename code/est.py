"""Hàm ước lượng dùng chung cho s03–s07 (không phải bước phân tích riêng).
Quy ước: tên hệ số trong estimates.json luôn là FDI, <k>, FDIx<k>, L1.lnCO2 (SPEC mục 6)."""
import contextlib
import io

import numpy as np
import pandas as pd
from scipy import stats

import common  # noqa: F401  (phải import trước pydynpd để có bản vá NumPy 2)
from common import CONTROLS, IQ_ALL, load_panel
from linearmodels.panel import PanelOLS, PooledOLS, RandomEffects
from pydynpd import regression

LAG = "L1.lnCO2"


def panel(winsor: bool = False) -> pd.DataFrame:
    """Bảng dữ liệu chuẩn; winsor=True: cắt FDI ở phân vị 1%/99% rồi tính lại biến trung tâm hoá & tương tác (D3)."""
    df = load_panel()
    if winsor:
        lo, hi = df["FDI"].quantile([0.01, 0.99])
        df["FDI"] = df["FDI"].clip(lo, hi)
        df["FDI_c"] = df["FDI"] - df["FDI"].mean()
        for k in IQ_ALL:
            df[f"FDIx{k}"] = df["FDI_c"] * df[f"{k}_c"]
    return df


def spec(df: pd.DataFrame, hyp: str, k: str | None = None):
    """Trả (df_mô_hình, danh_sách_biến_giải_thích) với tên biến chuẩn.
    H1: FDI+kiểm soát; H2: thêm k (mức gốc); H3: FDI, k, FDIxk đã trung tâm hoá (D3)."""
    d = df.copy()
    if hyp == "H1":
        x = ["FDI"]
    elif hyp == "H2":
        x = ["FDI", k]
    elif hyp == "H3":
        d["FDI"] = df["FDI_c"]
        d[k] = df[f"{k}_c"]
        d[f"FDIx{k}"] = df[f"FDIx{k}"]
        x = ["FDI", k, f"FDIx{k}"]
    else:
        raise ValueError(hyp)
    d = d.sort_values(["Country", "Year"]).reset_index(drop=True)
    d[LAG] = d.groupby("Country")["lnCO2"].shift(1)
    return d, x + CONTROLS


def _pack(mid, hyp, est, iq, nobs, ngroups, params, se, p, diag=None, extra=None):
    m = {"id": mid, "hyp": hyp, "estimator": est, "iq": iq, "nobs": int(nobs), "ngroups": int(ngroups),
         "coef": {n: {"b": float(params[n]), "se": float(se[n]), "p": float(p[n])} for n in params.index
                  if not str(n).startswith("Year_") and n != "const"},
         "diag": diag or {}}
    if extra:
        m.update(extra)
    return m


def static_fit(d: pd.DataFrame, xvars, est: str, mid: str, hyp: str, iq: str, dynamic: bool = False,
               return_res: bool = False, extra=None):
    """est ∈ POLS, FE, RE, FEDK. Hiệu ứng thời gian: PanelOLS(time_effects) hoặc dummy năm (POLS/RE)."""
    xs = ([LAG] if dynamic else []) + list(xvars)
    dd = d.dropna(subset=xs + ["lnCO2"]).copy() if dynamic else d.copy()
    dd = dd.set_index(["Country", "Year"])
    y, X = dd["lnCO2"], dd[xs]
    if est in ("POLS", "RE"):
        yd = pd.get_dummies(dd.index.get_level_values("Year"), prefix="Year", drop_first=True, dtype=float)
        yd.index = dd.index
        X = pd.concat([X, yd], axis=1)
        X.insert(0, "const", 1.0)
        mod = PooledOLS(y, X) if est == "POLS" else RandomEffects(y, X)
        res = mod.fit(cov_type="clustered", cluster_entity=True)
    elif est == "FE":
        res = PanelOLS(y, X, entity_effects=True, time_effects=True).fit(cov_type="clustered", cluster_entity=True)
    elif est == "FEDK":
        res = PanelOLS(y, X, entity_effects=True, time_effects=True).fit(cov_type="kernel")
    else:
        raise ValueError(est)
    ex = dict(extra or {})
    if est == "FEDK":
        ex["cov_type"] = "Driscoll-Kraay (kernel, time+entity FE)"
    m = _pack(mid, hyp, est + ("DYN" if dynamic and est in ("POLS", "FE") else ""), iq, res.nobs,
              y.index.get_level_values(0).nunique(), res.params, res.std_errors, res.pvalues, extra=ex)
    return (m, res) if return_res else m


def sgmm_fit(d: pd.DataFrame, xvars, mid: str, hyp: str, iq: str, gmm_lags: str = "2:4",
             iv_exog=None, extra=None, with_vcov_pair=None, pre=None, pre_lags: str = "2:3",
             nolevel: bool = False, diffh: bool = False):
    """System GMM 2 bước, collapse, dummy năm, Windmeijer (pydynpd). iv_exog: biến coi là iv ngoại sinh
    (mặc định: tất cả biến giải thích — A2 vòng 1)."""
    pre = list(pre or [])  # biến tiền định/nội sinh: công cụ GMM trễ pre_lags thay vì iv ngoại sinh
    iv_exog = [v for v in (xvars if iv_exog is None else iv_exog) if v not in pre]
    gm = f"gmm(lnCO2, {gmm_lags})" + (f" gmm({' '.join(pre)}, {pre_lags})" if pre else "")
    ivs = f" iv({' '.join(iv_exog)})" if iv_exog else ""
    cmd = f"lnCO2 {LAG} {' '.join(xvars)} | {gm}{ivs} | collapse timedumm{' nolevel' if nolevel else ''}"
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        r = regression.abond(cmd, d[["Country", "Year", "lnCO2"] + [c for c in dict.fromkeys(xvars)]], ["Country", "Year"])
    mod = r.models[0]
    t = mod.regression_table.set_index("variable")
    keep = [LAG] + list(xvars)
    params, se, p = t["coefficient"], t["std_err"], t["p_value"]
    diag = {"ar1_p": float(mod.AR_list[0].P_value), "ar2_p": float(mod.AR_list[1].P_value),
            "hansen_p": float(mod.hansen.p_value), "hansen_df": int(mod.hansen.df),
            "hansen_stat": float(mod.hansen.test_value), "n_instr": int(mod.z_information.num_instr)}
    # [A2 vòng 2] KTC 95% và Wald H0: rho = 1 cho L1.lnCO2
    b1, s1 = float(params[LAG]), float(se[LAG])
    diag.update({"L1_lo": b1 - 1.96 * s1, "L1_hi": b1 + 1.96 * s1,
                 "p_rho1": float(2 * stats.norm.sf(abs((b1 - 1) / s1)))})
    if diffh and not nolevel:  # [A3 vòng 2] Difference-in-Hansen thủ công (D14): J(SGMM) - J(Difference GMM cùng công cụ vi phân)
        try:
            kw = dict(gmm_lags=gmm_lags, iv_exog=iv_exog, pre=pre, pre_lags=pre_lags)
            dg = sgmm_fit(d, xvars, mid + "_dgmm", hyp, iq, nolevel=True, **kw)["diag"]
            c = diag["hansen_stat"] - dg["hansen_stat"]
            ddf = diag["hansen_df"] - dg["hansen_df"]
            diag.update({"diffhansen_stat": c, "diffhansen_df": ddf,
                         "diffhansen_p": float(stats.chi2.sf(c, ddf)) if (c >= 0 and ddf > 0) else None})
        except Exception as ex:  # ghi lại thay vì bỏ qua
            diag["diffhansen_error"] = repr(ex)[:100]
    ex = dict(extra or {})
    ex["gmm_lags"] = gmm_lags
    ex["command"] = cmd
    if with_vcov_pair:
        names = list(t.index)
        V = mod.step_results[-1].vcov
        a, b = (names.index(n) for n in with_vcov_pair)
        ex["vcov_pair"] = {"names": list(with_vcov_pair), "v11": float(V[a, a]), "v22": float(V[b, b]),
                           "v12": float(V[a, b])}
    m = _pack(mid, hyp, "DGMM" if nolevel else "SGMM", iq, mod.num_obs, mod.N, params.loc[keep], se.loc[keep], p.loc[keep], diag, ex)
    return m


def fedk_pair(res, a="FDI", b=None):
    c = res.cov
    return {"names": [a, b], "v11": float(c.loc[a, a]), "v22": float(c.loc[b, b]), "v12": float(c.loc[a, b])}


def longrun_from(params, cov, num, lag=LAG):
    """Hệ số dài hạn num/(1-rho), SE delta-method từ ma trận cov (có thể thay params bằng bản jackknife)."""
    b, r = float(params[num]), float(params[lag])
    c = cov
    g_b, g_r = 1 / (1 - r), b / (1 - r) ** 2
    var = g_b ** 2 * c.loc[num, num] + g_r ** 2 * c.loc[lag, lag] + 2 * g_b * g_r * c.loc[num, lag]
    se = float(np.sqrt(var))
    lr = b / (1 - r)
    return {"b": float(lr), "se": se, "p": float(2 * stats.norm.sf(abs(lr / se)))}


def longrun(res, num, lag=LAG):
    """Hệ số dài hạn num/(1-rho) với SE delta-method từ res.cov (mô hình động ρ<1). Trả {b, se, p}."""
    return longrun_from(res.params, res.cov, num, lag)


# ---------------------------------------------------------------- [Vòng 3] FE động hai chiều: FEDYN / FEDYNDK / FEDYNTR
def lagged(d: pd.DataFrame) -> pd.DataFrame:
    """Tính lại L1.lnCO2 trong chính tập d (dùng cho các nửa mẫu của jackknife)."""
    d = d.drop(columns=[LAG], errors="ignore").sort_values(["Country", "Year"]).reset_index(drop=True)
    d[LAG] = d.groupby("Country")["lnCO2"].shift(1)
    return d


def split_jackknife(d: pd.DataFrame, xs: list, full_params: pd.Series, halves=((2002, 2012), (2012, 2022))):
    """Split-panel jackknife (Dhaene–Jochmans 2015): 2*b_full - (b_1 + b_2)/2; mỗi nửa 11 năm (chung năm 2012),
    trễ & hiệu ứng nước+năm tính lại trong từng nửa."""
    subs = []
    for lo, hi in halves:
        s = lagged(d[(d["Year"] >= lo) & (d["Year"] <= hi)]).dropna(subset=xs + ["lnCO2"]).set_index(["Country", "Year"])
        r = PanelOLS(s["lnCO2"], s[xs], entity_effects=True, time_effects=True).fit()
        subs.append(r.params[xs])
    return 2 * full_params[xs] - (subs[0] + subs[1]) / 2, subs


def fedyn_fit(d, xvars, mid, hyp, iq, label="FEDYNDK", cov="kernel", trend=False, jk=False, extra=None):
    """FE hai chiều + L1.lnCO2. label: FEDYN (SE cụm), FEDYNDK (Driscoll–Kraay), FEDYNTR (DK + xu thế riêng từng nước).
    jk=True: thêm trường `jackknife` (mọi hệ số) + `longrun` (jackknife) + `longrun_uncorrected`."""
    xs = [LAG] + list(xvars)
    dd = d.dropna(subset=xs + ["lnCO2"]).copy()
    cols = list(xs)
    if trend:
        t = (dd["Year"] - dd["Year"].min()).astype(float)
        for i, c in enumerate(sorted(dd["Country"].unique())[1:]):  # bỏ 1 nước: tổng xu thế = xu thế chung ⊂ dummy năm
            dd[f"tr_{i}"] = np.where(dd["Country"] == c, t, 0.0)
            cols.append(f"tr_{i}")
    di = dd.set_index(["Country", "Year"])
    mod = PanelOLS(di["lnCO2"], di[cols], entity_effects=True, time_effects=True)
    res = mod.fit(cov_type="clustered", cluster_entity=True) if cov == "clustered" else mod.fit(cov_type="kernel")
    ex = dict(extra or {})
    ex["cov_type"] = "clustered by country" if cov == "clustered" else "Driscoll-Kraay (kernel)"
    m = _pack(mid, hyp, label, iq, res.nobs, dd["Country"].nunique(), res.params[cols], res.std_errors[cols],
              res.pvalues[cols], extra=ex)
    m["coef"] = {n: v for n, v in m["coef"].items() if not n.startswith("tr_")}
    if hyp == "H3" and not trend:  # FEDYNTR chỉ là kiểm định vững, không tính ME
        m["vcov_pair"] = fedk_pair(res, "FDI", f"FDIx{iq}")
    key = [n for n in ("FDI", iq, f"FDIx{iq}") if n in m["coef"]]
    if jk:
        pj, subs = split_jackknife(d, xs, res.params)
        c = res.cov
        m["jackknife"] = {n: {"b": float(pj[n]), "se": float(m["coef"][n]["se"]),
                              "p": float(2 * stats.norm.sf(abs(pj[n] / m["coef"][n]["se"]))),
                              "half1": float(subs[0][n]), "half2": float(subs[1][n])} for n in xs}
        r_se = m["coef"][LAG]["se"]
        m["jackknife"][LAG].update({"lo": float(pj[LAG] - 1.96 * r_se), "hi": float(pj[LAG] + 1.96 * r_se)})
        if pj[LAG] < 1:
            m["longrun"] = {n: longrun_from(pj, c, n) for n in key}
        else:
            m["longrun"] = {}
        if res.params[LAG] < 1:
            m["longrun_uncorrected"] = {n: longrun_from(res.params, c, n) for n in key}
    return m, res


def fd_fit(d, xvars, mid, hyp, iq, extra=None):
    """Sai phân đầu: ΔlnCO2 ~ Δ(kiểm soát) + (FDI, IQk, tương tác ở mức) + hiệu ứng năm, SE Driscoll–Kraay (D23c)."""
    dd = d.sort_values(["Country", "Year"]).copy()
    dd["dy"] = dd.groupby("Country")["lnCO2"].diff()
    for c in CONTROLS:
        dd[c] = dd.groupby("Country")[c].diff()
    dd = dd.dropna(subset=["dy"] + list(xvars)).set_index(["Country", "Year"])
    res = PanelOLS(dd["dy"], dd[list(xvars)], time_effects=True).fit(cov_type="kernel")
    ex = dict(extra or {})
    ex["cov_type"] = "Driscoll-Kraay (kernel)"
    return _pack(mid, hyp, "FD", iq, res.nobs, dd.index.get_level_values(0).nunique(), res.params, res.std_errors,
                 res.pvalues, extra=ex)
