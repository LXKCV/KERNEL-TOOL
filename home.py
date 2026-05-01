import time
import sys
from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align



ASCII_LINES = [
    r" ██╗  ██╗███████╗██████╗ ███╗   ██╗███████╗██╗     ",
    r" ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔════╝██║     ",
    r" █████╔╝ █████╗  ██████╔╝██╔██╗ ██║█████╗  ██║     ",
    r" ██╔═██╗ ██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝  ██║     ",
    r" ██║  ██╗███████╗██║  ██║██║ ╚████║███████╗███████╗",
    r" ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝",
    r"",
    r"    ████████╗ ██████╗  ██████╗ ██╗      ",
    r"    ╚══██╔══╝██╔═══██╗██╔═══██╗██║      ",
    r"       ██║   ██║   ██║██║   ██║██║      ",
    r"       ██║   ██║   ██║██║   ██║██║      ",
    r"       ██║   ╚██████╔╝╚██████╔╝███████╗ ",
    r"       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝ ",
]
SUBTITLE = "[ Advanced Multitool Interface ]"

MENU_ITEMS = [
    ("[1]", "Cyber Defense"),
    ("[2]", "Process Monitor"),
    ("[3]", "File Inspector"),
    ("[4]", "System Info"),
    ("[5]", "Crypto Vault"),
    ("[Q]", "Quit"),
]


def glow_color(distance: float) -> str:
    if distance < 2:
        t = distance / 2.0
        r = int(180 + (75 * (1 - t)))
        g = int(220 + (35 * (1 - t)))
        b = 255
    elif distance < 7:
        t = (distance - 2) / 5.0
        r = int(180 * (1 - t))
        g = int(220 * (1 - t * 0.8))
        b = 255
    elif distance < 16:
        t = (distance - 7) / 9.0
        r = 0
        g = int(80 * (1 - t))
        b = int(255 - t * 120)
    else:
        r, g, b = 15, 30, 90
    return f"#{max(0, min(255, r)):02x}{max(0, min(255, g)):02x}{max(0, min(255, b)):02x}"


def render_title(glow_x: float) -> Text:
    result = Text()
    for row, line in enumerate(ASCII_LINES):
        color = glow_color(abs(row - glow_x) * 0.5)
        result.append(line + "\n", style=f"bold {color}")
    return result


def render_subtitle(glow_x: float, art_width: int) -> Text:
    offset = (art_width - len(SUBTITLE)) // 2
    result = Text(" " * offset)
    for col, ch in enumerate(SUBTITLE):
        color = glow_color(abs((col + offset) - glow_x) * 0.8)
        result.append(ch, style=f"bold italic {color}")
    return result



def render_menu() -> Text:
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


def build_frame(glow_x: float) -> Text:
    art_width = max(len(line) for line in ASCII_LINES)
    frame = Text("\n")
    frame.append_text(render_title(glow_x))
    frame.append("\n")
    frame.append_text(render_subtitle(glow_x, art_width))
    frame.append_text(render_menu())
    frame.append("\n\n  ▸ ", style="bold #00cfff")
    frame.append("Select an option below", style="#334d80")
    return frame



    fps = 30
    glow_x = -20.0
    end = time.time() + seconds
    with Live(console=console, refresh_per_second=fps, screen=True) as live:
        while time.time() < end:
            live.update(Align.left(build_frame(glow_x)))
            glow_x += 2.5
            if glow_x > 110:
                glow_x = -20.0
            time.sleep(1 / fps)


def main_menu(console: Console) -> None:
    while True:
        console.clear()
        console.print(build_frame(10))
        choice = input("\nChoice: ").strip().lower()

        if choice == "1":
            cyber_defense_menu(console)
        elif choice == "q":
            console.print("\n[bold #00cfff]  ◈  KERNEL TOOL terminated.[/]\n")
            return
        elif choice in {"2", "3", "4", "5"}:
            console.print("[yellow]This module is not implemented yet.[/]")
            input("Press Enter to continue...")
        else:
            console.print("[yellow]Invalid choice.[/]")
            input("Press Enter to continue...")


def main() -> None:
    console = Console()
    try:

    except KeyboardInterrupt:
        pass

    run_main_menu(console)


if __name__ == "__main__":
    main()
