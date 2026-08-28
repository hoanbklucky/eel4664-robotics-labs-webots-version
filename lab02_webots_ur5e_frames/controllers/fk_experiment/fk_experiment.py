#!/usr/bin/env python3
"""Visit three FK vertices, close an air-drawn loop, and print measurements."""

from controller import Robot
import numpy as np

from ur5e_devices import JOINT_NAMES, UR5eDevices


TARGETS = (
    ("A", np.array([0.0, -1.20, 1.20, -1.50, -1.57, 0.0])),
    ("B", np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30])),
    ("C", np.array([-0.30, -0.90, 1.10, -1.40, -1.20, -0.20])),
    ("A-return", np.array([0.0, -1.20, 1.20, -1.50, -1.57, 0.0])),
)
MOVE_DURATION = 8.0
SETTLE_DURATION = 1.0


def cubic_blend(s):
    """Return a smooth 0-to-1 blend with zero endpoint velocity."""
    s = float(np.clip(s, 0.0, 1.0))
    return 3.0 * s**2 - 2.0 * s**3


def print_measurement(label, arm):
    """Print synchronized joint and read-only tool measurements."""
    q_measured = arm.positions()
    position, rpy = arm.measured_tool_pose()
    test_point = arm.measured_tool_test_point()

    print(f"\n===== POSE {label} MEASUREMENT =====")
    print("Joint order:", ", ".join(JOINT_NAMES))
    print("Measured q [rad]:", np.array2string(q_measured, precision=6))
    if position is not None:
        print("Tool position [m]:", np.array2string(position, precision=6))
        print("Tool RPY [rad]:", np.array2string(rpy, precision=6))
    if test_point is not None:
        print("Tool test point [m]:", np.array2string(test_point, precision=6))


robot = Robot()
arm = UR5eDevices(robot)
if robot.step(arm.time_step) == -1:
    raise SystemExit

q_start = arm.positions()
print("FK air-drawing started: A -> B -> C -> A.")

for label, q_goal in TARGETS:
    print(f"Moving to Pose {label}: {np.array2string(q_goal, precision=3)}")
    move_start = robot.getTime()

    while robot.step(arm.time_step) != -1:
        elapsed = robot.getTime() - move_start
        q_command = q_start + cubic_blend(elapsed / MOVE_DURATION) * (q_goal - q_start)
        arm.command_positions(q_command)
        if elapsed >= MOVE_DURATION:
            break
    else:
        raise SystemExit

    # Hold briefly so the measured values represent the settled pose.
    settle_start = robot.getTime()
    while robot.step(arm.time_step) != -1:
        arm.command_positions(q_goal)
        if robot.getTime() - settle_start >= SETTLE_DURATION:
            break
    else:
        raise SystemExit

    if label == "A-return":
        print("[LOOP CLOSED] Returned to Pose A.")
    else:
        print_measurement(label, arm)
    q_start = arm.positions()

print("\n[EXPERIMENT DONE] Air-drawn loop A -> B -> C -> A completed.")

# Keep the final target active until the student pauses or resets Webots.
while robot.step(arm.time_step) != -1:
    arm.command_positions(q_start)
