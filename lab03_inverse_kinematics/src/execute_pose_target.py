#!/usr/bin/env python3
"""Provided mission helpers connecting IK to the Lab 2 device adapter."""
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
    result = ik_solver(fk, q_seed, target)
    if not result.converged:
        raise RuntimeError(f"IK failed: {result.reason}")
    q_goal = np.asarray(result.q, dtype=float)
    predicted = np.asarray(fk(q_goal), dtype=float)
    if q_goal.shape != q_seed.shape or not np.all(np.isfinite(q_goal)):
        raise ValueError("IK returned an invalid joint vector")
    if predicted.shape != (4, 4) or not np.all(np.isfinite(predicted)):
        raise ValueError("FK returned an invalid predicted pose")
    if not safety_check(q_seed, q_goal):
        raise ValueError("the proposed joint path failed the safety check")
    return PoseMission(target, q_goal, predicted, result)


def execute_pose_mission(adapter, mission, interpolate, duration, logger):
    """Execute only a prepared mission with smooth commands and logging."""
    if duration <= 0:
        raise ValueError("duration must be positive")
    q0 = np.asarray(adapter.positions(), dtype=float)
    start = adapter.robot.getTime()
    while adapter.robot.step(adapter.time_step) != -1:
        elapsed = adapter.robot.getTime() - start
        q_command = interpolate(q0, mission.q_goal, elapsed, duration)
        adapter.command_positions(q_command)
        logger(elapsed, q_command, adapter.positions(), adapter.measured_tool_pose())
        if elapsed >= duration:
            break
    return np.asarray(adapter.positions()), adapter.measured_tool_pose()