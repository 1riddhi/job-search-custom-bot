import re
from config import BAD_KEYWORDS, INDIA_LOCATIONS


def is_role(title: str) -> bool:
    if not title:
        return False

    t = title.lower()
    t = re.sub(r"[^a-z0-9\s]", " ", t)
    t = re.sub(r"\s+", " ", t)

    for bad in BAD_KEYWORDS:
        if bad in t:
            return False

    return True


def is_india(location) -> bool:
    if not location:
        return False

    loc = str(location).lower()
    return any(x in loc for x in INDIA_LOCATIONS)


def extract_yoe(text: str):
    if not text:
        return None

    text = text.lower()

    patterns = [
        r"(\d+)\+?\s*years?\s*(?:of experience)?",
        r"(\d+)\+?\s*yrs?",
        r"(\d+)\+?\s*years?\s*experience",
        r"at least\s*(\d+)\s*years?",
        r"minimum\s*(\d+)\s*years?",
        r"(\d+)\s*to\s*(\d+)\s*years?",
        r"(\d+)\+?\s*years?\s*in",
        r"(\d+)\+?\s*years?\s*working",
        r"(\d+)\+?\s*years?\s*professional",
        r"(\d+)\s*\+\s*years?"
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            return int(m.group(1))

    return None