import json
import re
import time
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

console = Console()

DATA_FILE = Path(__file__).with_name("osint_4_data.json")


def load_data():
    if not DATA_FILE.exists():
        return {}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


DATA = load_data()

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


def glow_color(distance):
    distance = max(0.0, min(distance, 20.0))
    intensity = max(0.15, 1.0 - (distance / 18.0))
    r = int(180 * (0.4 + intensity))
    g = int((140 + 115 * intensity) * (0.7 + intensity))
    b = 255
    return f"#{r:02x}{g:02x}{b:02x}"


results = []
found = 0
checked = 0
username_global = ""


def render(glow_x):
    t = Text()
    for i, line in enumerate([l for l in ASCII_LINES.splitlines() if l.strip()]):
        t.append(line + "\n", style=f"bold {glow_color(abs(i - glow_x))}")

    t.append("\n╔════════════════════════════╗\n", style="cyan")
    t.append("║   OSINT USERNAME SCANNER  ║\n", style="cyan")
    t.append("╚════════════════════════════╝\n", style="cyan")

    t.append(f"\nTARGET : {username_global}")
    t.append(f"\nFOUND  : {found}/{len(DATA)}")
    t.append(f"\nCHECKED: {checked}\n")
    t.append("\nosint@kernel: ~/home/osint-tools/username-checker$ \n")

    for r in results[-10:]:
        t.append(r + "\n")

    return Align.left(t)


async def check(session, name, data, username):
    url = (data.get("url") or "").replace("%USERNAME%", username)
    method = (data.get("method") or "get").lower()
    verification = (data.get("verification") or "status").lower()
    except_list = [x.replace("%USERNAME%", username) for x in (data.get("except") or [])]

    try:
        if method == "post":
            response = await session.post(url, timeout=10)
        else:
            response = await session.get(url, timeout=10)

        found_local = False
        if response.status == 200:
            text = await response.text()
            soup = BeautifulSoup(text, "html.parser")
            page_content = re.sub(r"<[^>]*>", "", text.lower().replace(url.lower(), "").replace(f"/{username.lower()}", ""))
            page_text = soup.get_text().lower().replace(url.lower(), "")
            page_title = soup.title.string.lower() if soup.title and soup.title.string else ""

            if "status" in verification:
                found_local = True
                for item in except_list:
                    low = item.lower()
                    if low in page_content or low in page_text or low in page_title:
                        found_local = False
                        break

            elif "username" in verification:
                for item in except_list:
                    low = item.lower()
                    page_content = page_content.replace(low, "")
                    page_text = page_text.replace(low, "")
                    page_title = page_title.replace(low, "")
                low_user = username.lower()
                found_local = low_user in page_title or low_user in page_content or low_user in page_text

            elif "keyword" in verification:
                found_local = False
                for item in except_list:
                    low = item.lower()
                    if low in page_content or low in page_text or low in page_title:
                        found_local = True
                        break

        return name, url, found_local, None
    except asyncio.TimeoutError:
        return name, url, False, "Error: Timeout"
    except aiohttp.ClientError:
        return name, url, False, "Error: Connection failed"
    except Exception as e:
        return name, url, False, f"Error: {e}"


async def scanner(username):
    global results, found, checked
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [check(session, name, data, username) for name, data in DATA.items()]

        for task in asyncio.as_completed(tasks):
            name, url, ok, err = await task
            checked += 1
            if ok:
                found += 1
                results.append(f"[FOUND] {name:<15} -> {url}")
            elif err:
                results.append(f"[ERROR] {name:<15} -> {err}")
            else:
                results.append(f"[MISS ] {name}")


def run():
    global results, found, checked, username_global, DATA
    DATA = load_data()
    results = []
    found = 0
    checked = 0

    glow_x = -10
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
    asyncio.run(live_mode())


async def live_mode():
    task = asyncio.create_task(scanner(username_global))
    glow_x = -10

    with Live(render(glow_x), refresh_per_second=30, console=console, screen=True) as live:
        while not task.done():
            live.update(render(glow_x))
            glow_x += 0.5
            await asyncio.sleep(0.05)
        await task

    console.clear()
    print("\nSCAN FINISHED\n")
    print(f"FOUND: {found}/{len(DATA)}\n")
    for r in results:
        print(r)
    input("\n0 = BACK")
