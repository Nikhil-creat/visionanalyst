import re


class KnowledgeBase:
    """Hybrid retrieval: TF-IDF cosine (semantic-ish) blended with keyword overlap."""

    def __init__(self):
        self.chunks = []

    def add(self, text: str, size: int = 80):
        w = text.split()
        self.chunks += [" ".join(w[i:i + size]) for i in range(0, len(w), size)]

    def add_pdf(self, file):
        from pypdf import PdfReader
        self.add(" ".join(p.extract_text() or "" for p in PdfReader(file).pages))

    def search(self, q: str, k: int = 3):
        if not self.chunks:
            return []
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        v = TfidfVectorizer(stop_words="english").fit(self.chunks + [q])
        sem = cosine_similarity(v.transform([q]), v.transform(self.chunks))[0]
        qs = set(re.findall(r"\w+", q.lower()))
        kw = [len(qs & set(re.findall(r"\w+", c.lower()))) / (len(qs) or 1) for c in self.chunks]
        score = [0.6 * s + 0.4 * w for s, w in zip(sem, kw)]
        return sorted(zip(score, self.chunks), reverse=True)[:k]
