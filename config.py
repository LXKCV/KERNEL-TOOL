import random
import string
import sys
import time


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


def decrypt_print(text: str, delay: float = 0.008, scramble_cycles: int = 2) -> None:
    alphabet = string.ascii_uppercase + string.digits + "#@%&*"

    for ch in text:
        if ch in "\n\t ":
            sys.stdout.write(ch)
            sys.stdout.flush()
            continue

        for _ in range(scramble_cycles):
            sys.stdout.write(random.choice(alphabet))
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\b")

        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)


def decrypt_block(lines: list[str], line_pause: float = 0.03) -> None:
    for line in lines:
        decrypt_print(line)
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(line_pause)
