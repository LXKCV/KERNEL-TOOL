import re
import time
import random
import string
import socket
import smtplib

from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

from config import glow_color, Add, Error, Info, Input, WaitMsg

try:
    import dns.resolver
except Exception:
    dns = None

console = Console()

ASCII_LINES = """
                                           ▓█████  ███▄ ▄███▓ ▄▄▄       ██▓ ██▓        ██▓     ▒█████   ▒█████   ██ ▄█▀ █    ██  ██▓███  
                                           ▓█   ▀ ▓██▒▀█▀ ██▒▒████▄    ▓██▒▓██▒       ▓██▒    ▒██▒  ██▒▒██▒  ██▒ ██▄█▒  ██  ▓██▒▓██░  ██▒
                                           ▒███   ▓██    ▓██░▒██  ▀█▄  ▒██▒▒██░       ▒██░    ▒██░  ██▒▒██░  ██▒▓███▄░ ▓██  ▒██░▓██░ ██▓▒
                                           ▒▓█  ▄ ▒██    ▒██ ░██▄▄▄▄██ ░██░▒██░       ▒██░    ▒██   ██░▒██   ██░▓██ █▄ ▓▓█  ░██░▒██▄█▓▒ ▒
                                           ░▒████▒▒██▒   ░██▒ ▓█   ▓██▒░██░░██████▒   ░██████▒░ ████▓▒░░ ████▓▒░▒██▒ █▄▒▒█████▓ ▒██▒ ░  ░
                                           ░░ ▒░ ░░ ▒░   ░  ░ ▒▒   ▓▒█░░▓  ░ ▒░▓  ░   ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░
                                            ░ ░  ░░  ░      ░  ▒   ▒▒ ░ ▒ ░░ ░ ▒  ░   ░ ░ ▒  ░  ░ ▒ ▒░   ░ ▒ ▒░ ░ ░▒ ▒░░░▒░ ░ ░ ░▒ ░     
                                              ░   ░      ░     ░   ▒    ▒ ░  ░ ░        ░ ░   ░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░░ ░  ░░░ ░ ░ ░░       
                                              ░  ░       ░         ░  ░ ░      ░  ░       ░  ░    ░ ░      ░ ░  ░  ░      ░              
"""


def render(glow_x: float):
    t = Text()
    for i, line in enumerate(ASCII_LINES.splitlines()):
        t.append(line + "\n", style=f"bold {glow_color(abs(i - glow_x))}")

    title = "ENTER EMAIL TO ANALYZE"
    sub = "(0 = BACK)"
    color = glow_color(glow_x)
    width = max(len(title), len(sub))

    t.append("\n")
    t.append("╔" + "═" * (width + 2) + "╗\n", style=color)
    t.append(f"║ {title.ljust(width)} ║\n", style=color)
    t.append(f"║ {sub.ljust(width)} ║\n", style=color)
    t.append("╚" + "═" * (width + 2) + "╝\n", style=color)
    return t


def target_get_ip(domain: str):
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def ip_get_dns(ip: str):
    try:
        return socket.gethostbyaddr(ip)[0]
    except Exception:
        return None


def lookup(email: str, socket_timeout: float):
    try:
        domain_all = email.split("@")[-1]
    except Exception:
        domain_all = None
    try:
        name = email.split("@")[0]
    except Exception:
        name = None
    try:
        domain = re.search(r"@([^@.]+)\.", email).group(1)
    except Exception:
        domain = None
    try:
        tld = f".{email.split('.')[-1]}"
    except Exception:
        tld = None

    valid_syntax = re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None

    domain_ip = target_get_ip(domain_all) if domain_all else None
    domain_reverse_dns = ip_get_dns(domain_ip) if domain_ip else None

    domain_smtp_banner = None
    domain_starttls = None
    domain_smtp_check = None
    domain_catch_all = None

    try:
        if dns is not None and domain_all:
            mx_servers = [str(r.exchange).rstrip(".") for r in dns.resolver.resolve(domain_all, "MX")]
            for server in mx_servers:
                try:
                    s = smtplib.SMTP(timeout=socket_timeout)
                    _, banner = s.connect(server)
                    domain_smtp_banner = banner.decode() if isinstance(banner, bytes) else str(banner)
                    s.ehlo()
                    domain_starttls = s.has_extn("starttls")
                    s.mail("test@test.com")
                    code_real, _ = s.rcpt(email)
                    fake = "".join(random.choices(string.ascii_lowercase, k=10))
                    code_fake, _ = s.rcpt(f"{fake}@{domain_all}")
                    domain_smtp_check = code_real == 250
                    domain_catch_all = code_fake == 250
                    s.quit()
                    break
                except Exception:
                    continue
    except Exception:
        pass

    email_infos = {
        "Email": email,
        "Name": name,
        "Domain": domain,
        "Domain all": domain_all,
        "TLD": tld,
        "Valid syntax": valid_syntax,
        "Domain IP": domain_ip,
        "Domain reverse DNS": domain_reverse_dns,
        "Domain SMTP banner": domain_smtp_banner,
        "Domain STARTTLS": domain_starttls,
        "Domain SMTP valid": domain_smtp_check,
        "Domain catch-all": domain_catch_all,
    }

    for k, v in email_infos.items():
        if v is not None:
            Add(f"{k}: {v}")


def run():
    fps = 30
    glow_x = -20
    with Live(console=console, refresh_per_second=fps, screen=True) as live:
        for _ in range(50):
            live.update(Align.left(render(glow_x)))
            glow_x += 2.5
            if glow_x > len(ASCII_LINES.splitlines()) + 40:
                glow_x = -20
            time.sleep(1 / fps)

    while True:
        console.clear()
        console.print(render(glow_x))

        email = Input("Email -> ").strip()
        if email == "0":
            return
        if "@" not in email:
            Error("Invalid email format.")
            time.sleep(1)
            continue

        timeout_raw = Input("Max socket timeout (default: 5) -> ").strip()
        timeout = 5.0
        if timeout_raw:
            try:
                timeout = float(timeout_raw)
            except ValueError:
                Error("Invalid timeout value.")
                time.sleep(1)
                continue

        Info(f"Max socket timeout: {timeout}s")
        WaitMsg("Scanning...")
        lookup(email, timeout)
        input("\nENTER TO CONTINUE...")
