#!/usr/bin/env python3
"""Lab 00/01 demonstration controller for the shared UR5e world."""
from controller import Robot
import numpy as np
from ur5e_devices import JOINT_NAMES, UR5eDevices

def cubic_blend(s):
    """Zero-velocity endpoint blend for 0 <= s <= 1."""
    s = np.clip(s, 0.0, 1.0)
    return float(3.0 * s**2 - 2.0 * s**3)

robot = Robot()
arm = UR5eDevices(robot)
if robot.step(arm.time_step) == -1:
    raise SystemExit
q0 = arm.positions()
q_goal = np.array([0.0, -1.20, 1.20, -1.50, -1.57, 0.0])
duration = 8.0
t0 = robot.getTime()
print("Joint order:", ", ".join(JOINT_NAMES))
print("Initial q [rad]:", np.array2string(q0, precision=4))
print("Target  q [rad]:", np.array2string(q_goal, precision=4))

while robot.step(arm.time_step) != -1:
    elapsed = robot.getTime() - t0
    q_command = q0 + cubic_blend(elapsed / duration) * (q_goal - q0)
    arm.command_positions(q_command)
    if elapsed >= duration:
        position, rpy = arm.measured_tool_pose()
        print("Final q [rad]:", np.array2string(arm.positions(), precision=4))
        print("Tool position [m]:", np.array2string(position, precision=4))
        print("Tool RPY [rad]:", np.array2string(rpy, precision=4))
        break
while robot.step(arm.time_step) != -1:
    arm.command_positions(q_goal)
