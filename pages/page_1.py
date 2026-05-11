from config import decrypt_block, print_ascii_header


def run():
    print_ascii_header("TOOL INFOS")
    decrypt_block([
        "[KERNEL TOOL :: TOOL INFOS]",
        "...",
        "Access granted.",
        "",
    ])
    print("TOOL INFOS")
    input("Enter to BACK")
