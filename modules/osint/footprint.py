import re
import urllib.parse
import urllib.request
from typing import Dict, List


def _fetch(url: str, timeout: int = 10) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return res.read().decode("utf-8", errors="ignore")


def email_osint(email: str) -> Dict:
    domain = email.split("@")[-1] if "@" in email else ""
    patterns = {
        "valid_format": bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email)),
        "domain": domain,
        "possible_breaches_source": "Use HaveIBeenPwned API key for direct breach lookup",
    }
    return patterns


def username_search(username: str) -> List[Dict[str, str]]:
    platforms = {
        "GitHub": f"https://github.com/{username}",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "Twitter": f"https://x.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
    }
    results = []
    for name, url in platforms.items():
        status = "unknown"
        try:
            req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as res:
                status = "found" if res.status < 400 else "not_found"
        except Exception:
            status = "not_found"
        results.append({"platform": name, "url": url, "status": status})
    return results
