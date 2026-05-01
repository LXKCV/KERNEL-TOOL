from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

from .common import fetch_url


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        for key, value in attrs:
            if key.lower() == "href" and value:
                self.links.append(value)


def extract_links(url: str) -> dict:
    result = fetch_url(url)
    parser = AnchorParser()
    parser.feed(result.body)

    base_domain = urlparse(result.url).netloc
    internal, external = set(), set()

    for href in parser.links:
        absolute = urljoin(result.url, href)
        if urlparse(absolute).scheme not in {"http", "https"}:
            continue
        if urlparse(absolute).netloc == base_domain:
            internal.add(absolute)
        else:
            external.add(absolute)

    return {
        "final_url": result.url,
        "status_code": result.status_code,
        "internal_links": sorted(internal),
        "external_links": sorted(external),
    }
