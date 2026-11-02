"""Optional local Hugging Face model adapter. No model is downloaded implicitly."""
import os
from functools import lru_cache


@lru_cache(maxsize=2)
def _pipeline(model_name):
    from transformers import pipeline
    return pipeline("text-classification", model=model_name, truncation=True)


def classify(text: str) -> dict:
    model_name = os.getenv("HF_MODEL")
    if not model_name:
        return {"available": False, "reason": "HF_MODEL is not configured; offline heuristic analysis was used."}
    try:
        classifier = _pipeline(model_name)
        return {"available": True, "model": model_name, "result": classifier(text[:4000])}
    except Exception as exc:
        return {"available": False, "reason": f"Configured model unavailable ({type(exc).__name__}); offline heuristic analysis was used."}
