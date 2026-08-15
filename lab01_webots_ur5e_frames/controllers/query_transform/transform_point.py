#!/usr/bin/env python3
"""Transform points and directions with a homogeneous transformation."""

import numpy as np


def transform_point(T_ab, p_b):
    """Return the coordinates of point ``p_b`` expressed in frame ``a``."""
    # Convert lists or tuples to floating-point NumPy arrays. This lets the
    # function accept inputs such as [1, 2, 3] as well as np.array objects.
    T_ab = np.asarray(T_ab, dtype=float)
    p_b = np.asarray(p_b, dtype=float)

    # Catch common mistakes early instead of allowing a confusing matrix
    # multiplication error later.
    if T_ab.shape != (4, 4):
        raise ValueError("T_ab must have shape (4, 4)")
    if p_b.shape != (3,):
        raise ValueError("p_b must have shape (3,)")
    if not np.all(np.isfinite(T_ab)) or not np.all(np.isfinite(p_b)):
        raise ValueError("inputs must contain only finite values")

    # A point uses homogeneous coordinate 1. Therefore, the translation in
    # the last column of T_ab is included in the result.
    p_b_homogeneous = np.append(p_b, 1.0)
    p_a_homogeneous = T_ab @ p_b_homogeneous

    # The first three entries are the ordinary x, y, and z coordinates.
    return p_a_homogeneous[:3]


def transform_direction(T_ab, v_b):
    """Transform free direction ``v_b`` from frame ``b`` to frame ``a``."""
    T_ab = np.asarray(T_ab, dtype=float)
    v_b = np.asarray(v_b, dtype=float)

    if T_ab.shape != (4, 4):
        raise ValueError("T_ab must have shape (4, 4)")
    if v_b.shape != (3,):
        raise ValueError("v_b must have shape (3,)")
    if not np.all(np.isfinite(T_ab)) or not np.all(np.isfinite(v_b)):
        raise ValueError("inputs must contain only finite values")

    # A free direction uses homogeneous coordinate 0. Multiplying the
    # translation column by zero prevents translation from changing it.
    v_b_homogeneous = np.append(v_b, 0.0)
    v_a_homogeneous = T_ab @ v_b_homogeneous
    return v_a_homogeneous[:3]
