# Run iter 1
## Đã làm (ứng với từng ACTION-id)
- **A1** Xây pipeline: code/est.py (hàm dùng chung), s01_describe, s02_corr_vif, s03_static, s04_diagnostics, s05_gmm, s06_marginal, s07_robust, run_all.py. Chạy ~9 giây, không lỗi; estimates.json có 51 mô hình (đủ 7 H1 + H2/H3 x {FEDK,SGMM} x 7 IQ, thêm 13 mô hình winsorize H1w/H3w). Tóm tắt: results/summaries/s01–s07.md; bảng: results/tables/*.csv.
- **A2** SGMM đúng cú pháp mẫu (gmm(lnCO2,2:4) iv(tất cả X) collapse timedumm; IQk, FDIxIQk là iv ngoại sinh). Mọi SGMM có ar1_p, ar2_p, hansen_p, n_instr (29–31 ≤ 73). AR(2) p=0,50–0,58; Hansen p=0,58–0,67. Lấy chỉ số qua mod.regression_table, mod.hansen, mod.AR_list, mod.z_information.num_instr, mod.num_obs, mod.N.
- **A3** s06: ME tại P10/25/50/75/90 bằng delta method; vcov SGMM lấy từ mod.step_results[-1].vcov (pydynpd CÓ trả vcov, đã hiệu chỉnh Windmeijer; thứ tự = regression_table), FEDK từ res.cov. File results/tables/marginal_effects.csv (iq,pct,iq_value,me,se,p,est) + marginal_effects_winsor.csv. s06 chạy SAU s07.
## Kết quả checks.py: WARN (FAIL=0, WARN=24)
- 23 WARN LAG_GE1 (mọi SGMM có L1.lnCO2 ≈ 1,07–1,08; H1: 1,084) + WARN BOND_BOUND: SGMM 1,084 ngoài [FE động 0,851; POLS động 0,984].
- Không FAIL; MISSING_MODELS/NO_ESTIMATES/MARGINAL đã hết. VIF max = 3,92 (6 WGI chung: 8,22).
## Kết quả chính (để evaluator đánh giá)
- Chẩn đoán M1: Hausman p=5e-8 (V chỉ xác định gần dương, eig min ≈ -9e-9); Wald nhóm p=0; Wooldridge AR(1) p=3e-24; Pesaran CD p=0,38 (không bác bỏ dù |rho| TB=0,47).
- H1: FDI FE-DK +0,0059 (p=0,005), FE +0,0059 (p=0,035); SGMM +0,0007 (p=0,37, ns); POLS/FE động +0,0012/+0,0014 (p~0,015). Cùng dấu, nhưng SGMM không có ý nghĩa.
- H2: SGMM IQk dương (ns, riêng PV p=0,08, IQ_PCA p=0,09), FEDK IQk âm (GE, RQ, PV, CC*, PCA có ý nghĩa) → ngược dấu ở cả 7 IQ.
- H3: tương tác chỉ có ý nghĩa ở FEDK-PV (-0,0038, p<0,001); SGMM không có tương tác nào p<0,05. ME SGMM: 0/5 phân vị có ý nghĩa ở mọi IQ (trừ GE đổi dấu p10→p90, ns); ME FEDK luôn dương, giảm theo IQ ở PV/CC/VA.
- Winsorize FDI: FEDK vẫn dương (+0,008); SGMM FDI +0,0016 (p=0,14).
## Thay đổi đặc tả (đã ghi DECISIONS: D10–D13)
- Không đổi đặc tả; D10–D13 chỉ ghi chi tiết triển khai (hiệu ứng thời gian, Hausman, winsorize, CD) và hiện trạng SGMM.
## Vấn đề/Đề xuất
1. SGMM L1>1 và ngoài cận Bond là vấn đề chính (D9 xác nhận). Bảng results/tables/sgmm_sensitivity_H1.csv (9 đặc tả, không dùng để chọn kết quả): L1 từ 1,04 đến 1,24 ở MỌI biến thể (gmm 2:3, 3:5, 2:2; X tiền định gmm(2:3); Difference GMM nolevel) → công cụ mức trễ yếu/giả định dừng của hiệu ứng nước (hệ thống) có thể bị vi phạm; chưa có biến thể nào vào cận Bond. Đề xuất evaluator: cân nhắc X tiền định + 3:5, bỏ năm 2020 (COVID) hoặc xác minh pydynpd bằng phần mềm khác (xtabond2) trước khi kết luận.
2. FDI p=0,009 chỉ khi coi FDI tiền định (gmm 2:3) — khác biệt do đặc tả công cụ, không được dùng để chốt kết quả (SPEC mục 7).
3. FEDK vs SGMM ngược dấu ở H2 (mọi IQ): cần giải thích (FE khử hiệu ứng nước; SGMM dùng biến đổi mức qua công cụ yếu).
4. Pesaran CD không bác bỏ trong khi |rho| TB cao: cân nhắc kiểm định CD tín hiệu (Pesaran 2015/Frees) nếu cần biện minh FEDK; hiện biện minh bằng Wald + Wooldridge.
5. Thứ tự run_all: s07 trước s06 (s06 cần mô hình H3 của s07).
