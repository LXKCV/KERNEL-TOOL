import socket
from typing import Iterable


def safe_port_scan(host: str, ports: Iterable[int], timeout: float = 0.4) -> dict[int, str]:
    """Perform a conservative TCP connect scan on selected ports."""
    results: dict[int, str] = {}
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            code = sock.connect_ex((host, port))
            results[port] = "open" if code == 0 else "closed"
    return results
