#!/usr/bin/env python3
"""Provided Cartesian-waypoint and straightness helpers for Lab 5."""

import numpy as np


def sample_positions(p_start, p_goal, count):
    """Return equally spaced Cartesian positions including both endpoints."""
    p_start = np.asarray(p_start, dtype=float)
    p_goal = np.asarray(p_goal, dtype=float)
    if p_start.shape != (3,) or p_goal.shape != (3,):
        raise ValueError("positions must have shape (3,)")
    if count < 2:
        raise ValueError("count must be at least 2")
    fractions = np.linspace(0.0, 1.0, count)[:, None]
    return p_start + fractions * (p_goal - p_start)


def solve_waypoints(targets, q_seed, ik_solver, branch_jump_limit=np.pi / 2):
    """Solve sequentially and reuse each accepted result as the next seed."""
    q_previous = np.asarray(q_seed, dtype=float)
    solutions = []
    for index, target in enumerate(targets):
        result = ik_solver(target, q_previous)
        if isinstance(result, tuple):
            q_candidate, converged = result[:2]
        else:
            q_candidate = result
            converged = q_candidate is not None
        if not converged:
            raise RuntimeError(f"IK failed at waypoint {index}")
        q_candidate = np.asarray(q_candidate, dtype=float)
        if q_candidate.shape != q_previous.shape or not np.all(np.isfinite(q_candidate)):
            raise ValueError(f"invalid IK result at waypoint {index}")
        if np.max(np.abs(q_candidate - q_previous)) > branch_jump_limit:
            raise RuntimeError(f"IK branch jump at waypoint {index}")
        solutions.append(q_candidate.copy())
        q_previous = q_candidate
    return np.asarray(solutions)


def line_distance(point, start, goal):
    """Return the distance from a point to a finite line segment."""
    point = np.asarray(point, dtype=float)
    start = np.asarray(start, dtype=float)
    goal = np.asarray(goal, dtype=float)
    direction = goal - start
    length_squared = float(direction @ direction)
    if length_squared <= 0:
        return float(np.linalg.norm(point - start))
    fraction = float((point - start) @ direction / length_squared)
    closest = start + np.clip(fraction, 0.0, 1.0) * direction
    return float(np.linalg.norm(point - closest))
