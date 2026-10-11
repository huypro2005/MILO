# Review iter 2 — CONTINUE (chặn bởi Q1: cần tác giả chọn nhánh A/B trước vòng 3)
## Điểm rubric (tổng 17/22 = 77%; R3 là P1 = 0 → chưa hội tụ). Chấm theo rubric đã sửa vòng này
| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 Pipeline | 2 | checks FAIL=0; đủ mô hình bắt buộc + H2_FEDYN_k |
| R2 Hợp lệ SGMM | 2 | AR(2) p 0,495–0,535; Hansen 0,58–0,67 (đặc tả chính); #iv 29–31; DiffH 0,30–0,41 |
| R3 Động học | 0 | SGMM ρ=1,084 [0,97; 1,20], ngoài cận [0,851; 0,984]; 12/12 đặc tả (9 nhạy cảm + C0–C2) vi phạm; đã có KTC, p(ρ=1)=0,156, DiffH → phần báo cáo đủ, nhưng tiêu chí chính không đạt; lên 1 nếu tác giả chọn nhánh A |
| R4 Chẩn đoán tĩnh | 1 | Mundlak χ²(5)=20,75 p=0,0009 → FE ✔; nhưng CIPS lnCO2 (xu thế) p=0,38, lnY p=0,80 không bác bỏ I(1), FDI I(0) → FEDK tĩnh chưa kiểm tra dừng phần dư/đồng liên kết (nguy cơ hồi quy giả mạo) |
| R5 Liêm chính | 2 | D14 ghi trước khi chạy; áp đúng: không chọn C1 dù FDI p=0,009; không thử thêm biến thể; báo mọi ứng viên |
| R6 H1 | 1 | SGMM +0,0007 (p 0,37; winsor p 0,14); FEDK +0,0059 (p 0,005; winsor +0,0082); FEDYN +0,0014 (p 0,018), dài hạn +0,0092 (p 0,031); AH +0,0008 (p 0,47) → kết luận phụ thuộc Q1 |
| R7 H2 | 2 | Bảng 7 IQ × FEDK/SGMM/FEDYN; FEDK âm có ý nghĩa ở GE/RQ/PV, nhưng FE động: 7/7 ns, 6/7 đổi dấu → đã giải thích được nguồn ngược dấu (bỏ sót động học) |
| R8 H3 + ME | 2 | ME 5 phân vị có SE; SGMM 0/5 mọi IQ; FEDK PV ME +0,010→+0,0027 (p90 ns) |
| R9 Vững | 1 | Bảng vững có, nhưng quy tắc D15f gắn "KHÔNG VỮNG" cho H3 vì đổi dấu của hệ số ≈0, ns cả hai bên (\|b\|<0,004) → gây hiểu nhầm |
| R10 Tái lập | 2 | meta.versions đủ 7 gói; seed 20240229; tóm tắt ≤38 dòng |
| R11 Xác minh | 2 | MC 200 lần: bias SGMM +0,030/+0,009, DGMM −0,004/−0,001; AH-mức 1,184 [0,95; 1,42] → ρ>1 là đặc tính dữ liệu |
## Trạng thái giả thuyết
| H | Trạng thái | Lý do ngắn |
|---|---|---|
| H1 | CHƯA ĐỦ BẰNG CHỨNG | Nhánh A (SGMM chính): theo SPEC = BÁC BỎ (p 0,37). Nhánh B (FE động): nghiêng ỦNG HỘ Haven nhưng nhỏ (+1 điểm % GDP FDI → +0,14% CO₂ ngắn hạn, ~+0,9% dài hạn); cần jackknife + SE DK |
| H2 | CHƯA ĐỦ BẰNG CHỨNG (nghiêng BÁC BỎ) | Khác biệt giữa k chỉ có ở FEDK tĩnh (mô hình bỏ sót động học, Y có thể I(1)); mọi mô hình động (SGMM, FEDYN) 7/7 không ý nghĩa ở 5% |
| H3 | BÁC BỎ (5/6 k); PV chờ FE động | SGMM 0/7 tương tác, 0/5 ME; FEDK chỉ FDI×PV −0,0038*** (winsor −0,0042***), ME không đổi dấu trong vùng dữ liệu; chưa có H3_FEDYN |
## KHUYẾN NGHỊ cho Q1: chọn NHÁNH B (ước lượng chính = FE động hai chiều, SE Driscoll–Kraay, hiệu chỉnh lệch Nickell bằng split-panel jackknife), giữ SGMM làm kiểm định vững có ghi hạn chế
Lý do: (1) cận Bond vi phạm ở 12/12 đặc tả, IV độc lập (AH) cũng 1,18 → không phải lỗi công cụ; (2) ρ không khác 1 + CIPS không bác bỏ I(1) → giả định dừng theo trung bình của phương trình mức (cốt lõi SGMM) đáng ngờ; DiffH df 1–3 công suất thấp nên p=0,40 không bảo chứng; (3) T=21 không còn "T nhỏ": lệch Nickell ≈ −(1+ρ)/T ≈ −0,09 cho ρ và nhỏ hơn cho β(X), hiệu chỉnh được; (4) ρ≥1 làm hệ số dài hạn β/(1−ρ) của SGMM vô nghĩa → không trả lời được câu hỏi chính sách. Rủi ro: đổi sau khi đã thấy FE có ý nghĩa giống "chọn kết quả đẹp" → bắt buộc ghi tiêu chí trước (A/B-1) và báo SGMM song song; lưu ý nhánh B KHÔNG làm kết quả "đẹp hơn" đồng đều (H2 mất ý nghĩa ở FE động). Nhánh A hợp lệ nếu dàn bài/hội đồng bắt buộc SGMM, nhưng H1 sẽ bị bác bỏ bởi một ước lượng mà chính ta chứng minh là thiếu tin cậy.
## ACTION cho vòng 3 (chung C1–C2 + một nhánh; ≤6/nhánh)
- [C1][P1] H3_FEDYN_k (7 IQ; FE hai chiều + L1.lnCO2; SE cụm VÀ Driscoll–Kraay) + ME tại 5 phân vị IQ (delta) → marginal_effects.csv cột est=FEDYN. — Lý do: H3-PV hiện chỉ dựa vào FEDK tĩnh. — Xong khi: 7 mô hình trong estimates.json, s06 có dòng FEDYN, nêu PV còn ý nghĩa không.
- [C2][P1] Dừng phần dư cho mô hình tĩnh: CIPS (p-value MC như D15b) trên phần dư FE hai chiều của H1 và H2_k; báo cùng CIPS phần dư FEDYN. — Lý do: lnCO2, lnY không bác bỏ I(1) → FEDK tĩnh có thể giả mạo. — Xong khi: bảng resid_unit_root.csv + s04; nếu phần dư không dừng → ghi DECISIONS: FEDK tĩnh chỉ là tham chiếu.
- [C3][P3] Sửa quy tắc vững D15f theo R9 mới (dấu chỉ tính khi ≥1 bên p<0,10) bằng dòng DECISIONS mới, chạy lại bảng s07 (không đổi mô hình). — Xong khi: s07 có cột "kết luận theo quy tắc mới", H3 không còn "KHÔNG VỮNG" do hệ số ns≈0.
**Nhánh A — giữ SGMM (C0) làm chính:**
- [A-1][P1] Khoá C0 (D18: lý do = D14/D17 + quyết định tác giả); bỏ mọi tính dài hạn từ SGMM; s05 thêm mục "Hạn chế" 5 dòng (ρ KTC, AH, CIPS, sim, cận Bond). — Xong khi: D18 có, meta.main_estimator=SGMM, s05 có mục Hạn chế.
- [A-2][P2] Kiểm định vững động: FEDYN-DK + jackknife (như B-2) cho H1–H3 làm phụ lục. — Xong khi: bảng so SGMM vs FEDYN-jackknife cho FDI, IQk, FDI×IQk.
**Nhánh B — chuyển ước lượng chính sang FE động:**
- [B-1][P1] TRƯỚC khi chạy: D18 ghi lý do chẩn đoán (cận Bond 12/12, AH, CIPS) + tiêu chí ủng hộ mới (H1: β(FDI) p<0,05 ở FEDYN-DK VÀ cùng dấu ở jackknife + FEDK; H2/H3 như SPEC với FEDYN-DK); thừa nhận đã thấy FEDYN SE cụm (FDI p=0,018). Orchestrator sửa SPEC mục 1/4/6 (thêm EST `FEDYNDK`), meta.main_estimator. — Xong khi: D18 + SPEC cập nhật trước commit code.
- [B-2][P1] FEDYNDK cho H1, H2_k, H3_k (15 mô hình) + split-panel jackknife (Dhaene–Jochmans 2015: 2β̂ − (β̂_T1+β̂_T2)/2, chia theo năm) cho ρ và mọi β; dài hạn delta trên ρ jackknife. — Xong khi: estimates.json có 15 FEDYNDK + trường `jackknife`; ρ_jk<1 và KTC báo.
- [B-3][P2] Vững đối với nghiệm đơn vị/xu thế riêng: (i) mô hình sai phân đầu ΔlnCO2 (ΔlnY, ΔURB, ΔTO, ΔCrdt, FDI, IQk, dummy năm, SE DK); (ii) FEDYN có xu thế tuyến tính riêng từng nước. Quy tắc diễn giải ghi trong D18. — Xong khi: bảng robust_dyn.csv, s07 thêm 2 cột.
## CHECKS_REQUEST
1. Gộp 23 WARN LAG_GE1 thành 1 dòng tóm tắt (số mô hình, khoảng ρ) — giữ mức WARN/FAIL như cũ; hiện gây nhiễu che các WARN khác.
2. RESID_UR: WARN nếu CIPS lnCO2 (trường hợp chính) p>0,05 mà thiếu `tests.resid_cips_p`; WARN nếu resid p>0,10.
3. Bảng điểm giả thuyết đọc `meta.main_estimator` (cột chính = FEDYNDK nếu nhánh B; luôn kèm cột SGMM, FEDK).
4. JACKKNIFE (nhánh B): FAIL nếu main=FEDYNDK mà thiếu `jackknife` hoặc ρ_jk ≥ 1.
## Tự cải thiện (đã sửa EVAL_RUBRIC.md)
- R3: thêm mức 1 khi vi phạm là đặc tính dữ liệu đã chứng minh + tác giả chấp nhận; tiêu chí cho FE động chính (ρ<1 + hiệu chỉnh Nickell). R4: yêu cầu dừng phần dư/đồng liên kết khi Y I(1). R9: quy tắc vững theo kết luận. +3 bẫy (hồi quy không cân bằng; đổi ước lượng chính hậu nghiệm; mô phỏng chỉ DGP dừng). Nhật ký vòng 2.
- Tự phê bình vòng 1: (a) A2 yêu cầu nghiệm đơn vị nhưng không nêu hệ quả cho mô hình tĩnh (đồng liên kết) → bỏ sót, nay thành C2; (b) A1 chỉ yêu cầu DGP dừng nên xác minh được code nhưng không giải thích vì sao DGMM 1,24>POLS trên dữ liệu thật; (c) A6 không đặt quy tắc vững → modeler tự đặt D15f có lỗi diễn giải; (d) vòng 1 chấm R7=1 vì "ngược dấu chưa giải thích" — đúng hướng, A5 đã giải thích được.
## Câu hỏi cho tác giả
1. **Q1 (chặn vòng 3)**: Nhánh A (giữ SGMM chính + hạn chế) hay **Nhánh B (khuyến nghị: FE động DK + jackknife chính, SGMM là vững)**? Nhánh B cần sửa dàn bài mục phương pháp (Chương 3).
2. Q2 vẫn mở: D1 (lnY là mức GDP/người) và D8 (tiêu chí "đang phát triển").
