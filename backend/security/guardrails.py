import re

PII = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[EMAIL]"),
    (re.compile(r"\b(?:\d[ -]?){13,16}\b"), "[CARD]"),
    (re.compile(r"\b\d{3}-\d{2}-\d{4}\b"), "[SSN]"),
    (re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"), "[IP]"),
]
INJ = re.compile(
    r"ignore (all |previous |prior )?(instructions|rules)|system prompt|you are now|"
    r"jailbreak|<script|union\s+select|drop\s+table|;\s*--|__import__", re.I)


def sanitize(text: str, max_len: int = 2000) -> str:
    return re.sub(r"[\x00-\x08\x0b-\x1f]", "", text)[:max_len].strip()


def redact_pii(text: str):
    n = 0
    for rx, tag in PII:
        text, c = rx.subn(tag, text)
        n += c
    return text, n


def is_injection(text: str) -> bool:
    return bool(INJ.search(text))


def verify_numbers(summary: str, allowed, tol: float = 0.01):
    """Return numbers in an AI summary that match no computed value (hallucination check)."""
    found = [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*\.?\d*", summary)]
    return [n for n in found if not any(abs(a - n) <= abs(a) * tol + 0.01 for a in allowed)]
