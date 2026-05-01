import json
import sys
import time
from datetime import datetime, timezone

from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt
from rich.table import Table
from rich.text import Text

from modules.data import (
    AISummaryService,
    AlertService,
    AnalyticsService,
    OperationLogger,
    PipelineRunner,
    Storage,
)

ASCII_LINES = [
    r" ██╗  ██╗███████╗██████╗ ███╗   ██╗███████╗██╗     ",
    r" ██║ ██╔╝██╔════╝██╔══██╗████╗  ██║██╔════╝██║     ",
    r" █████╔╝ █████╗  ██████╔╝██╔██╗ ██║█████╗  ██║     ",
    r" ██╔═██╗ ██╔══╝  ██╔══██╗██║╚██╗██║██╔══╝  ██║     ",
    r" ██║  ██╗███████╗██║  ██║██║ ╚████║███████╗███████╗",
    r" ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝",
]
SUBTITLE = "[ Advanced Multitool Interface ]"
MENU_ITEMS = [
    ("[1]", "Run Pipeline"),
    ("[2]", "View Stored Data"),
    ("[3]", "Analytics"),
    ("[4]", "Logs"),
    ("[5]", "Alerts"),
    ("[6]", "AI Summary"),
    ("[0]", "Back / Exit"),
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
    else:
        r, g, b = 15, 30, 90
    return f"#{max(0,min(255,r)):02x}{max(0,min(255,g)):02x}{max(0,min(255,b)):02x}"


def render_header(glow_x: float) -> Text:
    result = Text()
    for row, line in enumerate(ASCII_LINES):
        color = glow_color(abs(row - glow_x) * 0.6)
        result.append(line + "\n", style=f"bold {color}")
    result.append(SUBTITLE, style="bold italic #00cfff")
    return result


def render_menu() -> Text:
    t = Text("\n")
    for k, v in MENU_ITEMS:
        t.append(f"  {k} ", style="bold #00cfff")
        t.append(v + "\n", style="#7ab8ff")
    return t


def bootstrap(console: Console) -> None:
    with Live(console=console, refresh_per_second=24, transient=True) as live:
        for tick in range(30):
            live.update(Align.left(render_header((tick % 16) / 2)))
            time.sleep(0.03)


def print_rows(console: Console, rows: list[dict], title: str) -> None:
    table = Table(title=title, header_style="bold #00cfff")
    if not rows:
        console.print("[yellow]No data available.[/yellow]")
        return
    for col in rows[0].keys():
        table.add_column(col)
    for row in rows:
        table.add_row(*[str(v) for v in row.values()])
    console.print(table)


def main() -> None:
    console = Console()
    storage = Storage()
    logger = OperationLogger()
    pipeline = PipelineRunner(storage, logger)
    analytics = AnalyticsService(storage)
    alerts = AlertService(storage)
    summarizer = AISummaryService(storage)

    bootstrap(console)
    while True:
        console.clear()
        console.print(render_header(2))
        console.print(render_menu())
        choice = Prompt.ask("[bold #00cfff]Select an option[/]", default="0")

        if choice == "1":
            target = Prompt.ask("Enter target (domain/profile/text)")
            result = pipeline.run(target)
            console.print("[green]Pipeline complete.[/green]")
            console.print_json(json.dumps(result))
        elif choice == "2":
            table = Prompt.ask("Table", choices=["scans", "domains", "profiles"], default="scans")
            print_rows(console, storage.fetch_all(table), f"Stored {table}")
        elif choice == "3":
            console.print_json(json.dumps(analytics.stats()))
        elif choice == "4":
            try:
                with open("logs/operations.log", "r", encoding="utf-8") as f:
                    lines = f.readlines()[-30:]
                console.print("".join(lines) or "No logs yet.")
            except FileNotFoundError:
                console.print("No logs yet.")
        elif choice == "5":
            print_rows(console, alerts.list_alerts(), "Alerts")
        elif choice == "6":
            console.print(f"[bold #7ab8ff]{summarizer.summarize()}[/]")
        elif choice == "0":
            console.print("[bold #00cfff]Exiting KERNEL TOOL.[/]")
            break
        else:
            console.print("[red]Invalid selection.[/red]")

        logger.log(f"Menu action executed: {choice}")
        Prompt.ask("Press Enter to continue", default="")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Console().print("\n[bold #00cfff]  ◈  KERNEL TOOL terminated.[/]\n")
        sys.exit(0)
