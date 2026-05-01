from rich.console import Console

from .domain_analysis import analyze_domain
from .footprint import email_osint, username_search
from .identity_mapping import map_identity
from .reputation import reputation_score
from .reverse_image import reverse_image_search
from .search import multi_source_search


def run_osint_menu(console: Console) -> None:
    while True:
        console.print("\n[bold #00cfff]OSINT Module[/]")
        console.print("[#7ab8ff][1] Search\n[2] Domain Analysis\n[3] Email/Username Scan\n[4] Identity Mapping\n[5] Reverse Image\n[6] Reputation Score\n[0] Back[/]")
        choice = input("Select: ").strip()

        try:
            if choice == "1":
                q = input("Query: ").strip()
                console.print(multi_source_search(q))
            elif choice == "2":
                d = input("Domain: ").strip()
                console.print(analyze_domain(d))
            elif choice == "3":
                email = input("Email (optional): ").strip()
                username = input("Username (optional): ").strip()
                if email:
                    console.print(email_osint(email))
                if username:
                    console.print(username_search(username))
            elif choice == "4":
                usernames = [x.strip() for x in input("Usernames (comma): ").split(",") if x.strip()]
                emails = [x.strip() for x in input("Emails (comma): ").split(",") if x.strip()]
                domains = [x.strip() for x in input("Domains (comma): ").split(",") if x.strip()]
                console.print(map_identity(usernames, emails, domains))
            elif choice == "5":
                image_url = input("Image URL: ").strip()
                console.print(reverse_image_search(image_url))
            elif choice == "6":
                d = input("Domain: ").strip()
                console.print(reputation_score(d))
            elif choice == "0":
                return
            else:
                console.print("[red]Invalid selection.[/]")
        except Exception as exc:
            console.print(f"[red]Error:[/] {exc}")
