from detection.text_preprocessor import sentences, words
from functools import lru_cache
import os


def semantic_redundancy(text: str) -> dict:
    ss = sentences(text)
    if len(ss) < 2:
        return {"score": 0, "similar_pairs": [], "method": "insufficient sentences for redundancy comparison"}
    # Use sentence embeddings only when explicitly configured. The deterministic fallback
    # is word-set overlap and is labeled as a proxy in the result.
    embedding_model = os.getenv("HF_EMBEDDING_MODEL")
    if embedding_model:
        try:
            model = _embedding_model(embedding_model)
            embeddings = model.encode(ss, normalize_embeddings=True)
            import numpy as np
            pairs = []
            for i in range(len(ss)):
                for j in range(i + 1, len(ss)):
                    similarity = float(np.dot(embeddings[i], embeddings[j]))
                    if similarity >= 0.78:
                        pairs.append({"sentences": [ss[i], ss[j]], "similarity": round(similarity, 2)})
            score = round(min(100, 100 * len(pairs) / max(1, len(ss) * (len(ss) - 1) / 2) * 1.8))
            return {"score": score, "similar_pairs": pairs[:8], "method": f"sentence embeddings ({embedding_model}); cosine threshold 0.78"}
        except Exception:
            pass
    # Word-set Jaccard similarity is a deterministic offline proxy, not a semantic model.
    sets = [set(words(s)) for s in ss]
    pairs = []
    for i, left in enumerate(sets):
        for j in range(i + 1, len(sets)):
            right = sets[j]
            union = left | right
            similarity = len(left & right) / len(union) if union else 0
            if similarity >= 0.55:
                pairs.append({"sentences": [ss[i], ss[j]], "similarity": round(similarity, 2)})
    score = round(min(100, 100 * len(pairs) / max(1, len(ss) * (len(ss) - 1) / 2) * 1.8))
    return {"score": score, "similar_pairs": pairs[:8], "method": "word overlap proxy; optional embedding models are not enabled"}


@lru_cache(maxsize=2)
def _embedding_model(model_name):
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(model_name)
