# Run iter 3
## Đã làm (ứng với từng ACTION-id)
- **C1** (s05, s06): 7 mô hình `H3_FEDYN_k` (FE 2 chiều + L1.lnCO2, SE cụm; có vcov_pair) + ME 5 phân vị est=FEDYN trong marginal_effects.csv. H3 FEDYN: FDI×k 0/7 p<0,05 (PV −0,0006, p=0,327). ME theo PV: p10 +0,0021 (p=0,043) → p90 +0,0009 (p=0,147): KHÔNG đổi dấu, tương tác PV KHÔNG còn ý nghĩa ở FE động (chỉ FEDK tĩnh −0,0038***).
- **C2** (s04, s09): CIPS phần dư u=y−Xb, MC 1000 lần đúng N=73,T=21 dưới null "không đồng liên kết" (D21, ghi trước) → results/tables/resid_unit_root.csv, `tests.resid_cips_p`. H1 tĩnh: CIPS −2,02 (tới hạn 5% −2,07), p_mc=0,083; H2_k: 0,080–0,130. KHÔNG bác bỏ I(1) → FEDK tĩnh chỉ là tham chiếu. Phần dư FEDYN (H1, H2): p_mc=0,001 (null thường, chỉ thông tin).
- **C3** (s07): quy tắc D22 (ghi trước); bảng s07 có cột cũ D15f và cột mới. H3 FEDYNDK vs IQ_PCA/winsor: "NS CẢ HAI/VỮNG DẤU" thay vì "KHÔNG VỮNG". Chỉ còn "KHÔNG VỮNG" nếu có cặp ngược dấu với p<0,10 (không có ở FEDYNDK).
- **B-2** (s10_fedyndk.py mới, est.py): 15 mô hình FEDYNDK (H1, H2×7, H3×7) + 8 bản winsorize (H1w, H3w×7), mỗi mô hình có `jackknife` (mọi hệ số, nửa mẫu 2002–12/2012–22, SE = SE DK mẫu đầy đủ), `longrun`, `longrun_uncorrected`; ME FEDYNDK (est=FEDYNDK) và ME jackknife (marginal_effects_jk.csv); meta.main_estimator="FEDYNDK". Bảng: fedyndk_main.csv, longrun_fedyndk.csv.
- **B-3** (s07): FD (ΔlnCO2, SE DK, năm) và FEDYNTR (FEDYN + xu thế riêng 72 nước, SE DK) cho 15 đặc tả → robust_dyn.csv, bảng (B) trong s07.md.
## Kết quả checks.py: FAIL (FAIL=23, WARN=6)
- 23 FAIL đều là `*:JACKKNIFE` "ρ_jackknife ≥ 1" (1,027–1,040): toàn bộ 23 mô hình FEDYNDK. Không có FAIL nào khác (MISSING_MODELS, AR2, Hansen đều đạt).
- WARN: LAG_GE1 (23 SGMM, 1,072–1,084), BOND_BOUND (SGMM 1,084 ngoài [0,851; 0,984]), HANSEN_HIGH ×2, DGMM_GT_POLS ×2 (đều là SGMM đã biết từ vòng 2). RESID_UR không WARN (p=0,083 ≤ 0,10).
- Bảng điểm (FEDYNDK chính): H1 FDI +0,0014** (SGMM +0,0007 ns; FEDK +0,0059***); H2 0/7 p<0,10 chính (PV +0,0143, p=0,106); H3 0/7 tương tác ns.
## Kết luận cơ học theo D18 (ghi trước)
- H1 ỦNG HỘ (p=0,021; jk +0,0016; FEDK +) — nhỏ: +1 điểm % GDP FDI → +0,14% CO₂ ngắn hạn; winsor vẫn p=0,026 (+0,0022). Nhưng hai nửa mẫu trái dấu (+0,0033 / −0,0011) và FD cho −0,0000 (p=0,98), FEDYNTR +0,0013 (p=0,06) → bảng vững động: "KHÔNG KẾT LUẬN".
- H2 KHÔNG ỦNG HỘ (0/6 khía cạnh p<0,05 ở FEDYNDK; dấu khác nhau nhưng mọi ns). H3 KHÔNG ỦNG HỘ (0/6; ME P90−P10 có p trùng p tương tác, 0,38–0,92).
## Thay đổi đặc tả (đã ghi DECISIONS: D21, D22, D23, D24)
- Không đổi đặc tả D18. D21/D22 là quy tắc ghi trước khi chạy; D23 là chi tiết triển khai (SE jackknife = SE DK đầy đủ; thêm winsorize cho FEDYNDK vì SPEC mục 1 yêu cầu vững winsorize).
## Vấn đề/Đề xuất
1. **ρ_jk = 1,03 [0,96; 1,10] ≥ 1 (FAIL JACKKNIFE)**: hiệu chỉnh Nickell đẩy ρ từ 0,851 lên 1,03; hai nửa mẫu (T=10) cho 0,67–0,68, tức độ lệch khớp công thức −(1+ρ)/T nên ρ thật ≈ 1 (nhất quán SGMM 1,08, AH 1,18, CIPS I(1)). KTC chứa 1 → không phân biệt được với nghiệm đơn vị; hệ số dài hạn β/(1−ρ) không xác định (R3 theo rubric vẫn chưa đạt). Cần evaluator/tác giả quyết: (a) thừa nhận ρ≈1 và diễn giải FEDYNDK như mô hình ngắn hạn/tăng trưởng (kèm FD), bỏ mọi tính dài hạn; hoặc (b) kiểm chứng jackknife bằng Monte Carlo ở ρ∈{0,95; 1} (chưa làm vì ngoài ACTION). KHÔNG đổi tiêu chí D18 để "qua" check.
2. Bằng chứng cho H1 mỏng: lệch ổn định chỉ ở FE động; FD ≈ 0 ngụ ý FDI ảnh hưởng mức chứ không ảnh hưởng tốc độ thay đổi; hai nửa mẫu trái dấu. Nên báo kết quả H1 là "ủng hộ yếu".
3. SE của jackknife dùng SE DK mẫu đầy đủ (xấp xỉ tiệm cận); bootstrap theo nước sẽ chặt chẽ hơn nếu cần.
4. FEDYNTR/FD ME và vcov không tính (FEDYNTR không có vcov_pair). Checks vẫn FAIL theo thiết kế cho tới khi quyết định mục 1.
