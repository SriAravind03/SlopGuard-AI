from collections import Counter

from detection.text_preprocessor import sentences, words


def analyze_repetition(text: str) -> dict:
    ss = sentences(text)
    normalized = [" ".join(words(s)) for s in ss]
    repeated = [s for s, n in Counter(normalized).items() if len(s) >= 16 and n > 1]
    tokens = words(text)
    bigrams = list(zip(tokens, tokens[1:]))
    repeated_bigrams = sum(n - 1 for n in Counter(bigrams).values() if n > 1)
    token_ratio = repeated_bigrams / max(1, len(bigrams))
    sentence_ratio = sum(normalized.count(s) - 1 for s in set(normalized) if s in repeated) / max(1, len(ss))
    score = round(min(100, (token_ratio * 180 + sentence_ratio * 100)))
    return {"score": score, "repeated_sentences": repeated[:8], "repeated_bigram_ratio": round(token_ratio, 3)}
