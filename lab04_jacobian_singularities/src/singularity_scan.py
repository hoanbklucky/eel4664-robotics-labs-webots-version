#!/usr/bin/env python3
"""Provided singularity-metric and scan helpers for Lab 4."""

import numpy as np


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
    """Evaluate supplied configurations; plotting and printing stay outside."""
    rows = []
    for index, q in enumerate(configurations):
        q = np.asarray(q, dtype=float)
        metrics = singularity_metrics(jacobian_fn(q), rank_tolerance)
        rows.append({"index": index, "q": q.copy(), **metrics})
    return rows
