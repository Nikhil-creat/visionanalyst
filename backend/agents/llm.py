import requests

import config

SYS = "You are VisionAnalyst. Use ONLY the numbers provided. Never calculate."


def ask_llm(prompt: str):
    """Groq -> Gemini -> Ollama. Returns None when everything is offline (graceful degradation)."""
    try:
        if config.GROQ_API_KEY:
            r = requests.post("https://api.groq.com/openai/v1/chat/completions", timeout=30,
                              headers={"Authorization": "Bearer " + config.GROQ_API_KEY},
                              json={"model": "llama-3.3-70b-versatile",
                                    "messages": [{"role": "system", "content": SYS},
                                                 {"role": "user", "content": prompt}]})
            return r.json()["choices"][0]["message"]["content"]
        if config.GEMINI_API_KEY:
            u = ("https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:"
                 "generateContent?key=" + config.GEMINI_API_KEY)
            r = requests.post(u, timeout=30, json={"contents": [{"parts": [{"text": SYS + "\n" + prompt}]}]})
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        r = requests.post(config.OLLAMA_URL + "/api/generate", timeout=60,
                          json={"model": "llama3.3", "prompt": SYS + "\n" + prompt, "stream": False})
        return r.json()["response"]
    except Exception:
        return None
