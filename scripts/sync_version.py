#!/usr/bin/env python3
"""Sync addons/music-assistant-skill/config.yaml version with the top-level VERSION file.

Usage: ./scripts/sync_version.py
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / 'VERSION'
CONFIG = ROOT / 'addons' / 'music-assistant-skill' / 'config.yaml'


def read_version():
    if not VERSION_FILE.exists():
        raise SystemExit(f"VERSION file not found at {VERSION_FILE}")
    text = VERSION_FILE.read_text(encoding='utf-8').strip()
    # Accept the file being wrapped in code fences (some repos do)
    if text.startswith('```'):
        # take the inner lines
        lines = [l for l in text.splitlines() if not l.strip().startswith('```')]
        text = '\n'.join(lines).strip()
    return text


def sync():
    ver = read_version()
    if not CONFIG.exists():
        raise SystemExit(f"config.yaml not found at {CONFIG}")

    lines = CONFIG.read_text(encoding='utf-8').splitlines()
    old = None
    updated = False
    for i, line in enumerate(lines):
        if line.strip().startswith('version:'):
            old = line.split(':', 1)[1].strip().strip('"').strip("'")
            lines[i] = f'version: "{ver}"'
            updated = True
            break

    if not updated:
        raise SystemExit("version field not found in config.yaml")

    if old == ver:
        print(f"config.yaml already at version {ver}")
        return 0

    CONFIG.write_text("\n".join(lines) + "\n", encoding='utf-8')
    print(f"Updated config.yaml version: {old} -> {ver}")
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(sync())
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        raise
