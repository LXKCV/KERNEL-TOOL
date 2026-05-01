from .storage import Storage


class AlertService:
    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    def list_alerts(self, limit: int = 20) -> list[dict]:
        return self.storage.fetch_all("alerts")[:limit]
