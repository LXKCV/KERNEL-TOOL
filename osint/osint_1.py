import time
import random
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

console = Console()


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


def render(glow_x):
    t = Text()

    for i, line in enumerate(ASCII_LINES.splitlines()):
        color = glow_color(abs(i - glow_x))
        t.append(line + "\n", style=f"bold {color}")

    title = "ENTER NUMBER OF IPs TO GENERATE"
    sub = "(0 = BACK)"

    color = glow_color(glow_x)
    width = max(len(title), len(sub))

    t.append("\n")
    t.append("╔" + "═" * (width + 2) + "╗\n", style=color)
    t.append(f"║ {title.ljust(width)} ║\n", style=color)
    t.append(f"║ {sub.ljust(width)} ║\n", style=color)
    t.append("╚" + "═" * (width + 2) + "╝\n", style=color)

    return t



def generate_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"



def run():

    fps = 30
    frame_delay = 1 / fps
    glow_x = -20
    tick = 0

    with Live(console=console, refresh_per_second=fps, screen=True) as live:
        for _ in range(60):
            frame = render(glow_x)
            live.update(Align.left(frame))

            glow_x += 2.5
            if glow_x > len(ASCII_LINES.splitlines()) + 40:
                glow_x = -20

            tick += 1
            time.sleep(frame_delay)

    console.clear()
    console.print(render(glow_x))

    user_input = input("osint@kernel: ~/home/osint-tools/ip-generator$ ").strip()

    if user_input == "0":
        return

    if not user_input.isdigit():
        print("invalid input")
        time.sleep(0.8)
        return

    count = int(user_input)

    if count <= 0:
        print("invalid number")
        time.sleep(0.8)
        return

    if count > 100:
        print("max 100 IPs")
        time.sleep(0.8)
        return

    print(f"\nGENERATING {count} IPs...\n")

    ips = []
    for i in range(count):
        ip = generate_ip()
        ips.append(ip)
        print(f"[{i+1}] {ip}")

    input("\nENTER TO BACK...")
