#!/usr/bin/env python3
"""Provided analytical planar 2R IK warm-up."""
import numpy as np


def planar_2r_ik(x, y, l1, l2):
    if not np.all(np.isfinite([x, y, l1, l2])) or l1 <= 0 or l2 <= 0:
        raise ValueError("inputs must be finite and link lengths positive")
    c2 = (x*x + y*y - l1*l1 - l2*l2) / (2*l1*l2)
    if c2 < -1.0-1e-12 or c2 > 1.0+1e-12:
        raise ValueError("target is outside the 2R workspace")
    c2 = np.clip(c2, -1.0, 1.0)
    solutions = []
    for s2 in (np.sqrt(max(0.0, 1-c2*c2)), -np.sqrt(max(0.0, 1-c2*c2))):
        q2 = np.arctan2(s2, c2)
        q1 = np.arctan2(y, x) - np.arctan2(l2*s2, l1+l2*c2)
        candidate = np.array([q1, q2])
        if not any(np.allclose(candidate, old) for old in solutions):
            solutions.append(candidate)
    return solutions