import importlib
import time
import sys
import os
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

def run():
    print("OSINT TOOLS")
    input("Enter to BACK")


console = Console()

# ─────────────────────────────────────────────
# ASCII ART (IDENTIQUE MAIS TEXTE MODIFIÉ)
# ─────────────────────────────────────────────

ASCII_LINES = """                          !
                                           ██ ▄█▀▓█████  ██▀███   ███▄    █ ▓█████  ██▓        ▒█████    ██████  ██▓ ███▄    █ ▄▄▄█████▓
                                           ██▄█▒ ▓█   ▀ ▓██ ▒ ██▒ ██ ▀█   █ ▓█   ▀ ▓██▒       ▒██▒  ██▒▒██    ▒ ▓██▒ ██ ▀█   █ ▓  ██▒ ▓▒
                                          ▓███▄░ ▒███   ▓██ ░▄█ ▒▓██  ▀█ ██▒▒███   ▒██░       ▒██░  ██▒░ ▓██▄   ▒██▒▓██  ▀█ ██▒▒ ▓██░ ▒░
                                          ▓██ █▄ ▒▓█  ▄ ▒██▀▀█▄  ▓██▒  ▐▌██▒▒▓█  ▄ ▒██░       ▒██   ██░  ▒   ██▒░██░▓██▒  ▐▌██▒░ ▓██▓ ░ 
                                          ▒██▒ █▄░▒████▒░██▓ ▒██▒▒██░   ▓██░░▒████▒░██████▒   ░ ████▓▒░▒██████▒▒░██░▒██░   ▓██░  ▒██▒ ░ 
                                          ▒ ▒▒ ▓▒░░ ▒░ ░░ ▒▓ ░▒▓░░ ▒░   ▒ ▒ ░░ ▒░ ░░ ▒░▓  ░   ░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░░▓  ░ ▒░   ▒ ▒   ▒ ░░   
                                          ░ ░▒ ▒░ ░ ░  ░  ░▒ ░ ▒░░ ░░   ░ ▒░ ░ ░  ░░ ░ ▒  ░     ░ ▒ ▒░ ░ ░▒  ░ ░ ▒ ░░ ░░   ░ ▒░    ░    
                                          ░ ░░ ░    ░     ░░   ░    ░   ░ ░    ░     ░ ░      ░ ░ ░ ▒  ░  ░  ░   ▒ ░   ░   ░ ░   ░      
                                          ░  ░      ░  ░   ░              ░    ░  ░    ░  ░       ░ ░        ░   ░           ░          
                                                                                              

                                                                                                                               





                                     ╔═══════════════════════════════╗                        ╔═══════════════════════════════╗
                                     ║            OSINT              ║                        ║            DISCORD            ║
                                     ║═══════════════════════════════║                        ║═══════════════════════════════║
                                     ║ ★  Many Osint Tool            ║                        ║ ★ Join for updates & support  ║
                                     ║                               ║                        ║ .gg/                          ║
                                     ╚═══════════════════════════════╝                        ╚═══════════════════════════════╝

                           ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
                           ║                                        ✦✧✦ OSINT PANEL ✦✧✦                                                 ║
                           ║                                                                                                            ║
                           ║                                                                                                            ║
                           ║                 [1] IP Generator     │ [2] IP Lookup        │ [3] IP Intelligence Panel                    ║
                           ║                                                                                                            ║
                           ║                 [4] Username Checker │ [5] Tool 5           │ [6] Tool 6                                   ║
                           ║                                                                                                            ║
                           ║                 [7] Tool 7           │ [8] Tool 8           │ [9] Tool 9                                   ║
                           ║                                                                                                            ║
                           ║                 [10] Tool 10         │ [11] SOON..          │ [0] BACK                                     ║
                           ║                                                                                                            ║   
                           ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝


"""

SUBTITLE = ""


def get_art_width():
    return max(len(line) for line in ASCII_LINES.splitlines())


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


def render_title(glow_x):
    t = Text()
    for i, line in enumerate(ASCII_LINES.splitlines()):
        color = glow_color(abs(i - glow_x))
        t.append(line + "\n", style=f"bold {color}")
    return t


def build_frame(glow_x, tick, art_width):
    frame = Text()
    frame.append("\n")
    frame.append_text(render_title(glow_x))
    frame.append("\n\n")
    return frame


# ─────────────────────────────────────────────
# ROUTER OSINT
# ─────────────────────────────────────────────
def route_to_osint(choice):
    try:
        module = importlib.import_module(f"osint.osint_{choice}")
        if hasattr(module, "run"):
            module.run()
    except Exception as e:
        print(f"Erreur: {e}")
        time.sleep(1)


# ─────────────────────────────────────────────
# MAIN LOOP
# ─────────────────────────────────────────────
def run():
    fps = 30
    frame_delay = 1 / fps
    glow_x = -20
    tick = 0

    while True:
        art_width = get_art_width()
        glow_cycle = art_width + 40

        with Live(console=console, refresh_per_second=fps, screen=True) as live:
            for _ in range(60):
                frame = build_frame(glow_x, tick, art_width)
                live.update(Align.left(frame))

                glow_x += 2.5
                if glow_x > glow_cycle:
                    glow_x = -20

                tick += 1
                time.sleep(frame_delay)

        console.clear()
        console.print(Align.left(build_frame(glow_x, tick, art_width)))

        tools = [
            f for f in os.listdir("osint")
            if f.startswith("osint_") and f.endswith(".py")
        ]

        user_input = input("osint@kernel: ~/home/osint-tools$ ").strip()

        if user_input == "0":
            break

        if user_input.isdigit():
            file = f"osint_{user_input}.py"

            if file in tools:
                console.clear()
                print(f"\nRouting to {file}...\n")

                route_to_osint(int(user_input))

                console.clear()
            else:
                print("\nTool inexistant\n")
                time.sleep(0.8)
        else:
            print("\nCommande invalide\n")
            time.sleep(0.8)