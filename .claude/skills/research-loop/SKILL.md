---
name: research-loop
description: Chạy vòng lặp nghiên cứu modeler → checks.py → evaluator (tự cải thiện) cho đề tài FDI–CO₂–thể chế, đến khi CONVERGED hoặc hết số vòng. Dùng khi tác giả gõ /research-loop hoặc yêu cầu "chạy tiếp vòng lặp".
---
# Quy trình vòng lặp nghiên cứu (session chính = orchestrator)

```
          ┌──────────────────────────────────────────────────────┐
          ▼                                                      │
 STATE.md ACTION ─▶ [modeler] code + run_all.py ─▶ [checks.py] ─▶ [evaluator] ─▶ review.md
                                                    (tự động,      │  ├─ ACTION mới → STATE.md
                                                     0 token)      │  ├─ sửa EVAL_RUBRIC.md (tự cải thiện)
                                                                   │  └─ CHECKS_REQUEST → orchestrator sửa checks.py
                                                                   ▼
                                                CONVERGED → [econ-analyst] viết Chương 4–5
```

## Mỗi vòng N (tối đa số vòng ghi trong STATE.md, mặc định 4)
1. **Modeler**: gọi Agent `modeler` (nếu tên agent chưa được nạp trong session, dùng `general-purpose` với prompt "Đọc và làm theo `.claude/agents/modeler.md`"). Prompt chỉ cần: số vòng N + "làm các ACTION trong knowledge/STATE.md". Chạy foreground.
2. **Checks** (orchestrator tự chạy): `PYTHONIOENCODING=utf-8 python code/checks.py`. Không đưa output đầy đủ vào prompt agent — evaluator tự đọc `results/summaries/checks.md`.
3. **Evaluator**: gọi Agent `evaluator` với: số vòng N. Nó ghi `loop/iter_N/review.md`.
4. **Orchestrator cập nhật**:
   - Chép ACTION từ review vào `knowledge/STATE.md`, tăng vòng, thêm dòng Lịch sử.
   - Nếu có `CHECKS_REQUEST` hợp lý → sửa `code/checks.py` (orchestrator là người duy nhất sửa file này), chạy lại checks để xác nhận.
   - **Meta-kiểm tra evaluator** (cải thiện chính agent đánh giá): nếu evaluator (a) bỏ sót một FAIL/WARN của checks, (b) đưa ACTION không kiểm chứng được, (c) đề xuất đổi đặc tả vì p-value, hoặc (d) vượt giới hạn độ dài → sửa `.claude/agents/evaluator.md` hoặc `EVAL_RUBRIC.md` và ghi vào "Nhật ký cải tiến".
5. **Dừng** khi: `CONVERGED`; hoặc evaluator có "Câu hỏi cho tác giả" chặn tiến trình; hoặc hết số vòng; hoặc 2 vòng liên tiếp không cải thiện tổng điểm rubric (báo tác giả).
6. Khi CONVERGED: gọi `econ-analyst` viết `report/chuong4_ketqua.md`, `report/chuong5_hamy.md`.

## Tiết kiệm token
- Agent chỉ đọc file tóm tắt (`results/summaries/*.md`, `review.md`, `run.md`), không đọc dữ liệu thô / docx.
- Prompt gửi agent ngắn: không dán lại SPEC — agent tự đọc file.
- Modeler dùng `sonnet`; evaluator/analyst dùng `opus`. Vòng sau modeler chỉ sửa file liên quan đến ACTION.
- Báo cáo cho tác giả sau mỗi vòng: ≤ 8 dòng (checks, điểm rubric, trạng thái H1–H3, việc tiếp theo).
