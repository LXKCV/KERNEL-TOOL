import socket
import ssl
from datetime import datetime, timezone
from typing import Dict

from .domain_analysis import whois_lookup


def ssl_check(domain: str) -> Dict:
    ctx = ssl.create_default_context()
    with socket.create_connection((domain, 443), timeout=7) as sock:
        with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
            cert = ssock.getpeercert()
            return {
                "subject": cert.get("subject", []),
                "issuer": cert.get("issuer", []),
                "not_after": cert.get("notAfter"),
            }


def _parse_date(value: str):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None


def reputation_score(domain: str) -> Dict:
    score = 100
    indicators = []

    try:
        ssl_data = ssl_check(domain)
    except Exception as exc:
        ssl_data = {"error": str(exc)}
        score -= 35
        indicators.append("No valid SSL/TLS certificate on 443")

    whois = whois_lookup(domain)
    created = _parse_date(whois.get("created", "")) if isinstance(whois, dict) else None
    if created:
        age_days = (datetime.now(timezone.utc) - created).days
    else:
        age_days = None
        score -= 10
        indicators.append("Domain age unknown")

    if age_days is not None and age_days < 180:
        score -= 25
        indicators.append("Very young domain (<180 days)")

    if domain.count("-") >= 2 or len(domain.split(".")[0]) > 20:
        score -= 15
        indicators.append("Suspicious domain naming pattern")

    return {
        "domain": domain,
        "score": max(0, min(100, score)),
        "ssl": ssl_data,
        "domain_age_days": age_days,
        "indicators": indicators,
    }
