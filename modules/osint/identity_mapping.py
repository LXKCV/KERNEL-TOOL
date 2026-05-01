from typing import Dict, List


def map_identity(usernames: List[str], emails: List[str], domains: List[str]) -> Dict:
    links = []
    for u in usernames:
        for e in emails:
            if u.lower() in e.lower():
                links.append({"type": "username-email", "username": u, "email": e, "confidence": "medium"})
        for d in domains:
            if u.lower() in d.lower():
                links.append({"type": "username-domain", "username": u, "domain": d, "confidence": "low"})

    for e in emails:
        e_dom = e.split("@")[-1] if "@" in e else ""
        for d in domains:
            if e_dom == d or e_dom.endswith("." + d):
                links.append({"type": "email-domain", "email": e, "domain": d, "confidence": "high"})

    return {"links": links, "input": {"usernames": usernames, "emails": emails, "domains": domains}}
