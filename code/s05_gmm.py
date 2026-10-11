"""[Vòng 2: + KTC/p(rho=1), Difference-in-Hansen, 3 ứng viên theo D14 (A1–A3, A5)]
Bước 5–8: System GMM 2 bước (H1, H2, H3 x 6 WGI) + POLS/FE động (cận Bond) + bảng nhạy cảm công cụ (H1).
Đặc tả SGMM chính (vòng 1, theo STATE A2): gmm(lnCO2, 2:4) collapse; mọi biến giải thích là iv ngoại sinh; dummy năm.
Bảng nhạy cảm chỉ để chẩn đoán/báo cáo (SPEC mục 7.3), KHÔNG thay đặc tả chính."""
import pandas as pd

import common
import est
import s08_verify
import s09_unitroot
from common import IQ, IQ_ALL, TABLES, save_summary


def sensitivity(d, x):
    """Các đặc tả công cụ khác cho H1 -> results/tables/sgmm_sensitivity_H1.csv."""
    variants = [
        ("MAIN gmm(y,2:4); X exog-iv", dict()),
        ("gmm(y,2:3); X exog-iv", dict(gmm_lags="2:3")),
        ("gmm(y,3:5); X exog-iv", dict(gmm_lags="3:5")),
        ("gmm(y,2:2); X exog-iv", dict(gmm_lags="2:2")),
        ("gmm(y,2:4); FDI tien dinh gmm(2:3)", dict(pre=["FDI"])),
        ("gmm(y,2:4); FDI+kiem soat noi sinh gmm(2:3)", dict(pre=x)),
        ("gmm(y,3:5); FDI+kiem soat gmm(3:4)", dict(gmm_lags="3:5", pre=x, pre_lags="3:4")),
        ("Difference GMM (nolevel), X exog-iv", dict(nolevel=True)),
        ("Difference GMM (nolevel), X noi sinh gmm(2:3)", dict(nolevel=True, pre=x)),
    ]
    rows = []
    for label, kw in variants:
        try:
            m = est.sgmm_fit(d, x, "tmp", "H1", "NONE", **kw)
            c, f, dg = m["coef"][est.LAG], m["coef"]["FDI"], m["diag"]
            rows.append({"spec": label, "L1_b": c["b"], "L1_se": c["se"], "FDI_b": f["b"], "FDI_p": f["p"],
                         "ar1_p": dg["ar1_p"], "ar2_p": dg["ar2_p"], "hansen_p": dg["hansen_p"],
                         "n_instr": dg["n_instr"], "nobs": m["nobs"]})
        except Exception as ex:  # ghi lại lỗi thay vì bỏ qua
            rows.append({"spec": label, "error": repr(ex)[:120]})
    return pd.DataFrame(rows)


def candidates(d, x, lo, hi):
    """D14: 3 ứng viên cố định, tiêu chí ghi trước kết quả. Trả (bảng, ứng viên được chọn hoặc None)."""
    cands = [("C0", "MAIN: gmm(y,2:4), X ngoại sinh", dict()),
             ("C1", "FDI tiền định gmm(FDI,2:3)", dict(pre=["FDI"])),
             ("C2", "FDI+lnY,URB,TO,Crdt nội sinh gmm(.,2:3)", dict(pre=x))]
    rows, fits = [], {}
    for cid, label, kw in cands:
        m = est.sgmm_fit(d, x, f"H1_SGMM_{cid}", "H1", "NONE", diffh=True, **kw)
        c, dg, f = m["coef"][est.LAG], m["diag"], m["coef"]["FDI"]
        dh = dg.get("diffhansen_p")
        ok = {"AR2>0.05": dg["ar2_p"] > 0.05, "0.1<Hansen<0.9": 0.1 < dg["hansen_p"] < 0.9,
              "DiffH>0.05": dh is not None and dh > 0.05, "L1 trong cận Bond": lo <= c["b"] <= hi}
        rows.append({"cand": cid, "spec": label, "L1_b": c["b"], "L1_se": c["se"], "L1_lo": dg["L1_lo"], "L1_hi": dg["L1_hi"],
                     "p_rho1": dg["p_rho1"], "FDI_b": f["b"], "FDI_p": f["p"], "ar2_p": dg["ar2_p"], "hansen_p": dg["hansen_p"],
                     "diffhansen_p": dh, "diffhansen_df": dg.get("diffhansen_df"), "n_instr": dg["n_instr"], **ok,
                     "dat_ca_4": all(ok.values())})
        fits[cid] = m
    df = pd.DataFrame(rows)
    ok_ids = [r["cand"] for r in rows if r["dat_ca_4"]]
    chosen = max(ok_ids, key=lambda c: ["C0", "C1", "C2"].index(c)) if ok_ids else None
    return df, chosen, fits


