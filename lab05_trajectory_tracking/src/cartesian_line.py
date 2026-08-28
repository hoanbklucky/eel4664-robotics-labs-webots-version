#!/usr/bin/env python3
"""Starter for a practical straight-line Cartesian waypoint trajectory."""

import numpy as np


def sample_positions(p_start, p_goal, count):
    """Return equally spaced Cartesian positions including both endpoints."""
    p_start = np.asarray(p_start, dtype=float)
    p_goal = np.asarray(p_goal, dtype=float)
    if p_start.shape != (3,) or p_goal.shape != (3,):
        raise ValueError("positions must have shape (3,)")
    if count < 2:
        raise ValueError("count must be at least 2")
    # TODO: implement without a robotics trajectory library.
    raise NotImplementedError


def solve_waypoints(targets, q_seed, ik_solver):
    """Solve sequentially, reusing each solution as the next seed."""
    # TODO: reject nonconvergence, limit violations, and branch jumps.
    raise NotImplementedError


def line_distance(point, start, goal):
    """Measure distance to the finite line segment."""
    # TODO: implement projection with endpoint clamping.
    raise NotImplementedError
