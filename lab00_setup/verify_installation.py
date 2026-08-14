#!/usr/bin/env python3
"""Verify the pinned Webots R2025a setup and six-lab repository structure."""

from importlib.util import find_spec
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_ROOT = Path(r"C:\webots-eel4664-sample\projects")
SAMPLE_WORLD = SAMPLE_ROOT / "robots/universal_robots/worlds/ure.wbt"
UR5E_PROTO = SAMPLE_ROOT / "robots/universal_robots/protos/UR5e.proto"
SIMULATION_PROJECTS = (
    "lab01_webots_ur5e_frames",
    "lab02_forward_inverse_kinematics",
    "lab03_jacobian_singularities",
    "lab04_trajectory_tracking",
    "lab05_dynamics_control_identification",
    "lab06_integrated_manipulation",
)
REQUIRED_README_SECTIONS = (
    "## Mission",
    "## Success Criteria",
    "## Learning Objectives",
    "## Prerequisites",
    "## Background",
    "## Provided Files",
    "## Part 1 - Setup / Validation",
    "## Part 2 - Core Implementation",
    "## Part 3 - Robot Experiment",
    "## Part 4 - Quantitative Analysis",
    "## Engineering Questions",
    "## What to Submit",
    "## Troubleshooting",
)


def report(ok, message):
    print(f"[{'PASS' if ok else 'FAIL'}] {message}")
    return ok


python_on_path = shutil.which("python") or shutil.which("python.exe")
course_version = sys.version_info[:2] in ((3, 11), (3, 12))
is_64_bit = sys.maxsize > 2**32

print(f"[INFO] Running interpreter: {sys.executable}")
checks = [
    report(sys.platform == "win32", "Windows 10/11 course platform"),
    report(
        python_on_path is not None,
        "python.exe is on PATH; install from python.org and select Add python.exe to PATH if this fails",
    ),
    report(course_version, f"Python {sys.version.split()[0]} (course requires 3.11 or 3.12)"),
    report(is_64_bit, "64-bit Python interpreter"),
    report(find_spec("numpy") is not None, "NumPy import is available"),
    report(find_spec("matplotlib") is not None, "Matplotlib import is available"),
    report((ROOT / "docs/TROUBLESHOOTING_WEBOTS.md").is_file(), "Webots recovery guide exists"),
    report((ROOT / "lab00_setup/prepare_webots_sample.ps1").is_file(), "R2025a sample preparation exists"),
    report((ROOT / "lab00_setup/worlds/setup_smoke_test_starter.wbt").is_file(), "setup smoke-test world exists"),
    report(
        (ROOT / "webots/controllers/diagnostic_minimal/diagnostic_minimal.py").is_file(),
        "canonical minimal diagnostic exists",
    ),
    report(
        (ROOT / "webots/controllers/diagnostic_devices/diagnostic_devices.py").is_file(),
        "canonical device diagnostic exists",
    ),
]

for project_name in SIMULATION_PROJECTS:
    project = ROOT / project_name
    readme_path = project / "README.md"
    starters = list((project / "worlds").glob("*_starter.wbt"))
    diagnostics = all(
        (project / "controllers" / name / f"{name}.py").is_file()
        for name in ("diagnostic_minimal", "diagnostic_devices")
    )
    readme = readme_path.read_text(encoding="utf-8") if readme_path.is_file() else ""
    starter_is_protected = len(starters) == 1 and all(
        "#VRML_SIM R2025a utf8" in world.read_text(encoding="utf-8")
        and "COURSE STARTER: DO NOT OVERWRITE" in world.read_text(encoding="utf-8")
        for world in starters
    )
    workflow_is_documented = all(
        phrase in readme
        for phrase in (
            "File -> Save World As...",
            "diagnostic_minimal",
            "diagnostic_devices",
            "**One joint:**",
            "**Full algorithm:**",
        )
    )
    sections_are_complete = all(section in readme for section in REQUIRED_README_SECTIONS)
    checks.append(report(starter_is_protected, f"{project_name}: one protected R2025a starter world"))
    checks.append(report(diagnostics, f"{project_name}: both diagnostic controllers installed"))
    checks.append(report(workflow_is_documented, f"{project_name}: staged safety workflow documented"))
    checks.append(report(sections_are_complete, f"{project_name}: required student-facing sections present"))

webots = shutil.which("webots") or shutil.which("webots.exe")
known_windows = Path(r"C:\Program Files\Webots\msys64\mingw64\bin\webots.exe")
checks.append(
    report(
        webots is not None or known_windows.is_file(),
        "Webots executable found (confirm Help > About says R2025a)",
    )
)
checks.append(
    report(
        SAMPLE_WORLD.is_file() and UR5E_PROTO.is_file(),
        "local official R2025a sample and UR5e PROTO exist",
    )
)

print("[INFO] Nightly/development Webots builds are unsupported for this course.")
raise SystemExit(0 if all(checks) else 1)