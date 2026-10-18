#!/usr/bin/env python3
"""Quick check for the two-line Lab 4 Cartesian path controller."""

from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lab04_singularities.src.cartesian_path_controller import (  # noqa: E402
    cartesian_path_controller,
)


def main():
    J = np.eye(6)
    pose_error = np.array([0.01, -0.02, 0.03, 0.0, 0.01, -0.01])
    feedforward_twist = np.array([0.02, 0.0, 0.0, 0.0, 0.0, 0.0])
    gain = 2.0
    expected = feedforward_twist + gain * pose_error

    try:
        joint_rate = cartesian_path_controller(
            J, pose_error, feedforward_twist, gain
        )
    except NotImplementedError as error:
        print(f"NOT READY: {error}")
        return 1

    if not np.allclose(joint_rate, expected):
        print("CHECK FAILED: review both controller hints in the README.")
        print("Expected:", expected)
        print("Received:", joint_rate)
        return 1

    print("PASS: the Cartesian path controller is ready for Webots.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
