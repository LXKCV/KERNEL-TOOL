import math
import re

COMMON_PASSWORDS = {
    "123456", "password", "123456789", "qwerty", "abc123", "password1", "admin",
    "letmein", "welcome", "iloveyou", "123123", "000000"
}


def _charset_size(password: str) -> int:
    size = 0
    if re.search(r"[a-z]", password):
        size += 26
    if re.search(r"[A-Z]", password):
        size += 26
    if re.search(r"\d", password):
        size += 10
    if re.search(r"[^a-zA-Z0-9]", password):
        size += 32
    return size


def analyze_password_strength(password: str) -> dict:
    if not password:
        return {"score": 0, "entropy": 0.0, "label": "Very Weak", "common": False}

    charset = _charset_size(password)
    entropy = len(password) * math.log2(charset) if charset else 0.0
    lowered = password.lower()
    common = lowered in COMMON_PASSWORDS

    if common or entropy < 28:
        label, score = "Very Weak", 1
    elif entropy < 36:
        label, score = "Weak", 2
    elif entropy < 60:
        label, score = "Moderate", 3
    elif entropy < 80:
        label, score = "Strong", 4
    else:
        label, score = "Very Strong", 5

    return {
        "score": score,
        "entropy": round(entropy, 2),
        "label": label,
        "common": common,
    }
