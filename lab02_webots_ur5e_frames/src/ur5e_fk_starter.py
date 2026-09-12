#!/usr/bin/env python3
"""Student starter for nominal UR5e modified-DH forward kinematics."""
import numpy as np

# Each row is (alpha_{i-1} [rad], a_{i-1} [m], d_i [m],
# theta_offset_i [rad]). The column order matches the modified-DH table used
# in class.
UR5E_MDH = (
    (0.0,          0.0,       0.1625, 0.0),
    (np.pi / 2.0,  0.0,       0.0,    0.0),
    (0.0,          0.4250,    0.0,    0.0),
    (0.0,          0.3922,   -0.1333, 0.0),
    (np.pi / 2.0,  0.0,       0.0997, 0.0),
    (-np.pi / 2.0, 0.0,      -0.0996, 0.0),
)


# Webots encoder directions mapped to Craig modified-DH theta directions.
WEBOTS_TO_MDH_SIGN = np.array([1.0, -1.0, -1.0, -1.0, 1.0, -1.0])
# Fixed rotation from the Webots tool frame to Craig frame {6}.
# It is part of the supplied model convention, not a quantity students fit.
T_6_TOOL = np.array([
    [-1.0,  0.0,  0.0, 0.0],
    [ 0.0,  0.0, -1.0, 0.0],
    [ 0.0, -1.0,  0.0, 0.0],
    [ 0.0,  0.0,  0.0, 1.0],
])


def dh_transform(alpha_previous, a_previous, d, theta):
    """Return the modified-DH transform from frame {i-1} to frame {i}."""
    c_theta = np.cos(theta)
    s_theta = np.sin(theta)
    c_alpha = np.cos(alpha_previous)
    s_alpha = np.sin(alpha_previous)

    # Compare the entries below with the matrix in the Lab 2 README.
    # Replace only these two None values with the correct expressions.
    row_2_column_1 = None  # TODO 1
    row_3_column_4 = None  # TODO 2

    if row_2_column_1 is None or row_3_column_4 is None:
        raise NotImplementedError("Complete the two marked modified-DH entries")

    return np.array([
        [c_theta,            -s_theta,            0.0,      a_previous],
        [row_2_column_1,      c_theta * c_alpha, -s_alpha, -s_alpha * d],
        [s_theta * s_alpha,   c_theta * s_alpha,  c_alpha,  row_3_column_4],
        [0.0,                 0.0,                0.0,      1.0],
    ], dtype=float)


def forward_kinematics(q):
    """Return T_0_6 for six joint angles in radians."""
    q = np.asarray(q, dtype=float)
    if q.shape != (6,) or not np.all(np.isfinite(q)):
        raise ValueError("q must contain six finite joint angles")
    # Start at frame {0}. Each right multiplication appends the transform
    # from the current link frame to the next link frame. After all six
    # iterations, T = T_0_1 @ T_1_2 @ ... @ T_5_6 = T_0_6.
    T = np.eye(4)
    for qi, direction, (alpha_previous, a_previous, d, offset) in zip(
            q, WEBOTS_TO_MDH_SIGN, UR5E_MDH):
        theta = direction * qi + offset
        T = T @ dh_transform(alpha_previous, a_previous, d, theta)
    return T
