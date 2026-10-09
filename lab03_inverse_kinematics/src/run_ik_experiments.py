#!/usr/bin/env python3
"""Provided offline runner for the two Lab 3 IK targets and one failure case."""
from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from lab02_webots_ur5e_frames.src.ur5e_fk_starter import T_6_TOOL, forward_kinematics
from lab03_inverse_kinematics.src.numerical_ik import numerical_ik


def fk_tool(q):
    return forward_kinematics(q) @ T_6_TOOL


def print_result(label, result):
    print(f"\n{label}")
    print("  converged:", result.converged)
    print("  reason:", result.reason)
    print("  iterations:", result.iterations)
    print("  final q [rad]:", np.array2string(result.q, precision=5))
    print(f"  position error [mm]: {1000.0*result.position_error:.3f}")
    print(f"  orientation error [deg]: {np.rad2deg(result.orientation_error):.3f}")


q_reference_a = np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30])
q_reference_b = np.array([-0.30, -0.90, 1.10, -1.40, -1.20, -0.20])
q_seed = np.array([0.10, -0.60, 0.80, -0.80, -0.90, 0.10])
limits = np.full(6, 2.0*np.pi)

targets = {
    "Target A": fk_tool(q_reference_a),
    "Target B": fk_tool(q_reference_b),
}

for label, target in targets.items():
    result = numerical_ik(
        fk_tool,
        q_seed,
        target,
        lower_limits=-limits,
        upper_limits=limits,
    )
    print_result(label, result)

unreachable = targets["Target A"].copy()
unreachable[:3, 3] += np.array([1.5, 0.0, 0.0])
print_result(
    "Unreachable target",
    numerical_ik(
        fk_tool,
        q_seed,
        unreachable,
        lower_limits=-limits,
        upper_limits=limits,
    ),
)