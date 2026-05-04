import importlib
import os
import platform
import shutil
import subprocess
import sys
import termios
import threading
import tty
from typing import Callable


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


def _resolve_decrypt_block() -> Callable[[list[str]], None]:
    for module_name in ("utils.animation", "utilsanimation"):
        try:
            module = importlib.import_module(module_name)
            decrypt_block = getattr(module, "decrypt_block", None)
            if callable(decrypt_block):
                return decrypt_block
        except Exception:
            continue

    def _fallback(lines: list[str]) -> None:
        for line in lines:
            print(line)

    return _fallback


def _load_psutil():
    try:
        return importlib.import_module("psutil")
    except Exception:
        return None


def get_system_info() -> list[str]:
    psutil = _load_psutil()
    os_info = f"OS: {platform.system()} {platform.release()} ({platform.version()})"
    cpu_name = platform.processor() or "Unknown CPU"
    if psutil:
        cpu_cores = psutil.cpu_count(logical=False) or psutil.cpu_count(logical=True) or 1
        cpu_usage = psutil.cpu_percent(interval=0.2)
    else:
        cpu_cores = os.cpu_count() or 1
        cpu_usage = 0.0
    cpu_info = f"CPU: {cpu_name} | Cores: {cpu_cores} | Usage: {cpu_usage:.1f}%"
    if psutil:
        memory = psutil.virtual_memory()
        ram_total_gb = memory.total / (1024**3)
        ram_percent = memory.percent
        disk = psutil.disk_usage("/")
        disk_total_gb = disk.total / (1024**3)
        disk_percent = disk.percent
    else:
        ram_total_gb = 0.0
        ram_percent = 0.0
        disk_total, disk_used, _ = shutil.disk_usage("/")
        disk_total_gb = disk_total / (1024**3)
        disk_percent = (disk_used / disk_total * 100) if disk_total else 0.0
    ram_info = f"RAM: {ram_total_gb:.2f} GB | Used: {ram_percent:.1f}%"
    disk_info = f"Disk: {disk_total_gb:.2f} GB | Used: {disk_percent:.1f}%"
    gpu_info = "GPU: Not detected"
    try:
        if shutil.which("lspci"):
            result = subprocess.run(["lspci"], capture_output=True, text=True, check=False)
            gpu_lines = [line.strip() for line in result.stdout.splitlines() if "VGA" in line or "3D" in line or "Display" in line]
            if gpu_lines:
                gpu_info = f"GPU: {gpu_lines[0]}"
        else:
            gpu_info = "GPU: Not detected (lspci unavailable)"
    except Exception as exc:
        gpu_info = f"GPU: Not detected ({exc})"
    return [os_info, cpu_info, ram_info, disk_info, gpu_info]


def listen_ctrl_x(callback: Callable[[], None]) -> threading.Thread:
    def _listener() -> None:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                if os.read(fd, 1) == b"\x18":
                    callback()
                    return
        except Exception:
            return
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    thread = threading.Thread(target=_listener, daemon=True)
    thread.start()
    return thread


def run() -> None:
    decrypt_block = _resolve_decrypt_block()
    def _go_home() -> None:
        import home

        print("\n\033[1;96mReturning to home...\033[0m")
        home.main()
        os._exit(0)

    def _hex_to_ansi(hex_color: str) -> str:
        r = int(hex_color[1:3], 16)
        g = int(hex_color[3:5], 16)
        b = int(hex_color[5:7], 16)
        return f"\033[1;38;2;{r};{g};{b}m"

    def _print_colored_info(infos: list[str]) -> None:
        for idx, line in enumerate(infos):
            color = _hex_to_ansi(glow_color(idx))
            print(f"{color}{line}\033[0m")

    def _render() -> None:
        infos = get_system_info()
        decrypt_block([
            "[KERNEL TOOL :: PAGE 2]",
            "Decrypting module interface...",
            "Access granted.",
            "",
            "=== SYSTEM INFO ===",
            *infos,
            "",
            "Press CTRL + X to return home",
        ])
        _print_colored_info(infos)

    _render()
    listen_ctrl_x(_go_home)

    while True:
        try:
            user_input = input("user@kernel: ~/home$ ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting page 2...")
            break
        if user_input == "exit":
            print("Exiting page 2...")
            break
        if user_input == "clear":
            print("\033c", end="")
            _render()
            continue
        if user_input == "info":
            _print_colored_info(get_system_info())
            continue
        print("Command not found")


if __name__ == "__main__":
    run()
