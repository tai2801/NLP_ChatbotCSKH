# -*- coding: utf-8 -*-
"""
NLP core:
- Intent classification: TF-IDF (word n-gram 1-2) + Logistic Regression (scikit-learn),
  trả probability làm confidence score.
- Semantic search nhẹ: TF-IDF cosine similarity trên câu hỏi của knowledge base.
- Entity extraction: regex cho mã đơn (TZxxxxxx), số điện thoại VN, khớp tên sản phẩm.
Không dùng sentence-transformers (nặng, cần tải model) — xem docs/LIMITATIONS.md.
"""
import re
import unicodedata

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics.pairwise import cosine_similarity

from .data import INTENTS, PRODUCTS

CONFIDENCE_THRESHOLD = 0.45


def normalize(text: str) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[^a-zà-ỹ0-9\s]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def _strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


class IntentClassifier:
    def __init__(self):
        texts, labels = [], []
        for intent, samples in INTENTS.items():
            for s in samples:
                texts.append(normalize(s))
                labels.append(intent)
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
        X = self.vectorizer.fit_transform(texts)
        self.model = LogisticRegression(max_iter=1000, C=10.0)
        self.model.fit(X, labels)

    def predict(self, text):
        x = self.vectorizer.transform([normalize(text)])
        proba = self.model.predict_proba(x)[0]
        idx = int(proba.argmax())
        return self.model.classes_[idx], float(proba[idx])


class KBSearch:
    """Tìm câu trả lời theo ngữ nghĩa (xấp xỉ) bằng TF-IDF cosine trên KB."""

    def __init__(self, entries):
        self.entries = entries
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        corpus = [normalize(e["question"]) + " " + normalize(e["intent"]) for e in entries]
        self.matrix = self.vectorizer.fit_transform(corpus) if corpus else None

    def search(self, text, intent=None, top_k=1):
        if not self.entries or self.matrix is None:
            return []
        x = self.vectorizer.transform([normalize(text)])
        sims = cosine_similarity(x, self.matrix)[0]
        ranked = sorted(range(len(sims)), key=lambda i: -sims[i])
        out = []
        for i in ranked:
            e = self.entries[i]
            if intent and e["intent"] != intent:
                continue
            out.append((e, float(sims[i])))
            if len(out) >= top_k:
                break
        return out


_ORDER_RE = re.compile(r"\bTZ\s?(\d{6})\b", re.IGNORECASE)
_PHONE_RE = re.compile(r"\b(0\d{9})\b")
_PHONE_SPACED_RE = re.compile(r"\b(0\d{3})[\s.](\d{3})[\s.](\d{3})\b")


def extract_entities(text):
    raw = text or ""
    entities = {}
    m = _ORDER_RE.search(raw)
    if m:
        entities["order_code"] = "TZ" + m.group(1)
    m = _PHONE_RE.search(raw.replace(" ", "").replace(".", "")) if not _PHONE_RE.search(raw) else _PHONE_RE.search(raw)
    if m:
        entities["phone"] = m.group(1)
    low = _strip_accents(raw.lower())
    for p in PRODUCTS:
        tokens = _strip_accents(p.lower()).split()
        # khớp theo 2 token đặc trưng cuối (vd "sonicbuds pro", "pro 14")
        key = " ".join(tokens[-2:]) if len(tokens) >= 2 else tokens[0]
        if key in low:
            entities["product"] = p
            break
    return entities
