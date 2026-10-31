# VisionAnalyst Enterprise OS v6 (includes v3, v4, v5)
By **Nikhil Chary Sriramoju**. Static, no build step.
Backend: see backend/ (Streamlit, tests, Docker). Run: cd backend && pip install -r requirements.txt && streamlit run app.py
Features: AES-GCM key vault, video hero, neural-mesh background, ⌘K command palette, orchestration graph, streaming Groq/Gemini chatbot (voice in/out, RAG citations, PII masking, injection guard, rate limit), BM25 Knowledge Hub, Vision Inspector (local analysis + Gemini vision), AI/Security lab with hallucination check, RBAC and SHA-256 audit chain, live telemetry, PWA, CSP.
## Deploy (GitHub Pages)
Repo Settings → Pages → Source: **Deploy from a branch** → `main` / `/ (root)`. Keep `.nojekyll`.
Free keys: console.groq.com/keys · aistudio.google.com/apikey (paste in the 💬 chat ⚙️). Never commit keys.
## v4-v6 highlights
Data Workspace (CSV file/URL/WebSocket → plan → confidence gate → self-healing execution → verified summary → CSV/Excel/JSON/Markdown/PDF/PNG downloads); one-key provider auto-detect (gsk_ → Groq, AIza → Gemini) with model auto-select and failover (+ local Ollama); live telemetry and OTLP-style trace export; exportable chat and audit log.
CSP allows `https:`/`wss:` connections so you can load data from any URL; tighten `connect-src` in index.html if you only need Groq/Gemini.
