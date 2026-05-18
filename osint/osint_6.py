import time
from pathlib import Path
from typing import Dict, Any

from rich.console import Console
from rich.text import Text
from rich.live import Live
from rich.align import Align

from config import glow_color, Add, Error, Info, Input, WaitMsg

from PIL import Image
import exifread
from PyPDF2 import PdfReader

console = Console()

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf"}

ASCII_LINES = """
                                           ███▄ ▄███▓▓█████▄▄▄█████▓ ▄▄▄      ▓█████▄  ▄▄▄     ▄▄▄█████▓ ▄▄▄          ██▓     ▒█████   ▒█████   ██ ▄█▀ █    ██  ██▓███  
                                          ▓██▒▀█▀ ██▒▓█   ▀▓  ██▒ ▓▒▒████▄    ▒██▀ ██▌▒████▄   ▓  ██▒ ▓▒▒████▄       ▓██▒    ▒██▒  ██▒▒██▒  ██▒ ██▄█▒  ██  ▓██▒▓██░  ██▒
                                          ▓██    ▓██░▒███  ▒ ▓██░ ▒░▒██  ▀█▄  ░██   █▌▒██  ▀█▄ ▒ ▓██░ ▒░▒██  ▀█▄     ▒██░    ▒██░  ██▒▒██░  ██▒▓███▄░ ▓██  ▒██░▓██░ ██▓▒
                                          ▒██    ▒██ ▒▓█  ▄░ ▓██▓ ░ ░██▄▄▄▄██ ░▓█▄   ▌░██▄▄▄▄██░ ▓██▓ ░ ░██▄▄▄▄██    ▒██░    ▒██   ██░▒██   ██░▓██ █▄ ▓▓█  ░██░▒██▄█▓▒ ▒
                                          ▒██▒   ░██▒░▒████▒ ▒██▒ ░  ▓█   ▓██▒░▒████▓  ▓█   ▓██▒ ▒██▒ ░  ▓█   ▓██▒   ░██████▒░ ████▓▒░░ ████▓▒░▒██▒ █▄▒▒█████▓ ▒██▒ ░  ░
                                          ░ ▒░   ░  ░░░ ▒░ ░ ▒ ░░    ▒▒   ▓▒█░ ▒▒▓  ▒  ▒▒   ▓▒█░ ▒ ░░    ▒▒   ▓▒█░   ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒░▒░▒░ ▒ ▒▒ ▓▒░▒▓▒ ▒ ▒ ▒▓▒░ ░  ░
                                          ░  ░      ░ ░ ░  ░   ░      ▒   ▒▒ ░ ░ ▒  ▒   ▒   ▒▒ ░   ░      ▒   ▒▒ ░   ░ ░ ▒  ░  ░ ▒ ▒░   ░ ▒ ▒░ ░ ░▒ ▒░░░▒░ ░ ░ ░▒ ░     
                                          ░      ░      ░    ░        ░   ▒    ░ ░  ░   ░   ▒    ░        ░   ▒        ░ ░   ░ ░ ░ ▒  ░ ░ ░ ▒  ░ ░░ ░  ░░░ ░ ░ ░░       
                                                 ░      ░  ░              ░  ░   ░          ░  ░              ░  ░       ░  ░    ░ ░      ░ ░  ░  ░      ░              
                                                                      ░                                                                                                        
"""


def render(glow_x: float):
    t = Text()
    for i, line in enumerate(ASCII_LINES.splitlines()):
        t.append(line + "\n", style=f"bold {glow_color(abs(i - glow_x))}")

    title = "ENTER FILE PATH FOR METADATA LOOKUP"
    sub = "(0 = BACK)"
    color = glow_color(glow_x)
    width = max(len(title), len(sub))

    t.append("\n")
    t.append("╔" + "═" * (width + 2) + "╗\n", style=color)
    t.append(f"║ {title.ljust(width)} ║\n", style=color)
    t.append(f"║ {sub.ljust(width)} ║\n", style=color)
    t.append("╚" + "═" * (width + 2) + "╝\n", style=color)
    return t


def format_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size_bytes} B"


def extract_image_metadata(path: Path) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}

    with path.open("rb") as fh:
        tags = exifread.process_file(fh, details=False)

    with Image.open(path) as img:
        width, height = img.size
        metadata["Resolution"] = f"{width} x {height}"

    metadata["Camera"] = str(tags.get("Image Model", "Non disponible"))
    metadata["Date"] = str(tags.get("EXIF DateTimeOriginal", tags.get("Image DateTime", "Non disponible")))
    metadata["Software"] = str(tags.get("Image Software", "Non disponible"))

    gps_lat = tags.get("GPS GPSLatitude")
    gps_lon = tags.get("GPS GPSLongitude")
    metadata["GPS"] = f"Lat: {gps_lat} | Lon: {gps_lon}" if gps_lat and gps_lon else "Non disponible"
    metadata["EXIF"] = ", ".join(tags.keys()) if tags else "Aucune metadata EXIF"
    return metadata


def extract_pdf_metadata(path: Path) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}
    reader = PdfReader(str(path))
    meta = reader.metadata or {}

    metadata["Author"] = str(meta.get("/Author", "Non disponible"))
    metadata["Creator"] = str(meta.get("/Creator", "Non disponible"))
    metadata["Date"] = str(meta.get("/CreationDate", "Non disponible"))
    metadata["Pages"] = str(len(reader.pages))
    metadata["Producer"] = str(meta.get("/Producer", "Non disponible"))
    return metadata


def run_lookup(raw_path: str):
    try:
        path = Path(raw_path.strip().strip('"').strip("'"))
        if not path.exists():
            Error("File not found.")
            return

        ext = path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            Error("Unsupported format. Use PNG/JPG/JPEG/WEBP/PDF.")
            return

        WaitMsg("Extracting metadata...")

        file_type = f"Image {ext.upper().replace('.', '')}"
        if ext == ".pdf":
            file_type = "PDF"
            data = extract_pdf_metadata(path)
        else:
            data = extract_image_metadata(path)

        print("\n━━━━━━━━━━")
        Add(f"Fichier: {path.name}")
        Add(f"Type: {file_type}")
        Add(f"Taille: {format_size(path.stat().st_size)}")
        Add(f"Chemin: {path.resolve()}")
        print()

        for key, value in data.items():
            Add(f"{key}: {value}")

        print("━━━━━━━━━━\n")
    except Exception as exc:
        Error(f"Metadata lookup failed: {exc}")


def run():
    fps = 30
    glow_x = -20

    with Live(console=console, refresh_per_second=fps, screen=True) as live:
        for _ in range(50):
            live.update(Align.left(render(glow_x)))
            glow_x += 2.5
            if glow_x > len(ASCII_LINES.splitlines()) + 40:
                glow_x = -20
            time.sleep(1 / fps)

    while True:
        console.clear()
        console.print(render(glow_x))

        user_input = Input("File path -> ").strip()
        if user_input == "0":
            return

        run_lookup(user_input)
        input("ENTER TO CONTINUE...")


if __name__ == "__main__":
    run()
