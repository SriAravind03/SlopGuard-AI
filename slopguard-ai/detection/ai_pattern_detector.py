from detection.quality_analyzer import analyze_quality
from detection.text_preprocessor import sentences


def detect_patterns(text: str) -> dict:
    q = analyze_quality(text)
    n = max(1, q["sentence_count"])
    uniformity = max(0, 100 - min(100, q["sentence_length_variation"] * 5))
    score = round(min(100, q["generic_pattern_score"] * .45 + uniformity * .3 + (100 - q["vocabulary_diversity"]) * .25))
    ss = sentences(text)
    return {"score": score, "signals": [label for label, yes in [
        ("frequent generic phrasing", q["generic_phrase_count"] > 0),
        ("similar sentence lengths", uniformity > 65 and len(ss) > 3),
        ("low vocabulary diversity", q["vocabulary_diversity"] < 45 and q["word_count"] > 30),
    ] if yes], "authorship_assessment": "Inconclusive: linguistic patterns cannot establish AI authorship."}
