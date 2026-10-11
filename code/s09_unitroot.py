"""A2 (vòng 2): kiểm định nghiệm đơn vị bảng cho lnCO2, lnY, FDI.
CIPS (Pesaran 2007; CADF trung bình, có trung bình theo lát cắt) và IPS-t-bar (không hiệu chỉnh phụ thuộc chéo).
Phân vị tới hạn / p-value: mô phỏng Monte Carlo theo đúng N=73, T=21 dưới H0 (bước ngẫu nhiên không dịch chuyển;
CIPS: có nhân tố chung f_t và tải λ_i ~ U(0,5; 1,5); IPS: nhiễu độc lập) — tránh dùng bảng tra với N, T không khớp.
H0: có nghiệm đơn vị ở mọi nước; bác bỏ khi thống kê nhỏ hơn giá trị tới hạn (đuôi trái)."""
import numpy as np
import pandas as pd

import common
import est
from common import TABLES

SEED = 20240229
MC_REPS = 1000


def _wide(d, col):
    return d.pivot(index="Country", columns="Year", values=col).values


def cadf_t(Y, p=1, trend=False, cross=True):
    """Thống kê t của hệ số y_{s-1} trong hồi quy (C)ADF cho từng nước; trả mảng (N,)."""
    N, T = Y.shape
    dY = np.diff(Y, axis=1)  # dY[:, s-1] = Δy_s
    yb = Y.mean(0)
    dyb = np.diff(yb)
    ss = np.arange(p + 1, T)  # s = p+1..T-1
    n = len(ss)
    cols = [np.ones((N, n))]
    if trend:
        cols.append(np.tile(ss.astype(float), (N, 1)))
    cols.append(Y[:, ss - 1])
    ilag = len(cols) - 1
    if cross:
        cols.append(np.tile(yb[ss - 1], (N, 1)))
        cols.append(np.tile(dyb[ss - 1], (N, 1)))
        for j in range(1, p + 1):
            cols.append(np.tile(dyb[ss - 1 - j], (N, 1)))
    for j in range(1, p + 1):
        cols.append(dY[:, ss - 1 - j])
    X = np.stack(cols, axis=2)  # (N, n, k)
    y = dY[:, ss - 1]
    XtX = np.einsum("nti,ntj->nij", X, X)
    inv = np.linalg.inv(XtX)
    beta = np.einsum("nij,ntj,nt->ni", inv, X, y)
    res = y - np.einsum("nti,ni->nt", X, beta)
    s2 = (res ** 2).sum(1) / (n - X.shape[2])
    return beta[:, ilag] / np.sqrt(s2 * inv[:, ilag, ilag])


def mc_null(N, T, p, trend, cross, reps, rng):
    out = np.empty(reps)
    for r in range(reps):
        e = rng.normal(size=(N, T))
        if cross:
            lam = rng.uniform(0.5, 1.5, size=(N, 1))
            e = e + lam * rng.normal(size=(1, T))
        Y = np.cumsum(e, axis=1)
        out[r] = cadf_t(Y, p, trend, cross).mean()
    return out


def _dm2(a):
    return a - a.mean(1, keepdims=True) - a.mean(0, keepdims=True) + a.mean()


def mc_null_resid(N, T, k, reps, rng, cases):
    """[Vòng 3, D21] Null "không đồng liên kết": y và k biến giải thích là bước ngẫu nhiên độc lập (có nhân tố chung),
    hồi quy FE hai chiều, u = y - X b (giữ hiệu ứng), CIPS(u). Trả {case: mảng thống kê}; case = (lags, trend)."""
    out = {c: np.empty(reps) for c in cases}

    def rw():
        e = rng.normal(size=(N, T)) + rng.uniform(0.5, 1.5, size=(N, 1)) * rng.normal(size=(1, T))
        return np.cumsum(e, axis=1)
    for r in range(reps):
        y = rw()
        X = np.stack([rw() for _ in range(k)], axis=2)
        Xd = np.stack([_dm2(X[:, :, j]) for j in range(k)], axis=2)
        b = np.linalg.lstsq(Xd.reshape(-1, k), _dm2(y).reshape(-1), rcond=None)[0]
        u = y - X @ b
        for (p, tr) in cases:
            out[(p, tr)][r] = cadf_t(u, p, tr, True).mean()
    return out


def run_tests(d, specs=(("lnCO2", True), ("lnY", True), ("FDI", False))):
    """specs: (biến, có_xu_thế). Báo cả hai trường hợp (hằng số / hằng số+xu thế) để minh bạch."""
    rng = np.random.default_rng(SEED)
    rows = []
    N, T = _wide(d, "lnCO2").shape
    cache = {}
    for var, main_trend in specs:
        Y = _wide(d, var)
        for trend in (False, True):
            for p in (0, 1):
                for stat, cross in (("CIPS", True), ("IPS", False)):
                    key = (p, trend, cross)
                    if key not in cache:
                        cache[key] = mc_null(N, T, p, trend, cross, MC_REPS, rng)
                    null = cache[key]
                    obs = cadf_t(Y, p, trend, cross).mean()
                    rows.append({"var": var, "stat": stat, "trend": trend, "lags": p, "value": obs,
                                 "crit5": np.quantile(null, 0.05), "crit10": np.quantile(null, 0.10),
                                 "p_mc": (1 + (null <= obs).sum()) / (1 + len(null)),
                                 "main_case": trend == main_trend})
    return pd.DataFrame(rows)


def summary_lines(ur):
    L = ["- A2 Nghiệm đơn vị bảng (H0: có nghiệm đơn vị; MC N=73,T=21, 1000 lần; trường hợp chính: lnCO2, lnY có xu thế, FDI chỉ hằng số):"]
    for var in ["lnCO2", "lnY", "FDI"]:
        s = ur[(ur["var"] == var) & ur.main_case]
        cell = lambda stat, p: s[(s.stat == stat) & (s.lags == p)].iloc[0]
        L.append(f"  - {var}: " + "; ".join(f"{st} p={l}: {cell(st, l).value:.2f} (p_mc {cell(st, l).p_mc:.3f})"
                                           for st in ["CIPS", "IPS"] for l in (0, 1)))
    return L


if __name__ == "__main__":
    d = est.panel()
    ur = run_tests(d)
    ur.to_csv(TABLES / "unit_root.csv", index=False)
    print("\n".join(summary_lines(ur)))
