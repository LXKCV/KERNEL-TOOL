from .common import fetch_url

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Content-Type-Options",
    "X-Frame-Options",
    "Referrer-Policy",
    "Permissions-Policy",
]


def analyze_headers(url: str) -> dict:
    result = fetch_url(url)
    headers = result.headers
    missing = [h for h in SECURITY_HEADERS if h not in headers]
    return {
        "final_url": result.url,
        "status_code": result.status_code,
        "headers": headers,
        "missing_security_headers": missing,
    }
