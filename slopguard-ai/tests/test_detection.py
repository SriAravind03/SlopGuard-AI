import pytest

from detection.repetition_detector import analyze_repetition
from detection.scoring_engine import analyze_text
from detection.semantic_analyzer import semantic_redundancy


def test_analysis_returns_bounded_transparent_metrics():
    result = analyze_text("The study measured 12 participants in May. The study measured 12 participants in May. Researchers published their method and raw data.")
    assert 0 <= result["slop_pattern_score"] <= 100
    assert 0 <= result["content_quality_score"] <= 100
    assert "cannot establish AI authorship" in result["ai_authorship_assessment"]
    assert result["repetition_score"] > 0


def test_repetition_and_semantic_signals():
    text = "".join(["The project uses careful review and clear records. "] * 4)
    assert analyze_repetition(text)["score"] > 0
    assert semantic_redundancy(text)["score"] > 0


def test_empty_and_large_inputs():
    with pytest.raises(ValueError): analyze_text("  ")
    with pytest.raises(ValueError): analyze_text("x" * 50001)
