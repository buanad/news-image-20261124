#!/usr/bin/env python3
"""news-image-20261124 entry program.

Copies the pre-rendered poster ``entry.png`` (1024x1024, the world news of
Tuesday 24 November 2026 in one picture, draw7 template) byte-for-byte into
the harness output directory.

Standard library only; no network, no randomness, no third-party packages.
The poster itself is deterministic: it was rendered once by draw7.py and is
shipped in this repository as ``entry.png``.
"""

import hashlib
import os
import shutil
import sys

SOURCE_NAME = "entry.png"
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576  # entry image cap: 1 MiB


def output_dir():
    """Harness output directory: $MAKEFUN_OUTPUT_DIR, else /output."""
    chosen = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(chosen, exist_ok=True)
    return chosen


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_NAME)
    if not os.path.isfile(source):
        print(f"error: {SOURCE_NAME} not found next to main.py", file=sys.stderr)
        return 1

    dest = os.path.join(output_dir(), SOURCE_NAME)

    with open(source, "rb") as fh:
        magic = fh.read(len(PNG_MAGIC))
    if magic != PNG_MAGIC:
        print("error: entry.png is not a PNG (bad signature)", file=sys.stderr)
        return 1
    if os.path.getsize(source) > MAX_BYTES:
        print("error: entry.png exceeds the 1 MiB cap", file=sys.stderr)
        return 1

    shutil.copyfile(source, dest)

    copied = os.path.getsize(dest)
    expected = os.path.getsize(source)
    if copied != expected:
        print(
            f"error: copied {copied} bytes, expected {expected}",
            file=sys.stderr,
        )
        return 1

    def sha256(path):
        digest = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                digest.update(chunk)
        return digest.hexdigest()

    if sha256(source) != sha256(dest):
        print("error: SHA-256 mismatch after copy", file=sys.stderr)
        return 1

    print(f"wrote {dest} ({copied} bytes, sha256 {sha256(dest)[:12]}...)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
