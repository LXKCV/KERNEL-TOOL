import json

from .archive_explorer import archive_explorer
from .headers_analysis import analyze_headers
from .link_extractor import extract_links
from .performance_scan import performance_scan
from .site_mapper import map_site
from .tech_detection import detect_technologies

MENU = """
[1] Tech Detection
[2] Headers Analysis
[3] Link Extractor
[4] Site Mapper
[5] Performance Scan
[6] Archive Explorer
[0] Back
"""


def _ask_url() -> str:
    return input("Target URL or domain: ").strip()


def run_web_recon_menu() -> None:
    while True:
        print("\n=== Web Recon ===")
        print(MENU)
        choice = input("Select option: ").strip()
        if choice == "0":
            return

        try:
            if choice == "1":
                result = detect_technologies(_ask_url())
            elif choice == "2":
                result = analyze_headers(_ask_url())
            elif choice == "3":
                result = extract_links(_ask_url())
            elif choice == "4":
                result = map_site(_ask_url())
            elif choice == "5":
                result = performance_scan(_ask_url())
            elif choice == "6":
                result = archive_explorer(_ask_url())
            else:
                print("Invalid option.")
                continue

            print(json.dumps(result, indent=2))
        except Exception as exc:
            print(f"Error: {exc}")
