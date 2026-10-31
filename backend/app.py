import pandas as pd
import plotly.express as px
import streamlit as st

from agents.executor import execute
from agents.llm import ask_llm
from agents.planner import make_plan
from agents.rag_agent import KnowledgeBase
from agents.router import classify
from agents.vision_agent import analyze
from config import CONF_THRESHOLD, ROLES
from export import report_generator as rg
from security.guardrails import is_injection, redact_pii, sanitize, verify_numbers
from security.rbac import AuditLog, can
from telemetry.observability import Tracer

st.set_page_config("VisionAnalyst Enterprise OS", "👁️", layout="wide")
S = st.session_state
S.setdefault("audit", AuditLog())
S.setdefault("tr", Tracer())
S.setdefault("kb", KnowledgeBase())
S.setdefault("pii", 0)
with st.sidebar:
    st.title("👁️ VisionAnalyst")
    role = st.selectbox("RBAC profile", list(ROLES))
    st.caption("LLM: Groq → Gemini → Ollama → offline stats")
    st.metric("PII items masked", S.pii)
    st.write("Audit chain valid:", S.audit.verify())
t1, t2, t3, t4, t5 = st.tabs(["Agent Workspace", "AutoML Studio", "Knowledge Hub", "Vision Inspector", "Telemetry & Audit"])
up = st.sidebar.file_uploader("CSV data", type="csv")
df = pd.read_csv(up) if up else pd.DataFrame({"region": list("NSEW"), "revenue": [120, 98, 144, 88], "units": [340, 290, 410, 250]})
with t1:
    q = st.text_input("Ask in plain English", "total revenue by region")
    if st.button("Run agents") and can(role, "run_agents"):
        q = sanitize(q)
        if is_injection(q):
            st.error("Blocked: possible injection.")
            S.audit.add(role, "blocked injection")
        else:
            q, n = redact_pii(q)
            S.pii += n
            with S.tr.span("route"):
                intent = classify(q)
            with S.tr.span("plan"):
                plan = make_plan(q, df)
            st.json({"intent": intent, **plan.model_dump()})
            if plan.confidence < CONF_THRESHOLD:
                st.warning("Confidence below 80%. Please clarify which column and operation you mean.")
            else:
                with S.tr.span("execute"):
                    out, plan, log = execute(df, plan)
                st.code("\n".join(log))
                st.dataframe(out) if can(role, "view_raw") else st.info("Raw data hidden for your role.")
                if len(out.columns) > 1:
                    st.plotly_chart(px.bar(out, x=out.columns[0], y=out.columns[1]))
                nums = out.select_dtypes("number").to_numpy().ravel().tolist()
                summ = (ask_llm("Summarize in 3 sentences: " + out.to_json()) if can(role, "ai_call") else None) \
                    or "Statistical summary: " + out.describe().to_string()
                bad = verify_numbers(summ, nums + out.select_dtypes("number").describe().to_numpy().ravel().tolist())
                st.write(summ)
                st.warning(f"Unverified numbers: {bad}") if bad else st.success("Hallucination check passed")
                S.audit.add(role, q, plan.confidence)
                if can(role, "export"):
                    c = st.columns(4)
                    c[0].download_button("JSON", rg.to_json(out, summ), "report.json")
                    c[1].download_button("Excel", rg.to_excel(out), "report.xlsx")
                    c[2].download_button("PDF", rg.to_pdf("VisionAnalyst Report", summ[:900], out), "report.pdf")
                    c[3].download_button("PPTX", rg.to_pptx("VisionAnalyst Report", summ[:600], out), "report.pptx")
with t2:
    from agents import automl_agent as ml
    col = st.selectbox("Numeric column", df.select_dtypes("number").columns)
    st.dataframe(ml.forecast(df[col], 3))
    st.dataframe(ml.anomalies(df[col]))
with t3:
    d = st.text_area("Add policy text")
    if st.button("Index") and d:
        S.kb.add(d)
    s = st.text_input("Search")
    for sc, ch in S.kb.search(s) if s else []:
        st.write(round(sc, 2), ch)
with t4:
    f = st.file_uploader("Chart image", type=["png", "jpg"])
    if f:
        st.json(analyze(f.read()))
with t5:
    st.json(S.tr.steps)
    st.dataframe(pd.DataFrame(S.audit.rows))
