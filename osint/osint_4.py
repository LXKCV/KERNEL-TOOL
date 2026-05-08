import time
import asyncio
import aiohttp
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
                                           █    ██   ██████ ▓█████  ██▀███   ███▄    █  ▄▄▄       ███▄ ▄███▓▓█████
                                           ██  ▓██▒▒██    ▒ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▒████▄    ▓██▒▀█▀ ██▒▓█   ▀
                                          ▓██  ▒██░░ ▓██▄   ▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒██  ▀█▄  ▓██    ▓██░▒███
                                          ▓▓█  ░██░  ▒   ██▒▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒░██▄▄▄▄██ ▒██    ▒██ ▒▓█  ▄
                                          ▒▒█████▓ ▒██████▒▒░▒████▒░██▓ ▒██▒▒██░   ▓██░ ▓█   ▓██▒▒██▒   ░██▒░▒████▒
                                          ░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒  ▒▒   ▓▒█░░ ▒░   ░  ░░░ ▒░ ░
                                          ░░▒░ ░ ░ ░ ░▒  ░ ░ ░ ░  ░  ░▒ ░ ▒░░ ░░   ░ ▒░  ▒   ▒▒ ░░  ░      ░ ░ ░  ░
                                           ░░░ ░ ░ ░  ░  ░     ░     ░░   ░    ░   ░ ░   ░   ▒   ░      ░      ░
                                             ░           ░     ░  ░   ░              ░       ░  ░       ░      ░  ░
"""


# ─────────────────────────────────────────────
# SITES
# ─────────────────────────────────────────────
SITES = {
    "GitHub": "https://github.com/{}",
    "Reddit": "https://reddit.com/user/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Instagram": "https://www.instagram.com/{}/",
    "Twitter": "https://x.com/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "Pinterest": "https://www.pinterest.com/{}/",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "YouTube": "https://www.youtube.com/@{}",
    "Telegram": "https://t.me/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "GitLab": "https://gitlab.com/{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Medium": "https://medium.com/@{}",
    "Patreon": "https://www.patreon.com/{}",
    "Kaggle": "https://www.kaggle.com/{}",
    "DockerHub": "https://hub.docker.com/u/{}",
    "VSCO": "https://vsco.co/{}/gallery",
    "Chess": "https://www.chess.com/member/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Fiverr": "https://www.fiverr.com/{}",
    "DeviantArt": "https://www.deviantart.com/{}",
    "Behance": "https://www.behance.net/{}",
    "Guns.lol": "https://guns.lol/{}",
}


# ─────────────────────────────────────────────
# RENDER UI
# ─────────────────────────────────────────────
def render(glow_x):
    t = Text()

    for i, line in enumerate(ASCII_LINES.splitlines()):
        color = glow_color(abs(i - glow_x))
        t.append(line + "\n", style=f"bold {color}")

    title = "ENTER USERNAME TO CHECK"
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
# CHECKER
# ─────────────────────────────────────────────
async def check_site(session, site, url, username):
    full_url = url.format(username)

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        async with session.get(
            full_url,
            headers=headers,
            timeout=8,
            allow_redirects=True
        ) as response:

            text = await response.text()

            if response.status == 200:

                lower = text.lower()

                bad_strings = [
                    "not found",
                    "page unavailable",
                    "doesn't exist",
                    "error",
                    "404"
                ]

                if any(x in lower for x in bad_strings):
                    return ("MISS", site, full_url)

                return ("FOUND", site, full_url)

            return ("MISS", site, full_url)

    except:
        return ("ERROR", site, full_url)


async def scan_username(username):

    results = []

    connector = aiohttp.TCPConnector(ssl=False)

    async with aiohttp.ClientSession(
        connector=connector
    ) as session:

        tasks = []

        for site, url in SITES.items():
            tasks.append(
                check_site(session, site, url, username)
            )

        results = await asyncio.gather(*tasks)

    return results


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def run():

    fps = 30
    frame_delay = 1 / fps
    glow_x = -20

    # ─── INTRO ANIMATION ───
    with Live(console=console, refresh_per_second=fps, screen=True) as live:

        for _ in range(60):

            frame = render(glow_x)
            live.update(Align.left(frame))

            glow_x += 2.5

            if glow_x > len(ASCII_LINES.splitlines()) + 40:
                glow_x = -20

            time.sleep(frame_delay)

    # ─── INPUT ───
    console.clear()
    console.print(render(glow_x))

    username = input(
        "osint@kernel: ~/home/osint-tools/username-checker$ "
    ).strip()

    if username == "0":
        return

    if len(username) < 2:
        print("invalid username")
        time.sleep(1)
        return

    console.clear()

    print(f"\nSCANNING 100+ SITES FOR: {username}\n")

    start = time.time()

    results = asyncio.run(
        scan_username(username)
    )

    found = 0
    miss = 0
    errors = 0

    for status, site, url in results:

        if status == "FOUND":
            found += 1
            print(f"[FOUND] {site:<20} -> {url}")

        elif status == "MISS":
            miss += 1
            print(f"[MISS ] {site:<20}")

        else:
            errors += 1
            print(f"[ERROR] {site:<20}")

    elapsed = round(time.time() - start, 2)

    print("\n══════════════════════════════")
    print(f"FOUND : {found}")
    print(f"MISS  : {miss}")
    print(f"ERROR : {errors}")
    print(f"TIME  : {elapsed}s")
    print("══════════════════════════════")

    input("\nENTER TO BACK...")