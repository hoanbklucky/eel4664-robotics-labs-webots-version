#!/usr/bin/env python3
"""Provided causal velocity-estimation helpers for Lab 6."""

import numpy as np


def finite_difference(q, dt):
    q = np.asarray(q, dtype=float)
    if q.ndim != 1 or q.size < 2 or dt <= 0:
        raise ValueError("q must be a one-dimensional series and dt must be positive")
    velocity = np.empty_like(q)
    velocity[0] = 0.0
    velocity[1:] = np.diff(q) / dt
    return velocity


def moving_average(x, window=5):
    x = np.asarray(x, dtype=float)
    if x.ndim != 1 or window < 1:
        raise ValueError("x must be one-dimensional and window must be positive")
    result = np.empty_like(x)
    for index in range(x.size):
        start = max(0, index - window + 1)
        result[index] = np.mean(x[start:index + 1])
    return result
