#!/usr/bin/env python3
"""Lab 2 demonstration controller for the shared UR5e world."""
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
q_goal = q0.copy()
q_goal[0] += 0.10
duration = 4.0
settle_duration = 1.0
tracking_tolerance = 1e-3
t0 = robot.getTime()
print("Joint order:", ", ".join(JOINT_NAMES))
print("Initial q [rad]:", np.array2string(q0, precision=6))
print("Target  q [rad]:", np.array2string(q_goal, precision=6))

while robot.step(arm.time_step) != -1:
    elapsed = robot.getTime() - t0
    q_command = q0 + cubic_blend(elapsed / duration) * (q_goal - q0)
    arm.command_positions(q_command)
    if elapsed >= duration:
        break

# setPosition() specifies a target; the simulated joint does not reach it
# instantaneously. Hold the final target before recording alignment data.
print(f"Settling for {settle_duration:.1f} s before measurement...")
settle_start = robot.getTime()
while robot.step(arm.time_step) != -1:
    arm.command_positions(q_goal)
    if robot.getTime() - settle_start >= settle_duration:
        q_final = arm.positions()
        q_error = q_goal - q_final
        max_error = float(np.max(np.abs(q_error)))
        position, rpy = arm.measured_tool_pose()
        test_point = arm.measured_tool_test_point()

        print("Final q [rad]:", np.array2string(q_final, precision=6))
        print("Tracking error target - measured [rad]:",
              np.array2string(q_error, precision=6))
        print(f"Maximum absolute tracking error [rad]: {max_error:.6e}")
        if max_error <= tracking_tolerance:
            print(f"[TRACKING PASS] maximum error <= {tracking_tolerance:.1e} rad")
        else:
            print(f"[TRACKING WARNING] maximum error > {tracking_tolerance:.1e} rad")
        if position is not None:
            print("Tool position [m]:", np.array2string(position, precision=6))
            print("Tool RPY [rad]:", np.array2string(rpy, precision=6))
        if test_point is not None:
            print("Tool test point [m]:", np.array2string(test_point, precision=6))
        break

# Continue holding the final configuration after reporting the measurements.
while robot.step(arm.time_step) != -1:
    arm.command_positions(q_goal)
