import ipaddress
import socket
import subprocess


def _guess_local_cidr() -> str:
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    net = ipaddress.ip_network(f"{ip}/24", strict=False)
    return str(net)


def discover_local_devices(target_cidr: str | None = None, timeout_ms: int = 800) -> list[dict[str, str]]:
    """Use nmap ARP/ping discovery if available for local devices."""
    cidr = target_cidr or _guess_local_cidr()
    cmd = ["nmap", "-sn", "-n", "--max-retries", "1", "--host-timeout", f"{timeout_ms}ms", cidr]

    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
    except FileNotFoundError:
        return [{"error": "nmap not found. Install nmap for network discovery."}]
    except subprocess.CalledProcessError as exc:
        return [{"error": f"scan failed: {exc.output.strip()}"}]

    devices: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in output.splitlines():
        line = line.strip()
        if line.startswith("Nmap scan report for"):
            if current:
                devices.append(current)
            current = {"host": line.removeprefix("Nmap scan report for ").strip(), "mac": "unknown"}
        elif line.startswith("MAC Address:") and current is not None:
            current["mac"] = line.split("MAC Address:", 1)[1].strip()
    if current:
        devices.append(current)

    return devices
