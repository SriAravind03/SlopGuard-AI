from detection.huggingface_analyzer import classify
from detection.openai_analyzer import analyze_with_openai
from detection.scoring_engine import analyze_text


def test_missing_external_services_fall_back(monkeypatch):
    monkeypatch.delenv("HF_MODEL", raising=False)
    monkeypatch.delenv("HF_EMBEDDING_MODEL", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    result = analyze_text("A short report contains 3 documented examples and a link to the source dataset.")
    assert result["huggingface_analysis"]["available"] is False
    assert result["semantic"]["method"] in {"word overlap proxy; optional embedding models are not enabled", "insufficient sentences for redundancy comparison"}
    assert analyze_with_openai("content")["available"] is False


def test_unconfigured_classifier_is_offline(monkeypatch):
    monkeypatch.delenv("HF_MODEL", raising=False)
    assert classify("hello")["available"] is False
