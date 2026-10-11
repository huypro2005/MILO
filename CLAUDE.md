.c# Dự án: FDI → CO₂, vai trò điều tiết của chất lượng thể chế (73 nước đang phát triển, 2002–2022)
Tác giả: Võ Thị Linh Nhi (người mới nghiên cứu — giải thích ngắn gọn, tiếng Việt).

## Bản đồ thư mục
| Đường dẫn | Nội dung | Ai ghi |
|---|---|---|
| `DATA_FINAL.xlsx`, `DÀN BÀI THUNGHIEM.docx`, `image.png` | Dữ liệu gốc, dàn bài, giả thuyết — KHÔNG sửa | tác giả |
| `knowledge/SPEC.md` | Đặc tả: giả thuyết, biến, mô hình, quy trình, hợp đồng đầu ra | orchestrator |
| `knowledge/DECISIONS.md` | Nhật ký quyết định phương pháp (chống p-hacking) | modeler, evaluator |
| `knowledge/STATE.md` | Vòng lặp hiện tại + ACTION đang mở | orchestrator |
| `knowledge/EVAL_RUBRIC.md` | Tiêu chí đánh giá (evaluator tự cải thiện) | evaluator |
| `code/common.py` | Nạp & biến đổi dữ liệu, vá pydynpd, ghi kết quả | (hạ tầng) |
| `code/sNN_*.py`, `code/run_all.py` | Pipeline phân tích | modeler |
| `code/checks.py` | Bộ kiểm thử tự động + bảng điểm giả thuyết | chỉ orchestrator |
| `results/estimates.json`, `results/summaries/*.md`, `results/tables/` | Kết quả (agent đọc bản tóm tắt) | modeler/checks |
| `loop/iter_N/run.md`, `review.md` | Nhật ký từng vòng | modeler / evaluator |
| `report/` | Bản thảo Chương 4–5 | econ-analyst |

## Agent (`.claude/agents/`) và vòng lặp (`/research-loop`)
modeler (code, sonnet) → checks.py (tự động) → evaluator (đánh giá + tự cải thiện rubric, opus) → lặp; hội tụ → econ-analyst (viết).

## Quy ước
- Chạy Python: `PYTHONIOENCODING=utf-8 python code/<file>.py` (Python hệ thống 3.13; venv bị Windows chặn — DECISIONS D7).
- Mọi kết quả kiểm định là trung thực: bác bỏ giả thuyết cũng là kết quả hợp lệ.
