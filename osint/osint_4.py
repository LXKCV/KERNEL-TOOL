import time
import asyncio
import aiohttp
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

console = Console()

# ─────────────────────────────────────────────
# DATABASE (INTERNAL OSINT DATA)
# ─────────────────────────────────────────────

DATA = {
    "Steam": {
        "url": "https://steamcommunity.com/id/%USERNAME%",
        "method": "get",
        "verification": "status",
        "except": None
    },
    "Telegram": {
        "url": "https://t.me/%USERNAME%",
        "method": "get",
        "verification": "keyword",
        "except": ["if you have telegram", "contact @%USERNAME%"]
    },
    "TikTok": {
        "url": "https://www.tiktok.com/@%USERNAME%",
        "method": "get",
        "verification": "keyword",
        "except": ["couldn't find this account", "not found"]
    },
    "Instagram": {
        "url": "https://www.instagram.com/%USERNAME%",
        "method": "get",
        "verification": "keyword",
        "except": ["sorry, this page isn't available"]
    },
    "GitHub": {
        "url": "https://github.com/%USERNAME%",
        "method": "get",
        "verification": "status",
        "except": None
    },
    "YouTube": {
        "url": "https://www.youtube.com/@%USERNAME%",
        "method": "get",
        "verification": "keyword",
        "except": ["this channel does not exist"]
    },
    "Twitch": {
        "url": "https://www.twitch.tv/%USERNAME%",
        "method": "get",
        "verification": "keyword",
        "except": ["isn't currently live", "404"]
    }
}

# ─────────────────────────────────────────────
# ASCII UI (IDENTIQUE)
# ─────────────────────────────────────────────

ASCII_LINES = """                          
                                           █    ██   ██████ ▓█████  ██▀███   ███▄    █  ▄▄▄       ███▄ ▄███▓▓█████     ▄████▄   ██░ ██ ▓█████  ▄████▄   ██ ▄█▀▓█████  ██▀███  
                                           ██  ▓██▒▒██    ▒ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▒████▄    ▓██▒▀█▀ ██▒▓█   ▀    ▒██▀ ▀█  ▓██░ ██▒▓█   ▀ ▒██▀ ▀█   ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒
                                          ▓██  ▒██░░ ▓██▄   ▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██  ▀█▄  ▓██    ▓██░▒███      ▒▓█    ▄ ▒██▀▀██░▒███   ▒▓█    ▄ ▓███▄░ ▒███   ▓██ ░▄█ ▒
                                          ▓▓█  ░██░  ▒   ██▒▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄    ▒▓▓▄ ▄██▒░▓█ ░██ ▒▓█  ▄ ▒▓▓▄ ▄██▒▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  
                                          ▒▒█████▓ ▒██████▒▒░▒████▒░██▓ ▒██▒▒██░   ▓██░ ▓█   ▓██▒▒██▒   ░██▒░▒████▒   ▒ ▓███▀ ░░▓█▒░██▓░▒████▒▒ ▓███▀ ░▒██▒ █▄░▒████▒░██▓ ▒██▒
                                         ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░   ░ ░▒ ▒  ░ ▒ ░░▒░▒░░ ▒░ ░░ ░▒ ▒  ░▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░
                                         ░░▒░ ░ ░ ░ ░▒  ░ ░ ░ ░  ░  ░▒ ░ ▒░░ ░░   ░ ▒░  ▒   ▒▒ ░░  ░      ░ ░ ░  ░     ░  ▒    ▒ ░▒░ ░ ░ ░  ░  ░  ▒   ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░
                                          ░░░ ░ ░ ░  ░  ░     ░     ░░   ░    ░   ░ ░   ░   ▒   ░      ░      ░      ░         ░  ░░ ░   ░   ░        ░ ░░ ░    ░     ░░   ░ 
                                            ░           ░     ░  ░   ░              ░       ░  ░       ░      ░  ░   ░ ░       ░  ░  ░   ░  ░░ ░      ░  ░      ░  ░   ░     
                                                                                             ░                       ░  
"""

