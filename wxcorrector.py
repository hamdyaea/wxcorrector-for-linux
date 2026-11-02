#!/usr/bin/env python3
# Developer: Hamdy Abou El Anein
# Contact: info@daylightlinux.ch
# SPDX-License-Identifier: GPL-3.0-only
"""Dry-run-first WX satellite TLE updater."""
import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil
import tempfile
from urllib.request import Request, urlopen

DEFAULT_URL = "https://celestrak.org/NORAD/elements/weather.txt"
DEFAULT_DEST = Path("/usr/share/wx/tle/weather.txt")
MAX_BYTES = 2_000_000

def download_tle(url: str, opener=urlopen) -> bytes:
    if not url.startswith("https://"):
        raise ValueError("Only HTTPS is supported")
    with opener(Request(url, headers={"User-Agent": "WXCorrector/2.0"}), timeout=15) as response:
        data = response.read(MAX_BYTES + 1)
    if not data or len(data) > MAX_BYTES or b"\x00" in data:
        raise ValueError("Invalid or oversized TLE data")
    return data

def install_tle(destination: Path, data: bytes) -> Path | None:
    if not destination.parent.is_dir():
        raise FileNotFoundError("Destination directory does not exist")
    if destination.is_symlink():
        raise ValueError("Refusing to overwrite symlink")
    backup = None
    if destination.exists():
        backup = destination.with_name(destination.name + "." + datetime.now().strftime("%Y%m%d%H%M%S%f") + ".bak")
        shutil.copy2(destination, backup)
    fd, temp_name = tempfile.mkstemp(prefix=".wx-tle-", dir=destination.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temp_name, destination)
    finally:
        Path(temp_name).unlink(missing_ok=True)
    return backup

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--destination", type=Path, default=DEFAULT_DEST)
    parser.add_argument("--apply", action="store_true", help="Download and replace the TLE file")
    args = parser.parse_args()
    if not args.apply:
        print(f"DRY RUN: would download {args.url} and update {args.destination}")
        return
    try:
        data = download_tle(args.url)
        backup = install_tle(args.destination, data)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"Updated {args.destination} ({len(data)} bytes)")
    if backup:
        print(f"Backup: {backup}")

if __name__ == "__main__":
    main()
