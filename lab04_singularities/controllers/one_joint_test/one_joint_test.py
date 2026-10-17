#!/usr/bin/env python3
"""Move one UR5e joint slightly and compare predicted and measured tool motion."""

from pathlib import Path
import sys

import numpy as np
from controller import Robot


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from lab02_webots_ur5e_frames.src.ur5e_fk_starter import (  # noqa: E402
    T_6_TOOL,
    forward_kinematics,
)


JOINT_NAMES = (
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
)

# This small base-joint motion is safe in the supplied starter world.
TEST_JOINT_INDEX = 0
DELTA_Q = 0.10  # rad, approximately 5.7 degrees
MOVE_DURATION = 3.0  # s
SETTLE_DURATION = 1.0  # s


def cubic_blend(progress):
    """Return a zero-endpoint-velocity blend for 0 <= progress <= 1."""
    progress = np.clip(progress, 0.0, 1.0)
    return float(3.0 * progress**2 - 2.0 * progress**3)


def tool_position_from_fk(q):
    """Return the tool-frame origin predicted by the Lab 2 FK model."""
    return (forward_kinematics(q) @ T_6_TOOL)[:3, 3]


robot = Robot()
time_step = int(robot.getBasicTimeStep())
motors = [robot.getDevice(name) for name in JOINT_NAMES]
sensors = [robot.getDevice(f"{name}_sensor") for name in JOINT_NAMES]
tool_position = robot.getDevice("tool_position")

for sensor in sensors:
    sensor.enable(time_step)
tool_position.enable(time_step)

if robot.step(time_step) == -1:
    raise SystemExit

q_start = np.array([sensor.getValue() for sensor in sensors], dtype=float)
q_goal = q_start.copy()
q_goal[TEST_JOINT_INDEX] += DELTA_Q

predicted_start = tool_position_from_fk(q_start)
predicted_goal = tool_position_from_fk(q_goal)
measured_start = np.array(tool_position.getValues(), dtype=float)

print("[ONE-JOINT TEST]")
print("Joint order:", ", ".join(JOINT_NAMES))
print(f"Moving only {JOINT_NAMES[TEST_JOINT_INDEX]} by {DELTA_Q:.3f} rad")
print("Initial q [rad]:", np.array2string(q_start, precision=6))
print("Target  q [rad]:", np.array2string(q_goal, precision=6))
print("Predicted tool displacement [m]:",
      np.array2string(predicted_goal - predicted_start, precision=6))

start_time = robot.getTime()
while robot.step(time_step) != -1:
    elapsed = robot.getTime() - start_time
    command = q_start + cubic_blend(elapsed / MOVE_DURATION) * (q_goal - q_start)
    for motor, position in zip(motors, command):
        motor.setPosition(float(position))
    if elapsed >= MOVE_DURATION:
        break

settle_start = robot.getTime()
while robot.step(time_step) != -1:
    for motor, position in zip(motors, q_goal):
        motor.setPosition(float(position))
    if robot.getTime() - settle_start >= SETTLE_DURATION:
        break

q_final = np.array([sensor.getValue() for sensor in sensors], dtype=float)
measured_final = np.array(tool_position.getValues(), dtype=float)

print("Final q [rad]:", np.array2string(q_final, precision=6))
print("Measured tool displacement [m]:",
      np.array2string(measured_final - measured_start, precision=6))
print("Compare the signs and dominant direction of the two displacement vectors.")
print("Reset Webots before repeating the test.")

# Hold the final configuration so the result remains visible.
while robot.step(time_step) != -1:
    for motor, position in zip(motors, q_goal):
        motor.setPosition(float(position))
