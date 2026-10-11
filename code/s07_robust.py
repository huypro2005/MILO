"""[Vòng 3: + FD/FEDYNTR (B-3), quy tắc vững D22 (C3), tóm tắt viết lại ở verdicts()]
Bước 10: kiểm định vững.
(a) IQ_PCA thay IQk cho H2, H3 (FEDK + SGMM) — các id bắt buộc H2/H3_{FEDK,SGMM}_IQ_PCA.
(b) Winsorize FDI 1%/99% cho H1 và H3 (FEDK + SGMM): id H1w_*, H3w_* (hyp H1/H3, thêm cờ 'winsor': True).
Đặc tả giống hệt đặc tả chính (không chỉnh theo kết quả)."""
import pandas as pd

import common
import est
from common import IQ_ALL, TABLES, save_summary


def run():
    df = est.panel()
    dw = est.panel(winsor=True)
    models = []
    # (a) IQ_PCA
    k = "IQ_PCA"
    d2, x2 = est.spec(df, "H2", k)
    models.append(est.static_fit(d2, x2, "FEDK", f"H2_FEDK_{k}", "H2", k))
    models.append(est.sgmm_fit(d2, x2, f"H2_SGMM_{k}", "H2", k))
    d3, x3 = est.spec(df, "H3", k)
    m, res = est.static_fit(d3, x3, "FEDK", f"H3_FEDK_{k}", "H3", k, return_res=True)
    m["vcov_pair"] = est.fedk_pair(res, "FDI", f"FDIx{k}")
    models.append(m)
    models.append(est.sgmm_fit(d3, x3, f"H3_SGMM_{k}", "H3", k, with_vcov_pair=("FDI", f"FDIx{k}")))
    # (b) winsorize FDI
    d1, x1 = est.spec(dw, "H1")
    models.append(est.static_fit(d1, x1, "FEDK", "H1w_FEDK_NONE", "H1", "NONE", extra={"winsor": True}))
    models.append(est.sgmm_fit(d1, x1, "H1w_SGMM_NONE", "H1", "NONE", extra={"winsor": True}))
    for k in IQ_ALL:
        d3, x3 = est.spec(dw, "H3", k)
        m, res = est.static_fit(d3, x3, "FEDK", f"H3w_FEDK_{k}", "H3", k, return_res=True, extra={"winsor": True})
        m["vcov_pair"] = est.fedk_pair(res, "FDI", f"FDIx{k}")
        models.append(m)
        models.append(est.sgmm_fit(d3, x3, f"H3w_SGMM_{k}", "H3", k, extra={"winsor": True},
                                   with_vcov_pair=("FDI", f"FDIx{k}")))
    pd.DataFrame([{"model": m["id"], "var": n, **c, **m["diag"], "nobs": m["nobs"]}
                  for m in models for n, c in m["coef"].items()]).to_csv(TABLES / "robust.csv", index=False)
    # [B-3] vững động: sai phân đầu (FD) và FE động + xu thế riêng từng nước (FEDYNTR), mọi H1/H2/H3 (D23c,d)
    dyn = []
    for h, k in [("H1", "NONE")] + [(h, k) for h in ("H2", "H3") for k in IQ_ALL]:
        d, x = est.spec(df, h, None if k == "NONE" else k)
        dyn.append(est.fd_fit(d, x, f"{h}_FD_{k}", h, k))
        dyn.append(est.fedyn_fit(d, x, f"{h}_FEDYNTR_{k}", h, k, label="FEDYNTR", cov="kernel", trend=True)[0])
    models += dyn
    return models, {}


def _conc(by, pairs):
    """pairs: [(id_gốc, id_so, biến_gốc, biến_so)] -> (n, cùng dấu, cùng kết luận ý nghĩa 5%, danh sách lệch)."""
    n = sg = si = 0
    odd = []
    for a, b, va, vb in pairs:
        ca, cb = by[a]["coef"][va], by[b]["coef"][vb]
        n += 1
        s1 = ca["b"] * cb["b"] > 0
        s2 = (ca["p"] < .05) == (cb["p"] < .05)
        sg += s1
        si += s2
        if not (s1 and s2):
            odd.append(a.split("_", 2)[2] + ":" + ("dấu" if not s1 else "p"))
    return n, sg, si, odd


def _cls(ca, cb):
    """D22: ns = cả hai p>=0,10 (dấu không tính); ok = cùng dấu & >=1 bên p<0,10; bad = ngược dấu & >=1 bên p<0,10."""
    if ca["p"] >= .10 and cb["p"] >= .10:
        return "ns", ca["b"] * cb["b"] > 0
    return ("ok" if ca["b"] * cb["b"] > 0 else "bad"), ca["b"] * cb["b"] > 0


def _new_verdict(by, pairs):
    cl, same = [], []
    for a, b, va, vb in pairs:
        c, sg = _cls(by[a]["coef"][va], by[b]["coef"][vb])
        cl.append(c)
        same.append(sg)
    n = len(cl)
    cnt = f"{cl.count('ok')}/{cl.count('ns')}/{cl.count('bad')}"
    if "bad" in cl:
        v = "KHÔNG VỮNG"
    elif cl.count("ok") == n:
        v = "VỮNG"
    elif cl.count("ns") == n:
        v = "VỮNG DẤU (ns cả hai)" if all(same) else "NS CẢ HAI"
    else:
        v = "VỮNG (còn lại ns)"
    return v, cnt


