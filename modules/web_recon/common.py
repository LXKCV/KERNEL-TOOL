import time
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

DEFAULT_TIMEOUT = 10
USER_AGENT = "KernelTool-WebRecon/1.0"


@dataclass
class FetchResult:
    url: str
    status_code: int
    headers: dict
    body: str
    elapsed_ms: float


def normalize_url(url: str) -> str:
    parsed = urlparse(url.strip())
    if not parsed.scheme:
        return f"https://{url.strip()}"
    return url.strip()


def fetch_url(url: str, timeout: int = DEFAULT_TIMEOUT) -> FetchResult:
    target = normalize_url(url)
    req = Request(target, headers={"User-Agent": USER_AGENT})
    start = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as res:
            body = res.read(512000).decode("utf-8", errors="ignore")
            elapsed = (time.perf_counter() - start) * 1000
            return FetchResult(
                url=res.geturl(),
                status_code=getattr(res, "status", 200),
                headers={k: v for k, v in res.getheaders()},
                body=body,
                elapsed_ms=elapsed,
            )
    except HTTPError as exc:
        elapsed = (time.perf_counter() - start) * 1000
        return FetchResult(target, exc.code, dict(exc.headers.items()), "", elapsed)
    except URLError as exc:
        raise RuntimeError(f"Network error while requesting {target}: {exc}") from exc
