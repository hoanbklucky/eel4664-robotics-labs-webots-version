#!/usr/bin/env python3
"""Student scaffold for finite-difference damped-least-squares IK."""
from dataclasses import dataclass

import numpy as np


@dataclass
class IKResult:
    q: np.ndarray
    converged: bool
    iterations: int
    position_error: float
    orientation_error: float
    residual_history: list
    reason: str


def pose_error(T_current, T_target):
    """Return a 6-vector [position_error, orientation_error] in one stated frame."""
    # TODO: validate both transforms and implement the documented error convention.
    raise NotImplementedError


def finite_difference_jacobian(fk_fn, q, h=1e-5):
    """Return a centered-difference 6x6 task Jacobian from the student's FK."""
    # TODO: perturb one joint at a time and keep the pose-error frame consistent.
    raise NotImplementedError


def damped_least_squares_step(J, error, damping):
    """Solve (J J.T + damping^2 I) y = error, then return J.T y."""
    # TODO: validate shapes and use np.linalg.solve; do not form an inverse.
    raise NotImplementedError


def numerical_ik(
    fk_fn,
    q0,
    target,
    *,
    alpha=0.3,
    damping=0.02,
    finite_difference_step=1e-5,
    max_joint_step=0.10,
    position_tolerance=1e-3,
    orientation_tolerance=np.deg2rad(0.5),
    max_iterations=500,
    lower_limits=None,
    upper_limits=None,
):
    """Iterate safely and return IKResult for convergence or explicit failure."""
    q = np.asarray(q0, dtype=float).copy()
    target = np.asarray(target, dtype=float)
    # TODO: validate inputs and limits.
    # TODO: record separate position/orientation residuals every iteration.
    # TODO: stop only when both tolerances pass.
    # TODO: clamp the update and enforce limits.
    # TODO: return an IKResult for every terminal condition.
    raise NotImplementedError
