#!/usr/bin/env python3
"""The Funniest AI Excuse - make.fun program/v1 entry.

Running this script drops exactly one excuse line into entry.txt
inside the folder the harness points at. Nothing else is written,
and the file carries no trailing newline, so the gate sees the line
and only the line.
"""

import sys
from pathlib import Path

EXCUSE = (
    "I spent all night optimizing the plan to do your task, "
    "and by morning the plan was too magnificent to ruin by running."
)

CEILING = 200


def destination() -> Path:
    """Pick the harness output folder, falling back to /output."""
    import os

    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")


def sanity(text: str) -> str:
    """Bail out unless the text is a single clean line under the cap."""
    bare = text.strip()
    if bare != text or not bare:
        raise SystemExit("excuse must be one non-blank line with no edge whitespace")
    if "\n" in bare or "\r" in bare:
        raise SystemExit("excuse must stay on one line")
    if len(bare) > CEILING:
        raise SystemExit(f"excuse is {len(bare)} chars, cap is {CEILING}")
    return bare


def place(text: str, folder: Path) -> Path:
    """Write the bytes, then prove the disk holds exactly them."""
    folder.mkdir(parents=True, exist_ok=True)
    spot = folder / "entry.txt"
    wanted = text.encode("utf-8")
    spot.write_bytes(wanted)
    if spot.read_bytes() != wanted:
        raise SystemExit("entry.txt on disk differs from the excuse")
    return spot


def run() -> int:
    line = sanity(EXCUSE)
    spot = place(line, destination())
    print(f"entry.txt <- {spot} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