# ─────────────────────────────────────────────
# GLOW SYSTEM
# ─────────────────────────────────────────────

def glow_color(distance):
    distance = max(0.0, min(distance, 20.0))
    intensity = max(0.15, 1.0 - (distance / 18.0))

    r = int(180 * (0.4 + intensity))
    g = int((140 + 115 * intensity) * (0.7 + intensity))
    b = 255

    return f"#{r:02x}{g:02x}{b:02x}"


# ─────────────────────────────────────────────
# STATE
# ─────────────────────────────────────────────

results = []
found = 0
checked = 0
username_global = ""


# ─────────────────────────────────────────────
# UI RENDER
# ─────────────────────────────────────────────

def render(glow_x):
    t = Text()

    for i, line in enumerate(ASCII_LINES.splitlines()):
        t.append(line + "\n", style=f"bold {glow_color(abs(i - glow_x))}")

    t.append("\n╔════════════════════════════╗\n", style="cyan")
    t.append("║   OSINT USERNAME SCANNER  ║\n", style="cyan")
    t.append("╚════════════════════════════╝\n", style="cyan")

    t.append(f"\nTARGET : {username_global}")
    t.append(f"\nFOUND  : {found}/{len(DATA)}")
    t.append(f"\nCHECKED: {checked}\n")

    t.append("\n──── LIVE RESULTS ────\n")

    for r in results[-10:]:
        t.append(r + "\n")

    return Align.left(t)


# ─────────────────────────────────────────────
# CORE CHECK ENGINE (MERGED LOGIC)
# ─────────────────────────────────────────────

async def check(session, name, data, username):
    url = data["url"].replace("%USERNAME%", username)
    method = data.get("method", "get")
    verification = data.get("verification", "status")
    except_list = data.get("except") or []

    try:
        if method == "post":
            r = await session.post(url, timeout=10)
        else:
            r = await session.get(url, timeout=10)

        text = (await r.text()).lower()

        ok = False

        # ── STATUS MODE ──
        if verification == "status":
            ok = (r.status == 200)

        # ── KEYWORD MODE ──
        elif verification == "keyword":
            ok = True
            for bad in except_list:
                if bad and bad.lower() in text:
                    ok = False

        # fallback anti false positive
        if "not found" in text or "doesn't exist" in text:
            ok = False

        return name, url, ok

    except:
        return name, url, False


# ─────────────────────────────────────────────
# SCANNER ENGINE
# ─────────────────────────────────────────────

async def scanner(username):
    global results, found, checked

    async with aiohttp.ClientSession() as session:

        tasks = [
            check(session, name, data, username)
            for name, data in DATA.items()
        ]

        for task in asyncio.as_completed(tasks):
            name, url, ok = await task

            checked += 1

            if ok:
                found += 1
                results.append(f"[FOUND] {name:<12} → {url}")
            else:
                results.append(f"[MISS ] {name}")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

def run():
    global results, found, checked, username_global

    results = []
    found = 0
    checked = 0

    glow_x = -10

    # BOOT ANIMATION
    with Live(console=console, refresh_per_second=30, screen=True) as live:
        for _ in range(40):
            live.update(Align.left(render(glow_x)))
            glow_x += 2
            time.sleep(0.03)

    console.clear()

    username_global = input("osint@kernel: ~/home/osint-tools/username-checker$ ").strip()

    if username_global == "0":
        return

    console.clear()

    async def live_mode():
        task = asyncio.create_task(scanner(username_global))

        with Live(console=console, refresh_per_second=30, screen=True) as live:
            while not task.done():
                live.update(render(glow_x))
                time.sleep(0.05)

            await task

    asyncio.run(live_mode())

    console.clear()

    print("\nSCAN FINISHED\n")
    print(f"FOUND: {found}/{len(DATA)}\n")

    for r in results:
        print(r)

    input("\n0 = BACK")