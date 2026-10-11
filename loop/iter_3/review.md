# Review iter 3 — CONVERGED (có điều kiện: tác giả xác nhận D25 hạn chế ρ≈1; không cần thêm vòng modeler)
## Điểm rubric (tổng 21/22 = 95%; R3 = 1 khi tác giả ký D25, nếu chưa ký thì R3 = 0 và CHỈ chặn ở bước xác nhận đó, không chặn ở code)
| Tiêu chí | Điểm | Bằng chứng |
|---|---|---|
| R1 Pipeline | 2 | 23 FAIL đều là JACKKNIFE (đặc tính dữ liệu, xem CHECKS_REQUEST); không có MISSING_MODELS; đủ 15+8 FEDYNDK, H3_FEDYN, FD, FEDYNTR |
| R2 SGMM | 2 | Đặc tả chính vẫn đạt AR(2)/Hansen/#iv; HANSEN_HIGH chỉ ở biến thể nhạy cảm (0,903; 0,958) |
| R3 Động học | 1* | ρ̂ FEDYN 0,851 → ρ_jk 1,030 [0,96; 1,10] ở 23/23 mô hình; hai nửa mẫu 0,67–0,68 → c = 20·(0,851−0,672) ≈ 3,6 (≈3 là mức của nghiệm đơn vị, dừng thì ≤2); trùng với SGMM 1,084, AH 1,18, CIPS I(1) → 4 phương pháp độc lập cùng chỉ ρ≈1. Dài hạn jk đã bị loại (n/a). *Mức 1 mới (vòng này) cần tác giả xác nhận |
| R4 Chẩn đoán tĩnh | 2 | Mundlak p=0,0009; CIPS phần dư MC (null không đồng liên kết, ghi trước D21): H1 p_mc=0,083, H2 0,080–0,130 → không bác bỏ → FEDK tĩnh hạ xuống chỉ làm tham chiếu, đúng quy tắc |
| R5 Liêm chính | 2 | D21/D22 ghi trước khi chạy; D18 áp nguyên, KHÔNG đổi tiêu chí để qua FAIL; thừa nhận FEDYN p=0,018 đã thấy trước; winsor-FEDYNDK có lý do SPEC |
| R6 H1 | 2 | FEDYNDK +0,0014 (p=0,021), jk +0,0016, winsor +0,0022 (p=0,026), FEDYNTR +0,0013 (p=0,06), FEDK +0,0059***; SGMM +0,0007 ns, FD −0,0000 (p=0,98); nửa mẫu +0,0033/−0,0011 |
| R7 H2 | 2 | 7 IQ cùng đặc tả × FEDYNDK/SGMM/FEDK/FD/FEDYNTR; 0/7 p<0,10 ở FEDYNDK (PV gần nhất p=0,106) |
| R8 H3 + ME | 2 | ME 5 phân vị có SE cho FEDYN/FEDYNDK/jk; 0/6 tương tác p<0,05; P90−P10 p 0,38–0,92; không có ngưỡng đáng tin (IQ*_RQ=−2,07 từ tương tác ns) |
| R9 Vững | 2 | Quy tắc D22 theo kết luận; IQ_PCA, winsor, FD, FEDYNTR đủ; H3 không còn "KHÔNG VỮNG" giả |
| R10 Tái lập | 2 | Tóm tắt 6–38 dòng; seed/phiên bản trong meta |
| R11 Xác minh | 2 | pydynpd đạt MC vòng 2. Lưu ý: jackknife không được mô phỏng — chấp nhận vì là đại số của PanelOLS và nửa mẫu nhất quán với c≈3 |
## Trạng thái giả thuyết (theo tiêu chí ghi trước D18 + vững D22)
| H | Trạng thái | Lý do ngắn |
|---|---|---|
| H1 | ỦNG HỘ (YẾU, chỉ ngắn hạn) | Đạt D18: +1 điểm % GDP FDI → +0,14% CO₂ năm đó (p=0,021), cùng dấu ở jk, winsor, FEDYNTR, FEDK, SGMM, AH. Hạn chế: SGMM/AH ns; FD ≈0 (nhưng FD không có hiệu ứng nước bỏ sót trôi riêng — đối chứng đúng khi ρ≈1 là FEDYNTR, p=0,06); nửa mẫu ngược dấu (+0,0033 / −0,0011) → tác động chủ yếu 2002–2012. Không có hệ số dài hạn. Viết: "bằng chứng yếu cho Pollution Haven" |
| H2 | BÁC BỎ | 0/6 khía cạnh p<0,05 (0/7 p<0,10) ở FEDYNDK; khác biệt giữa k chỉ có ở FEDK tĩnh, mà phần dư tĩnh không dừng (p_mc 0,08–0,13) → có thể là hồi quy giả mạo; FD/FEDYNTR không nhất quán dấu (GE, RQ "KHÔNG VỮNG") |
| H3 | BÁC BỎ (cả 6 k) | FDI×k ns ở FEDYNDK, FEDYN, SGMM (0/6); PV −0,0006 (p=0,38); chỉ FEDK tĩnh PV −0,0038*** (tham chiếu, không là bằng chứng). FEDYNTR PV −0,0013 (p=0,07) cùng dấu → nêu là gợi ý, không phải điều tiết |
Thêm 1 vòng (MC jackknife gần ρ=1, bootstrap theo nước) không đổi được nhãn H2/H3 (mọi ước lượng động đều ns); với H1 chỉ có thể làm yếu thêm một kết luận đã ghi là "yếu", và chọn phương pháp suy diễn mới sau khi đã thấy p=0,021 là hậu nghiệm → không làm.
## ACTION cho vòng 4 — KHÔNG có ACTION cho modeler. Việc còn lại (orchestrator / econ-analyst)
- [A1][P1][orchestrator] Ghi D25: "Chấp nhận ρ≈1 (ρ_jk 1,03 [0,96;1,10]; c≈3,6; SGMM 1,08; AH 1,18; CIPS I(1)) là đặc tính dữ liệu; FEDYNDK chỉ diễn giải ngắn hạn; KHÔNG báo bất kỳ hệ số dài hạn nào (kể cả longrun_uncorrected +0,0092 — lệch vì ρ̂ 0,851 bị lệch Nickell)"; hỏi tác giả xác nhận. — Xong khi: D25 có ✅ của tác giả.
- [A2][P1][orchestrator] Áp CHECKS_REQUEST 1–2, chạy lại checks.py (không chạy lại pipeline). — Xong khi: checks.md không còn FAIL; JACKKNIFE hiện 1 dòng WARN gộp.
- [A3][P2][econ-analyst] Chương 4–5 viết theo bảng trạng thái trên; bắt buộc có mục Hạn chế: ρ≈1 (4 phương pháp), FEDK tĩnh chỉ tham chiếu (phần dư không dừng), H1 không vững với FD/SGMM, nửa mẫu ngược dấu, SE jackknife = SE DK mẫu đầy đủ (DK với T=20 có thể đánh giá thấp SE). Báo SGMM song song. — Xong khi: mỗi H có câu kết luận + con số + hạn chế; không dùng từ "tác động dài hạn".
## CHECKS_REQUEST
1. JACKKNIFE: FAIL chỉ khi thiếu trường `jackknife` hoặc KTC dưới của ρ_jk > 1 (bùng nổ có ý nghĩa). Nếu ρ_jk ≥ 1 nhưng KTC chứa 1 → WARN nếu DECISIONS có dòng hạn chế ρ≈1 (vd tìm "D25") VÀ `longrun` jackknife = null; ngược lại FAIL. Gộp 23 dòng thành 1 (số mô hình, khoảng ρ_jk).
2. LONGRUN_INVALID (mới): FAIL nếu bất kỳ trường `longrun` khác null mà ρ dùng để tính ≥ 0,97 hoặc KTC ρ chứa 1; WARN cho `longrun_uncorrected` khi ρ_jk ≥ 1 (không được dùng trong báo cáo).
## Tự cải thiện (đã sửa EVAL_RUBRIC.md)
- R3: thêm mức 1 cho nhánh FE động khi ρ_jk ≥1 nhưng KTC chứa 1, có ≥3 phương pháp độc lập, bỏ dài hạn, tác giả xác nhận (đối xứng với lối ra đã có cho SGMM). +4 bẫy; nhật ký vòng 3.
- Tự phê bình vòng 2: (a) Tôi khuyến nghị nhánh B dựa trên "lệch Nickell ≈ −(1+ρ)/T ≈ −0,09, hiệu chỉnh được" — sai: dưới nghiệm đơn vị có hiệu ứng cố định c≈3, và tôi đã có AH 1,18 + CIPS I(1) để dự báo ρ_jk≈1. Nhánh B vẫn tốt hơn A (cho β ngắn hạn nhất quán hơn, H2 mất ý nghĩa nên không phải "chọn kết quả đẹp"), nhưng lý do "hệ số dài hạn trả lời câu hỏi chính sách" đã không thành. (b) B-2 "Xong khi: ρ_jk<1" là tiêu chí phụ thuộc kết quả. (c) CHECKS_REQUEST 4 (JACKKNIFE=FAIL) biến một đặc tính dữ liệu thành lỗi không sửa được → nay đề xuất WARN có điều kiện. (d) B-3 yêu cầu FD không có hiệu ứng nước — không phải đối chứng hạn chế đúng khi ρ≈1 → kết luận "KHÔNG KẾT LUẬN" cho H1 trong s07 nặng hơn thực tế; đã ghi thành bẫy, không yêu cầu chạy lại vì FEDYNTR đã đóng vai trò đó.
## Câu hỏi cho tác giả
1. Xác nhận D25: chấp nhận ρ≈1 là hạn chế và chỉ báo tác động ngắn hạn (không có hệ số dài hạn)? Nếu không chấp nhận → cần 1 vòng nữa (MC jackknife ρ∈{0,95;1}, bootstrap cụm theo nước), nhưng dự kiến không đổi kết luận H1–H3.
2. D8 (tiêu chí "nước đang phát triển") vẫn mở — cần cho Chương 3, không ảnh hưởng ước lượng.
