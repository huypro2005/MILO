# Checks — FAIL (FAIL=1, WARN=7)

Ký hiệu: *** p<.01, ** p<.05, * p<.10, ns không ý nghĩa

- **WARN** `LAG_GE1`: 23 SGMM có L1.lnCO2 ≥ 1 (khoảng 1.072–1.084)
- **FAIL** `JACKKNIFE`: 23 mô hình FEDYNDK có ρ_jk ≥ 1 (khoảng 1.027–1.040), KTC chứa 1 — chờ tác giả xác nhận D25
- **WARN** `LONGRUN_UNCORR`: 23 mô hình có longrun_uncorrected với ρ_jk ≥ 1 — KHÔNG dùng trong báo cáo
- **WARN** `BOND_BOUND`: SGMM L1=1.084 nằm ngoài [FE 0.851, POLS 0.984]
- **WARN** `sgmm_sensitivity_H1:HANSEN_HIGH`: 'gmm(y,2:4); FDI+kiem soat noi sinh gmm(2:3)' Hansen p=0.903 > 0.9
- **WARN** `sgmm_sensitivity_H1:HANSEN_HIGH`: 'gmm(y,3:5); FDI+kiem soat gmm(3:4)' Hansen p=0.958 > 0.9
- **WARN** `sgmm_sensitivity_H1:DGMM_GT_POLS`: 'Difference GMM (nolevel), X exog-iv' ρ=1.244 > POLS động 0.984
- **WARN** `sgmm_sensitivity_H1:DGMM_GT_POLS`: 'Difference GMM (nolevel), X noi sinh gmm(2:3)' ρ=1.084 > POLS động 0.984
- PASS `H1_SGMM_NONE:RHO_EQ1`: ρ=1.084, KTC95%=[0.968, 1.199], z(ρ=1)=1.42

## Bảng điểm giả thuyết

| H | Biến | FEDYNDK (chính) | SGMM | FEDK | Cùng dấu? |
|---|---|---|---|---|---|
| H1 | FDI | +0.0014 ** | +0.0007 ns | +0.0059 *** | có |
| H2 | CC | -0.0126 ns | +0.0212 ns | -0.0559 * | **KHÔNG** |
| H2 | GE | +0.0021 ns | +0.0101 ns | -0.1154 *** | **KHÔNG** |
| H2 | PV | +0.0143 ns | +0.0165 * | -0.0401 ** | **KHÔNG** |
| H2 | RQ | +0.0068 ns | +0.0124 ns | -0.0842 *** | **KHÔNG** |
| H2 | RL | +0.0178 ns | +0.0092 ns | -0.0274 ns | **KHÔNG** |
| H2 | VA | +0.0172 ns | +0.0148 ns | -0.0305 ns | **KHÔNG** |
| H2 | IQ_PCA | +0.0045 ns | +0.0053 * | -0.0269 ** | **KHÔNG** |
| H3 | FDIxCC | -0.0001 ns | +0.0011 ns | -0.0021 ns | **KHÔNG** |
| H3 | FDIxGE | +0.0008 ns | +0.0036 ns | -0.0005 ns | **KHÔNG** |
| H3 | FDIxPV | -0.0006 ns | -0.0006 ns | -0.0038 *** | có |
| H3 | FDIxRQ | +0.0009 ns | +0.0002 ns | +0.0027 ns | có |
| H3 | FDIxRL | +0.0004 ns | +0.0000 ns | -0.0005 ns | **KHÔNG** |
| H3 | FDIxVA | +0.0006 ns | +0.0003 ns | -0.0028 ns | **KHÔNG** |
| H3 | FDIxIQ_PCA | +0.0001 ns | +0.0002 ns | -0.0005 ns | **KHÔNG** |
