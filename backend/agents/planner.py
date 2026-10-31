from typing import Literal, Optional

from pydantic import BaseModel, Field

AGG = {"total": "sum", "sum": "sum", "average": "mean", "avg": "mean", "mean": "mean",
       "min": "min", "max": "max", "count": "count", "median": "median"}


class Plan(BaseModel):
    op: Literal["aggregate", "group_by", "pivot", "describe", "forecast", "anomaly"]
    column: Optional[str] = None
    by: Optional[str] = None
    agg: Literal["sum", "mean", "min", "max", "count", "median"] = "sum"
    horizon: int = Field(3, ge=1, le=36)
    confidence: float = Field(0.5, ge=0, le=1)


def make_plan(text: str, df) -> Plan:
    """Rule-based planner: strict, schema-validated JSON plan with a confidence score."""
    t = text.lower()
    num = list(df.select_dtypes("number").columns)
    cat = [c for c in df.columns if c not in num]
    col = next((c for c in num if c.lower() in t), None)
    by = next((c for c in cat if c.lower() in t), None)
    ops = [("forecast", ("forecast", "predict", "next")), ("anomaly", ("anomal", "outlier")),
           ("pivot", ("pivot",)), ("group_by", (" by ", " per ", "each")),
           ("describe", ("summary", "describe", "overview")), ("aggregate", ("total", "sum", "average", "mean", "max", "min", "count"))]
    op = next((o for o, ws in ops if any(w in f" {t} " for w in ws)), None)
    conf = 0.4 + (0.3 if op else 0) + (0.3 if col or op == "describe" else 0)
    if op == "group_by" and not by:
        conf -= 0.2
    agg = next((v for k, v in AGG.items() if k in t), "sum")
    return Plan(op=op or "describe", column=col or (num[0] if num else None), by=by,
                agg=agg, confidence=round(max(conf, 0), 2))
