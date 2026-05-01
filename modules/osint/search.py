import re
import urllib.parse
import urllib.request
from typing import Dict, List

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"


def _fetch(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read().decode("utf-8", errors="ignore")


def search_duckduckgo(query: str, limit: int = 5) -> List[Dict[str, str]]:
    url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    html = _fetch(url)
    pattern = re.compile(r'<a rel="nofollow" class="result__a" href="(.*?)">(.*?)</a>', re.I)
    results = []
    for href, title in pattern.findall(html)[:limit]:
        clean_title = re.sub("<.*?>", "", title)
        results.append({"engine": "DuckDuckGo", "title": clean_title, "url": href})
    return results


def search_bing(query: str, limit: int = 5) -> List[Dict[str, str]]:
    url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
    html = _fetch(url)
    blocks = re.findall(r'<li class="b_algo".*?</li>', html, re.S)
    results = []
    for block in blocks[:limit]:
        m_url = re.search(r'<h2><a href="(.*?)"', block)
        m_title = re.search(r'<h2><a href=".*?">(.*?)</a>', block)
        if m_url and m_title:
            title = re.sub("<.*?>", "", m_title.group(1))
            results.append({"engine": "Bing", "title": title, "url": m_url.group(1)})
    return results


def search_google(query: str, limit: int = 5) -> List[Dict[str, str]]:
    # Safe placeholder: Google Programmable Search API can be configured via env vars.
    return [{
        "engine": "Google",
        "title": "Configure GOOGLE_API_KEY and GOOGLE_CSE_ID for live Google results",
        "url": "https://developers.google.com/custom-search/v1/overview",
    }][:limit]


def multi_source_search(query: str, limit: int = 5) -> Dict[str, List[Dict[str, str]]]:
    data = {}
    for name, fn in [("google", search_google), ("bing", search_bing), ("duckduckgo", search_duckduckgo)]:
        try:
            data[name] = fn(query, limit)
        except Exception as exc:
            data[name] = [{"engine": name.title(), "title": f"Error: {exc}", "url": ""}]
    return data
