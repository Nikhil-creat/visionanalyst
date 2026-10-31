# VisionAnalyst Enterprise OS: Master Site
Static showcase by **Nikhil Chary Sriramoju**: video hero, 8-agent overview, self-healing demo, AI & security lab (CSV analyzer with hallucination check, PII redactor, injection guard, RBAC, SHA-256 audit chain), VisionBot chatbot (Groq + Gemini, BYOK), PWA, CSP.

## Deploy on GitHub Pages
1. Create a **public** repo, e.g. `visionanalyst` (no README).
2. Upload everything from this folder (keep `index.html` at the repo root, include `.nojekyll` and `.github`).
   Termux: `unzip visionanalyst-master.zip && cd visionanalyst-master && git init && git add . && git commit -m "VisionAnalyst" && git branch -M main && git remote add origin https://github.com/Nikhil-creat/visionanalyst.git && git push -u origin main`
3. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions** (or "Deploy from a branch" → `main` / `/ (root)`).
4. Wait ~1 minute: https://nikhil-creat.github.io/visionanalyst/

## API keys (free)
Groq: console.groq.com/keys · Gemini: aistudio.google.com/apikey. Open the 💬 chat, tap ⚙️, paste the key. Keys stay in your browser's localStorage and are never committed. Do not hard-code keys in the repo.

## Notes
Security is client-side (demo-grade); real enforcement needs the Streamlit backend from the spec.
