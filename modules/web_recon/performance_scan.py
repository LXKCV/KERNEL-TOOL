from .common import fetch_url


def performance_scan(url: str) -> dict:
    result = fetch_url(url)
    headers = {k.lower(): v for k, v in result.headers.items()}
    insights = []

    if "cache-control" not in headers:
        insights.append("Missing Cache-Control header; caching policy could be improved.")
    if "content-encoding" not in headers:
        insights.append("Compression header not found; enable gzip/brotli for better transfer speed.")
    if result.elapsed_ms > 1000:
        insights.append("High server response time detected (>1000 ms).")
    elif result.elapsed_ms > 400:
        insights.append("Moderate response time detected; consider backend and CDN optimization.")

    return {
        "final_url": result.url,
        "status_code": result.status_code,
        "response_time_ms": round(result.elapsed_ms, 2),
        "insights": insights or ["No obvious basic performance issues detected."],
    }
