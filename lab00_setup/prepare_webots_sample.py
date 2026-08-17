#!/usr/bin/env python3
"""Prepare a local, pinned copy of the official Webots R2025a UR5e sample."""

from pathlib import Path
import os
import re
import shutil
import subprocess
import sys
import tempfile

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
DESTINATION = REPOSITORY_ROOT / "webots" / "vendor" / "webots_r2025a"
PROJECT_ROOT = DESTINATION / "projects"
SAMPLE_WORLD = PROJECT_ROOT / "robots" / "universal_robots" / "worlds" / "ure.wbt"
COURSE_CONTROLLER_SOURCE = REPOSITORY_ROOT / "webots" / "controllers" / "eel4664_ur5e"
COURSE_CONTROLLER_TARGET = (
    PROJECT_ROOT / "robots" / "universal_robots" / "controllers" / "eel4664_ur5e"
)

SPARSE_PATHS = (
    "projects/appearances",
    "projects/bounding_objects",
    "projects/default",
    "projects/devices/robotiq",
    "projects/objects/apartment_structure",
    "projects/objects/backgrounds",
    "projects/objects/cabinet",
    "projects/objects/chairs",
    "projects/objects/computers",
    "projects/objects/drinks",
    "projects/objects/factory",
    "projects/objects/floors",
    "projects/objects/geometries",
    "projects/objects/solids",
    "projects/objects/tables",
    "projects/objects/telephone",
    "projects/robots/universal_robots",
    "projects/vehicles/protos/generic",
)

WEBOTS_URL = re.compile(r"webots://projects/([^\"' \t\r\n]+)")


def run(command):
    """Run one Git command and fail with its original exit code."""
    print("[RUN]", " ".join(str(part) for part in command))
    subprocess.run(command, check=True)


def install_course_controllers():
    """Install the course and diagnostic controllers beside the vendor sample."""
    COURSE_CONTROLLER_TARGET.mkdir(parents=True, exist_ok=True)
    for filename in ("eel4664_ur5e.py", "ur5e_devices.py"):
        shutil.copy2(COURSE_CONTROLLER_SOURCE / filename, COURSE_CONTROLLER_TARGET / filename)

    for name in ("diagnostic_minimal", "diagnostic_devices"):
        source = REPOSITORY_ROOT / "webots" / "controllers" / name / f"{name}.py"
        target = PROJECT_ROOT / "robots" / "universal_robots" / "controllers" / name
        target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target / f"{name}.py")


def convert_project_urls():
    """Make downloaded Webots project URLs resolve inside the pinned local copy."""
    for file_path in PROJECT_ROOT.rglob("*"):
        if not file_path.is_file() or file_path.suffix.lower() not in {".proto", ".wbt"}:
            continue
        text = file_path.read_text(encoding="utf-8")
        if "webots://projects/" not in text:
            continue

        def replace(match):
            asset = PROJECT_ROOT.joinpath(*match.group(1).split("/"))
            if not asset.exists():
                return match.group(0)
            return os.path.relpath(asset, file_path.parent).replace(os.sep, "/")

        file_path.write_text(WEBOTS_URL.sub(replace, text), encoding="utf-8", newline="\n")


def prepare():
    if SAMPLE_WORLD.is_file():
        convert_project_urls()
        install_course_controllers()
        print(f"[READY] Official Universal Robots sample: {SAMPLE_WORLD}")
        return

    if DESTINATION.exists():
        raise RuntimeError(
            f"Destination exists but is incomplete: {DESTINATION}\n"
            "Remove only this incomplete webots/vendor/webots_r2025a folder, then run the command again."
        )
    if shutil.which("git") is None:
        raise RuntimeError("Git is required and was not found on PATH.")

    with tempfile.TemporaryDirectory(prefix="webots-r2025a-") as temporary_name:
        temporary = Path(temporary_name)
        run(
            [
                "git",
                "clone",
                "--depth",
                "1",
                "--branch",
                "R2025a",
                "--filter=blob:none",
                "--sparse",
                "https://github.com/cyberbotics/webots.git",
                str(temporary),
            ]
        )
        run(["git", "-C", str(temporary), "sparse-checkout", "set", *SPARSE_PATHS])
        DESTINATION.mkdir(parents=True)
        shutil.copytree(temporary / "projects", PROJECT_ROOT)

    convert_project_urls()
    install_course_controllers()
    print(f"[READY] Official Universal Robots sample: {SAMPLE_WORLD}")


if __name__ == "__main__":
    try:
        prepare()
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"[FAIL] {error}", file=sys.stderr)
        raise SystemExit(1)
