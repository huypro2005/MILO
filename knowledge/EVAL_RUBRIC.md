# EVAL_RUBRIC — Tiêu chí của evaluator (file sống, evaluator tự cải thiện)
Mỗi tiêu chí 0 (không đạt) · 1 (một phần) · 2 (đạt). Ngưỡng CONVERGED: không có tiêu chí P1 nào = 0, và tổng ≥ 80% điểm tối đa.

| # | Ưu tiên | Tiêu chí | Đạt (2) khi |
|---|---|---|---|
| R1 | P1 | Hoàn chỉnh pipeline | `run_all.py` chạy không lỗi; checks.py không có FAIL MISSING_MODELS |
| R2 | P1 | Hợp lệ SGMM | Mọi SGMM: AR(2) p>0,05, Hansen 0,05<p<0,99, số công cụ ≤ 73 |
| R3 | P1 | Động học hợp lý | Ước lượng động CHÍNH có ρ < 1 và (nếu là GMM) nằm trong cận Bond (FE động ≤ SGMM ≤ POLS động); báo KTC 95% của ρ và H0: ρ=1; có Difference-in-Hansen cho công cụ phương trình mức. **1 điểm** khi vi phạm đã được chứng minh là đặc tính dữ liệu (R11 đạt + IV độc lập + nghiệm đơn vị) VÀ tác giả đã chấp nhận ghi hạn chế (DECISIONS). Nếu ước lượng chính là FE động: ρ<1 và có hiệu chỉnh lệch Nickell (jackknife/LSDVC); **1 điểm** khi ρ_hiệu-chỉnh ≥1 nhưng KTC chứa 1, ≥3 phương pháp độc lập cùng chỉ ρ≈1, mọi hệ số dài hạn bị loại/không diễn giải, chỉ diễn giải ngắn hạn, và DECISIONS ghi hạn chế được tác giả xác nhận |
| R4 | P1 | Chẩn đoán mô hình tĩnh | Có Hausman **bền vững** (Mundlak/cluster) khi có phương sai thay đổi/tự tương quan, Wooldridge AR, phương sai thay đổi, Pesaran CD; lựa chọn FE/RE/FEDK có lý do; nếu biến phụ thuộc không bác bỏ nghiệm đơn vị → có kiểm định dừng phần dư/đồng liên kết cho mô hình tĩnh (nếu không, chấm tối đa 1) |
| R5 | P1 | Liêm chính đặc tả | Mọi thay đổi có dòng DECISIONS với lý do phương pháp; không đổi đặc tả vì p-value |
| R6 | P2 | H1 có kết luận rõ | Dấu, độ lớn, ý nghĩa của FDI ở SGMM & FEDK; diễn giải được (Haven vs Halo) |
| R7 | P2 | H2 so sánh được 6 khía cạnh | Bảng 6 hệ số cùng đặc tả; nêu khía cạnh nào khác biệt |
| R8 | P2 | H3 + tác động biên | Hệ số tương tác + ME tại phân vị IQ có SE; nêu ngưỡng IQ nếu ME đổi dấu |
| R9 | P2 | Tính vững | IQ_PCA cho H2/H3 và winsorize FDI; nêu kết luận nào vững/không vững; quy tắc vững xét theo **kết luận** (dấu chỉ tính khi ít nhất một bên p<0,10; đổi dấu giữa hai hệ số cùng ns không là "không vững") |
| R10 | P3 | Gọn & tái lập | Tóm tắt ≤ 40 dòng/bước; không hard-code con số; seed/phiên bản (python, pydynpd, linearmodels, numpy) ghi trong meta |
| R11 | P1 | Xác minh bộ ước lượng | pydynpd (đã vá) tái tạo được ρ đã biết trên panel mô phỏng cùng N,T (sai lệch ≤ 0,05) và khớp ước lượng IV độc lập (Anderson–Hsiao) về hướng |

