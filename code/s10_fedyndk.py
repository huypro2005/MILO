"""[Vòng 3, D18/D23] Ước lượng CHÍNH: FE động hai chiều + SE Driscoll–Kraay (FEDYNDK) + split-panel jackknife
(Dhaene–Jochmans 2015, nửa mẫu 2002–2012 / 2012–2022) cho H1, H2 (6 WGI + IQ_PCA), H3 (6 WGI + IQ_PCA).
Gồm cả bản winsorize FDI (kiểm định vững, đặc tả giữ nguyên). Tóm tắt kết luận theo tiêu chí D18 ở verdicts()."""
import numpy as np
import pandas as pd
from scipy import stats

import common
import est
from common import IQ, IQ_ALL, TABLES, save_summary

HEAD = ["| model | ρ | ρ_jk [KTC95%] | FDI b (p) | FDI jk | k b (p) | k jk | FDIxk b (p) | FDIxk jk |", "|---|---|---|---|---|---|---|---|---|"]


def _c(m, n, jk=False):
    c = (m.get("jackknife") if jk else m["coef"]).get(n)
    return "" if c is None else f"{c['b']:+.4f}" + ("" if jk else f" ({c['p']:.3f})")


def fit_all(df, winsor=False):
    models = []
    pre = "w" if winsor else ""
    ex = {"winsor": True} if winsor else None
    cases = [("H1", "NONE")] + [(h, k) for h in ("H2", "H3") for k in IQ_ALL]
    if winsor:
        cases = [("H1", "NONE")] + [("H3", k) for k in IQ_ALL]
    for h, k in cases:
        d, x = est.spec(df, h, None if k == "NONE" else k)
        m, _ = est.fedyn_fit(d, x, f"{h}{pre}_FEDYNDK_{k}", h, k, label="FEDYNDK", cov="kernel", jk=True, extra=ex)
        models.append(m)
    return models


def run():
    models = fit_all(est.panel())
    models += fit_all(est.panel(winsor=True), winsor=True)
    main = [m for m in models if "winsor" not in m]
    rows = []
    for m in models:
        for n, c in m["coef"].items():
            j = m["jackknife"][n]
            rows.append({"model": m["id"], "var": n, **c, "jk_b": j["b"], "jk_se": j["se"], "jk_p": j["p"],
                         "half1": j["half1"], "half2": j["half2"]})
    pd.DataFrame(rows).to_csv(TABLES / "fedyndk_main.csv", index=False)
    pd.DataFrame([{"model": m["id"], "var": n, "version": v, **c} for m in models
                  for v, key in (("jackknife", "longrun"), ("uncorrected", "longrun_uncorrected"))
                  for n, c in m.get(key, {}).items()]).to_csv(TABLES / "longrun_fedyndk.csv", index=False)

    L = ["# s10 FEDYNDK (ước lượng chính, D18): FE động 2 chiều + SE Driscoll–Kraay + split-panel jackknife",
         "- jk = 2b − (b[2002–12]+b[2012–22])/2; SE jk = SE DK mẫu đầy đủ (D23a); bảng đủ: fedyndk_main.csv, longrun_fedyndk.csv"] + HEAD
    for m in main:
        k = m["iq"]
        j = m["jackknife"][est.LAG]
        L.append(f"| {m['id'].replace('_FEDYNDK', '')} | {m['coef'][est.LAG]['b']:.3f} | {j['b']:.3f} [{j['lo']:.2f}, {j['hi']:.2f}] | "
                 f"{_c(m, 'FDI')} | {_c(m, 'FDI', True)} | {_c(m, k) if k != 'NONE' else ''} | {_c(m, k, True) if k != 'NONE' else ''} | "
                 f"{_c(m, 'FDIx' + k) if k != 'NONE' else ''} | {_c(m, 'FDIx' + k, True) if k != 'NONE' else ''} |")
    h1 = main[0]
    lr, lu = h1.get("longrun", {}).get("FDI"), h1.get("longrun_uncorrected", {}).get("FDI")
    L.append("- Dài hạn FDI (H1) = β/(1−ρ): " + (f"jackknife {lr['b']:+.4f} (se {lr['se']:.4f}, p={lr['p']:.3f}); " if lr else "jackknife n/a (ρ_jk≥1); ")
             + (f"chưa hiệu chỉnh {lu['b']:+.4f} (se {lu['se']:.4f}, p={lu['p']:.3f})" if lu else "chưa hiệu chỉnh n/a"))
    save_summary("s10", "\n".join(L) + "\n")
    return models, {}


