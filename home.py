import importlib
import time
import sys
import threading
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

from utils.animation import decrypt_print


# ─────────────────────────────────────────────
#  ASCII ART DEFINITION
# ─────────────────────────────────────────────

ASCII_LINES = """
 ██╗  ██╗███████╗██████╗ ███╗   ██╗███████╗██╗     
 ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔════╝██║     
 █████╔╝ █████╗  ██████╔╝██╔██╗ ██║█████╗  ██║     
 ██╔═██╗ ██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝  ██║     
 ██║  ██╗███████╗██║  ██║██║ ╚████║███████╗███████╗
 ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝

    ████████╗ ██████╗  ██████╗ ██╗      
    ╚══██╔══╝██╔═══██╗██╔═══██╗██║      
       ██║   ██║   ██║██║   ██║██║      
       ██║   ██║   ██║██║   ██║██║      
       ██║   ╚██████╔╝╚██████╔╝███████╗ 
       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ 
"""

SUBTITLE = "[ Copyright (c) 2026 LXKCV and Astral ]"
ASCII_MENU = """ 


                                     ╔═══════════════════════════════╗                        ╔═══════════════════════════════╗
                                     ║            GITHUB             ║                        ║            DISCORD            ║
                                     ║═══════════════════════════════║                        ║═══════════════════════════════║
                                     ║ ★ Put a star for more updates ║                        ║ ★ Join for updates & support  ║
                                     ║ github.com/LXKCV/KERNEL-TOOL  ║                        ║ discord.gg/LXKCV              ║
                                     ╚═══════════════════════════════╝                        ╚═══════════════════════════════╝

                           ╔════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
                           ║                                        ✦✧✦ DASHBOARD ✦✧✦                                                   ║
                           ║                        Welcome to KERNEL-TOOL, the ultimate Free + OpenSource Tool                         ║
                           ║                                                                                                            ║
                           ║                 [1] Tools Infos      │ [2] System Infos      │ [3] Token Login                             ║
                           ║                                                                                                            ║
                           ║                 [4] IP Lookup        │ [5] IP DDOS (extrem)  │ [6] Osint + Report                          ║
                           ║                                                                                                            ║
                           ║                 [7] Osint Tool       │ [8] Osint CTF         │ [9] Tool 9                                  ║
                           ║                                                                                                            ║
                           ║                 [10] Tool 10         │ [11] SOON..           │ [0] Exit                                    ║
                           ║                                                                                                            ║   
                           ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
"""

# ─────────────────────────────────────────────
#  GLOW COLOR CALCULATION
# ─────────────────────────────────────────────

def glow_color(distance: float) -> str:
    """Return an RGB hex color based on distance from glow center."""
    if distance < 2:
        # Bright white-blue core
        t = distance / 2.0
        r = int(180 + (75 * (1 - t)))
        g = int(220 + (35 * (1 - t)))
        b = 255
    elif distance < 7:
        # Electric cyan → bright blue
        t = (distance - 2) / 5.0
        r = int(180 * (1 - t))
        g = int(220 * (1 - t * 0.8))
        b = 255
    elif distance < 16:
        # Bright blue → deep blue
        t = (distance - 7) / 9.0
        r = 0
        g = int(80 * (1 - t))
        b = int(255 - t * 120)
    else:
        # Dim base: deep navy
        r, g, b = 15, 30, 90

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f"#{r:02x}{g:02x}{b:02x}"


    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def render_text_block(text: str, glow_x: float, axis: str = "row", speed: float = 0.6) -> Text:
    result = Text()
    for row, line in enumerate(text.splitlines()):
        for col, ch in enumerate(line):
            pos = row if axis == "row" else col
            dist = abs(pos - glow_x)
            color = glow_color(dist * speed)
            result.append(ch, style=f"bold {color}")
        result.append("\n")
    return result

PAGES = {i: f"page_{i}" for i in range(1, 11)}

ART_WIDTH = max(len(line) for line in ASCII_LINES.splitlines())
current_page = ""
running = True

def build_frame(glow_x: float, page_content: str = "") -> Text:
    frame = Text()
    frame.append("\n")
    frame.append_text(render_text_block(ASCII_LINES, glow_x, axis="row", speed=0.6))
    frame.append("\n")
    frame.append_text(render_text_block(SUBTITLE, glow_x, axis="col", speed=0.8))
    frame.append("\n")
    frame.append_text(render_text_block(ASCII_MENU, glow_x, axis="row", speed=0.6))
    if page_content:
        frame.append("\n\n")
        frame.append_text(render_text_block(page_content, glow_x, axis="col", speed=0.7))
    frame.append("\n")
    frame.append("  ▸ ", style="bold #00cfff")
    frame.append("Choose an option and press Enter", style="#334d80")
    return frame


def route_to_page(choice: int) -> None:
    global current_page
    page_name = PAGES.get(choice)
    if not page_name:
        current_page = "Page introuvable."
        return

    try:
        module = importlib.import_module(f"pages.{page_name}")
        if hasattr(module, "run"):
            result = module.run()
            current_page = str(result) if result is not None else f"{page_name}.run() executed."
        else:
            current_page = f"Erreur: pages.{page_name} ne contient pas run()."
    except ModuleNotFoundError:
        current_page = f"Page {choice} introuvable (pages/{page_name}.py)."
    except Exception as e:
        current_page = f"Erreur: {e}"


def animation_loop(console: Console):
    global running, current_page

    glow_x = -20.0
    sweep_speed = 1.2
    glow_cycle = max(ART_WIDTH, 120) + 30
    fps = 30
    frame_delay = 1.0 / fps
    with Live(console=console, refresh_per_second=fps, screen=True) as live:
        while running:
            live.update(Align.left(build_frame(glow_x, current_page)))
            glow_x += sweep_speed
            if glow_x > glow_cycle:
                glow_x = -20.0
            time.sleep(frame_delay)


def main():
    global running, current_page
    console = Console()

    thread = threading.Thread(target=animation_loop, args=(console,), daemon=True)
    thread.start()

    valid_choices = {str(i) for i in range(0, 11)}
    while running:
        user_input = input("\n[ KERNEL TOOL ] Enter option (0-10): ").strip()
        if user_input not in valid_choices:
            current_page = "Choix invalide. Utilisez 0 à 10."
            continue
        if user_input == "0":
            running = False
            break
        route_to_page(int(user_input))

    decrypt_print("\nTerminating session...\n")
    decrypt_print("◈  KERNEL TOOL terminated.\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
