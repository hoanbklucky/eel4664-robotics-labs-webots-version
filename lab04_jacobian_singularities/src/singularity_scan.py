#!/usr/bin/env python3
"""Singularity metrics used by the supplied Lab 4 Webots demonstration."""

from pathlib import Path
import sys

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from lab04_jacobian_singularities.src.jacobian_starter import analytic_jacobian


DEMO_CONFIGURATIONS = {
    "bent elbow / well conditioned": np.array(
        [0.20, -0.80, 1.00, -1.10, -0.70, 0.30]
    ),
    "almost straight elbow / near singular": np.array(
        [0.20, -0.80, 0.03, -1.10, -0.70, 0.30]
    ),
}


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


def scan_configurations(configurations, jacobian_fn, rank_tolerance=1e-6):
    """Evaluate a sequence of joint configurations."""
    rows = []
    for index, q in enumerate(configurations):
        q = np.asarray(q, dtype=float)
        metrics = singularity_metrics(jacobian_fn(q), rank_tolerance)
        rows.append({"index": index, "q": q.copy(), **metrics})
    return rows


def main():
    """Print the metrics for the two poses used by the Webots controller."""
    for label, q in DEMO_CONFIGURATIONS.items():
        metrics = singularity_metrics(analytic_jacobian(q))
        print(f"\n{label.upper()}")
        print("q [rad]:", np.array2string(q, precision=3))
        print("singular values:",
              np.array2string(metrics["singular_values"], precision=5))
        print(f"sigma_min: {metrics['sigma_min']:.6f}")
        print(f"rank: {metrics['rank']}")
        print(f"condition number: {metrics['condition_number']:.1f}")


if __name__ == "__main__":
    main()
