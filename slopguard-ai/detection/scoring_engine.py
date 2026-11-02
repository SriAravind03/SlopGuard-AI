from detection.ai_pattern_detector import detect_patterns
from detection.quality_analyzer import analyze_quality
from detection.repetition_detector import analyze_repetition
from detection.semantic_analyzer import semantic_redundancy
from detection.text_preprocessor import normalize_text, sentences
from detection.huggingface_analyzer import classify


def analyze_text(raw_text: str) -> dict:
    text = normalize_text(raw_text)
    if not text:
        raise ValueError("Enter some text to analyze.")
    if len(text) > 50000:
        raise ValueError("Text exceeds the 50,000 character analysis limit.")
    q = analyze_quality(text)
    rep = analyze_repetition(text)
    sem = semantic_redundancy(text)
    ai = detect_patterns(text)
    hf = classify(text[:4000])
    # Explicit weighted rubric: low density, repetition, redundancy, generic phrases and stuffing.
    slop = round(min(100, max(0, .25 * (100 - q["information_density"]) + .22 * rep["score"] + .18 * sem["score"] + .20 * q["generic_pattern_score"] + .10 * q["keyword_stuffing_score"] + .05 * ai["score"])))
    quality = 100 - slop
    classification = "Likely Low-Quality / Slop-Like" if slop >= 60 else "Mixed Quality" if slop >= 35 else "High-Quality Content"
    reasons = []
    if q["information_density"] < 35: reasons.append("Low information-density proxy")
    if rep["score"] >= 20: reasons.append("Repeated phrases or adjacent word pairs")
    if sem["score"] >= 20: reasons.append("Sentences share substantial word overlap")
    if q["generic_phrase_count"]: reasons.append("Generic writing phrases detected")
    if q["keyword_stuffing_score"]: reasons.append("Potentially overused content keywords")
    if not reasons: reasons.append("Few measured low-quality signals were found")
    suggestions = []
    if q["generic_phrase_count"]: suggestions.append("Replace generic transitions with specific claims or examples.")
    if rep["score"] >= 15 or sem["score"] >= 15: suggestions.append("Remove repeated ideas and keep the clearest explanation of each point.")
    if q["information_density"] < 45: suggestions.append("Add concrete evidence, sources, examples, or actionable detail.")
    if not suggestions: suggestions.append("Keep claims sourced and preserve the specific details that make the text useful.")
    suspicious = [s for s in sentences(text) if any(p in s.casefold() for p in ("in today's world", "it is important to note", "plays a crucial role", "delve into", "it is worth noting"))][:8]
    return {"content_quality_score": quality, "slop_pattern_score": slop, "classification": classification,
        "ai_authorship_assessment": ai["authorship_assessment"], "ai_like_pattern_score": ai["score"],
        "repetition_score": rep["score"], "information_density": q["information_density"],
        "semantic_redundancy": sem["score"], "linguistic_diversity": q["vocabulary_diversity"],
        "metrics": q, "repetition": rep, "semantic": sem, "ai_patterns": ai,
        "huggingface_analysis": hf,
        "reasons": reasons, "suggestions": suggestions, "suspicious_sentences": suspicious,
        "scoring_method": "Slop pattern score = 25% inverse density + 22% repetition + 18% redundancy + 20% generic phrase score + 10% keyword stuffing + 5% AI-like pattern signals. This estimates writing quality signals, not authorship."}
