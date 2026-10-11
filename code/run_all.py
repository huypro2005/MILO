"""Chạy toàn bộ pipeline s01–s07 và ghi results/estimates.json.
Thứ tự: s01..s05, s07, rồi s06 (s06 cần các mô hình H3 của s07 để tính tác động biên cho IQ_PCA/winsorize)."""
import platform
import sys
import time
from importlib import metadata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import common  # noqa: E402  (trước pydynpd)
import s01_describe, s02_corr_vif, s03_static, s04_diagnostics, s05_gmm, s06_marginal, s07_robust, s08_verify, s09_unitroot, s10_fedyndk  # noqa: E402,E401


def main():
    t0 = time.time()
    models, tests = [], {}
    for name, mod in [("s01", s01_describe), ("s02", s02_corr_vif), ("s03", s03_static), ("s04", s04_diagnostics),
                      ("s05", s05_gmm), ("s10", s10_fedyndk), ("s07", s07_robust)]:
        m, t = mod.run()
        models += m
        tests.update(t)
        print(f"{name} xong ({time.time() - t0:.0f}s): +{len(m)} mô hình", flush=True)
    s07_robust.verdicts(models)  # bảng vững (D22) + vững động, cần mô hình của s04/s05/s07/s10
    d18 = s10_fedyndk.verdicts(models)  # kết luận cơ học theo tiêu chí D18
    s06_marginal.run(models)
    print(f"s06 xong ({time.time() - t0:.0f}s)", flush=True)
    versions = {"python": platform.python_version(),
                **{p: metadata.version(p) for p in ("numpy", "pandas", "scipy", "statsmodels", "pydynpd", "linearmodels")}}
    tests["d18_verdict"] = d18
    meta = {"iteration": 3, "main_estimator": "FEDYNDK", "versions": versions,
            "seeds": {"montecarlo_pydynpd": s08_verify.SEED, "montecarlo_unitroot": s09_unitroot.SEED,
                      "montecarlo_resid_cips": s09_unitroot.SEED + 3,
                      "mc_reps": {"pydynpd": s08_verify.REPS, "unitroot": s09_unitroot.MC_REPS}},
            "sgmm_spec": "gmm(lnCO2,2:4) collapse timedumm, 2-step Windmeijer; X = iv ngoại sinh",
            "fedk": "PanelOLS entity+time effects, kernel (Driscoll-Kraay)",
            "fedyndk": "PanelOLS entity+time effects + L1.lnCO2, kernel (Driscoll-Kraay); split-panel jackknife 2002-2012/2012-2022 (D18, D23)"}
    common.save_estimates(models, tests, meta)
    print(f"estimates.json: {len(models)} mô hình")


if __name__ == "__main__":
    main()
