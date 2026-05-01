import json
import sys
import time

from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.text import Text

from modules.cyber_defense.menu import cyber_defense_menu
from modules.data.alerts import AlertService
from modules.data.analytics import AnalyticsService
from modules.data.logger import OperationLogger
from modules.data.pipeline import PipelineRunner
from modules.data.storage import Storage
from modules.data.summary import AISummaryService
from modules.osint.menu import run_osint_menu
from modules.web_recon.cli import run_web_recon_menu

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
""".strip("\n").splitlines()

SUBTITLE = "[ Copyright (c) 2026 LXKCV and Astral ]"
MENU_ITEMS = [
    ("[1]", "Data Pipeline"),
    ("[2]", "Cyber Defense"),
    ("[3]", "OSINT"),
    ("[4]", "Web Recon"),
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
    offset = max(0, (art_width - len(SUBTITLE)) // 2)
    result = Text(" " * offset)
    for col, ch in enumerate(SUBTITLE):
        color = glow_color(abs((col + offset) - glow_x) * 0.8)
        result.append(ch, style=f"bold italic {color}")
    return result


def render_status(tick: int) -> Text:
    states = ["◈  SYSTEM ONLINE", "◈  SYSTEM ONLINE", "◈  SYSTEM ONLINE ", "◈  INITIALIZING"]
    label = states[tick % len(states)] + ("·" * (tick % 4))
    bar = Text()
    bar.append("  ┌──────────────────────────────────────────┐\n", style="#1a3a8f")
    bar.append("  │  ", style="#1a3a8f")
    bar.append(label.ljust(42), style="bold #00bfff")
    bar.append("│\n", style="#1a3a8f")
    bar.append("  └──────────────────────────────────────────┘", style="#1a3a8f")
    return bar


def render_menu() -> Text:
    menu = Text()
    menu.append("\n  ╔═══════════════════════════════════════════╗\n", style="#0a2a6e")
    menu.append("  ╠═══════════════════════════════════════════╣\n", style="#0a2a6e")
    for key, label in MENU_ITEMS:
        menu.append("  ║  ", style="#0a2a6e")
        menu.append(key, style="bold #00cfff")
        menu.append(f"  {label:<37}", style="#7ab8ff")
        menu.append("║\n", style="#0a2a6e")
    menu.append("  ╚═══════════════════════════════════════════╝", style="#0a2a6e")
    return menu


def build_frame(glow_x: float, tick: int) -> Text:
    art_width = max(len(line) for line in ASCII_LINES)
    frame = Text("\n")
    frame.append_text(render_title(glow_x))
    frame.append("\n")
    frame.append_text(render_subtitle(glow_x, art_width))
    frame.append("\n\n")
    frame.append_text(render_status(tick))
    frame.append_text(render_menu())
    frame.append("\n\n  ▸ ", style="bold #00cfff")
    frame.append("Choisis un chiffre puis Entrée", style="#334d80")
    return frame


def run_data_menu(console: Console) -> None:
    storage = Storage()
    logger = OperationLogger()
    pipeline = PipelineRunner(storage, logger)
    analytics = AnalyticsService(storage)
    alerts = AlertService(storage)
    summary = AISummaryService(storage)

    while True:
        console.print("\n[bold #00cfff]Data Pipeline[/]")
        console.print("[bold #7ab8ff][1][/] Run Pipeline")
        console.print("[bold #7ab8ff][2][/] View Stored Data")
        console.print("[bold #7ab8ff][3][/] Analytics")
        console.print("[bold #7ab8ff][4][/] Logs")
        console.print("[bold #7ab8ff][5][/] Alerts")
        console.print("[bold #7ab8ff][6][/] AI Summary")
        console.print("[bold #7ab8ff][0][/] Back")
        choice = input("Select option: ").strip()

        if choice == "1":
            target = input("Target: ").strip()
            console.print(json.dumps(pipeline.run(target), indent=2))
        elif choice == "2":
            table = input("Table (scans/domains/profiles/alerts): ").strip().lower()
            if table in {"scans", "domains", "profiles", "alerts"}:
                console.print(json.dumps(storage.fetch_all(table), indent=2))
            else:
                console.print("[yellow]Invalid table[/]")
        elif choice == "3":
            console.print(json.dumps(analytics.stats(), indent=2))
        elif choice == "4":
            try:
                with open("logs/operations.log", "r", encoding="utf-8") as f:
                    console.print(f.read() or "No logs yet.")
            except FileNotFoundError:
                console.print("No logs yet.")
        elif choice == "5":
            console.print(json.dumps(alerts.list_alerts(), indent=2))
        elif choice == "6":
            console.print(summary.summarize())
        elif choice == "0":
            return
        else:
            console.print("[yellow]Invalid option[/]")


def main() -> None:
    console = Console()
    fps = 30
    glow_x = -20.0
    tick = 0
    sweep_speed = 2.5
    glow_cycle = max(len(line) for line in ASCII_LINES) + 40

    try:
        with Live(console=console, refresh_per_second=fps, screen=True) as live:
            for _ in range(45):
                live.update(Align.left(build_frame(glow_x, tick)))
                glow_x = -20.0 if glow_x > glow_cycle else glow_x + sweep_speed
                tick += 1
                time.sleep(1.0 / fps)

        while True:
            console.clear()
            console.print(build_frame(glow_x, tick))
            choice = input("\nSelect category: ").strip().lower()
            if choice == "1":
                run_data_menu(console)
            elif choice == "2":
                cyber_defense_menu(console)
            elif choice == "3":
                run_osint_menu(console)
            elif choice == "4":
                run_web_recon_menu()
            elif choice in {"q", "0"}:
                console.print("\n[bold #00cfff]  ◈  KERNEL TOOL terminated.[/]\n")
                sys.exit(0)
            else:
                console.print("[yellow]Invalid selection[/]")
                time.sleep(1)

    except KeyboardInterrupt:
        console.clear()
        console.print("\n[bold #00cfff]  ◈  KERNEL TOOL terminated.[/]\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
