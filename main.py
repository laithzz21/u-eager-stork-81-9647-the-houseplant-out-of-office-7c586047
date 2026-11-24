#!/usr/bin/env python3
"""Entry for make.fun bounty: the houseplant out-of-office.

Prints the single-line out-of-office auto-reply, written as if a
houseplant wrote it, to stdout and also writes it to the output
directory (``/output/entry.txt`` by default, or ``$MAKEFUN_OUTPUT`` when
set), verifying the written file by reading it back.

The entry is 111 characters, within the competition's 120-character limit.

Python 3.13, stdlib only, deterministic: no network, clock, or randomness.
"""

import os
import sys

MAX_CHARS = 120

ENTRY = (
    "Out of office. I'm a fern, ignored since March. Water me before you "
    "email me again — I'm crispy, not corporate."
)


def validate(text: str) -> None:
    """The entry must be a single line of 1-120 characters.

    It must also read as an out-of-office reply (it opens with the
    phrase) and carry no leading or trailing whitespace, so the counted
    length is exactly the visible text.
    """
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError(f"entry must be 1-{MAX_CHARS} characters, got {len(text)}")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "Out of office" not in text:
        raise ValueError("entry must read as an out-of-office auto-reply")
    # The reply must be written in the houseplant's own voice: it names
    # the plant (the fern, ignored since March) rather than the human.
    if "fern" not in text.lower():
        raise ValueError("entry must be written as the houseplant")


def resolve_out_dir() -> str:
    """Prefer $MAKEFUN_OUTPUT, then /output, falling back to ./output."""
    requested = os.environ.get("MAKEFUN_OUTPUT") or "/output"
    try:
        os.makedirs(requested, exist_ok=True)
        probe = os.path.join(requested, ".write_probe")
        with open(probe, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(probe)
        return requested
    except OSError:
        fallback = os.path.join(os.getcwd(), "output")
        os.makedirs(fallback, exist_ok=True)
        return fallback


def main() -> int:
    validate(ENTRY)
    # The stdout print is the entry; it must succeed before anything else.
    print(ENTRY, flush=True)
    try:
        out_dir = resolve_out_dir()
        path = os.path.join(out_dir, "entry.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(ENTRY)
        # Verify the written file by reading it back.
        with open(path, "r", encoding="utf-8") as f:
            written = f.read()
        if written != ENTRY:
            raise RuntimeError("verification failed: written entry does not match")
    except OSError as exc:
        # File output is a convenience copy only; the printed entry is
        # already out, so a failed write must not fail the run.
        print(f"warning: could not write entry.txt: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
