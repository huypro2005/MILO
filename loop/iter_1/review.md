# Review iter 1 — CONTINUE
## Điểm rubric (tổng 13/22 = 59%; R3, R11 là P1 = 0 → chưa hội tụ)
| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 Pipeline | 2 | run_all ~9s không lỗi; 51 mô hình; checks FAIL=0 |
| R2 Hợp lệ SGMM | 2 | AR(2) p=0,50–0,58; Hansen p=0,58–0,67; #iv 29–31 ≤ 73 |
| R3 Động học | 0 | L1=1,084 (se 0,059) ngoài cận [FE 0,851; POLS 0,984]; 23 WARN LAG_GE1; 9/9 biến thể nhạy cảm L1∈[1,039; 1,244]; chưa có KTC, H0 ρ=1, diff-Hansen |
| R4 Chẩn đoán tĩnh | 1 | Có đủ 4 kiểm định; nhưng Hausman phi-robust (p=5e-8) trong khi het p=0, Wooldridge p=3e-24; CD p=0,38 với \|ρ\| TB 0,47 |
| R5 Liêm chính | 2 | Không đổi đặc tả; D10–D13 đủ lý do; báo cả 9 đặc tả nhạy cảm, tự cảnh báo FDI p=0,009 chỉ ở biến thể FDI tiền định |
| R6 H1 | 1 | FEDK +0,0059 (p=0,005), SGMM +0,0007 (p=0,37) cùng dấu; nhưng SGMM chính chưa tin cậy (R3) → chưa diễn giải Haven/Halo |
| R7 H2 | 1 | Đủ bảng 7 IQ; FEDK âm (GE −0,115***, RQ −0,084***, PV −0,040**), SGMM dương ns ở cả 7 → ngược dấu chưa giải thích |
| R8 H3 + ME | 2 | ME delta-method tại 5 phân vị, vcov Windmeijer; IQ* báo đủ; SGMM 0/5 phân vị ý nghĩa ở mọi IQ |
| R9 Vững | 1 | Đã chạy IQ_PCA + winsorize; thiếu kết luận "vững/không vững" theo từng H; H3w_SGMM_GE FDI p=0,027 vs gốc 0,089 chưa bàn |
| R10 Tái lập | 1 | Tóm tắt ≤ 24 dòng; meta không ghi phiên bản thư viện |
| R11 Xác minh bộ ước lượng (mới) | 0 | Difference GMM ρ=1,244 > POLS 0,984 — trái lý thuyết (DGMM lệch xuống khi công cụ yếu); pydynpd đã vá (D7) chưa được kiểm |
## Trạng thái giả thuyết
| H | Trạng thái | Lý do ngắn |
|---|---|---|
| H1 | CHƯA ĐỦ BẰNG CHỨNG | Theo SPEC chưa đạt (SGMM p=0,37), nhưng SGMM vi phạm động học (ρ>1) nên chưa thể bác bỏ; FEDK +0,0059*** (vững winsor +0,0082***) nghiêng Haven, quy mô nhỏ (+1 điểm % GDP → +0,6% CO₂) |
| H2 | CHƯA ĐỦ BẰNG CHỨNG | FEDK: khác biệt mức ý nghĩa giữa k (GE/RQ/PV có, RL/VA không) → ủng hộ một phần; SGMM tất cả ns và ngược dấu FEDK ở 7/7 |
| H3 | CHƯA ĐỦ BẰNG CHỨNG (nghiêng BÁC BỎ) | SGMM 0/7 tương tác p<0,05, ME 0/5 phân vị; FEDK chỉ PV (−0,0038***, vững winsor −0,0042***) |
## ACTION cho vòng 2
- [A1][P1] Xác minh pydynpd đã vá: mô phỏng panel AR(1) N=73, T=21, ρ=0,8 (và 0,95), hiệu ứng cố định + 1 X ngoại sinh, seed cố định; chạy SGMM & DGMM cùng cú pháp chính; thêm ước lượng Anderson–Hsiao (Δy trên ΔL1.y, công cụ L2.y, linearmodels IV2SLS) trên dữ liệu thật. — Lý do: DGMM 1,24 > POLS là dấu hiệu lỗi cài đặt; không được diễn giải SGMM khi chưa loại trừ. — Xong khi: bảng sim (ρ thật, ρ̂ SGMM/DGMM, bias) + AH trên dữ liệu thật trong s05.md; nếu bias > 0,05 → ghi DECISIONS và dừng hỏi tác giả.
- [A2][P1] Tính bền/nghiệm đơn vị: CIPS (Pesaran 2007) hoặc IPS cho lnCO2, lnY, FDI; báo KTC 95% L1 và Wald H0: ρ=1 cho mọi SGMM (hiện z≈(1,084−1)/0,059≈1,42 → không bác bỏ ρ=1). — Lý do: sd_within lnCO2 = 0,24 ≪ between 1,32; ρ≈1 làm công cụ mức yếu và hiệu ứng dài hạn β/(1−ρ) vô nghĩa. — Xong khi: bảng unit root + cột L1_lo, L1_hi, p(ρ=1) trong s05.md.
- [A3][P1] Difference-in-Hansen (C-test) cho nhóm công cụ phương trình mức (giả định dừng điều kiện ban đầu) ở SGMM chính và 2 biến thể "X tiền định". TRƯỚC khi chạy, ghi vào DECISIONS quy tắc chọn đặc tả dựa trên lý thuyết/chẩn đoán (vd: lnY, Crdt nội sinh do nhân quả ngược; tiêu chí: AR2>0,05, 0,1<Hansen<0,9, diff-Hansen>0,05, L1 trong cận Bond) — KHÔNG dựa vào p của FDI. — Xong khi: diff-Hansen p cho 3 đặc tả + dòng DECISIONS có quy tắc ghi trước kết quả.
- [A4][P2] Hausman bền vững: kiểm định Mundlak (thêm trung bình nhóm của X vào RE, Wald cluster-robust). — Lý do: het p=0, AR p=3e-24 → Hausman cổ điển không hợp lệ, V gần suy biến (eig −9e-9). — Xong khi: tests.hausman_robust_p trong estimates.json + s03.md.
- [A5][P2] Cầu nối giải thích ngược dấu H2: ước lượng H2_FEDYN_k (FE động, 7 IQ) + hệ số dài hạn β/(1−ρ) có SE delta-method cho FEDYN (ρ<1). — Lý do: FEDK tĩnh vs SGMM động không so trực tiếp; cần biết dấu âm FE còn khi thêm động học không. — Xong khi: bảng 7 dòng trong s05.md, nêu dấu có giữ không.
- [A6][P3] s07.md thêm bảng "vững/không vững" theo H (gốc vs IQ_PCA vs winsor: cùng dấu? cùng mức ý nghĩa?); meta ghi phiên bản python/numpy/pydynpd/linearmodels, seed. — Xong khi: checks đọc được meta.versions.
## CHECKS_REQUEST
1. LAG_CI: WARN nếu KTC 95% của L1.lnCO2 nằm hoàn toàn trên 1 (FAIL nếu cả SGMM chính); báo p(ρ=1).
2. HANSEN_HIGH trên bảng sgmm_sensitivity_*.csv: WARN nếu hansen_p > 0,9 (hiện 2/9 biến thể: 0,903; 0,958).
3. DIFF_HANSEN: WARN nếu thiếu diag.diffhansen_p ở SGMM chính, FAIL nếu < 0,05.
4. DGMM_GT_POLS: WARN nếu bất kỳ DGMM nào có ρ > POLS động.
5. META_VERSIONS: WARN nếu meta thiếu versions.
## Tự cải thiện (đã sửa gì trong EVAL_RUBRIC.md)
- R3: thêm KTC, H0 ρ=1, diff-Hansen. R4: bắt buộc Hausman bền vững. R10: phiên bản thư viện. Thêm R11 (P1) xác minh bộ ước lượng.
- Thêm 5 bẫy: DGMM>POLS; so cận Bond bằng điểm; chọn hậu nghiệm biến thể p<0,05; Hansen tăng vọt; Hausman cổ điển khi có khuyết tật. Ghi nhật ký vòng 1.
- Tự phê bình vòng 0 (STATE A2): yêu cầu coi mọi X là iv ngoại sinh khiến vòng 1 không có đặc tả nội sinh nào được chọn trước; lẽ ra phải đặt quy tắc chọn đặc tả từ đầu → nay thành A3.
## Câu hỏi cho tác giả
1. Nếu A1/A2 cho thấy lnCO2 gần nghiệm đơn vị (ρ không khác 1) và SGMM không vào cận Bond ở mọi đặc tả hợp lý: chấp nhận báo cáo SGMM kèm hạn chế, hay chuyển ước lượng chính sang FEDK/FE động (cần sửa dàn bài)?
2. D1 (lnY là mức GDP/người, không phải tốc độ tăng) và D8 (tiêu chí "đang phát triển") vẫn ⏳ — cần xác nhận để viết Chương 3.
