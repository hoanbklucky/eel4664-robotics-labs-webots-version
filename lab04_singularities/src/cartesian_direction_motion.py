#!/usr/bin/env python3
"""Guarded inverse-differential-motion helpers for Lab 4."""

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
    """Compute one supplied guarded damped-least-squares step."""
    q = np.asarray(q, dtype=float)
    desired_twist = np.asarray(desired_twist, dtype=float)
    J = np.asarray(jacobian(q), dtype=float)
    if q.ndim != 1 or desired_twist.shape != (J.shape[0],):
        raise ValueError("q and desired_twist have incompatible shapes")
    if damping <= 0 or max_joint_rate <= 0 or min_sigma_stop < 0:
        raise ValueError("damping and rate limit must be positive")

    singular_values = np.linalg.svd(J, compute_uv=False)
    sigma_min = float(singular_values[-1])
    condition_number = (
        np.inf if sigma_min <= 1e-12
        else float(singular_values[0] / sigma_min)
    )
    if sigma_min < min_sigma_stop:
        return DifferentialStep(
            np.zeros_like(q), sigma_min, condition_number, True,
            "minimum singular value below stop threshold",
        )

    system = J @ J.T + damping**2 * np.eye(J.shape[0])
    qdot = J.T @ np.linalg.solve(system, desired_twist)

    qdot = np.asarray(qdot, dtype=float)
    peak = float(np.max(np.abs(qdot)))
    if peak > max_joint_rate:
        qdot = qdot * (max_joint_rate / peak)
    return DifferentialStep(qdot, sigma_min, condition_number, False)


def run_motion(adapter, step_function, duration_s):
    """Run a guarded step function through a small Webots adapter interface."""
    if duration_s <= 0:
        raise ValueError("duration_s must be positive")
    start = adapter.get_time()
    rows = []
    while adapter.step():
        elapsed = adapter.get_time() - start
        if elapsed >= duration_s:
            break
        q = np.asarray(adapter.read_joint_positions(), dtype=float)
        result = step_function(q)
        rows.append({
            "time": adapter.get_time(),
            "q": q.copy(),
            "qdot_command": result.qdot.copy(),
            "sigma_min": result.sigma_min,
            "condition_number": result.condition_number,
            "stopped": result.stopped,
            "reason": result.reason,
        })
        if result.stopped:
            break
        adapter.command_joint_velocities(result.qdot)
    adapter.stop()
    return rows
