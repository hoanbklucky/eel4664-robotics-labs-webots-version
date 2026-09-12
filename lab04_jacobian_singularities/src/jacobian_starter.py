#!/usr/bin/env python3
"""Guided geometric-Jacobian implementation for the Lab 2 modified-DH model."""
import numpy as np

from lab02_webots_ur5e_frames.src.ur5e_fk_starter import (
    UR5E_MDH,
    dh_transform,
    forward_kinematics,
)


def _validate_transform(T, name):
    T = np.asarray(T, dtype=float)
    if T.shape != (4, 4) or not np.all(np.isfinite(T)):
        raise ValueError(f"{name} must be a finite 4-by-4 transform")
    return T


def pose_difference(T_from, T_to):
    """Return a small base-frame pose change from T_from to T_to."""
    T_from = _validate_transform(T_from, "T_from")
    T_to = _validate_transform(T_to, "T_to")
    position_change = T_to[:3, 3] - T_from[:3, 3]
    rotation_change = 0.5 * sum(
        np.cross(T_from[:3, column], T_to[:3, column])
        for column in range(3)
    )
    return np.concatenate((position_change, rotation_change))


def numerical_jacobian(fk_pose_fn, q, eps=1e-6):
    """Return a centered-difference 6-by-n Jacobian for the chosen endpoint."""
    q = np.asarray(q, dtype=float)
    if q.ndim != 1 or not np.all(np.isfinite(q)) or eps <= 0:
        raise ValueError("q must be a finite vector and eps must be positive")

    J = np.zeros((6, q.size))
    for joint in range(q.size):
        step = np.zeros_like(q)
        step[joint] = eps
        T_minus = fk_pose_fn(q - step)
        T_plus = fk_pose_fn(q + step)
        J[:, joint] = pose_difference(T_minus, T_plus) / (2.0 * eps)
    return J


def modified_dh_joint_axes(q):
    """Return joint origins, joint axes, and T_0_6 for the Lab 2 MDH chain."""
    q = np.asarray(q, dtype=float)
    if q.shape != (6,) or not np.all(np.isfinite(q)):
        raise ValueError("q must contain six finite joint angles")

    T = np.eye(4)
    origins = []
    axes = []

    for qi, (alpha_previous, a_previous, d, offset) in zip(q, UR5E_MDH):
        # Modified DH applies the fixed Rx(alpha_{i-1}) and Tx(a_{i-1})
        # before the variable rotation Rz(theta_i). Joint i therefore rotates
        # about the z-axis of this intermediate joint frame.
        c_alpha = np.cos(alpha_previous)
        s_alpha = np.sin(alpha_previous)
        T_fixed = np.array([
            [1.0, 0.0,      0.0,      a_previous],
            [0.0, c_alpha, -s_alpha,   0.0],
            [0.0, s_alpha,  c_alpha,   0.0],
            [0.0, 0.0,      0.0,       1.0],
        ])
        T_world_joint = T @ T_fixed
        origins.append(T_world_joint[:3, 3].copy())
        axes.append(T_world_joint[:3, 2].copy())

        T = T @ dh_transform(alpha_previous, a_previous, d, qi + offset)

    return np.asarray(origins), np.asarray(axes), T


def analytic_jacobian(q, endpoint_fk=forward_kinematics):
    """Return the base-frame geometric Jacobian for the selected endpoint."""
    origins, axes, _ = modified_dh_joint_axes(q)
    p_endpoint = _validate_transform(endpoint_fk(q), "endpoint pose")[:3, 3]
    J = np.zeros((6, 6))

    for joint, (origin, axis) in enumerate(zip(origins, axes)):
        # Fill only these two repeated geometric-Jacobian relationships.
        linear_column = None   # TODO 1: use axis, origin, and p_endpoint
        angular_column = None  # TODO 2: use the revolute-joint axis

        if linear_column is None or angular_column is None:
            raise NotImplementedError("Complete the two marked Jacobian expressions")

        J[:3, joint] = linear_column
        J[3:, joint] = angular_column

    return J
