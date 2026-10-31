import contextlib
import json
import logging
import time

log = logging.getLogger("visionanalyst")
logging.basicConfig(level=logging.INFO, format="%(message)s")


class Tracer:
    def __init__(self):
        self.steps, self.tokens = [], 0

    @contextlib.contextmanager
    def span(self, name: str):
        t = time.perf_counter()
        try:
            yield
        finally:
            rec = {"step": name, "ms": round((time.perf_counter() - t) * 1000, 2)}
            self.steps.append(rec)
            log.info(json.dumps(rec))
