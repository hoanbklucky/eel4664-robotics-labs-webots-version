#!/usr/bin/env python3
"""Singularity metrics used by the supplied Lab 4 Webots demonstration."""

from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lab04_singularities.src.jacobian_starter import analytic_jacobian
from lab04_singularities.src.jacobian_starter import modified_dh_joint_axes
from lab02_webots_ur5e_frames.src.ur5e_fk_starter import (
    T_6_TOOL,
    forward_kinematics,
)


DEMO_CONFIGURATIONS = {
    "bent starting pose / well conditioned": np.array(
        [0.20, -0.80, 1.40, -1.10, -0.70, 0.30]
    ),
    "representative straight-elbow endpoint / near singular": np.array(
        [0.153691, -0.095845, -0.016114, -0.363319, -0.740916, 0.267112]
    ),
    "shoulder-test starting pose / well conditioned": np.array(
        [-1.971137, -2.076381, 0.639429, 1.329040, 1.291846, -0.601321]
    ),
    "representative shoulder midpoint / near singular": np.array(
        [-1.804500, -1.948532, 0.748482, 1.095687, 1.457550, -0.619310]
    ),
    "representative shoulder endpoint / recovered": np.array(
        [-1.992100, -1.801000, 0.716000, 0.976400, 1.271000, -0.599000]
    ),
}


def stylus_fk(q):
    """Return the pose of the visible stylus tip used in the Webots demo."""
    T_tool = forward_kinematics(q) @ T_6_TOOL
    T_tip = T_tool.copy()
    T_tip[:3, 3] += T_tool[:3, :3] @ np.array([0.0, 0.13, 0.0])
    return T_tip


def singularity_metrics(J, rank_tolerance=1e-6):
    """Return singular values and commonly reported conditioning metrics."""
    J = np.asarray(J, dtype=float)
    if J.ndim != 2 or not np.all(np.isfinite(J)):
        raise ValueError("J must be a finite matrix")
    if rank_tolerance <= 0:
        raise ValueError("rank_tolerance must be positive")

    singular_values = np.linalg.svd(J, compute_uv=False)
    sigma_min = float(singular_values[-1])
    sigma_max = float(singular_values[0])
    rank = int(np.sum(singular_values > rank_tolerance))
    condition_number = np.inf if sigma_min <= rank_tolerance else sigma_max / sigma_min
    manipulability = float(np.prod(singular_values))
    return {
        "singular_values": singular_values,
        "sigma_min": sigma_min,
        "rank": rank,
        "condition_number": condition_number,
        "manipulability": manipulability,
    }


def shoulder_radius(q):
    """Return horizontal distance from the wrist center to the base axis."""
    origins, _, _ = modified_dh_joint_axes(q)
    return float(np.linalg.norm(origins[3, :2]))


def scan_configurations(configurations, jacobian_fn, rank_tolerance=1e-6):
    """Evaluate a sequence of joint configurations."""
    rows = []
    for index, q in enumerate(configurations):
        q = np.asarray(q, dtype=float)
        metrics = singularity_metrics(jacobian_fn(q), rank_tolerance)
        rows.append({"index": index, "q": q.copy(), **metrics})
    return rows


def main():
    """Print metrics representative of the start and end of the approach."""
    for label, q in DEMO_CONFIGURATIONS.items():
        metrics = singularity_metrics(
            analytic_jacobian(q, endpoint_fk=stylus_fk)
        )
        print(f"\n{label.upper()}")
        print("q [rad]:", np.array2string(q, precision=3))
        print("singular values:",
              np.array2string(metrics["singular_values"], precision=5))
        print(f"sigma_min: {metrics['sigma_min']:.6f}")
        print(f"rank: {metrics['rank']}")
        print(f"condition number: {metrics['condition_number']:.1f}")
        if "shoulder" in label:
            print(f"wrist-center radius: {100.0 * shoulder_radius(q):.1f} cm")


if __name__ == "__main__":
    main()
