"""Deterministic pandas engine with a self-healing retry loop (no dynamic code execution)."""
import difflib
import traceback

import pandas as pd

from agents import automl_agent as ml
from agents.planner import Plan
from config import MAX_RETRIES


def run_plan(df: pd.DataFrame, p: Plan) -> pd.DataFrame:
    for c in (p.column, p.by):
        if c and c not in df.columns:
            raise KeyError(c)
    if p.op == "aggregate":
        return pd.DataFrame({p.column: [df[p.column].agg(p.agg)]})
    if p.op == "group_by":
        return df.groupby(p.by)[p.column].agg(p.agg).reset_index()
    if p.op == "pivot":
        return df.pivot_table(index=p.by, values=p.column, aggfunc=p.agg).reset_index()
    if p.op == "forecast":
        return ml.forecast(df[p.column], p.horizon)
    if p.op == "anomaly":
        return ml.anomalies(df[p.column])
    return df.describe().reset_index()


def default_replan(p: Plan, df: pd.DataFrame, err: Exception) -> Plan:
    """Fix a failed plan: map unknown column names to the closest real ones."""
    q = p.model_copy()
    for f in ("column", "by"):
        v = getattr(q, f)
        if v and v not in df.columns:
            m = difflib.get_close_matches(v, list(df.columns), n=1, cutoff=0.5)
            if not m:
                raise ValueError(f"No column resembling {v!r}") from err
            setattr(q, f, m[0])
    return q


def execute(df, plan: Plan, replan=default_replan, retries: int = MAX_RETRIES):
    log = []
    for attempt in range(1, retries + 2):
        try:
            out = run_plan(df, plan)
            log.append(f"attempt {attempt}: ok")
            return out, plan, log
        except Exception as e:  # self-healing: capture traceback, re-plan, retry
            log.append(f"attempt {attempt}: {type(e).__name__}: {e}\n{traceback.format_exc(limit=1)}")
            if attempt > retries:
                raise
            plan = replan(plan, df, e)
