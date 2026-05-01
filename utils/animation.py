import random
import string
import sys
import time


def decrypt_print(text: str, delay: float = 0.012, scramble_cycles: int = 2) -> None:
    """Print text with a cyber decrypting effect."""
    alphabet = string.ascii_uppercase + string.digits + "#@%&*"

    for idx, real_ch in enumerate(text):
        if real_ch in "\n\t ":
            sys.stdout.write(real_ch)
            sys.stdout.flush()
            continue

        for _ in range(scramble_cycles):
            fake = random.choice(alphabet)
            sys.stdout.write(fake)
            sys.stdout.flush()
            time.sleep(delay)
            sys.stdout.write("\b")
            sys.stdout.flush()

        sys.stdout.write(real_ch)
        sys.stdout.flush()
        time.sleep(delay)


def decrypt_block(lines: list[str], line_pause: float = 0.05) -> None:
    for line in lines:
        decrypt_print(line)
        sys.stdout.write("\n")
        sys.stdout.flush()
        time.sleep(line_pause)
