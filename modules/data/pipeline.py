from datetime import datetime, timezone
import re

from .storage import Storage
from .logger import OperationLogger


class PipelineRunner:
    def __init__(self, storage: Storage, logger: OperationLogger) -> None:
        self.storage = storage
        self.logger = logger

    def run(self, target: str) -> dict:
        now = datetime.now(timezone.utc).isoformat()
        self.logger.log(f"Pipeline started for target={target}")

        domain_matches = re.findall(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", target)
        profile_matches = re.findall(r"@([a-zA-Z0-9_]{3,})", target)
        domains = list(dict.fromkeys(domain_matches or [target.lower().replace(" ", "")]))
        profiles = [f"@{p}" for p in dict.fromkeys(profile_matches)] or ["@unknown"]

        result = {
            "target": target,
            "domains": domains,
            "profiles": profiles,
            "intel_score": min(100, 40 + len(domains) * 15 + len(profiles) * 10),
        }

        self.storage.save_scan(target, "pipeline", result, now)
        for d in domains:
            is_new = self.storage.upsert_domain(d, now)
            if is_new:
                self.storage.save_alert("new_domain", d, f"New domain discovered: {d}", now)
        for p in profiles:
            is_new = self.storage.upsert_profile(p, now)
            if is_new:
                self.storage.save_alert("new_profile", p, f"New profile discovered: {p}", now)

        self.logger.log(f"Pipeline finished for target={target}")
        return result
