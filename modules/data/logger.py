from datetime import datetime, timezone
from pathlib import Path


class OperationLogger:
    def __init__(self, log_file: str = "logs/operations.log") -> None:
        self.log_path = Path(log_file)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(self, message: str) -> None:
        ts = datetime.now(timezone.utc).isoformat()
        with self.log_path.open("a", encoding="utf-8") as f:
            f.write(f"{ts} | {message}\n")
