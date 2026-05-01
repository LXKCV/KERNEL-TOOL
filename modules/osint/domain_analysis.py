import json
import socket
import ssl
import urllib.parse
import urllib.request
from datetime import datetime
from typing import Dict, List


def _fetch_json(url: str, timeout: int = 10):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode("utf-8", errors="ignore"))


def whois_lookup(domain: str) -> Dict:
    # RDAP via IANA bootstrap.
    iana = _fetch_json("https://data.iana.org/rdap/dns.json")
    tld = domain.split(".")[-1].lower()
    service_url = None
    for entry in iana.get("services", []):
        tlds, urls = entry
        if tld in [x.lower() for x in tlds] and urls:
            service_url = urls[0]
            break
    if not service_url:
        return {"error": "No RDAP service found"}
    rdap = _fetch_json(urllib.parse.urljoin(service_url, f"domain/{domain}"))
    events = {ev.get("eventAction"): ev.get("eventDate") for ev in rdap.get("events", [])}
    return {
        "domain": domain,
        "handle": rdap.get("handle"),
        "status": rdap.get("status", []),
        "created": events.get("registration"),
        "expires": events.get("expiration"),
        "updated": events.get("last changed"),
    }


def dns_records(domain: str) -> Dict[str, List[str]]:
    out = {}
    try:
        out["A"] = sorted(set(i[4][0] for i in socket.getaddrinfo(domain, 80, proto=socket.IPPROTO_TCP)))
    except Exception:
        out["A"] = []
    # DNS over HTTPS for TXT/MX/NS
    for rtype in ["MX", "NS", "TXT"]:
        try:
            data = _fetch_json(f"https://dns.google/resolve?name={domain}&type={rtype}")
            out[rtype] = [a.get("data", "") for a in data.get("Answer", [])]
        except Exception:
            out[rtype] = []
    return out


def enumerate_subdomains(domain: str, limit: int = 50) -> List[str]:
    data = _fetch_json(f"https://crt.sh/?q=%25.{domain}&output=json")
    subs = set()
    for row in data:
        names = row.get("name_value", "").split("\n")
        for n in names:
            n = n.strip().lower()
            if n.endswith(domain.lower()):
                subs.add(n.replace("*.", ""))
    return sorted(subs)[:limit]


def analyze_domain(domain: str) -> Dict:
    return {
        "whois": whois_lookup(domain),
        "dns": dns_records(domain),
        "subdomains": enumerate_subdomains(domain),
    }