def run():
    df = est.panel()
    d, x = est.spec(df, "H1")
    models = [est.sgmm_fit(d, x, "H1_SGMM_NONE", "H1", "NONE", diffh=True),
              est.static_fit(d, x, "POLS", "H1_POLSDYN_NONE", "H1", "NONE", dynamic=True),
              est.static_fit(d, x, "FE", "H1_FEDYN_NONE", "H1", "NONE", dynamic=True, return_res=True)]
    m_fe, r_fe = models[2]
    m_fe["longrun"] = {"FDI": est.longrun(r_fe, "FDI")}
    models[2] = m_fe
    for k in IQ:
        d2, x2 = est.spec(df, "H2", k)
        models.append(est.sgmm_fit(d2, x2, f"H2_SGMM_{k}", "H2", k, diffh=True))
        d3, x3 = est.spec(df, "H3", k)
        models.append(est.sgmm_fit(d3, x3, f"H3_SGMM_{k}", "H3", k, with_vcov_pair=("FDI", f"FDIx{k}"), diffh=True))
    # [A5] FE động cho H2 (7 IQ) + hệ số dài hạn
    fedyn = []
    for k in IQ_ALL:
        d2, x2 = est.spec(df, "H2", k)
        m, r = est.static_fit(d2, x2, "FE", f"H2_FEDYN_{k}", "H2", k, dynamic=True, return_res=True)
        m["longrun"] = {"FDI": est.longrun(r, "FDI"), k: est.longrun(r, k)}
        fedk = est.static_fit(d2, x2, "FEDK", f"tmp_{k}", "H2", k)
        m["sign_same_as_fedk"] = bool(m["coef"][k]["b"] * fedk["coef"][k]["b"] > 0)
        m["fedk_iq_b"] = fedk["coef"][k]["b"]
        fedyn.append(m)
    models += fedyn
    # [C1 vòng 3] H3_FEDYN_k (7 IQ): FE hai chiều + L1.lnCO2, SE cụm theo nước; vcov_pair cho ME (est=FEDYN ở s06)
    for k in IQ_ALL:
        d3, x3 = est.spec(df, "H3", k)
        m, r = est.static_fit(d3, x3, "FE", f"H3_FEDYN_{k}", "H3", k, dynamic=True, return_res=True)
        m["vcov_pair"] = est.fedk_pair(r, "FDI", f"FDIx{k}")
        m["longrun"] = {"FDI": est.longrun(r, "FDI"), f"FDIx{k}": est.longrun(r, f"FDIx{k}")}
        models.append(m)
    pd.DataFrame([{"model": m["id"], "var": n, **c, **m["diag"], "nobs": m["nobs"]}
                  for m in models for n, c in m["coef"].items()]).to_csv(TABLES / "sgmm_main.csv", index=False)
    pd.DataFrame([{"model": m["id"], "var": n, **v} for m in models for n, v in m.get("longrun", {}).items()]
                 ).to_csv(TABLES / "longrun_fedyn.csv", index=False)
    sens = sensitivity(d, x)
    sens.to_csv(TABLES / "sgmm_sensitivity_H1.csv", index=False)

    by = {m["id"]: m for m in models}
    lo, hi = by["H1_FEDYN_NONE"]["coef"][est.LAG]["b"], by["H1_POLSDYN_NONE"]["coef"][est.LAG]["b"]
    s = by["H1_SGMM_NONE"]["coef"][est.LAG]["b"]
    cand, chosen, _ = candidates(d, x, lo, hi)
    cand.to_csv(TABLES / "sgmm_candidates_H1.csv", index=False)
    mc, ah = s08_verify.run_all_checks(d, x)
    ur = s09_unitroot.run_tests(df)
    ur.to_csv(TABLES / "unit_root.csv", index=False)

    f2 = lambda v: "n/a" if v is None else f"{v:.3f}"
    lines = ["# s05 System GMM (2 bước, collapse, Windmeijer, dummy năm) — vòng 2",
             f"- Cận Bond: FE động {lo:.3f} <= SGMM {s:.3f} <= POLS động {hi:.3f}? {'ĐẠT' if lo <= s <= hi else 'KHÔNG ĐẠT'}",
             "| model | L1 [KTC95%] | p(ρ=1) | FDI b (p) | AR2 | Hansen | DiffH | #iv |", "|---|---|---|---|---|---|---|---|"]
    for m in models[:3]:
        c, dg = m["coef"], m["diag"]
        l1 = f"{c[est.LAG]['b']:.3f}" + (f" [{dg['L1_lo']:.2f}, {dg['L1_hi']:.2f}]" if dg else "")
        lines.append(f"| {m['id']} | {l1} | {f2(dg.get('p_rho1'))} | {c['FDI']['b']:+.4f} ({c['FDI']['p']:.3f}) | "
                     f"{f2(dg.get('ar2_p'))} | {f2(dg.get('hansen_p'))} | {f2(dg.get('diffhansen_p'))} | {dg.get('n_instr', '')} |")
    for h in ("H2", "H3"):
        ms = [m for m in models if m["estimator"] == "SGMM" and m["hyp"] == h]
        rg = lambda f: f"{min(f(m) for m in ms):.3f}–{max(f(m) for m in ms):.3f}"
        dh = [m["diag"].get("diffhansen_p") for m in ms]
        dhs = "n/a" if None in dh else f"{min(dh):.3f}–{max(dh):.3f}"
        lines.append(f"- {h}_SGMM (6 IQ; bảng đủ ở sgmm_main.csv): L1 {rg(lambda m: m['coef'][est.LAG]['b'])}, "
                     f"KTC95% cận dưới {rg(lambda m: m['diag']['L1_lo'])}, p(ρ=1) {rg(lambda m: m['diag']['p_rho1'])}, "
                     f"AR2 {rg(lambda m: m['diag']['ar2_p'])}, Hansen {rg(lambda m: m['diag']['hansen_p'])}, DiffH {dhs}")
    lines += ["- A3 Ứng viên theo D14 (tiêu chí ghi trước): AR2>.05; .1<Hansen<.9; DiffH>.05; L1 trong cận Bond",
              "| cand | L1 | p(ρ=1) | FDI p | AR2 | Hansen | DiffH | đạt 4/4 |", "|---|---|---|---|---|---|---|---|"]
    for _, r in cand.iterrows():
        lines.append(f"| {r.cand} {r.spec[:22]} | {r.L1_b:.3f} | {r.p_rho1:.3f} | {r.FDI_p:.3f} | {r.ar2_p:.2f} | "
                     f"{r.hansen_p:.2f} | {f2(None if pd.isna(r.diffhansen_p) else r.diffhansen_p)} | {'CÓ' if r.dat_ca_4 else 'KHÔNG'} |")
    lines.append(f"  → Ứng viên được chọn theo D14: {chosen or 'KHÔNG CÓ (giữ C0 kèm hạn chế; câu hỏi Q1 cho tác giả)'}")
    lines.append(f"- Nhạy cảm công cụ H1 ({len(sens)} đặc tả, sgmm_sensitivity_H1.csv): L1 ∈ [{sens['L1_b'].min():.3f}, {sens['L1_b'].max():.3f}]")
    lines += s08_verify.summary_lines(mc, ah)
    lines += s09_unitroot.summary_lines(ur)
    lines += ["- A5 FE động H2 (T=21: lệch Nickell ≈ −(1+ρ)/T): | IQ | ρ | b(IQ) p | dài hạn IQ (se) | dấu như FEDK? |"]
    for m in fedyn:
        k = m["iq"]
        lr = m["longrun"][k]
        lines.append(f"  {k}: ρ {m['coef'][est.LAG]['b']:.3f}; {m['coef'][k]['b']:+.4f} ({m['coef'][k]['p']:.3f}); "
                     f"{lr['b']:+.3f} ({lr['se']:.3f}); {'giữ dấu' if m['sign_same_as_fedk'] else 'ĐỔI dấu'} (FEDK {m['fedk_iq_b']:+.4f})")
    h3 = [m for m in models if m["id"].startswith("H3_FEDYN_")]
    lines.append("- C1 H3_FEDYN (7 IQ, SE cụm): FDIxk b (p): " + "; ".join(
        f"{m['iq']} {m['coef']['FDIx' + m['iq']]['b']:+.4f} ({m['coef']['FDIx' + m['iq']]['p']:.3f})" for m in h3))
    save_summary("s05", chr(10).join(lines) + chr(10))
    return models, {"sgmm_candidates": cand.to_dict("records"), "sgmm_candidate_chosen": chosen}


if __name__ == "__main__":
    run()
    print(open(common.SUMM / "s05.md", encoding="utf-8").read())