## Bẫy thường gặp (kiểm tra mỗi vòng)
- SGMM hệ số trễ ≈ 1 hoặc > 1 → thử độ trễ công cụ khác (2:3, 3:5), coi biến kiểm soát là nội sinh/tiền định, kiểm tra cận Bond.
- Hansen p ≈ 1,000 → quá nhiều công cụ dù đã collapse.
- Tương tác có ý nghĩa nhưng tác động biên không ý nghĩa ở vùng có dữ liệu → không kết luận "điều tiết" mạnh.
- FE và SGMM ngược dấu → phải giải thích, không chọn cái "đẹp hơn".
- Difference GMM cho ρ > POLS động (lẽ ra lệch xuống phía FE khi công cụ yếu) → nghi lỗi cài đặt/vá thư viện, xác minh trước khi diễn giải.
- So cận Bond bằng ước lượng điểm là chưa đủ: xem KTC của ρ; ρ không khác 1 có ý nghĩa → nghi nghiệm đơn vị (kiểm định CIPS/IPS).
- Bảng nhạy cảm công cụ: biến thể duy nhất cho p<0,05 KHÔNG được chọn hậu nghiệm; quy tắc chọn đặc tả phải ghi vào DECISIONS TRƯỚC khi chạy lại.
- Hansen p tăng vọt (>0,9) khi thêm khối gmm() → dấu hiệu công cụ yếu/quá nhiều, không phải "đạt".
- Hausman cổ điển không hợp lệ khi có phương sai thay đổi/tự tương quan.
- Biến phụ thuộc I(1) (CIPS không bác bỏ) hồi quy trên X I(0) trong FE tĩnh → hồi quy không cân bằng/giả mạo; FEDK tĩnh khi Wooldridge AR p≈0 còn bỏ sót động học → không dùng FEDK tĩnh làm bằng chứng chính.
- Đổi ước lượng chính SAU khi đã thấy kết quả: chỉ hợp lệ nếu lý do là chẩn đoán (cận Bond, nghiệm đơn vị) và tiêu chí ủng hộ H1–H3 cho ước lượng mới được ghi DECISIONS TRƯỚC khi chạy; báo song song ước lượng cũ.
- Mô phỏng xác minh chỉ với DGP dừng không giải thích được ρ̂>1 trên dữ liệu thật → khi yêu cầu mô phỏng, nêu cả DGP gần nghiệm đơn vị/xu thế riêng.
- Tiêu chí "Xong khi" của ACTION KHÔNG được phụ thuộc kết quả ước lượng (vd "ρ_jk<1"): chỉ được yêu cầu cái phải tính/báo; kết quả xấu là hợp lệ. Kiểm tra tự động không FAIL vì đặc tính dữ liệu đã được chứng minh và ghi nhận → WARN.
- Trước khi khuyến nghị FE động + hiệu chỉnh Nickell khi đã nghi ρ≈1: dự báo kết quả. Với hiệu ứng cố định, lệch LSDV ≈ −c/T, c≈1+ρ (dừng) nhưng c≈3 (nghiệm đơn vị); ước lượng c ≈ T·(ρ̂_T − ρ̂_{T/2}) từ hai nửa mẫu. c≥3 → jackknife sẽ đưa ρ về ≈1.
- Khi ρ≈1: đối chứng hạn chế đúng của FE động là ΔY có hiệu ứng nước (trôi riêng) ≈ FE động + xu thế riêng; sai phân đầu KHÔNG có hiệu ứng nước bỏ sót trôi riêng → không dùng riêng nó để bác bỏ.
- Hai nửa mẫu ngược dấu cho hệ số chính → nêu bất ổn theo thời gian trong diễn giải, không ẩn trong trung bình jackknife.

## Nhật ký cải tiến (evaluator ghi khi sửa rubric)
| Vòng | Thay đổi | Vì sao |
|---|---|---|
| 0 | Khởi tạo | — |
| 1 | R3 thêm KTC/H0 ρ=1/diff-Hansen; R4 yêu cầu Hausman bền vững; R10 ghi phiên bản; thêm R11 (xác minh bộ ước lượng, P1); thêm 5 bẫy | Vòng 1: ρ>1 ở mọi 9 đặc tả kể cả Difference GMM (1,24>POLS 0,98) — rubric cũ không phân biệt lỗi cài đặt với vấn đề công cụ; Hausman phi-robust dù het p=0, AR p=3e-24 |
| 2 | R3 thêm mức 1 (vi phạm là đặc tính dữ liệu + tác giả chấp nhận) và nhánh FE động; R4 thêm kiểm định dừng phần dư/đồng liên kết khi Y I(1); R9 quy tắc vững theo kết luận; thêm 3 bẫy | Vòng 2: R11 đạt nhưng ρ>1 vẫn còn (AH 1,18; CIPS không bác bỏ I(1)) → R3 không bao giờ đạt nếu giữ SGMM, cần lối ra trung thực; FEDK tĩnh với lnCO2 I(1) chưa được kiểm tra giả mạo; bảng vững D15f gắn "KHÔNG VỮNG" cho đổi dấu của hệ số ≈0 ns |
| 3 | R3 thêm mức 1 cho nhánh FE động (ρ_jk≥1, KTC chứa 1, bỏ dài hạn, tác giả xác nhận); +4 bẫy (Xong-khi không phụ thuộc kết quả; dự báo lệch Nickell dưới nghiệm đơn vị c≈3; đối chứng ΔY cần hiệu ứng nước; nửa mẫu ngược dấu) | Vòng 3: B-2 đặt "Xong khi ρ_jk<1" và CHECKS_REQUEST JACKKNIFE=FAIL → 23 FAIL không sửa được bằng làm việc trung thực; evaluator vòng 2 đã có đủ dữ kiện (AH 1,18, CIPS I(1)) để dự báo ρ_jk≈1 (c ước lượng từ nửa mẫu = 20·0,179≈3,6) |
