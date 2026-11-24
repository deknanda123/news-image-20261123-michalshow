#!/usr/bin/env python3
"""Entry program for news-image-20261123.

Copies the shipped entry.png to the output directory as entry.png.
Pure Python standard library, no network, deterministic: every run
writes the exact same bytes.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "306565f4668530bbe0379355e2fa52eaaaffea78c067b4f3fda05deb76c288ac"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    if not os.path.isfile(SOURCE):
        print("entry.png missing next to main.py", file=sys.stderr)
        return 1
    if sha256_of(SOURCE) != EXPECTED_SHA256:
        print("shipped entry.png sha256 mismatch", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    if sha256_of(dest) != EXPECTED_SHA256:
        print("copied entry.png sha256 mismatch", file=sys.stderr)
        return 1
    print("wrote", dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
