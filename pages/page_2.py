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
            gpu_lines = [
                line.strip()
                for line in result.stdout.splitlines()
                if "VGA" in line or "3D" in line or "Display" in line
            ]
            if gpu_lines:
                gpu_info = f"GPU: {gpu_lines[0]}"
        else:
            gpu_info = "GPU: Not detected (lspci unavailable)"
    except Exception as exc:
        gpu_info = f"GPU: Not detected ({exc})"

    if not psutil:
        gpu_info += " | psutil unavailable"

    return [os_info, cpu_info, ram_info, disk_info, gpu_info]


def listen_ctrl_x(callback: Callable[[], None]) -> threading.Thread:
    def _listener() -> None:
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setcbreak(fd)
            while True:
                char = os.read(fd, 1)
                if char == b"\x18":
                    callback()
                    return
        except Exception:
            return
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    listener_thread = threading.Thread(target=_listener, daemon=True)
    listener_thread.start()
    return listener_thread


def run() -> None:
    decrypt_block = _resolve_decrypt_block()

    def _go_home() -> None:
        import home

        print("\nReturning to home...")
        home.run()
        os._exit(0)

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
            _render()
            continue
        if user_input == "info":
            for line in get_system_info():
                print(line)
            continue

        print("Command not found")


if __name__ == "__main__":
    run()
