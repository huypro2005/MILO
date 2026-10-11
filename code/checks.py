"""Bộ kiểm thử tự động của vòng lặp nghiên cứu (harness).
KHÔNG do modeler sửa. Chỉ evaluator đề xuất thêm kiểm tra (ghi vào EVAL_RUBRIC.md),
orchestrator mới sửa file này.
Đầu ra: results/checks.json + results/summaries/checks.md (bảng điểm giả thuyết)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import ESTIMATES, IQ_ALL, RESULTS, ROOT, TABLES, load_panel, save_summary  # noqa: E402

import pandas as pd  # noqa: E402

ALPHA = 0.05
MAIN_SGMM = "H1_SGMM_NONE"
DECISIONS = ROOT / "knowledge" / "DECISIONS.md"
MAIN = "SGMM"  # ghi đè bằng meta.main_estimator khi đọc estimates.json
REQUIRED = [f"H1_{e}_NONE" for e in ["POLS", "FE", "RE", "FEDK", "SGMM", "POLSDYN", "FEDYN", "FEDYNDK"]]
REQUIRED += [f"{h}_{e}_{k}" for h in ["H2", "H3"] for e in ["FEDK", "SGMM", "FEDYNDK"] for k in IQ_ALL]  # FEDYNDK: D18

out = []  # (mức, mã, thông điệp)


def add(level, cid, msg):
    out.append({"level": level, "id": cid, "msg": msg})


def p_of(m, name):
    c = (m or {}).get("coef", {}).get(name)
    return None if c is None else c.get("p")


def b_of(m, name):
    c = (m or {}).get("coef", {}).get(name)
    return None if c is None else c.get("b")


def star(p):
    if p is None:
        return "—"
    return "***" if p < .01 else "**" if p < .05 else "*" if p < .10 else "ns"


def fmt(b, p):
    return "thiếu" if b is None else f"{b:+.4f} {star(p)}"


def check_data():
    df = load_panel()
    if len(df) != 1533 or df["Country"].nunique() != 73:
        add("FAIL", "DATA_SHAPE", f"Kỳ vọng 1533 quan sát/73 nước, có {len(df)}/{df['Country'].nunique()}")
    if df[["lnCO2", "FDI", "lnY"] + IQ_ALL].isna().any().any():
        add("FAIL", "DATA_NA", "Có giá trị thiếu sau biến đổi")


def check_models(models, tests):
    by = {m["id"]: m for m in models}
    missing = [r for r in REQUIRED if r not in by]
    if missing:
        add("FAIL", "MISSING_MODELS", f"Thiếu {len(missing)} mô hình: {', '.join(missing[:8])}{'…' if len(missing) > 8 else ''}")

    lag_ge1 = []
    for m in models:
        if m.get("estimator") != "SGMM":
            continue
        d, mid = m.get("diag", {}), m["id"]
        if d.get("ar2_p") is None or d.get("hansen_p") is None:
            add("FAIL", f"{mid}:DIAG", "Thiếu ar2_p/hansen_p")
            continue
        if d["ar2_p"] < ALPHA:
            add("FAIL", f"{mid}:AR2", f"AR(2) p={d['ar2_p']:.3f} < 0.05 → công cụ không hợp lệ")
        if d.get("ar1_p") is not None and d["ar1_p"] >= ALPHA:
            add("WARN", f"{mid}:AR1", f"AR(1) p={d['ar1_p']:.3f} không ý nghĩa (kỳ vọng có)")
        if d["hansen_p"] < ALPHA:
            add("FAIL", f"{mid}:HANSEN", f"Hansen p={d['hansen_p']:.3f} < 0.05 → bác bỏ tính ngoại sinh công cụ")
        elif d["hansen_p"] > 0.99:
            add("WARN", f"{mid}:HANSEN_HI", f"Hansen p={d['hansen_p']:.3f} ≈ 1 → dấu hiệu quá nhiều công cụ")
        if d.get("n_instr") and m.get("ngroups") and d["n_instr"] > m["ngroups"]:
            add("FAIL", f"{mid}:NINSTR", f"Số công cụ {d['n_instr']} > số nhóm {m['ngroups']}")
        lag = b_of(m, "L1.lnCO2")
        if lag is not None and lag >= 1:
            lag_ge1.append(lag)
        # [vòng 1, CHECKS_REQUEST 1] KTC 95% của ρ nằm hoàn toàn trên 1
        se = (m["coef"].get("L1.lnCO2") or {}).get("se")
        if lag is not None and se:
            lo, z1 = lag - 1.96 * se, (lag - 1) / se
            if lo > 1:
                add("FAIL" if mid == MAIN_SGMM and MAIN == "SGMM" else "WARN", f"{mid}:LAG_CI", f"KTC95% ρ=[{lo:.3f}, {lag + 1.96 * se:.3f}] > 1")
            elif mid == MAIN_SGMM:
                add("PASS", f"{mid}:RHO_EQ1", f"ρ={lag:.3f}, KTC95%=[{lo:.3f}, {lag + 1.96 * se:.3f}], z(ρ=1)={z1:.2f}")
        # [vòng 1, CHECKS_REQUEST 3] Difference-in-Hansen cho công cụ phương trình mức
        if mid == MAIN_SGMM:
            dh = d.get("diffhansen_p")
            if dh is None:
                add("WARN", f"{mid}:DIFF_HANSEN", "Thiếu diag.diffhansen_p")
            elif dh < ALPHA:
                add("FAIL", f"{mid}:DIFF_HANSEN", f"Diff-Hansen p={dh:.3f} < 0.05 → công cụ mức không hợp lệ")

    # [vòng 2, CHECKS_REQUEST 1] gộp LAG_GE1 thành một dòng
    if lag_ge1:
        add("WARN", "LAG_GE1", f"{len(lag_ge1)} SGMM có L1.lnCO2 ≥ 1 (khoảng {min(lag_ge1):.3f}–{max(lag_ge1):.3f})")

    # [vòng 2, CHECKS_REQUEST 2] dừng phần dư của mô hình tĩnh
    rc = tests.get("resid_cips_p")
    if rc is None:
        add("WARN", "RESID_UR", "Thiếu tests.resid_cips_p (lnCO2/lnY có thể I(1) → FEDK tĩnh có nguy cơ hồi quy giả mạo)")
    elif rc > 0.10:
        add("WARN", "RESID_UR", f"CIPS phần dư p={rc:.3f} > 0.10 → phần dư không dừng")

    # [vòng 3, CHECKS_REQUEST 1] nhánh B: jackknife bắt buộc; ρ_jk ≥ 1 chỉ chấp nhận khi KTC chứa 1,
    # tác giả đã xác nhận hạn chế ρ≈1 (dòng D25 có ✅) và không báo hệ số dài hạn jackknife
    if MAIN != "SGMM":
        d25 = [ln for ln in DECISIONS.read_text(encoding="utf-8").splitlines() if ln.startswith("| D25 ")]
        d25_ok = bool(d25) and "✅" in d25[0]
        ge1 = []
        for m in (x for x in models if x.get("estimator") == MAIN):
            jk = (m.get("jackknife") or {}).get("L1.lnCO2") or {}
            b, lo_jk = jk.get("b"), jk.get("lo")
            if b is None:
                add("FAIL", f"{m['id']}:JACKKNIFE", "Thiếu jackknife['L1.lnCO2']")
            elif lo_jk is not None and lo_jk > 1:
                add("FAIL", f"{m['id']}:JACKKNIFE", f"KTC dưới ρ_jk={lo_jk:.3f} > 1 (bùng nổ)")
            elif b >= 1:
                ge1.append((b, bool(m.get("longrun"))))
        if ge1:
            rng = f"{len(ge1)} mô hình {MAIN} có ρ_jk ≥ 1 (khoảng {min(g[0] for g in ge1):.3f}–{max(g[0] for g in ge1):.3f}), KTC chứa 1"
            if d25_ok and not any(g[1] for g in ge1):
                add("WARN", "JACKKNIFE", rng + " — đã chấp nhận là hạn chế (D25)")
            else:
                add("FAIL", "JACKKNIFE", rng + (" — có longrun jackknife khác rỗng" if d25_ok else " — chờ tác giả xác nhận D25"))

    # [vòng 3, CHECKS_REQUEST 2] hệ số dài hạn không hợp lệ khi ρ gần/chứa 1
    uncorr = []
    for m in models:
        rho = (m.get("jackknife") or {}).get("L1.lnCO2") or (m.get("coef") or {}).get("L1.lnCO2") or {}
        rb, rse = rho.get("b"), rho.get("se")
        near1 = rb is not None and (rb >= 0.97 or (rse and rb - 1.96 * rse <= 1 <= rb + 1.96 * rse))
        if m.get("longrun") and near1:
            add("FAIL", f"{m['id']}:LONGRUN_INVALID", f"longrun tính với ρ={rb:.3f} (≥0,97 hoặc KTC chứa 1)")
        if m.get("longrun_uncorrected") and rb is not None and rb >= 1:
            uncorr.append(m["id"])
    if uncorr:
        add("WARN", "LONGRUN_UNCORR", f"{len(uncorr)} mô hình có longrun_uncorrected với ρ_jk ≥ 1 — KHÔNG dùng trong báo cáo")

    # Cận Bond (2002): FE động < SGMM < POLS động
    s, lo, hi = (b_of(by.get(i), "L1.lnCO2") for i in ["H1_SGMM_NONE", "H1_FEDYN_NONE", "H1_POLSDYN_NONE"])
    if None not in (s, lo, hi):
        if not (lo <= s <= hi):
            add("WARN", "BOND_BOUND", f"SGMM L1={s:.3f} nằm ngoài [FE {lo:.3f}, POLS {hi:.3f}]")
        else:
            add("PASS", "BOND_BOUND", f"SGMM L1={s:.3f} ∈ [{lo:.3f}, {hi:.3f}]")

    # [vòng 1, CHECKS_REQUEST 2 & 4] Bảng nhạy cảm công cụ
    for f in sorted(TABLES.glob("sgmm_sensitivity_*.csv")):
        sens = pd.read_csv(f)
        for _, r in sens[sens["hansen_p"] > 0.9].iterrows():
            add("WARN", f"{f.stem}:HANSEN_HIGH", f"'{r['spec']}' Hansen p={r['hansen_p']:.3f} > 0.9")
        if hi is not None:
            dg = sens[sens["spec"].str.contains("Difference|nolevel|DGMM", case=False)]
            for _, r in dg[dg["L1_b"] > hi].iterrows():
                add("WARN", f"{f.stem}:DGMM_GT_POLS", f"'{r['spec']}' ρ={r['L1_b']:.3f} > POLS động {hi:.3f}")

    if tests.get("vif_max") is not None and tests["vif_max"] > 10:
        add("WARN", "VIF", f"VIF max={tests['vif_max']:.1f} > 10")
    if not (TABLES / "marginal_effects.csv").exists():
        add("FAIL", "MARGINAL", "Thiếu results/tables/marginal_effects.csv")
    return by


def scoreboard(by):
    # [vòng 2, CHECKS_REQUEST 3] cột chính theo meta.main_estimator, luôn kèm SGMM và FEDK
    ests = list(dict.fromkeys([MAIN, "SGMM", "FEDK"]))
    head = [f"{e} (chính)" if e == MAIN else e for e in ests]
    rows = ["| H | Biến | " + " | ".join(head) + " | Cùng dấu? |", "|---" * (len(ests) + 3) + "|"]

    def row(h, var, suffix):
        bs = [b_of(by.get(f"{h}_{e}_{suffix}"), var) for e in ests]
        ps = [p_of(by.get(f"{h}_{e}_{suffix}"), var) for e in ests]
        known = [b for b in bs if b is not None]
        same = "—" if len(known) < 2 else ("có" if all(b > 0 for b in known) or all(b < 0 for b in known) else "**KHÔNG**")
        rows.append(f"| {h} | {var} | " + " | ".join(fmt(b, p) for b, p in zip(bs, ps)) + f" | {same} |")

    row("H1", "FDI", "NONE")
    for k in IQ_ALL:
        row("H2", k, k)
    for k in IQ_ALL:
        row("H3", f"FDIx{k}", k)
    return rows


def main():
    check_data()
    by = {}
    if not ESTIMATES.exists():
        add("FAIL", "NO_ESTIMATES", "Chưa có results/estimates.json")
    else:
        est = json.loads(ESTIMATES.read_text(encoding="utf-8"))
        global MAIN
        MAIN = est.get("meta", {}).get("main_estimator", "SGMM")
        by = check_models(est.get("models", []), est.get("tests", {}))
        if not est.get("meta", {}).get("versions"):  # [vòng 1, CHECKS_REQUEST 5]
            add("WARN", "META_VERSIONS", "meta thiếu versions (python/numpy/pydynpd/linearmodels)")

    n_fail = sum(o["level"] == "FAIL" for o in out)
    n_warn = sum(o["level"] == "WARN" for o in out)
    status = "FAIL" if n_fail else ("WARN" if n_warn else "PASS")
    (RESULTS / "checks.json").write_text(json.dumps({"status": status, "items": out}, indent=1, ensure_ascii=False), encoding="utf-8")

    lines = [f"# Checks — {status} (FAIL={n_fail}, WARN={n_warn})", "",
             "Ký hiệu: *** p<.01, ** p<.05, * p<.10, ns không ý nghĩa", ""]
    lines += [f"- **{o['level']}** `{o['id']}`: {o['msg']}" for o in out if o["level"] != "PASS"][:30]
    lines += [f"- PASS `{o['id']}`: {o['msg']}" for o in out if o["level"] == "PASS"]
    if by:
        lines += ["", "## Bảng điểm giả thuyết", ""] + scoreboard(by)
    save_summary("checks", "\n".join(lines) + "\n")
    print("\n".join(lines))
    return 0 if status != "FAIL" else 1


if __name__ == "__main__":
    sys.exit(main())
