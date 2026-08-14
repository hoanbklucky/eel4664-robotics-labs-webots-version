#!/usr/bin/env python3
"""Mission scaffold for safe Cartesian-direction motion."""

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class DifferentialStep:
    qdot: np.ndarray
    sigma_min: float
    condition_number: float
    stopped: bool
    reason: str = ""


def safe_differential_step(q, desired_twist, jacobian, damping,
                           max_joint_rate, min_sigma_stop):
    """Compute one guarded DLS step using the student's Jacobian."""
    q = np.asarray(q, dtype=float)
    desired_twist = np.asarray(desired_twist, dtype=float)
    # TODO: compute SVD metrics, stop when unsafe, form DLS explicitly,
    # and saturate the resulting joint-rate command.
    raise NotImplementedError


def run_motion(adapter, step_function, duration_s):
    """Execute guarded steps and return deterministic log rows."""
    # TODO: use simulation time and stop on limits, conditioning, or timeout.
    raise NotImplementedError
