# SPEC — Đặc tả nghiên cứu (nguồn sự thật duy nhất)

> Đề tài: Tác động của FDI đến phát thải CO₂: vai trò điều tiết của chất lượng thể chế tại các quốc gia đang phát triển.
> Tác giả: Võ Thị Linh Nhi. Mọi agent đọc file này TRƯỚC khi làm việc. Chỉ sửa khi có quyết định mới trong DECISIONS.md.

## 1. Giả thuyết → bằng chứng cần có
| H | Phát biểu | Mô hình | Hệ số kiểm định | Bằng chứng ủng hộ |
|---|---|---|---|---|
| H1 | FDI tác động đáng kể đến CO₂ | M1 | β(FDI) | p<0,05 ở FEDYNDK (chính) + jackknife cùng dấu + FEDK cùng dấu |
| H2 | Từng khía cạnh thể chế tác động khác biệt đến CO₂ | M2 × 6 (CC, GE, PV, RQ, RL, VA) | β(IQk) | FEDYNDK: ≥1 khía cạnh p<0,05 và các k khác nhau về dấu/mức ý nghĩa |
| H3 | Thể chế điều tiết quan hệ FDI–CO₂ | M3 × 6 | β(FDI×IQk) | FEDYNDK p<0,05 + jackknife cùng dấu + ME P10 vs P90 khác nhau có ý nghĩa |
| Vững | IQ_PCA; winsorize FDI; SGMM; sai phân đầu; xu thế riêng từng nước | | như trên | Quy tắc D18 |

**Ước lượng chính = FEDYNDK** (FE động hai chiều, SE Driscoll–Kraay, jackknife) — DECISIONS D18 (tác giả chọn nhánh B).

"Chứng minh" ở đây = **kiểm định**. Bác bỏ giả thuyết cũng là kết quả hợp lệ. CẤM chỉnh mô hình chỉ để có p<0,05 (xem mục 7).

## 2. Dữ liệu
- File: `DATA_FINAL.xlsx`, sheet `Sheet1` (dữ liệu), `MA_BIEN` (mã biến + danh sách nước).
- Bảng cân bằng: 73 nước × 21 năm (2002–2022) = 1.533 quan sát, không thiếu giá trị.
- Ngoại lai: FDI từ −37,2 đến 55,1 (% GDP) → kiểm tra vững bằng winsorize 1%/99%.

## 3. Biến (sau biến đổi trong `code/common.py::load_panel`)
| Tên trong code | Ý nghĩa | Ghi chú |
|---|---|---|
| lnCO2 | ln(CO₂ bình quân đầu người, tấn) | biến phụ thuộc |
| FDI | FDI ròng vào, % GDP | để dạng mức (có giá trị âm) |
| CC GE PV RQ RL VA | 6 chỉ số WGI (−2,5…+2,5) | biến điều tiết |
| IQ_PCA | PC1 của 6 WGI chuẩn hoá | chỉ dùng cho kiểm định vững |
| lnY | ln(GDP bình quân đầu người, USD 2015) | xem DECISIONS D1 |
| URB, TO, Crdt | đô thị hoá, độ mở thương mại, tín dụng tư nhân (% ) | kiểm soát |
| FDI_c, {k}_c, FDIx{k} | biến trung tâm hoá & tương tác | dùng trong M3 |

## 4. Mô hình
- M1: lnCO2 = f(FDI, lnY, URB, TO, Crdt) + μᵢ + λₜ
- M2: M1 + IQk
- M3: lnCO2 = f(FDI_c, IQk_c, FDIxIQk, kiểm soát) + μᵢ + λₜ
- Dạng động (ước lượng chính FEDYNDK và SGMM): thêm L1.lnCO2. Hệ số dài hạn = β/(1−ρ_jk), SE delta.
- Tác động biên H3: ∂lnCO2/∂FDI = β(FDI) + β(FDIxIQk)·(IQk − mean IQk), tính tại các phân vị 10/25/50/75/90 của IQk kèm SE (delta method).

