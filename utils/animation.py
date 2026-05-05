import random
import string
import sys
import time


def decrypt_print(text: str, delay: float = 0.008, scramble_cycles: int = 2) -> None:
    alphabet = string.ascii_uppercase + string.digits + "#@%&*"

    for ch in text:
        if ch in "\n\t ":
            sys.stdout.write(ch)
            sys.stdout.flush()
            continue

        # effet scramble
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