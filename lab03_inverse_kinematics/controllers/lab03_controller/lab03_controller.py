#!/usr/bin/env python3
"""Provided Lab 3 controller: solve one target, validate it, and move safely."""
from pathlib import Path
import sys

import numpy as np
from controller import Robot

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from lab02_webots_ur5e_frames.src.ur5e_fk_starter import T_6_TOOL, forward_kinematics
from lab03_inverse_kinematics.src.numerical_ik import numerical_ik
from ur5e_devices import JOINT_NAMES, UR5eDevices

TARGET_LABEL = "A"  # Run once with "A", reset Webots, and then run with "B".
TARGET_JOINTS = {
    "A": np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30]),
    "B": np.array([-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]),
}


def fk_tool(q):
    return forward_kinematics(q) @ T_6_TOOL


def cubic_blend(s):
    s = float(np.clip(s, 0.0, 1.0))
    return 3.0*s*s - 2.0*s*s*s


def rotation_to_rpy(R):
    pitch = np.arctan2(-R[2, 0], np.hypot(R[0, 0], R[1, 0]))
    roll = np.arctan2(R[2, 1], R[2, 2])
    yaw = np.arctan2(R[1, 0], R[0, 0])
    return np.array([roll, pitch, yaw])


if TARGET_LABEL not in TARGET_JOINTS:
    raise ValueError('TARGET_LABEL must be "A" or "B"')

robot = Robot()
arm = UR5eDevices(robot)
if robot.step(arm.time_step) == -1:
    raise SystemExit

q0 = arm.positions()
target = fk_tool(TARGET_JOINTS[TARGET_LABEL])
limits = np.full(6, 2.0*np.pi)
result = numerical_ik(
    fk_tool,
    q0,
    target,
    lower_limits=-limits,
    upper_limits=limits,
)

print("Target:", TARGET_LABEL)
print("Joint order:", ", ".join(JOINT_NAMES))
print("Initial q [rad]:", np.array2string(q0, precision=6))
print("Converged:", result.converged, "Reason:", result.reason)
print("Iterations:", result.iterations)
print(f"Solver position error [mm]: {1000.0*result.position_error:.3f}")
print(f"Solver orientation error [deg]: {np.rad2deg(result.orientation_error):.3f}")

if not result.converged or not np.all(np.isfinite(result.q)):
    print("No motion commanded because IK did not produce a valid solution.")
    raise SystemExit

q_goal = np.asarray(result.q)
if np.any(q_goal < -limits) or np.any(q_goal > limits):
    print("No motion commanded because the solution violates a joint limit.")
    raise SystemExit

predicted = fk_tool(q_goal)
print("Goal q [rad]:", np.array2string(q_goal, precision=6))
print("Predicted tool position [m]:", np.array2string(predicted[:3, 3], precision=6))
print("Predicted tool RPY [rad]:", np.array2string(rotation_to_rpy(predicted[:3, :3]), precision=6))

duration = 8.0
start_time = robot.getTime()
while robot.step(arm.time_step) != -1:
    elapsed = robot.getTime() - start_time
    q_command = q0 + cubic_blend(elapsed/duration) * (q_goal-q0)
    arm.command_positions(q_command)
    if elapsed >= duration:
        break

settle_start = robot.getTime()
while robot.step(arm.time_step) != -1:
    arm.command_positions(q_goal)
    if robot.getTime() - settle_start >= 1.0:
        measured_q = arm.positions()
        position, rpy = arm.measured_tool_pose()
        print("Measured q [rad]:", np.array2string(measured_q, precision=6))
        if position is not None:
            print("Webots tool position [m]:", np.array2string(position, precision=6))
            print("Webots tool RPY [rad]:", np.array2string(rpy, precision=6))
        break

while robot.step(arm.time_step) != -1:
    arm.command_positions(q_goal)