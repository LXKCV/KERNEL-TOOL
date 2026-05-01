from collections import deque
from urllib.parse import urlparse

from .common import normalize_url
from .link_extractor import extract_links


def map_site(url: str, max_pages: int = 20) -> dict:
    start = normalize_url(url)
    domain = urlparse(start).netloc
    queue = deque([start])
    visited = set()
    pages = []

    while queue and len(visited) < max_pages:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        try:
            links = extract_links(current)
        except Exception:
            continue

        pages.append({
            "url": current,
            "internal_links_count": len(links["internal_links"]),
            "external_links_count": len(links["external_links"]),
        })

        for link in links["internal_links"]:
            if urlparse(link).netloc == domain and link not in visited:
                queue.append(link)

    return {"domain": domain, "pages_crawled": len(pages), "pages": pages}
