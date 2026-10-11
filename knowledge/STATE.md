# STATE — Bảng trạng thái vòng lặp (orchestrator cập nhật sau mỗi bước)

- Vòng hiện tại: 3 → CONVERGED có điều kiện (loop/iter_3/review.md)
- Trạng thái: ⛔ CHỜ TÁC GIẢ xác nhận D25 (ρ≈1, chỉ diễn giải ngắn hạn). Xác nhận → đổi D25 thành ✅ → chạy checks (FAIL JACKKNIFE thành WARN) → gọi econ-analyst viết Chương 4–5 (ACTION A3 trong review vòng 3). Không xác nhận → thêm 1 vòng modeler (MC jackknife ρ∈{0,95;1}, bootstrap cụm).
- Vòng tối đa mỗi lần chạy: 4

## Câu hỏi đang chờ tác giả
- D25 (chặn bước viết). D8 tiêu chí "đang phát triển" (cho Chương 3, không chặn).

## Lịch sử
| Vòng | Checks | Rubric | Quyết định evaluator | Ghi chú orchestrator |
|---|---|---|---|---|
| 1 | WARN (0 FAIL, 24 WARN) | 13/22 (59%) | CONTINUE | Thêm 5 kiểm tra vào checks.py (LAG_CI, HANSEN_HIGH, DIFF_HANSEN, DGMM_GT_POLS, META_VERSIONS). Meta-kiểm tra evaluator: đạt (không bỏ sót WARN, ACTION kiểm chứng được, 41 dòng) → không sửa evaluator.md |
| 2 | WARN (0 FAIL, 28→7 WARN sau khi gộp) | 17/22 (77%) | CONTINUE, chặn bởi Q1 | Thêm 4 kiểm tra (gộp LAG_GE1, RESID_UR, bảng điểm theo main_estimator, JACKKNIFE). Meta-kiểm tra evaluator: đạt (45 dòng, tự phê bình 4 điểm, tách nhánh A/B đúng yêu cầu) |
| 3 | FAIL=1 (JACKKNIFE chờ D25), WARN=7 | 21/22 (95%, R3=1 khi D25 ✅) | CONVERGED có điều kiện | Tác giả chọn nhánh B (D18), xác nhận D1 (D19). Thêm JACKKNIFE có điều kiện + LONGRUN_INVALID/UNCORR (gộp 1 dòng). Meta-kiểm tra evaluator: đạt — tự phát hiện khuyến nghị nhánh B vòng 2 dựa trên giả định sai (ρ_jk<1) và tiêu chí "Xong khi" phụ thuộc kết quả; đã ghi thành bẫy trong rubric |
