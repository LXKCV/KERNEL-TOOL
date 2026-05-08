import time
import re
import socket
import threading
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

console = Console()

# ─────────────────────────────────────────────
# GLOW UI
# ─────────────────────────────────────────────
def glow_color(distance):
    distance = max(0.0, min(distance, 20.0))
    intensity = max(0.15, 1.0 - (distance / 18.0))

    r = int(180 * (0.4 + intensity))
    g = int((140 + 115 * intensity) * (0.7 + intensity))
    b = 255

    return f"#{r:02x}{g:02x}{b:02x}"


ASCII_LINES = """
                                           ██ ▄█▀▓█████  ██▀███   ███▄    █ ▓█████  ██▓       ▄▄▄█████▓ ▒█████   ▒█████   ██▓    
                                           ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▓█   ▀ ▓██▒       ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    
                                          ▓███▄░ ▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒███   ▒██░       ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    
                                          ▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒▒▓█  ▄ ▒██░       ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░    
                                          ▒██▒ █▄░▒████▒░██▓ ▒██▒▒██░   ▓██░░▒████▒░██████▒     ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒
                                          ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒░▓  ░     ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░
                                          ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░ ░░   ░ ▒░ ░ ░  ░░ ░ ▒  ░       ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░
                                             ░ ░░ ░    ░     ░░   ░    ░   ░ ░    ░     ░ ░        ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   
                                             ░  ░      ░  ░   ░              ░    ░  ░    ░  ░                ░ ░      ░ ░      ░ 
"""

# ─────────────────────────────────────────────
# UI RENDER
# ─────────────────────────────────────────────
def render(glow_x):
    t = Text()

    for i, line in enumerate(ASCII_LINES.splitlines()):
        color = glow_color(abs(i - glow_x))
        t.append(line + "\n", style=f"bold {color}")

    title = "ENTER IP TO ANALYZE"
    sub = "(0 = EXIT)"

    color = glow_color(glow_x)
    width = max(len(title), len(sub))

    t.append("\n")
    t.append("╔" + "═" * (width + 2) + "╗\n", style=color)
    t.append(f"║ {title.ljust(width)} ║\n", style=color)
    t.append(f"║ {sub.ljust(width)} ║\n", style=color)
    t.append("╚" + "═" * (width + 2) + "╝\n", style=color)

    return t


# ─────────────────────────────────────────────
# VALID IP
# ─────────────────────────────────────────────
def is_valid_ip(ip):
    pattern = r"^((25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(25[0-5]|2[0-4]\d|1?\d?\d)$"
    return re.match(pattern, ip) is not None


# ─────────────────────────────────────────────
# FAKE OSINT SIMULATION (NO API)
# ─────────────────────────────────────────────
def fake_ip_intel(ip):

    # heuristics simples (local logic)
    vpn_keywords = ["vpn", "proxy", "cloud", "hosting", "tor"]

    risk = 0

    # simulation ASN fake
    if ip.startswith("185.") or ip.startswith("146.") or ip.startswith("51."):
        isp = "Datacenter Provider (likely hosting)"
        risk += 40
    else:
        isp = "Residential ISP"

    # fake vpn guess
    vpn = "YES" if any(x in isp.lower() for x in vpn_keywords) else "NO"

    if vpn == "YES":
        risk += 30

    if "datacenter" in isp.lower():
        risk += 20

    risk = min(risk, 100)

    return {
        "IP": ip,
        "COUNTRY": "UNKNOWN (no API)",
        "CITY": "UNKNOWN",
        "REGION": "UNKNOWN",
        "ASN": "SIMULATED",
        "ISP": isp,
        "VPN/PROXY/TOR": vpn,
        "HOSTING": "YES" if "datacenter" in isp.lower() else "NO",
        "LATITUDE": "N/A",
        "LONGITUDE": "N/A",
        "TIMEZONE": "N/A",
        "REVERSE DNS": socket.getfqdn(ip),
        "RISK SCORE": f"{risk}/100"
    }


# ─────────────────────────────────────────────
# PORT SCANNER (REAL)
# ─────────────────────────────────────────────
def scan_ports(ip):

    ports = [21, 22, 80, 443, 3306, 3389]
    results = {}

    def check(port):
        s = socket.socket()
        s.settimeout(0.8)
        try:
            s.connect((ip, port))
            results[port] = "OPEN"
        except:
            results[port] = "CLOSED"
        finally:
            s.close()

    threads = []
    for p in ports:
        t = threading.Thread(target=check, args=(p,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return results


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
def run():

    fps = 30
    glow_x = -20

    with Live(console=console, refresh_per_second=fps, screen=True) as live:

        for _ in range(40):
            live.update(Align.left(render(glow_x)))
            glow_x += 2.5
            time.sleep(0.03)

    while True:

        console.clear()
        console.print(render(glow_x))

        ip = input("osint@kernel: ~/home/osint-tools/ip-intelligence-panel$ ").strip()

        if ip == "0":
            return

        if not is_valid_ip(ip):
            print("\nINVALID IP\n")
            time.sleep(1)
            continue

        print("\nANALYZING LOCAL INTEL...\n")

        data = fake_ip_intel(ip)
        ports = scan_ports(ip)

        print("\n=== IP INTEL ===")
        for k, v in data.items():
            print(f"{k}: {v}")

        print("\n=== PORT SCAN ===")
        for p, status in ports.items():
            print(f"{p}: {status}")

        input("\nPRESS ENTER...")