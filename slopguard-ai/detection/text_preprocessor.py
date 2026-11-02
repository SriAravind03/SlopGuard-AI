import re
import unicodedata


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = text.replace("\x00", " ")
    return re.sub(r"\s+", " ", text).strip()


def sentences(text: str) -> list[str]:
    if not text:
        return []
    # Split on sentence punctuation while preserving common decimal/abbreviation cases reasonably.
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'“‘])|\n+", text) if s.strip()]


def words(text: str) -> list[str]:
    return re.findall(r"[\w]+(?:['’][\w]+)?", text.casefold(), flags=re.UNICODE)
