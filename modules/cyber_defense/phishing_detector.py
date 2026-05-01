from urllib.parse import urlparse
import re

SUSPICIOUS_KEYWORDS = {"login", "verify", "secure", "update", "banking", "signin", "password", "wallet"}


def analyze_url(url: str) -> dict:
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = f"http://{url}"

    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    reasons: list[str] = []
    score = 0

    if parsed.scheme != "https":
        score += 2
        reasons.append("URL does not use HTTPS")

    if "@" in url:
        score += 3
        reasons.append("Contains '@' redirection pattern")

    if re.search(r"\d+\.\d+\.\d+\.\d+", host):
        score += 3
        reasons.append("Uses raw IP address instead of domain")

    if host.count("-") >= 3:
        score += 2
        reasons.append("Excessive hyphens in hostname")

    if len(host) > 45:
        score += 2
        reasons.append("Unusually long domain name")

    if any(keyword in f"{host}{path}" for keyword in SUSPICIOUS_KEYWORDS):
        score += 2
        reasons.append("Contains credential-themed keywords")

    if parsed.query and any(tok in parsed.query.lower() for tok in ["token", "session", "redirect"]):
        score += 1
        reasons.append("Query string contains sensitive-sounding parameters")

    risk = "Low"
    if score >= 7:
        risk = "High"
    elif score >= 4:
        risk = "Medium"

    return {
        "normalized_url": parsed.geturl(),
        "domain": host,
        "risk": risk,
        "score": score,
        "reasons": reasons or ["No major phishing heuristics triggered"],
    }