## 5. Quy trình (theo dàn bài 1.5) — file code tương ứng
| Bước | Nội dung | File |
|---|---|---|
| 1 | Thống kê mô tả | code/s01_describe.py |
| 2 | Tương quan + VIF | code/s02_corr_vif.py |
| 3 | POLS / FE / RE, Hausman | code/s03_static.py |
| 4 | Kiểm định khuyết tật: phương sai thay đổi, tự tương quan (Wooldridge), phụ thuộc chéo (Pesaran CD) → FE Driscoll–Kraay (FEDK) | code/s04_diagnostics.py |
| 5–8 | FEDYNDK + jackknife (chính) và SGMM (vững) cho H1, H2, H3 | code/s05_gmm.py |
| 9 | Tác động biên H3 | code/s06_marginal.py |
| 10 | Vững: IQ_PCA, winsorize FDI, sai phân đầu, xu thế riêng từng nước | code/s07_robust.py |
| — | Chạy toàn bộ | `python code/run_all.py` |
| — | Kiểm thử tự động (KHÔNG sửa) | `python code/checks.py` |

Công cụ: `linearmodels` (PanelOLS/RandomEffects/PooledOLS, `cov_type="kernel"` cho Driscoll–Kraay), `pydynpd` cho SGMM, `statsmodels` cho VIF.
Cú pháp SGMM mẫu đã chạy được:
`regression.abond("lnCO2 L1.lnCO2 FDI lnY URB TO Crdt | gmm(lnCO2, 2:4) iv(FDI lnY URB TO Crdt) | collapse timedumm", df, ["Country","Year"])`
Luôn dùng `collapse` (N=73 nhỏ → giữ số công cụ ≤ số nhóm).

## 6. Hợp đồng đầu ra `results/estimates.json` (checks.py đọc file này)
Ghi bằng `common.save_estimates(models, tests, meta)`.
```json
{"meta": {"iteration": 3, "main_estimator": "FEDYNDK"},
 "models": [{"id": "H3_SGMM_CC", "hyp": "H3", "estimator": "SGMM", "iq": "CC",
   "nobs": 1387, "ngroups": 73,
   "coef": {"L1.lnCO2": {"b": 0.9, "se": 0.05, "p": 0.0}, "FDI": {...}, "CC": {...}, "FDIxCC": {...}},
   "diag": {"ar1_p": 0.0, "ar2_p": 0.5, "hansen_p": 0.6, "n_instr": 29}}],
 "tests": {"hausman_p": 0.0, "wooldridge_ar1_p": 0.0, "het_p": 0.0, "pesaran_cd_p": 0.0, "vif_max": 3.2}}
```
- `id` = `{H}_{EST}_{IQ}`; EST ∈ POLS, FE, RE, FEDK, SGMM, POLSDYN, FEDYN, FEDYNDK; IQ ∈ NONE, CC…VA, IQ_PCA.
- Tên hệ số luôn là `FDI`, `<k>`, `FDIx<k>` (dù trong M3 dùng biến trung tâm hoá) — để checks.py so được.
- Bắt buộc có: H1_{POLS,FE,RE,FEDK,SGMM,POLSDYN,FEDYN}_NONE; H2_{FEDK,SGMM,FEDYNDK}_{k}, H3_{FEDK,SGMM,FEDYNDK}_{k} (và H1_FEDYNDK_NONE) với k ∈ 6 WGI + IQ_PCA.
- `meta.main_estimator` quyết định cột chính trong bảng điểm (SGMM mặc định). Nếu là ước lượng FE động, mỗi mô hình chính phải có `"jackknife": {"L1.lnCO2": {"b":..,"se":..}, "FDI": {...}}`; `tests.resid_cips_p` = CIPS phần dư mô hình tĩnh H1.
- Bảng tác động biên: `results/tables/marginal_effects.csv` (cột: iq, pct, iq_value, me, se, p).

## 7. Quy tắc liêm chính (chống p-hacking)
1. Chỉ được đổi đặc tả khi có **lý do phương pháp** (kiểm định chẩn đoán không đạt, lý thuyết), không phải vì kết quả không ý nghĩa.
2. Mọi thay đổi → ghi vào `knowledge/DECISIONS.md` (lý do, vòng lặp).
3. Báo cáo tất cả đặc tả đã thử, kể cả đặc tả cho kết quả "xấu".
4. Đặc tả chính (FEDYNDK, D18) được khoá; sau đó chỉ thêm kiểm định vững, không thay.
