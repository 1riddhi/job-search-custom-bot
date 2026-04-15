import re
from config import KEYWORDS, BAD_KEYWORDS, INDIA_LOCATIONS

def norm(x):
    return (x or "").lower()

def is_india(text):
    t = norm(text)
    return any(k in t for k in INDIA_LOCATIONS)

def is_bad_role(title):
    t = norm(title)
    return any(k in t for k in BAD_KEYWORDS)

def is_role(title):
    t = norm(title)
    return any(k in t for k in KEYWORDS) and not is_bad_role(title)

def extract_yoe(text):
    if not text:
        return "Not specified"

    patterns = [
        r"\d+\+?\s*years?",
        r"\d+\s*-\s*\d+\s*years?"
    ]

    for p in patterns:
        m = re.search(p, text.lower())
        if m:
            return m.group(0)

    return "Not specified"