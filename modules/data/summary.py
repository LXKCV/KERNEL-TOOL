from .storage import Storage


class AISummaryService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def summarize(self) -> str:
        scans = self.storage.fetch_all("scans")
        domains = self.storage.fetch_all("domains")
        profiles = self.storage.fetch_all("profiles")
        if not scans:
            return "No intelligence data collected yet. Run the pipeline first."

        top_target = scans[0]["target"]
        return (
            "AI Summary: "
            f"{len(scans)} scans have been collected. "
            f"Tracked assets include {len(domains)} domains and {len(profiles)} profiles. "
            f"The most recent investigation target is '{top_target}'."
        )
