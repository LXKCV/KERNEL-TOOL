import json
from urllib.parse import quote
from urllib.request import Request, urlopen

from .common import normalize_url, USER_AGENT


def archive_explorer(url: str, limit: int = 10) -> dict:
    target = normalize_url(url)
    encoded = quote(target, safe="")
    endpoint = (
        "https://web.archive.org/cdx/search/cdx"
        f"?url={encoded}&output=json&fl=timestamp,original,statuscode,mimetype&limit={limit}"
    )
    req = Request(endpoint, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=12) as res:
        data = json.loads(res.read().decode("utf-8", errors="ignore"))

    if not data or len(data) == 1:
        return {"target": target, "snapshots": []}

    snapshots = []
    for row in data[1:]:
        ts, original, status, mimetype = row
        snapshots.append(
            {
                "timestamp": ts,
                "archive_url": f"https://web.archive.org/web/{ts}/{original}",
                "status": status,
                "mimetype": mimetype,
            }
        )

    return {"target": target, "snapshots": snapshots}
