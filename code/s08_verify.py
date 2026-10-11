"""A1 (vòng 2): xác minh bộ ước lượng pydynpd đã vá (D7) bằng mô phỏng Monte Carlo + Anderson–Hsiao trên dữ liệu thật.
DGP: y_it = rho*y_i,t-1 + beta*x_it + mu_i + e_it (dừng, burn-in 60 kỳ), N=73, T=21; tỉ lệ between/within mô phỏng
dữ liệu thật (sd_between(y)=1,3; sigma_e=0,1). Ước lượng cùng cú pháp chính: gmm(y,2:4) iv(x) collapse timedumm."""
import contextlib
import io

import numpy as np
import pandas as pd

import common
import est
from common import CONTROLS, TABLES
from linearmodels.iv import IV2SLS
from pydynpd import regression

SEED = 20240229
N, T, BETA = 73, 21, 0.1
REPS = 200


def simulate(rho, rng):
    mu = rng.normal(0, 1.3 * (1 - rho), N)
    burn = 60
    x = np.zeros((N, T + burn))
    y = np.zeros((N, T + burn))
    for t in range(1, T + burn):
        x[:, t] = 0.7 * x[:, t - 1] + rng.normal(0, 1, N)
        y[:, t] = rho * y[:, t - 1] + BETA * x[:, t] + mu + rng.normal(0, 0.1, N)
    y, x = y[:, burn:], x[:, burn:]
    return pd.DataFrame({"Country": np.repeat(np.arange(1, N + 1), T), "Year": np.tile(np.arange(2002, 2002 + T), N),
                         "y": y.ravel(), "x": x.ravel()})


def _abond(cmd, d):
    with contextlib.redirect_stdout(io.StringIO()):
        r = regression.abond(cmd, d, ["Country", "Year"])
    t = r.models[0].regression_table.set_index("variable")
    return float(t.loc["L1.y", "coefficient"]), float(t.loc["x", "coefficient"])


def _pols_fe(d):
    d = d.copy()
    d["ly"] = d.groupby("Country")["y"].shift(1)
    d = d.dropna()
    X = np.column_stack([d["ly"], d["x"], np.ones(len(d))])
    pols = np.linalg.lstsq(X, d["y"].values, rcond=None)[0]
    dm = d[["y", "ly", "x"]] - d.groupby("Country")[["y", "ly", "x"]].transform("mean")
    fe = np.linalg.lstsq(dm[["ly", "x"]].values, dm["y"].values, rcond=None)[0]
    return pols[0], pols[1], fe[0], fe[1]


def montecarlo(rho, reps=REPS):
    rng = np.random.default_rng([SEED, int(rho * 100)])
    rows, fail = [], 0
    for _ in range(reps):
        d = simulate(rho, rng)
        try:
            sr, sb = _abond("y L1.y x | gmm(y, 2:4) iv(x) | collapse timedumm", d)
            dr, db = _abond("y L1.y x | gmm(y, 2:4) iv(x) | collapse timedumm nolevel", d)
        except Exception:
            fail += 1
            continue
        pr, pb, fr, fb = _pols_fe(d)
        rows.append(dict(SGMM=sr, DGMM=dr, POLS=pr, FE=fr, SGMM_b=sb, DGMM_b=db, POLS_b=pb, FE_b=fb))
    r = pd.DataFrame(rows)
    out = []
    for e in ["POLS", "FE", "DGMM", "SGMM"]:
        out.append({"rho_true": rho, "estimator": e, "reps": len(r), "fail": fail, "rho_hat": r[e].mean(),
                    "bias": r[e].mean() - rho, "sd": r[e].std(), "rmse": float(np.sqrt(((r[e] - rho) ** 2).mean())),
                    "beta_bias": r[e + "_b"].mean() - BETA})
    return out


def anderson_hsiao(d, x):
    """AH trên dữ liệu thật: Δy_t trên Δy_{t-1}, ΔX, dummy năm; công cụ y_{t-2} (mức) hoặc Δy_{t-2} (vi phân)."""
    d = d.sort_values(["Country", "Year"]).copy()
    g = d.groupby("Country")
    d["dy"], d["dy1"] = d["lnCO2"] - g["lnCO2"].shift(1), g["lnCO2"].shift(1) - g["lnCO2"].shift(2)
    d["y2"], d["dy2"] = g["lnCO2"].shift(2), g["lnCO2"].shift(2) - g["lnCO2"].shift(3)
    for v in x:
        d["d_" + v] = d[v] - g[v].shift(1)
    rows = []
    for label, inst in [("AH-mức (y_{t-2})", "y2"), ("AH-vi phân (Δy_{t-2})", "dy2")]:
        dd = d.dropna(subset=["dy", "dy1", inst] + ["d_" + v for v in x]).copy()
        yd = pd.get_dummies(dd["Year"], prefix="Y", drop_first=True, dtype=float)
        exog = pd.concat([dd[["d_" + v for v in x]], yd], axis=1)
        res = IV2SLS(dd["dy"], exog, dd[["dy1"]], dd[[inst]]).fit(cov_type="clustered", clusters=dd["Country"])
        f1 = res.first_stage.diagnostics.loc["dy1", "f.stat"]
        b, se = float(res.params["dy1"]), float(res.std_errors["dy1"])
        rows.append({"spec": label, "L1_b": b, "L1_se": se, "L1_lo": b - 1.96 * se, "L1_hi": b + 1.96 * se,
                     "FDI_b": float(res.params["d_FDI"]), "FDI_p": float(res.pvalues["d_FDI"]),
                     "F1": float(f1), "nobs": int(res.nobs)})
    return pd.DataFrame(rows)


def run_all_checks(d, x):
    mc = pd.DataFrame(montecarlo(0.8) + montecarlo(0.95))
    mc.to_csv(TABLES / "sim_pydynpd.csv", index=False)
    ah = anderson_hsiao(d, x)
    ah.to_csv(TABLES / "anderson_hsiao.csv", index=False)
    return mc, ah


def summary_lines(mc, ah):
    L = [f"- A1 Mô phỏng pydynpd (N={N},T={T},{REPS} lần, seed {SEED}, beta={BETA}): bias(ρ̂) = ρ̂−ρ"]
    for rho in sorted(mc.rho_true.unique()):
        s = mc[mc.rho_true == rho].set_index("estimator")
        L.append(f"  - ρ={rho}: " + "; ".join(f"{e} {s.loc[e, 'rho_hat']:.3f} (bias {s.loc[e, 'bias']:+.3f})"
                                              for e in ["POLS", "FE", "DGMM", "SGMM"]))
    bad = mc[(mc.estimator == "SGMM") & (mc.bias.abs() > 0.05)]
    L.append("  - " + ("SGMM bias > 0,05 ở ρ=" + ", ".join(map(str, bad.rho_true)) + " → xem DECISIONS D16"
                       if len(bad) else "SGMM |bias| ≤ 0,05 ở cả hai ρ → cài đặt pydynpd đã vá không có lỗi hệ thống"))
    for _, r in ah.iterrows():
        L.append(f"  - {r['spec']}: ρ̂ {r.L1_b:.3f} (se {r.L1_se:.3f}) KTC [{r.L1_lo:.2f}, {r.L1_hi:.2f}], "
                 f"F1 {r.F1:.1f}, FDI {r.FDI_b:+.4f} (p {r.FDI_p:.3f})")
    return L


if __name__ == "__main__":
    df = est.panel()
    d, x = est.spec(df, "H1")
    mc, ah = run_all_checks(d, x)
    print("\n".join(summary_lines(mc, ah)))
