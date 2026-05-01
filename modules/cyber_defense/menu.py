from rich.console import Console

from .file_analyzer import analyze_file
from .network_monitor import discover_local_devices
from .password_analyzer import analyze_password_strength
from .phishing_detector import analyze_url
from .port_scanner import safe_port_scan


def cyber_defense_menu(console: Console) -> None:
    while True:
        console.print("\n[bold #00cfff]Cyber Defense Module[/]")
        console.print("[bold #7ab8ff][1][/][0m Port Scanner")
        console.print("[bold #7ab8ff][2][/][0m Password Analyzer")
        console.print("[bold #7ab8ff][3][/][0m Network Monitor")
        console.print("[bold #7ab8ff][4][/][0m Phishing Detector")
        console.print("[bold #7ab8ff][5][/][0m File Analyzer")
        console.print("[bold #7ab8ff][0][/][0m Back")

        choice = input("Select option: ").strip()

        if choice == "1":
            host = input("Target host (default 127.0.0.1): ").strip() or "127.0.0.1"
            raw = input("Ports (e.g. 22,80,443): ").strip()
            ports = [int(p) for p in raw.split(",") if p.strip().isdigit()] or [22, 80, 443]
            try:
                results = safe_port_scan(host, ports)
                for port, status in results.items():
                    console.print(f" - {host}:{port} -> {status}")
            except Exception as exc:
                console.print(f"[red]Error:[/] {exc}")

        elif choice == "2":
            pwd = input("Enter password to analyze: ")
            result = analyze_password_strength(pwd)
            console.print(result)

        elif choice == "3":
            cidr = input("CIDR to scan (blank=auto local /24): ").strip() or None
            result = discover_local_devices(cidr)
            for device in result:
                console.print(device)

        elif choice == "4":
            url = input("URL to inspect: ").strip()
            result = analyze_url(url)
            console.print(result)

        elif choice == "5":
            path = input("Path to file: ").strip()
            result = analyze_file(path)
            console.print(result)

        elif choice == "0":
            return
        else:
            console.print("[yellow]Invalid option[/]")
