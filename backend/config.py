import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
CONF_THRESHOLD = 0.8
MAX_RETRIES = 3
ROLES = {
    "Admin": {"view_raw", "export", "run_agents", "ai_call"},
    "Data Analyst": {"view_raw", "export", "run_agents"},
    "Viewer": {"view_summary"},
}
