#!/usr/bin/env python3
"""Student starter for nominal UR5e standard-DH forward kinematics."""
import numpy as np

# Each row is (a_i [m], alpha_i [rad], d_i [m], theta_offset_i [rad]).
# Nominal UR5e values published by Universal Robots.
UR5E_DH = (
    (0.0,       np.pi / 2.0, 0.1625, 0.0),
    (-0.4250,   0.0,         0.0,    0.0),
    (-0.3922,   0.0,         0.0,    0.0),
    (0.0,       np.pi / 2.0, 0.1333, 0.0),
    (0.0,      -np.pi / 2.0, 0.0997, 0.0),
    (0.0,       0.0,         0.0996, 0.0),
)


def dh_transform(a, alpha, d, theta):
    """Return Rotz(theta) Transz(d) Transx(a) Rotx(alpha)."""
    raise NotImplementedError


def forward_kinematics(q):
    """Return T_0_6 for six joint angles in radians."""
    q = np.asarray(q, dtype=float)
    if q.shape != (6,) or not np.all(np.isfinite(q)):
        raise ValueError("q must contain six finite joint angles")
    T = np.eye(4)
    for qi, (a, alpha, d, offset) in zip(q, UR5E_DH):
        T = T @ dh_transform(a, alpha, d, qi + offset)
    return T
