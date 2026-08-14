#!/usr/bin/env python3
"""Basic rotation and homogeneous-transformation functions."""

import numpy as np


def rotx(theta):
    """Return the active right-handed rotation matrix about the x-axis."""
    c = np.cos(theta)
    s = np.sin(theta)

    # The x coordinate is unchanged. The lower-right 2-by-2 block rotates
    # the y-z plane according to the right-hand rule.
    return np.array([
        [1.0, 0.0, 0.0],
        [0.0, c, -s],
        [0.0, s, c],
    ])


def roty(theta):
    """Return the active right-handed rotation matrix about the y-axis."""
    c = np.cos(theta)
    s = np.sin(theta)

    # The y coordinate is unchanged while the x-z plane rotates.
    return np.array([
        [c, 0.0, s],
        [0.0, 1.0, 0.0],
        [-s, 0.0, c],
    ])


def rotz(theta):
    """Return the active right-handed rotation matrix about the z-axis."""
    c = np.cos(theta)
    s = np.sin(theta)

    # The upper-left block is the familiar 2-D rotation. A positive
    # 90-degree rotation maps the +x direction to +y.
    return np.array([
        [c, -s, 0.0],
        [s, c, 0.0],
        [0.0, 0.0, 1.0],
    ])


def homogeneous(R, p):
    """Build a 4-by-4 homogeneous transform from rotation and translation."""
    R = np.asarray(R, dtype=float)
    p = np.asarray(p, dtype=float)

    if R.shape != (3, 3):
        raise ValueError("R must have shape (3, 3)")
    if p.shape != (3,):
        raise ValueError("p must have shape (3,)")
    if not np.all(np.isfinite(R)) or not np.all(np.isfinite(p)):
        raise ValueError("inputs must contain only finite values")

    # Begin with identity so the bottom row is automatically [0, 0, 0, 1].
    T = np.eye(4)
    T[:3, :3] = R       # orientation of frame b expressed in frame a
    T[:3, 3] = p        # origin of frame b expressed in frame a
    return T


def invert_transform(T):
    """Invert a rigid homogeneous transform without a general matrix inverse."""
    T = np.asarray(T, dtype=float)
    if T.shape != (4, 4):
        raise ValueError("T must have shape (4, 4)")
    if not np.all(np.isfinite(T)):
        raise ValueError("T must contain only finite values")

    R = T[:3, :3]
    p = T[:3, 3]

    # Rotation matrices are orthonormal, so their inverse is their transpose.
    R_inverse = R.T

    # Reversing the translation requires expressing -p in the inverse frame.
    # It is generally not enough to use -p by itself.
    p_inverse = -R_inverse @ p
    return homogeneous(R_inverse, p_inverse)