def _dyn_verdict(main, others):
    """D22/B-3: so từng mô hình vững với FEDYNDK chính."""
    for o in others:
        if o["b"] * main["b"] < 0 and o["p"] < .10:
            return "KHÔNG VỮNG"
    if all(o["b"] * main["b"] > 0 for o in others):
        return "VỮNG" if any(o["p"] < .10 for o in others) else "VỮNG DẤU"
    return "KHÔNG KẾT LUẬN"


def verdicts(models):
    """[C3 vòng 3] Bảng vững theo quy tắc mới D22 (cột 'mới') cạnh quy tắc cũ D15f; bảng vững động B-3 (FD, FEDYNTR).
    Ghi toàn bộ results/summaries/s07.md (<= 40 dòng) và robust_dyn.csv."""
    by = {m["id"]: m for m in models}
    rows = []

    def add(h, what, est_, pairs):
        n, sg, si, odd = _conc(by, pairs)
        old = "VỮNG" if sg == n and si == n else ("VỮNG DẤU" if sg == n else "KHÔNG VỮNG")
        new, cnt = _new_verdict(by, pairs)
        rows.append(f"| {h} | {what} | {est_} | {cnt} | {old} | **{new}** | {'; '.join(odd)[:34]} |")
    for e in ("FEDYNDK", "SGMM", "FEDK"):
        add("H1", "FDI: gốc vs winsor", e, [(f"H1_{e}_NONE", f"H1w_{e}_NONE", "FDI", "FDI")])
        add("H2", "IQ_PCA vs từng IQk (6)", e, [(f"H2_{e}_{k}", f"H2_{e}_IQ_PCA", k, "IQ_PCA") for k in IQ_ALL[:-1]])
        add("H3", "FDIxIQ_PCA vs FDIxIQk (6)", e, [(f"H3_{e}_{k}", f"H3_{e}_IQ_PCA", f"FDIx{k}", "FDIxIQ_PCA") for k in IQ_ALL[:-1]])
        add("H3", "FDIxIQk gốc vs winsor (7)", e, [(f"H3_{e}_{k}", f"H3w_{e}_{k}", f"FDIx{k}", f"FDIx{k}") for k in IQ_ALL])
        add("H3", "FDI gốc vs winsor (7)", e, [(f"H3_{e}_{k}", f"H3w_{e}_{k}", "FDI", "FDI") for k in IQ_ALL])
    fm = lambda c: f"{c['b']:+.4f} ({c['p']:.2f})"
    drows, csv = [], []
    targets = [("H1", "NONE", "FDI")] + [("H2", k, k) for k in IQ_ALL] + [("H3", k, f"FDIx{k}") for k in IQ_ALL]
    for h, k, v in targets:
        mn, fd, tr = by[f"{h}_FEDYNDK_{k}"], by[f"{h}_FD_{k}"]["coef"][v], by[f"{h}_FEDYNTR_{k}"]["coef"][v]
        sg = by.get(f"{h}_SGMM_{k}", {"coef": {}})["coef"].get(v)
        c, jk = mn["coef"][v], mn["jackknife"][v]
        ver = _dyn_verdict(c, [fd, tr])
        drows.append(f"| {h} {v} | {fm(c)} | {jk['b']:+.4f} | {fm(fd)} | {fm(tr)} | **{ver}** |")
        csv.append({"hyp": h, "iq": k, "var": v, "fedyndk_b": c["b"], "fedyndk_p": c["p"], "jk_b": jk["b"], "fd_b": fd["b"],
                    "fd_p": fd["p"], "fedyntr_b": tr["b"], "fedyntr_p": tr["p"], "sgmm_b": sg and sg["b"], "sgmm_p": sg and sg["p"],
                    "verdict": ver})
    pd.DataFrame(csv).to_csv(TABLES / "robust_dyn.csv", index=False)
    L = ["# s07 Kiểm định vững (IQ_PCA; winsorize FDI; sai phân đầu; xu thế riêng) — vòng 3",
         "Bảng đủ: robust.csv (IQ_PCA, winsorize: FEDK+SGMM), fedyndk_main.csv (FEDYNDK), robust_dyn.csv (FD, FEDYNTR).",
         "## (A) So gốc vs vững. Quy tắc mới D22: cặp ok/ns-cả-hai/bad; ns = cả hai p>=0,10 (dấu không tính). Cũ D15f để đối chiếu",
         "| H | so sánh | ước lượng | ok/ns/bad | cũ D15f | mới D22 | lệch (cũ) |", "|---|---|---|---|---|---|---|"] + rows
    L += ["## (B) Vững động so với FEDYNDK chính [b (p)]: FD = ΔlnCO2 (SE DK, năm); TR = FEDYN + xu thế riêng từng nước (SE DK). VỮNG: cùng dấu & ≥1 p<0,10",
          "| biến | FEDYNDK | jackknife | FD | FEDYN+xu thế | kết luận |", "|---|---|---|---|---|---|"] + drows
    (common.SUMM / "s07.md").write_text(chr(10).join(L) + chr(10), encoding="utf-8")
    return rows


if __name__ == "__main__":
    run()
