# Run iter 2
## Đã làm (ứng với từng ACTION-id)
- **A1** code/s08_verify.py (gọi từ s05; bảng sim_pydynpd.csv, anderson_hsiao.csv; seed 20240229, 200 lần, N=73,T=21). Bias ρ̂: ρ=0,8: SGMM +0,030, DGMM −0,004, FE −0,019, POLS +0,181; ρ=0,95: SGMM +0,009, DGMM −0,001, FE −0,017, POLS +0,031 → bias < 0,05, pydynpd đã vá KHÔNG lỗi hệ thống (D16). Anderson–Hsiao dữ liệu thật: AH-mức ρ̂=1,184 (se 0,120; KTC 0,95–1,42; F1=18,6; FDI +0,0008 p=0,47) cũng >1; AH-vi phân suy biến (F1≈0, bỏ qua). ⇒ ρ>1 là đặc tính dữ liệu, không phải lỗi cài đặt.
- **A2** code/s09_unitroot.py (unit_root.csv; p-value Monte Carlo 1000 lần đúng N,T). Trường hợp chính: lnCO2 CIPS −2,28 (p_mc 0,38), lnY CIPS −2,02 (p 0,80) → KHÔNG bác bỏ nghiệm đơn vị (có xu thế); FDI CIPS −2,35 (p 0,003) → dừng. Lưu ý lnCO2 chỉ hằng số: CIPS p≈0,02 (bác bỏ) nên bằng chứng lnCO2 hơi hỗn hợp. KTC95% và p(ρ=1) đã vào diag mọi SGMM: H1 ρ=1,084 [0,97; 1,20], p(ρ=1)=0,156 (không bác bỏ ρ=1); H2/H3 cận dưới 0,96–0,97, p 0,16–0,19.
- **A3** Ghi D14 (quy tắc) TRƯỚC khi chạy. Diff-Hansen (tự tính J_sys−J_diff) p: C0 MAIN 0,400; C1 FDI tiền định 0,392; C2 mọi X nội sinh 0,704 → đạt. Nhưng L1 ngoài cận Bond ở cả 3 (1,084/1,043/1,039; C2 còn Hansen 0,904>0,9) → KHÔNG ứng viên đạt 4/4; theo D14 giữ C0 kèm hạn chế (D17). Mọi SGMM H2/H3 có diffhansen_p 0,30–0,41. Bảng: sgmm_candidates_H1.csv.
- **A4** s03: Mundlak (RE+dummy năm+trung bình nhóm, Wald cụm) chi2(5)=20,75, tests.hausman_robust_p=0,0009 → bác bỏ RE, ủng hộ FE (cổ điển p=5e-8 giữ như thông tin).
- **A5** H2_FEDYN_k (7 IQ) trong estimates.json; ρ FE động 0,850–0,854 (<1). Hệ số IQ trong FE động: CC −0,0126 (p 0,48) giữ dấu âm; GE/PV/RQ/RL/VA/IQ_PCA ĐỔI sang dương, đều ns (p 0,30–0,90). Dài hạn (delta): IQ −0,083…+0,120, se 0,09–0,12, không có ý nghĩa; FDI dài hạn H1 +0,0092 (se 0,0042, p 0,031). ⇒ dấu âm của FEDK KHÔNG bền khi thêm động học (chủ yếu mất ý nghĩa). longrun_fedyn.csv.
- **A6** s07.md thêm bảng vững/không vững (quy tắc D15f). meta.versions (python/numpy/pandas/scipy/statsmodels/pydynpd/linearmodels) + seeds trong run_all.
## Kết quả checks.py: WARN (FAIL=0, WARN=28)
- 23 LAG_GE1 (mọi SGMM ρ 1,07–1,08); BOND_BOUND (1,084 ngoài [0,851; 0,984]); 2 HANSEN_HIGH (biến thể nhạy cảm 0,903; 0,958); 2 DGMM_GT_POLS (1,244; 1,084). PASS RHO_EQ1 (z=1,42). DIFF_HANSEN và META_VERSIONS đã hết WARN.
## Thay đổi đặc tả (đã ghi DECISIONS: D14–D17)
- Không đổi đặc tả chính. D14 quy tắc chọn đặc tả; D15 chi tiết triển khai; D16 kết quả A1; D17 kết quả A3.
## Vấn đề/Đề xuất
1. Q1 cần tác giả: ρ không phân biệt được với 1, SGMM không vào cận Bond ở mọi đặc tả hợp lý, AH-mức cũng 1,18, CIPS không bác bỏ nghiệm đơn vị của lnCO2/lnY (có xu thế) → đề xuất xem xét ước lượng chính FEDK/FE động (sai phân đầu cho lnCO2 hoặc xu thế riêng từng nước) thay vì SGMM; ngoài phạm vi ACTION nên chưa chạy.
2. Bảng vững: H1 vững; H2 FEDK vững dấu nhưng khác ý nghĩa (3/6); H3 KHÔNG vững theo quy tắc, song các hệ số tương tác ≈0 (|b|<0,004) nên đổi dấu vô nghĩa thống kê; H3 FDI chính SGMM-GE p đổi 0,089→0,027 (winsor).
3. Diff-Hansen tính bằng hiệu J với DGMM (df chỉ 1–3, công suất thấp), không phải C-test từng nhóm; hạn chế cần nêu trong luận văn.
4. Thời gian chạy run_all tăng ~45–60s do mô phỏng.
