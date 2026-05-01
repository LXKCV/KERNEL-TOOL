import hashlib
import os
import re

SUSPICIOUS_EXTENSIONS = {".exe", ".dll", ".bat", ".ps1", ".scr", ".js", ".vbs", ".cmd", ".jar"}
SUSPICIOUS_STRINGS = [b"powershell", b"cmd.exe", b"wget ", b"curl ", b"base64", b"invoke-expression"]


def _hash_file(path: str, algo: str = "sha256") -> str:
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def analyze_file(path: str) -> dict:
    if not os.path.isfile(path):
        return {"error": "File not found"}

    size = os.path.getsize(path)
    ext = os.path.splitext(path)[1].lower()
    sha256 = _hash_file(path, "sha256")
    md5 = _hash_file(path, "md5")

    flags: list[str] = []
    if ext in SUSPICIOUS_EXTENSIONS:
        flags.append(f"Potentially risky extension: {ext}")
    if size > 25 * 1024 * 1024:
        flags.append("Large file (>25MB), inspect manually")

    try:
        with open(path, "rb") as f:
            blob = f.read(2 * 1024 * 1024)
        lowered = blob.lower()
        for marker in SUSPICIOUS_STRINGS:
            if marker in lowered:
                flags.append(f"Suspicious string marker found: {marker.decode(errors='ignore')}")

        if re.search(rb"https?://[^\s\"']+", blob):
            flags.append("Embedded URL found inside file content")
    except OSError as exc:
        return {"error": f"Failed to read file: {exc}"}

    return {
        "path": os.path.abspath(path),
        "size_bytes": size,
        "sha256": sha256,
        "md5": md5,
        "flags": flags or ["No obvious static red flags detected"],
    }
