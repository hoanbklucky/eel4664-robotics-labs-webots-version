#!/usr/bin/env python3
"""Check Webots-first prerequisites without importing Webots itself."""
from importlib.util import find_spec
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]

def report(ok, message):
    print(f"[{'PASS' if ok else 'FAIL'}] {message}")
    return ok

checks = [
    report(sys.version_info >= (3, 10), f"Python {sys.version.split()[0]} (3.10+ recommended)"),
    report(find_spec("numpy") is not None, "NumPy import is available"),
    report(find_spec("matplotlib") is not None, "Matplotlib import is available"),
    report((ROOT / "webots/worlds/eel4664_ur5e.wbt").is_file(), "course Webots world exists"),
    report((ROOT / "webots/controllers/eel4664_ur5e/eel4664_ur5e.py").is_file(), "UR5e controller exists"),
]
webots = shutil.which("webots") or shutil.which("webots.exe")
report(webots is not None, "Webots is on PATH (GUI launch is also acceptable)")
print("[INFO] Open webots/worlds/eel4664_ur5e.wbt and verify one smooth motion.")
raise SystemExit(0 if all(checks) else 1)
