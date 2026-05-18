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
=======
import os
import sys
import subprocess
from datetime import datetime
from pathlib import Path
import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ImageTk
import exifread
from PyPDF2 import PdfReader

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".pdf"}


class MetaDropApp(TkinterDnD.Tk):
    """MetaDrop - OSINT style metadata extractor for images and PDFs."""

    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("MetaDrop - Metadata Extractor")
        self.geometry("1080x760")
        self.minsize(980, 700)
        self.configure(bg="#0b0f16")
        self._center_window()

        self.current_file_path = None
        self.current_result_text = ""
        self.history = []
        self.preview_image_ref = None

        self._build_ui()

    def _center_window(self):
        self.update_idletasks()
        width, height = 1080, 760
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self):
        root = ctk.CTkFrame(self, fg_color="#0f1522", corner_radius=0)
        root.pack(fill="both", expand=True, padx=10, pady=10)

        title = ctk.CTkLabel(
            root,
            text="MetaDrop",
            font=("Segoe UI", 30, "bold"),
            text_color="#d6e4ff",
        )
        title.pack(pady=(12, 6))

        subtitle = ctk.CTkLabel(
            root,
            text="OSINT Metadata Inspector",
            font=("Segoe UI", 14),
            text_color="#7e95bd",
        )
        subtitle.pack(pady=(0, 12))

        self.drop_zone = ctk.CTkFrame(root, fg_color="#141d2d", corner_radius=14, height=170)
        self.drop_zone.pack(fill="x", padx=18, pady=10)
        self.drop_zone.pack_propagate(False)

        icon_label = ctk.CTkLabel(self.drop_zone, text="🗂️", font=("Segoe UI Emoji", 40))
        icon_label.pack(pady=(24, 4))

        drop_text = ctk.CTkLabel(
            self.drop_zone,
            text="Glisse une image ou un PDF ici",
            font=("Segoe UI", 20, "bold"),
            text_color="#cdd9f5",
        )
        drop_text.pack()

        choose_btn = ctk.CTkButton(self.drop_zone, text="Choisir un fichier", command=self.choose_file)
        choose_btn.pack(pady=(14, 10))
        self._add_hover_animation(choose_btn)

        self.drop_zone.drop_target_register(DND_FILES)
        self.drop_zone.dnd_bind("<<Drop>>", self.on_drop)

        info_frame = ctk.CTkFrame(root, fg_color="transparent")
        info_frame.pack(fill="x", padx=18, pady=(0, 8))

        self.file_badge = ctk.CTkLabel(info_frame, text="📄 Aucun fichier", font=("Segoe UI", 13, "bold"))
        self.file_badge.pack(side="left")

        self.size_label = ctk.CTkLabel(info_frame, text="Taille: -", font=("Segoe UI", 13), text_color="#8ba4cc")
        self.size_label.pack(side="left", padx=16)

        self.preview_label = ctk.CTkLabel(root, text="", width=140)
        self.preview_label.pack(pady=(0, 8))

        self.results_box = ctk.CTkTextbox(root, corner_radius=12, font=("Consolas", 13), wrap="word")
        self.results_box.pack(fill="both", expand=True, padx=18, pady=8)

        history_wrap = ctk.CTkFrame(root, fg_color="transparent")
        history_wrap.pack(fill="x", padx=18, pady=(2, 8))

        ctk.CTkLabel(history_wrap, text="Historique:", font=("Segoe UI", 13, "bold")).pack(side="left")
        self.history_menu = ctk.CTkOptionMenu(history_wrap, values=["Aucun"], command=self.open_from_history)
        self.history_menu.pack(side="left", padx=8)

        buttons = ctk.CTkFrame(root, fg_color="transparent")
        buttons.pack(fill="x", padx=18, pady=(4, 14))

        self.copy_btn = ctk.CTkButton(buttons, text="Copier", command=self.copy_result)
        self.copy_btn.pack(side="left", padx=(0, 8))
        self.export_btn = ctk.CTkButton(buttons, text="Exporter TXT", command=self.export_txt)
        self.export_btn.pack(side="left", padx=(0, 8))
        self.open_folder_btn = ctk.CTkButton(buttons, text="Ouvrir dossier", command=self.open_folder)
        self.open_folder_btn.pack(side="left")

        for btn in (self.copy_btn, self.export_btn, self.open_folder_btn):
            self._add_hover_animation(btn)

        self.results_box.insert("1.0", "Dépose un fichier pour extraire ses métadonnées...")

    def _add_hover_animation(self, button: ctk.CTkButton):
        default_color = button.cget("fg_color")
        hover_color = "#2c4f8f"
        button.bind("<Enter>", lambda _e: button.configure(fg_color=hover_color))
        button.bind("<Leave>", lambda _e: button.configure(fg_color=default_color))

    def on_drop(self, event):
        file_path = event.data.strip("{}")
        self.process_file(file_path)

    def choose_file(self):
        path = filedialog.askopenfilename(
            title="Choisir une image ou un PDF",
            filetypes=[("Supported", "*.png *.jpg *.jpeg *.webp *.pdf")],
        )
        if path:
            self.process_file(path)

    def process_file(self, file_path: str):
        try:
            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError("Fichier introuvable.")
            if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                raise ValueError("Format non supporté. Utilise PNG/JPG/JPEG/WEBP/PDF.")

            self.current_file_path = str(path)
            size_h = self.format_size(path.stat().st_size)
            self.size_label.configure(text=f"Taille: {size_h}")

            if path.suffix.lower() == ".pdf":
                meta = self.extract_pdf_metadata(path)
                detected_type = "PDF"
                icon = "📕"
                self.preview_label.configure(image=None, text="")
            else:
                meta = self.extract_image_metadata(path)
                detected_type = f"Image {path.suffix.upper().replace('.', '')}"
                icon = "🖼️"
                self.show_preview(path)

            output = self.format_output(path, detected_type, meta)
            self.file_badge.configure(text=f"{icon} {path.name}")
            self.set_result_text(output)
            self.push_history(str(path))
        except Exception as exc:
            self.set_result_text(f"Erreur: {exc}")
            messagebox.showerror("MetaDrop", f"Impossible de traiter ce fichier.\n\n{exc}")


    @staticmethod
    def format_size(size_bytes: int):
        units = ["B", "KB", "MB", "GB"]
        size = float(size_bytes)
        for unit in units:
            if size < 1024 or unit == units[-1]:
                return f"{size:.2f} {unit}"
            size /= 1024

    def extract_image_metadata(self, path: Path):
        result = {}
        with path.open("rb") as fh:
            tags = exifread.process_file(fh, details=False)

        with Image.open(path) as img:
            width, height = img.size
            result["Résolution"] = f"{width} x {height}"

        result["Appareil"] = str(tags.get("Image Model", "Non disponible"))
        result["Date"] = str(tags.get("EXIF DateTimeOriginal", tags.get("Image DateTime", "Non disponible")))
        result["Logiciel"] = str(tags.get("Image Software", "Non disponible"))

        gps_lat = tags.get("GPS GPSLatitude")
        gps_lon = tags.get("GPS GPSLongitude")
        if gps_lat and gps_lon:
            result["GPS"] = f"Lat: {gps_lat} | Lon: {gps_lon}"
        else:
            result["GPS"] = "Non disponible"

        result["EXIF brut"] = ", ".join(tags.keys()) if tags else "Aucune métadonnée EXIF détectée"
        return result

    def extract_pdf_metadata(self, path: Path):
        result = {}
        reader = PdfReader(str(path))
        meta = reader.metadata or {}

        result["Auteur"] = str(meta.get("/Author", "Non disponible"))
        result["Créateur"] = str(meta.get("/Creator", "Non disponible"))
        result["Date"] = str(meta.get("/CreationDate", "Non disponible"))
        result["Pages"] = str(len(reader.pages))
        result["Logiciel générateur"] = str(meta.get("/Producer", "Non disponible"))
        return result

    def format_output(self, path: Path, file_type: str, metadata: dict):
        lines = [
            "━━━━━━━━━━",
            "Fichier :",
            path.name,
            "",
            "Type :",
            file_type,
            "",
        ]

        for key, value in metadata.items():
            lines.extend([f"{key} :", str(value), ""])

        lines.append("━━━━━━━━━━")
        return "\n".join(lines)

    def show_preview(self, path: Path):
        try:
            with Image.open(path) as img:
                img.thumbnail((180, 180))
                photo = ImageTk.PhotoImage(img.copy())
            self.preview_image_ref = photo
            self.preview_label.configure(image=photo, text="")
        except Exception:
            self.preview_label.configure(text="Aperçu indisponible", image=None)

    def set_result_text(self, text: str):
        self.current_result_text = text
        self.results_box.delete("1.0", "end")
        self.results_box.insert("1.0", text)

    def push_history(self, file_path: str):
        if file_path in self.history:
            self.history.remove(file_path)
        self.history.insert(0, file_path)
        self.history = self.history[:10]
        self.history_menu.configure(values=self.history if self.history else ["Aucun"])
        if self.history:
            self.history_menu.set(self.history[0])

    def open_from_history(self, selection: str):
        if selection and selection != "Aucun":
            self.process_file(selection)

    def copy_result(self):
        if self.current_result_text:
            self.clipboard_clear()
            self.clipboard_append(self.current_result_text)
            messagebox.showinfo("MetaDrop", "Résultats copiés dans le presse-papiers.")

    def export_txt(self):
        if not self.current_result_text:
            return
        initial_name = f"metadrop_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        save_path = filedialog.asksaveasfilename(
            title="Exporter les métadonnées",
            defaultextension=".txt",
            initialfile=initial_name,
            filetypes=[("Text file", "*.txt")],
        )
        if save_path:
            with open(save_path, "w", encoding="utf-8") as fh:
                fh.write(self.current_result_text)
            messagebox.showinfo("MetaDrop", "Export TXT terminé.")

    def open_folder(self):
        if not self.current_file_path:
            return
        folder = str(Path(self.current_file_path).resolve().parent)
        if sys.platform.startswith("win"):
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])


def run():
    app = MetaDropApp()
    app.mainloop()

if __name__ == "__main__":
    run()
