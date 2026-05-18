import psutil
import platform
import socket
import os
import time
from datetime import datetime
from rich.console import Console
from rich.live import Live
from config import glow_color

console = Console()


# ─────────────────────────────────────────────
# GLOW COLOR
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "Unknown"


def uptime():
    seconds = time.time() - psutil.boot_time()
    return f"{int(seconds//3600)}h {int((seconds%3600)//60)}m"


def boot_time():
    return datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")


# ─────────────────────────────────────────────
# RENDER
# ─────────────────────────────────────────────
def render():
    cpu = psutil.cpu_percent()
    freq = psutil.cpu_freq()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    processes = len(psutil.pids())

    temp = "N/A"
    try:
        temps = psutil.sensors_temperatures()
        if temps:
            for name in temps:
                temp = f"{temps[name][0].current}°C"
                break
    except:
        pass

    return f"""

[{glow_color(cpu)}]================ SYSTEM INFO ================[/]

[{glow_color(cpu)}]CPU Usage      : {cpu}%[/]
[{glow_color(cpu)}]CPU Frequency  : {round(freq.current,2)} MHz[/]
[{glow_color(cpu)}]CPU Cores      : {psutil.cpu_count()}[/]

[{glow_color(ram.percent)}]RAM Usage      : {ram.percent}%[/]
[{glow_color(ram.percent)}]RAM Total      : {round(ram.total/1e9,2)} GB[/]
[{glow_color(ram.percent)}]RAM Available  : {round(ram.available/1e9,2)} GB[/]

[{glow_color(disk.percent)}]Disk Usage     : {disk.percent}%[/]
[{glow_color(disk.percent)}]Disk Total     : {round(disk.total/1e9,2)} GB[/]
[{glow_color(disk.percent)}]Disk Free      : {round(disk.free/1e9,2)} GB[/]

[{glow_color(6)}]OS             : {platform.system()} {platform.release()}[/]
[{glow_color(6)}]Hostname       : {platform.node()}[/]
[{glow_color(6)}]IP             : {get_ip()}[/]

[{glow_color(3)}]Processes      : {processes}[/]
[{glow_color(3)}]Temperature    : {temp}[/]

[{glow_color(2)}]Boot Time      : {boot_time()}[/]
[{glow_color(2)}]Uptime         : {uptime()}[/]

"""


# ─────────────────────────────────────────────
# ENTRY POINT (IMPORTANT POUR TON HOME)
# ─────────────────────────────────────────────
def run():
    with Live(render(), refresh_per_second=2, console=console) as live:
        try:
            while True:
                live.update(render())
                time.sleep(0.5)
        except KeyboardInterrupt:
            pass  # retour propre au home
