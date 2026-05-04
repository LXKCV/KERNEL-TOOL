import os
import platform
import shutil
import subprocess
import sys
import termios
import threading
import tty

from utils.animation import decrypt_block


def get_system_info() -> list[str]:
    os_info = f"OS: {platform.system()} {platform.release()}"

    cpu_name = platform.processor() or "Unknown CPU"
    cpu_cores = os.cpu_count() or 1
    cpu_info = f"CPU: {cpu_name} | Cores: {cpu_cores}"

    mem_total = 0.0
    mem_percent = 0.0
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as file:
            lines = file.read().splitlines()
        mem_total_kb = int(lines[0].split()[1])
        mem_avail_kb = int([line for line in lines if line.startswith("MemAvailable:")][0].split()[1])
        mem_total = mem_total_kb / (1024 * 1024)
        used_kb = mem_total_kb - mem_avail_kb
        mem_percent = (used_kb / mem_total_kb) * 100 if mem_total_kb else 0.0
    except Exception:
        pass
    ram_info = f"RAM: {mem_total:.2f} GB | Used: {mem_percent:.1f}%"

    disk_total, disk_used, _ = shutil.disk_usage("/")
    disk_total_gb = disk_total / (1024**3)
    disk_percent = (disk_used / disk_total * 100) if disk_total else 0.0
    disk_info = f"Disk: {disk_total_gb:.2f} GB | Used: {disk_percent:.1f}%"

    gpu_info = "GPU: Not detected"
    try:
        if shutil.which("lspci"):
            result = subprocess.run(["lspci"], capture_output=True, text=True, check=False)
            gpu_lines = [line.strip() for line in result.stdout.splitlines() if "VGA" in line or "3D" in line or "Display" in line]
            if gpu_lines:
                gpu_info = f"GPU: {gpu_lines[0]}"
    except Exception:
        gpu_info = "GPU: Not detected"

    return [os_info, cpu_info, ram_info, disk_info, gpu_info]


def listen_ctrl_x(callback):
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

    thread = threading.Thread(target=_listener, daemon=True)
    thread.start()
    return thread


def run() -> None:
    def _go_home() -> None:
        import home
        home.main()

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
            break

        if user_input == "exit":
            break
        if user_input == "clear":
            print("\033c", end="")
            _render()
            continue
        if user_input == "info":
            for line in get_system_info():
                print(line)
            continue

        print("Command not found")


if __name__ == "__main__":
    run()