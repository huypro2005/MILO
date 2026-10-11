"""Hàm dùng chung cho mọi script. Mọi bước phân tích PHẢI nạp dữ liệu qua load_panel()
để biến đổi biến thống nhất (xem knowledge/SPEC.md mục 3 và knowledge/DECISIONS.md).
File này thuộc "hạ tầng": modeler chỉ sửa khi evaluator yêu cầu và phải ghi vào DECISIONS.md."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

# --- Vá tương thích pydynpd (System GMM) với NumPy 2; xem knowledge/DECISIONS.md D7 ---
if not hasattr(np, "in1d"):
    np.in1d = np.isin
try:
    import math as _math, types as _types
    from pydynpd import specification_tests as _sp

    def _scalar(x):  # NumPy 2 không cho float()/math.sqrt() trên mảng 1x1
        return float(np.asarray(x).item())

    _sp.float = _scalar
    _sp.math = _types.SimpleNamespace(sqrt=lambda x: _math.sqrt(_scalar(x)))
except ImportError:
    pass

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "DATA_FINAL.xlsx"
RESULTS = ROOT / "results"
TABLES = RESULTS / "tables"
FIGS = RESULTS / "figures"
SUMM = RESULTS / "summaries"
ESTIMATES = RESULTS / "estimates.json"

IQ = ["CC", "GE", "PV", "RQ", "RL", "VA"]
IQ_ALL = IQ + ["IQ_PCA"]
CONTROLS = ["lnY", "URB", "TO", "Crdt"]


def _pca_index(df: pd.DataFrame) -> pd.Series:
    """Thành phần chính thứ nhất của 6 biến WGI đã chuẩn hoá; đổi dấu để tải trọng dương."""
    z = (df[IQ] - df[IQ].mean()) / df[IQ].std()
    vals, vecs = np.linalg.eigh(np.cov(z.T))
    w = vecs[:, np.argmax(vals)]
    w = w if w.sum() > 0 else -w
    return pd.Series(z.values @ w, index=df.index)


def load_panel() -> pd.DataFrame:
    df = pd.read_excel(DATA, sheet_name="Sheet1")
    df["lnCO2"] = np.log(df["CO2"])
    df["lnY"] = np.log(df["Y"])
    df["IQ_PCA"] = _pca_index(df)
    # Trung tâm hoá trước khi tạo biến tương tác (D3)
    df["FDI_c"] = df["FDI"] - df["FDI"].mean()
    for k in IQ_ALL:
        df[f"{k}_c"] = df[k] - df[k].mean()
        df[f"FDIx{k}"] = df["FDI_c"] * df[f"{k}_c"]
    return df.sort_values(["Country", "Year"]).reset_index(drop=True)


def save_summary(step: str, text: str) -> Path:
    """Ghi tóm tắt ngắn (<= 60 dòng) cho agent khác đọc thay vì đọc output thô."""
    SUMM.mkdir(parents=True, exist_ok=True)
    p = SUMM / f"{step}.md"
    p.write_text(text, encoding="utf-8")
    return p


def save_estimates(models: list, tests: dict, meta: dict | None = None) -> Path:
    """Ghi kết quả theo schema ở knowledge/SPEC.md mục 6 để checks.py chấm tự động."""
    RESULTS.mkdir(parents=True, exist_ok=True)
    ESTIMATES.write_text(json.dumps({"meta": meta or {}, "models": models, "tests": tests},
                                    indent=1, ensure_ascii=False, default=float), encoding="utf-8")
    return ESTIMATES
