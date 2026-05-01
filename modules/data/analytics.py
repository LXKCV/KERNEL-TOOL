from .storage import Storage


class AnalyticsService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def stats(self) -> dict:
        scans = self.storage.fetch_all("scans")
        domains = self.storage.fetch_all("domains")
        profiles = self.storage.fetch_all("profiles")

        recent_targets = [s["target"] for s in scans[:5]]
        relationships = []
        for scan in scans[:10]:
            relationships.append({
                "target": scan["target"],
                "result_size": len(scan["result_json"]),
            })

        return {
            "scan_count": len(scans),
            "domain_count": len(domains),
            "profile_count": len(profiles),
            "recent_targets": recent_targets,
            "relationships": relationships,
        }
