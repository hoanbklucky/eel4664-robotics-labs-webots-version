#!/usr/bin/env python3
"""Mission scaffold connecting student FK/IK to the Webots adapter."""

import numpy as np


def solve_pose_mission(target, q_seed, ik_solver, fk):
    """Solve and evaluate a target without depending on Webots APIs."""
    target = np.asarray(target, dtype=float)
    q_seed = np.asarray(q_seed, dtype=float)
    if target.shape != (4, 4):
        raise ValueError("target must be a 4x4 homogeneous transform")
    # TODO: call student IK, enforce limits, and evaluate using student FK.
    raise NotImplementedError


def command_solution(adapter, q_goal):
    """Send a checked solution through the Lab 1 adapter."""
    # TODO: use smooth motion, then read and log the achieved state.
    raise NotImplementedError
