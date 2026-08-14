#!/usr/bin/env python3
"""Mission scaffold connecting student IK to the Lab 1 FK/device adapter."""
from dataclasses import dataclass

import numpy as np


@dataclass
class PoseMission:
    target: np.ndarray
    q_goal: np.ndarray
    predicted_pose: np.ndarray
    solver_result: object


def prepare_pose_mission(target, q_seed, ik_solver, fk, safety_check):
    """Solve, verify, and reject unsafe endpoints before any Webots command."""
    target = np.asarray(target, dtype=float)
    q_seed = np.asarray(q_seed, dtype=float)
    if target.shape != (4, 4):
        raise ValueError("target must be a 4x4 homogeneous transform")

    # TODO: call ik_solver and require result.converged.
    # TODO: verify the endpoint with fk(result.q).
    # TODO: apply joint/path safety_check and return PoseMission.
    raise NotImplementedError


def execute_pose_mission(adapter, mission, interpolate, duration, logger):
    """Execute only a prepared mission with smooth commands and measured logging."""
    # TODO: read measured q0, sample interpolation with simulation time,
    # command through adapter, hold q_goal, and log command/measurement/tool pose.
    raise NotImplementedError
