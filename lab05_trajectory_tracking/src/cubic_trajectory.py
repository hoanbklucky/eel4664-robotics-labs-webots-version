#!/usr/bin/env python3
"""Cubic joint-trajectory equations for Lab 5."""

import numpy as np


def cubic_coefficients(q0, qf, v0, vf, duration):
    """Return coefficient arrays a0 through a3 for a multi-joint cubic."""
    q0, qf, v0, vf = np.broadcast_arrays(
        np.asarray(q0, dtype=float),
        np.asarray(qf, dtype=float),
        np.asarray(v0, dtype=float),
        np.asarray(vf, dtype=float),
    )
    if duration <= 0:
        raise ValueError("duration must be positive")

    delta_q = None  # TODO 1: desired final position minus initial position
    a2 = None       # TODO 2: (3*delta_q - (2*v0 + vf)*duration) / duration**2
    a3 = None       # TODO 3: (-2*delta_q + (v0 + vf)*duration) / duration**3
    if delta_q is None or a2 is None or a3 is None:
        raise NotImplementedError("Complete the three marked cubic equations")
    return np.stack((q0, v0, a2, a3))


def sample_cubic(coefficients, times):
    """Evaluate position, velocity, and acceleration at one or more times."""
    a0, a1, a2, a3 = np.asarray(coefficients, dtype=float)
    t = np.asarray(times, dtype=float)
    expanded = t.reshape(t.shape + (1,) * a0.ndim)
    q = a0 + a1 * expanded + a2 * expanded**2 + a3 * expanded**3
    qd = a1 + 2.0 * a2 * expanded + 3.0 * a3 * expanded**2
    qdd = 2.0 * a2 + 6.0 * a3 * expanded
    return q, qd, qdd
