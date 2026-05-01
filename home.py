import importlib
import time
import math
import sys
import shutil
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.columns import Columns
from rich.panel import Panel
from rich.rule import Rule
from rich import box
codex/create-multi-page-modular-system-oulpl3

from utils.animation import decrypt_print



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
codex/create-multi-page-modular-system-oulpl3

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f"#{r:02x}{g:02x}{b:02x}"

 main

    r = max(0, min(255, r))
    g = max(0, min(255, g))
    b = max(0, min(255, b))
    return f"#{r:02x}{g:02x}{b:02x}"


# ─────────────────────────────────────────────
#  ANIMATED TITLE RENDERER
# ─────────────────────────────────────────────

codex/create-multi-page-modular-system-oulpl3
# ─────────────────────────────────────────────
#  ANIMATED TITLE RENDERER
# ─────────────────────────────────────────────

=======
 main
def render_title(glow_x: float, art_width: int) -> Text:
    """Render the ASCII art with a vertical glow sweep."""
    result = Text()

    for row, line in enumerate(ASCII_LINES):
        dist = abs(row - glow_x)
        color = glow_color(dist * 0.5)  # *1.5 pour resserrer le faisceau
        for ch in line:
            result.append(ch, style=f"bold {color}")
        result.append("\n")

    return result


def render_subtitle(glow_x: float, art_width: int) -> Text:
    """Render the subtitle with a synced glow."""
    offset = (art_width - len(SUBTITLE)) // 2
    result = Text()
    result.append(" " * offset)
    for col, ch in enumerate(SUBTITLE):
        dist = abs((col + offset) - glow_x)
        color = glow_color(dist * 0.8)
        result.append(ch, style=f"bold italic {color}")
    return result


# ─────────────────────────────────────────────
#  STATUS BAR
# ─────────────────────────────────────────────

def render_status(tick: int) -> Text:
    """Animated status bar shown below the title."""
    states = ["◈  SYSTEM ONLINE", "◈  SYSTEM ONLINE", "◈  SYSTEM ONLINE ", "◈  INITIALIZING"]
    dots = "·" * (tick % 4)
    label = states[tick % len(states)] + dots

    bar = Text()
    bar.append("  ┌──────────────────────────────────────────┐\n", style="#1a3a8f")
    bar.append("  │  ", style="#1a3a8f")
    bar.append(label.ljust(42), style="bold #00bfff")
    bar.append("│\n", style="#1a3a8f")
    bar.append("  └──────────────────────────────────────────┘", style="#1a3a8f")
    return bar


# ─────────────────────────────────────────────
#  MENU PLACEHOLDER (expandable)
# ─────────────────────────────────────────────

MENU_ITEMS = [(f"[{i}]", f"Tool {i}") for i in range(1, 11)] + [("[0]", "Exit")]

def render_menu() -> Text:
    """Render the main menu."""
    menu = Text()
    menu.append("\n  ╔═══════════════════════════════════════════╗\n", style="#0a2a6e")
    menu.append("  ║", style="#0a2a6e")
    menu.append("                                  ", style="bold #1e5fbf")
    menu.append("║\n", style="#0a2a6e")
    menu.append("  ╠═══════════════════════════════════════════╣\n", style="#0a2a6e")

    for key, label in MENU_ITEMS:
        menu.append("  ║  ", style="#0a2a6e")
        menu.append(key, style="bold #00cfff")
        menu.append(f"  {label:<37}", style="#7ab8ff")
        menu.append("║\n", style="#0a2a6e")

    menu.append("  ╚═══════════════════════════════════════════╝", style="#0a2a6e")
    return menu


ART_WIDTH = max(len(line) for line in ASCII_LINES)

def build_frame(glow_x: float, tick: int) -> Text:
    """Assemble the full terminal frame."""
    frame = Text()
    frame.append("\n")
    frame.append_text(render_title(glow_x, ART_WIDTH))
    frame.append("\n")
    frame.append_text(render_subtitle(glow_x, ART_WIDTH))
    frame.append("\n\n")
    frame.append_text(render_status(tick))
    frame.append_text(render_menu())
    frame.append("\n\n")
    frame.append("  ▸ ", style="bold #00cfff")
    frame.append("Choose an option and press Enter", style="#334d80")
    return frame


def route_to_page(choice: int) -> None:
    module = importlib.import_module(f"pages.page_{choice}")
    if hasattr(module, "run"):
        module.run()


def main():
    console = Console()

    sweep_speed = 2.5
    glow_cycle = ART_WIDTH + 40
    fps = 30
    frame_delay = 1.0 / fps

    tick = 0
    glow_x = -20.0

    while True:
        console.clear()
        with Live(console=console, refresh_per_second=fps, screen=True) as live:
            for _ in range(60):
                frame = build_frame(glow_x, tick)
                live.update(Align.left(frame))
                glow_x += sweep_speed
                if glow_x > glow_cycle:
                    glow_x = -20.0
                tick += 1
                time.sleep(frame_delay)

        console.clear()
codex/create-multi-page-modular-system-oulpl3
        console.print(Align.left(build_frame(glow_x, tick)))
        decrypt_print("\n[ MENU ENCRYPTED INTERFACE ]\n")
        for i in range(1, 11):
            decrypt_print(f"[{i}] Tool {i}\n")
        decrypt_print("[0] Exit\n")

        print(build_frame(glow_x, tick))
main
        decrypt_print("\n[ KERNEL TOOL ] Enter option (0-10): ")
        user_input = input().strip()

        if user_input == "0":
            decrypt_print("\nTerminating session...\n")
codex/create-multi-page-modular-system-oulpl3
            decrypt_print("◈  KERNEL TOOL terminated.\n")

            console.print("\n[bold #00cfff]  ◈  KERNEL TOOL terminated.[/]\n")
 main
            sys.exit(0)

        if user_input.isdigit() and 1 <= int(user_input) <= 10:
            console.clear()
            decrypt_print(f"\nRouting to module page_{user_input}...\n\n")
            route_to_page(int(user_input))
            decrypt_print("\n\nReturning to home interface...\n")
            time.sleep(0.6)
        else:
            decrypt_print("\nInvalid selection. Try again.\n")
            time.sleep(0.8)


if __name__ == "__main__":
    main()
