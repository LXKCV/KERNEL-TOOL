import importlib
import time
import sys
import os
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align


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

                                                                 [ Copyright (c) 2026 LXKCV and Astral ]                                                                





                                     ╔═══════════════════════════════╗                        ╔═══════════════════════════════╗
                                     ║            GITHUB             ║                        ║            DISCORD            ║
                                     ║═══════════════════════════════║                        ║═══════════════════════════════║
                                     ║ ★ Put a star for more updates ║                        ║ ★ Join for updates & support  ║
                                     ║ github.com/LXKCV/KERNEL-TOOL  ║                        ║ discord.gg/LXKCV              ║
                                     ╚═══════════════════════════════╝                        ╚═══════════════════════════════╝

                           ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
                           ║                                        ✦✧✦ DASHBOARD ✦✧✦                                                   ║
                           ║                                                                                                            ║
                           ║                                                                                                            ║
                           ║                 [1] Tools Infos      │ [2] System Infos      │ [3] Token Login                             ║
                           ║                                                                                                            ║
                           ║                 [4] Osint Tools      │ [5] IP DDOS (extrem)  │ [6] Osint Tools                             ║
                           ║                                                                                                            ║
                           ║                 [7] Osint Tool       │ [8] Osint CTF         │ [9] Tool 9                                  ║
                           ║                                                                                                            ║
                           ║                 [10] Tool 10         │ [11] SOON..           │ [0] Exit                                    ║
                           ║                                                                                                            ║   
                           ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝

"""

SUBTITLE = ""





def get_art_width() -> int:
    lines = ASCII_LINES.splitlines()
    return max((len(line) for line in lines), default=0)

def glow_color(distance: float) -> str:
    distance = max(0.0, min(distance, 20.0))
    intensity = max(0.15, 1.0 - (distance / 18.0))
    neon_blue = 255
    neon_cyan = int(140 + 115 * intensity)
    neon_purple = int(180 * intensity)
  
    r = int(neon_purple * (0.4 + intensity))
    g = int(neon_cyan * (0.7 + intensity))
    b = int(neon_blue)
    r = max(30, min(255, r))
    g = max(60, min(255, g))
    b = max(180, min(255, b))

    return f"#{r:02x}{g:02x}{b:02x}"

def render_title(glow_x: float) -> Text:
    result = Text()
    lines = ASCII_LINES.splitlines()

    for row, line in enumerate(lines):
        dist = abs(row - glow_x)
        color = glow_color(dist * 0.5)

        for ch in line:
            result.append(ch, style=f"bold {color}")
        result.append("\n")

    return result


def render_subtitle(glow_x: float, art_width: int) -> Text:
    result = Text()
    offset = max((art_width - len(SUBTITLE)) // 2, 0)

    result.append(" " * offset)

    for col, ch in enumerate(SUBTITLE):
        dist = abs(col - glow_x)
        color = glow_color(dist * 0.8)
        result.append(ch, style=f"bold italic {color}")

    return result


def build_frame(glow_x: float, tick: int, art_width: int) -> Text:
    frame = Text()

    frame.append("\n")
    frame.append_text(render_title(glow_x))
    frame.append("\n")
    frame.append_text(render_subtitle(glow_x, art_width))
    frame.append("\n\n")
    return frame

def route_to_page(choice: int):
    module = importlib.import_module(f"pages.page_{choice}")
    if hasattr(module, "run"):
        module.run()




def main():
    console = Console()

    fps = 30
    frame_delay = 1.0 / fps
    sweep_speed = 2.5

    tick = 0
    glow_x = -20.0

    while True:
        art_width = get_art_width()
        glow_cycle = art_width + 40

        with Live(console=console, refresh_per_second=fps, screen=True) as live:
            for _ in range(60):
                frame = build_frame(glow_x, tick, art_width)
                live.update(Align.left(frame))

                glow_x += sweep_speed
                if glow_x > glow_cycle:
                    glow_x = -20.0

                tick += 1
                time.sleep(frame_delay)

        console.clear()
        console.print(Align.left(build_frame(glow_x, tick, art_width)))

        pages = [
            f for f in os.listdir("pages")
            if f.startswith("page_") and f.endswith(".py")
        ]

        user_input = input("user@kernel: ~/home$ ").strip()

        if user_input == "0":
            print("\n◈ TERMINATING SESSION\n")
            sys.exit(0)

        if user_input.isdigit():
            page_file = f"page_{user_input}.py"

            if page_file in pages:
                console.clear()
                print(f"\nRouting to {page_file}...\n")

                route_to_page(int(user_input))

                console.clear()
            else:
                print("\nPage inexistante\n")
                time.sleep(0.8)

        else:
            print("\nCommande invalide\n")
            time.sleep(0.8)


if __name__ == "__main__":
    main()