def verdicts(models):
    """Kết luận cơ học theo D18 (tiêu chí ghi trước). Nối thêm vào s10.md. Trả dict để run.md/checks dùng."""
    by = {m["id"]: m for m in models}
    P, N = "ỦNG HỘ", "KHÔNG ỦNG HỘ"
    h1, f1, out = by["H1_FEDYNDK_NONE"], by["H1_FEDK_NONE"], {}
    c, j, f = h1["coef"]["FDI"], h1["jackknife"]["FDI"], f1["coef"]["FDI"]
    ok1 = c["p"] < .05 and c["b"] * j["b"] > 0 and c["b"] * f["b"] > 0
    out["H1"] = P if ok1 else N
    L = ["", "## Kết luận cơ học theo tiêu chí D18 (ghi trước khi chạy)",
         f"- H1: β(FDI) FEDYNDK {c['b']:+.4f} (p={c['p']:.3f}); jackknife {j['b']:+.4f}; FEDK {f['b']:+.4f} → **{out['H1']}**"]
    h2 = [by[f"H2_FEDYNDK_{k}"] for k in IQ]
    sig = [m["iq"] for m in h2 if m["coef"][m["iq"]]["p"] < .05]
    sgn = {np.sign(m["coef"][m["iq"]]["b"]) for m in h2}
    pat = {m["coef"][m["iq"]]["p"] < .05 for m in h2}
    out["H2"] = P if (sig and (len(sgn) > 1 or len(pat) > 1)) else N
    L.append(f"- H2: k có p<0,05 ở FEDYNDK: {sig or 'không có'}; dấu khác nhau? {len(sgn) > 1}; ý nghĩa khác nhau? {len(pat) > 1} → **{out['H2']}**")
    df, rows = est.panel(), []
    for k in IQ:
        m = by[f"H3_FEDYNDK_{k}"]
        n = f"FDIx{k}"
        v = m["vcov_pair"]["v22"]
        x10, x90 = np.percentile(df[k], [10, 90])
        diff = m["coef"][n]["b"] * (x90 - x10)
        pd_ = float(2 * stats.norm.sf(abs(diff) / (abs(x90 - x10) * np.sqrt(v))))
        ok = m["coef"][n]["p"] < .05 and m["coef"][n]["b"] * m["jackknife"][n]["b"] > 0 and pd_ < .05
        out[f"H3_{k}"] = P if ok else N
        rows.append(f"{k}: {m['coef'][n]['b']:+.4f} (p={m['coef'][n]['p']:.3f}), jk {m['jackknife'][n]['b']:+.4f}, ME90−ME10={diff:+.4f} (p={pd_:.3f}) → {'ỦNG HỘ' if ok else 'không'}")
    L.append("- H3 (FDIxk; ME P90−P10 là tổ hợp tuyến tính nên p trùng p của tương tác): " + "; ".join(rows))
    p = common.SUMM / "s10.md"
    nl = chr(10)
    p.write_text(p.read_text(encoding="utf-8").rstrip(nl) + nl + nl.join(L) + nl, encoding="utf-8")
    return out


if __name__ == "__main__":
    ms, _ = run()
    print(open(common.SUMM / "s10.md", encoding="utf-8").read())
