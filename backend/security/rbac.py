import hashlib
import time

from config import ROLES


def can(role: str, action: str) -> bool:
    return action in ROLES.get(role, set())


class AuditLog:
    """Hash-chained, tamper-evident audit trail."""

    def __init__(self):
        self.rows, self._prev = [], "GENESIS"

    def add(self, role: str, action: str, confidence=None, tokens=0):
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        body = f"{self._prev}|{ts}|{role}|{action}|{confidence}|{tokens}"
        h = hashlib.sha256(body.encode()).hexdigest()
        self.rows.append({"ts": ts, "role": role, "action": action, "confidence": confidence,
                          "tokens": tokens, "prev": self._prev, "hash": h})
        self._prev = h

    def verify(self) -> bool:
        prev = "GENESIS"
        for r in self.rows:
            body = f"{prev}|{r['ts']}|{r['role']}|{r['action']}|{r['confidence']}|{r['tokens']}"
            if r["prev"] != prev or hashlib.sha256(body.encode()).hexdigest() != r["hash"]:
                return False
            prev = r["hash"]
        return True
