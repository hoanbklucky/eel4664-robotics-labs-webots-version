"""Reference solution for analytical and numerical inverse kinematics."""
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


def planar_2r_fk(q, lengths):
    q, lengths = np.asarray(q, float), np.asarray(lengths, float)
    if q.shape != (2,) or lengths.shape != (2,) or np.any(lengths <= 0):
        raise ValueError("expected two joints and two positive link lengths")
    q1, q2 = q
    l1, l2 = lengths
    return np.array([l1*np.cos(q1)+l2*np.cos(q1+q2),
                     l1*np.sin(q1)+l2*np.sin(q1+q2)])


def planar_3r_fk(q, lengths):
    q, lengths = np.asarray(q, float), np.asarray(lengths, float)
    if q.shape != (3,) or lengths.shape != (3,) or np.any(lengths <= 0):
        raise ValueError("expected three joints and three positive link lengths")
    angles = np.cumsum(q)
    position = np.array([np.sum(lengths*np.cos(angles)), np.sum(lengths*np.sin(angles))])
    return np.r_[position, angles[-1]]


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


def _transform(value, name):
    value = np.asarray(value, float)
    if value.shape != (4, 4) or not np.all(np.isfinite(value)):
        raise ValueError(f"{name} must be a finite 4x4 transform")
    return value


def pose_error(current, target):
    current, target = _transform(current, "current"), _transform(target, "target")
    position = target[:3, 3] - current[:3, 3]
    rotation = 0.5 * sum(np.cross(current[:3, i], target[:3, i]) for i in range(3))
    return np.r_[position, rotation]


def finite_difference_jacobian(fk_fn, q, h=1e-5):
    q = np.asarray(q, float)
    if q.ndim != 1 or not np.all(np.isfinite(q)) or h <= 0:
        raise ValueError("q must be a finite vector and h positive")
    jacobian = np.empty((6, q.size))
    for j in range(q.size):
        delta = np.zeros_like(q)
        delta[j] = h
        jacobian[:, j] = pose_error(fk_fn(q-delta), fk_fn(q+delta)) / (2*h)
    return jacobian


def damped_least_squares_step(jacobian, error, damping):
    jacobian, error = np.asarray(jacobian, float), np.asarray(error, float)
    if jacobian.ndim != 2 or error.shape != (jacobian.shape[0],) or damping < 0:
        raise ValueError("incompatible Jacobian/error or negative damping")
    system = jacobian @ jacobian.T + damping**2*np.eye(jacobian.shape[0])
    # TODO 1: Replace None with the DLS equation shown in the README.
    step = None
    if step is None:
        raise NotImplementedError("Complete TODO 1: the damped-least-squares step")
    return step


def numerical_ik(fk_fn, q0, target, *, alpha=0.3, damping=0.02,
                 finite_difference_step=1e-5, max_joint_step=0.10,
                 position_tolerance=1e-3, orientation_tolerance=np.deg2rad(0.5),
                 max_iterations=500, lower_limits=None, upper_limits=None):
    q = np.asarray(q0, float).copy()
    target = _transform(target, "target")
    if q.ndim != 1 or not np.all(np.isfinite(q)) or not (0 < alpha <= 1):
        raise ValueError("invalid seed or alpha")
    if min(finite_difference_step, max_joint_step, position_tolerance,
           orientation_tolerance) <= 0 or max_iterations < 1:
        raise ValueError("steps, tolerances, and iteration count must be positive")
    lower = np.full_like(q, -np.inf) if lower_limits is None else np.asarray(lower_limits, float)
    upper = np.full_like(q, np.inf) if upper_limits is None else np.asarray(upper_limits, float)
    if lower.shape != q.shape or upper.shape != q.shape or np.any(lower > upper):
        raise ValueError("invalid joint limits")
    q = np.clip(q, lower, upper)
    history = []
    for iteration in range(max_iterations+1):
        error = pose_error(fk_fn(q), target)
        p_error, r_error = np.linalg.norm(error[:3]), np.linalg.norm(error[3:])
        history.append((p_error, r_error))
        if p_error <= position_tolerance and r_error <= orientation_tolerance:
            return IKResult(q, True, iteration, p_error, r_error, history, "converged")
        if iteration == max_iterations:
            break
        jacobian = finite_difference_jacobian(fk_fn, q, finite_difference_step)
        delta_q = damped_least_squares_step(jacobian, error, damping)
        # TODO 2: Replace None with q + alpha times the DLS correction.
        q_proposed = None
        if q_proposed is None:
            raise NotImplementedError("Complete TODO 2: the joint update")
        q_next = np.clip(q + np.clip(q_proposed-q, -max_joint_step, max_joint_step), lower, upper)
        if np.allclose(q_next, q, atol=1e-14, rtol=0):
            return IKResult(q, False, iteration, p_error, r_error, history, "blocked by joint limits")
        q = q_next
    return IKResult(q, False, max_iterations, p_error, r_error, history, "iteration limit")
