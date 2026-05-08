import time
import re
import requests
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

console = Console()

# ─────────────────────────────────────────────
# GLOW
# ─────────────────────────────────────────────
def glow_color(distance):
    distance = max(0.0, min(distance, 20.0))
    intensity = max(0.15, 1.0 - (distance / 18.0))

    r = int(180 * (0.4 + intensity))
    g = int((140 + 115 * intensity) * (0.7 + intensity))
    b = 255

    r = max(30, min(255, r))
    g = max(60, min(255, g))
    b = max(180, min(255, b))

    return f"#{r:02x}{g:02x}{b:02x}"


# ─────────────────────────────────────────────
# ASCII
# ─────────────────────────────────────────────
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
# RENDER
# ─────────────────────────────────────────────
def render(glow_x):
    t = Text()

    for i, line in enumerate(ASCII_LINES.splitlines()):
        color = glow_color(abs(i - glow_x))
        t.append(line + "\n", style=f"bold {color}")

    title = "ENTER IP TO ANALYZE"
    sub = "(0 = BACK)"

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
# RISK SCORE
# ─────────────────────────────────────────────
def calculate_risk(org, hostname):

    risk = 0

    suspicious = [
        "vpn",
        "proxy",
        "hosting",
        "cloud",
        "digitalocean",
        "ovh",
        "m247",
        "tor",
        "amazon",
        "google",
        "microsoft"
    ]

    data = f"{org} {hostname}".lower()

    for word in suspicious:
        if word in data:
            risk += 20

    if risk > 100:
        risk = 100

    return f"{risk}/100"


# ─────────────────────────────────────────────
# LOOKUP
# ─────────────────────────────────────────────
def get_ip_info(ip):

    try:
        r = requests.get(f"https://ipinfo.io/{ip}/json", timeout=5)

        if r.status_code != 200:
            return None

        data = r.json()

        loc = data.get("loc", "?,?")
        lat, lon = loc.split(",")

        org = data.get("org", "?")
        hostname = data.get("hostname", "?")

        lowered = org.lower()

        vpn_detected = (
            "YES"
            if any(x in lowered for x in [
                "vpn",
                "proxy",
                "hosting",
                "cloud",
                "ovh",
                "tor",
                "digitalocean",
                "m247"
            ])
            else "NO"
        )

        return {
            "IP": ip,
            "COUNTRY": data.get("country", "?"),
            "CITY": data.get("city", "?"),
            "REGION": data.get("region", "?"),
            "ASN": org.split(" ")[0] if " " in org else "?",
            "ISP": org,
            "VPN/PROXY/TOR": vpn_detected,
            "HOSTING": "YES" if "hosting" in lowered or "cloud" in lowered else "NO",
            "LATITUDE": lat,
            "LONGITUDE": lon,
            "TIMEZONE": data.get("timezone", "?"),
            "REVERSE DNS": hostname,
            "RISK SCORE": calculate_risk(org, hostname)
        }

    except:
        return None


# ─────────────────────────────────────────────
# RUN
# ─────────────────────────────────────────────
def run():

    fps = 30
    frame_delay = 1 / fps
    glow_x = -20

    with Live(console=console, refresh_per_second=fps, screen=True) as live:

        for _ in range(50):

            live.update(Align.left(render(glow_x)))

            glow_x += 2.5

            if glow_x > len(ASCII_LINES.splitlines()) + 40:
                glow_x = -20

            time.sleep(frame_delay)

    while True:

        console.clear()
        console.print(render(glow_x))

        ip = input("osint@kernel: ~/home/osint-tools/ip-lookup$ ").strip()

        if ip == "0":
            return

        if not is_valid_ip(ip):

            print("\nINVALID IP\n")
            time.sleep(1)
            continue

        print("\nLOOKUP...\n")

        data = get_ip_info(ip)

        if not data:

            print("NO DATA FOUND")
            time.sleep(1)
            continue

        print("\nRESULTS:\n")

        for k, v in data.items():
            print(f"{k}: {v}")

        input("\nPRESS ENTER TO CONTINUE...")