INTENTS = {
    "automl": ("forecast", "predict", "anomal", "outlier", "importance", "cluster"),
    "rag": ("policy", "document", "guideline", "pdf"),
    "vision": ("image", "chart image", "screenshot"),
    "security": ("audit", "rbac", "permission"),
}


def classify(text: str) -> str:
    t = text.lower()
    for intent, words in INTENTS.items():
        if any(w in t for w in words):
            return intent
    return "analytics"
