import re
from collections import Counter

from detection.text_preprocessor import sentences, words

GENERIC_PHRASES = (
    "in today's world", "it is important to note", "plays a crucial role", "in conclusion",
    "delve into", "furthermore", "moreover", "it is worth noting", "a wide range of",
    "in summary", "on the other hand", "this comprehensive guide", "in the ever-evolving",
)
TRANSITIONS = ("however", "moreover", "furthermore", "additionally", "in conclusion", "therefore", "consequently")


def analyze_quality(text: str) -> dict:
    ss, tokens = sentences(text), words(text)
    counts = Counter(tokens)
    avg = sum(map(len, map(words, ss))) / max(1, len(ss))
    lengths = [len(words(s)) for s in ss]
    variance = (sum((n - avg) ** 2 for n in lengths) / max(1, len(lengths))) ** 0.5
    generic = [(phrase, len(re.findall(re.escape(phrase), text.casefold()))) for phrase in GENERIC_PHRASES]
    generic_total = sum(count for _, count in generic)
    transition_total = sum(text.casefold().count(t) for t in TRANSITIONS)
    # Repeated non-stopword terms can signal stuffing; common function words are excluded.
    stop = set("the a an and or but to of in on for with is are was were be this that it as by from at we you they their".split())
    content_tokens = [w for w in tokens if len(w) > 3 and w not in stop]
    keyword_hits = sorted(((w, n) for w, n in Counter(content_tokens).items() if n >= 4 and n / max(1, len(tokens)) > .035), key=lambda x: -x[1])[:8]
    diversity = len(set(tokens)) / max(1, len(tokens))
    # Density proxy rewards concrete named/numeric terms and penalizes generic filler and empty sentences.
    concrete = sum(bool(re.search(r"\d|\b[A-Z][a-z]{2,}\b", s)) for s in ss)
    density = max(0, min(100, round(65 * min(1, len(tokens) / 100) + 25 * concrete / max(1, len(ss)) - min(35, generic_total * 5))))
    generic_score = min(100, generic_total * 18 + transition_total * 4)
    stuffing = min(100, round(100 * sum(n for _, n in keyword_hits) / max(1, len(tokens)) * 3.5))
    return {
        "vocabulary_diversity": round(diversity * 100), "average_sentence_length": round(avg, 1),
        "sentence_length_variation": round(variance, 1), "information_density": density,
        "generic_phrase_count": generic_total, "generic_phrases": [p for p, n in generic if n],
        "generic_pattern_score": generic_score, "transition_count": transition_total,
        "keyword_stuffing_score": stuffing, "repeated_keywords": [w for w, _ in keyword_hits],
        "sentence_count": len(ss), "word_count": len(tokens),
    }
