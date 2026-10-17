#!/usr/bin/env python3
"""Run supplied baseline, undamped, and damped singularity trials."""

from pathlib import Path
import sys

import numpy as np
from controller import Robot


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from lab04_jacobian_singularities.src.jacobian_starter import analytic_jacobian  # noqa: E402


JOINT_NAMES = (
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
)

# The two trials differ mainly in elbow angle. The second pose is close to the
# straight-elbow singularity but remains slightly bent for a finite comparison.
WELL_CONDITIONED_Q = np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30])
NEAR_SINGULAR_Q = np.array([0.20, -0.80, 0.03, -1.10, -0.70, 0.30])

# Both trials request the same 6 cm translation while holding orientation.
# This world-frame direction is close to the motion direction lost when the
# elbow is straight in the selected configuration.
TRANSLATION_DIRECTION = np.array([0.66, 0.20, 0.71], dtype=float)
TRANSLATION_DIRECTION /= np.linalg.norm(TRANSLATION_DIRECTION)
REQUESTED_SPEED = 0.03  # m/s
TEST_DURATION = 2.0  # s
DAMPING = 0.05
MAX_COMMANDED_JOINT_RATE = 0.50  # rad/s during the cubic motion
MOVE_DURATION = 5.0  # s
SETTLE_DURATION = 1.0  # s


def cubic_blend(progress):
    """Return a smooth interpolation fraction for 0 <= progress <= 1."""
    progress = np.clip(progress, 0.0, 1.0)
    return float(3.0 * progress**2 - 2.0 * progress**3)


robot = Robot()
time_step = int(robot.getBasicTimeStep())
motors = [robot.getDevice(name) for name in JOINT_NAMES]
sensors = [robot.getDevice(f"{name}_sensor") for name in JOINT_NAMES]
tool_position = robot.getDevice("tool_position")

for sensor in sensors:
    sensor.enable(time_step)
tool_position.enable(time_step)


def step_or_exit():
    if robot.step(time_step) == -1:
        raise SystemExit


def measured_joints():
    return np.array([sensor.getValue() for sensor in sensors], dtype=float)


def command_joints(q):
    for motor, value in zip(motors, q):
        motor.setPosition(float(value))


def move_smoothly(q_goal, duration):
    """Move from the measured pose to q_goal using a cubic blend."""
    q_start = measured_joints()
    start_time = robot.getTime()
    while True:
        step_or_exit()
        elapsed = robot.getTime() - start_time
        blend = cubic_blend(elapsed / duration)
        command_joints(q_start + blend * (q_goal - q_start))
        if elapsed >= duration:
            break


def hold(q, duration):
    start_time = robot.getTime()
    while robot.getTime() - start_time < duration:
        step_or_exit()
        command_joints(q)


def rate_limit_for_cubic(qdot):
    """Scale qdot so the cubic interpolation never exceeds the safe rate."""
    qdot = np.asarray(qdot, dtype=float)
    peak_average_rate = float(np.max(np.abs(qdot)))
    # The derivative of 3s^2 - 2s^3 peaks at 1.5. The position change below
    # equals qdot * TEST_DURATION, so the actual peak rate is 1.5 * qdot.
    if 1.5 * peak_average_rate <= MAX_COMMANDED_JOINT_RATE:
        return qdot, 1.0
    scale = MAX_COMMANDED_JOINT_RATE / (1.5 * peak_average_rate)
    return scale * qdot, scale


def run_trial(label, q_pose, inverse_method):
    print(f"\n=== {label} ===")
    print("Moving to the test pose...")
    move_smoothly(q_pose, MOVE_DURATION)
    hold(q_pose, SETTLE_DURATION)

    q_start = measured_joints()
    J = analytic_jacobian(q_start)
    singular_values = np.linalg.svd(J, compute_uv=False)
    sigma_min = float(singular_values[-1])
    condition_number = float(singular_values[0] / sigma_min)

    desired_twist = np.zeros(6)
    desired_twist[:3] = REQUESTED_SPEED * TRANSLATION_DIRECTION

    undamped_qdot = np.linalg.solve(J, desired_twist)
    system = J @ J.T + DAMPING**2 * np.eye(6)
    damped_qdot = J.T @ np.linalg.solve(system, desired_twist)

    if inverse_method == "undamped":
        proposed_qdot = undamped_qdot
        method_description = "undamped inverse"
    elif inverse_method == "damped":
        proposed_qdot = damped_qdot
        method_description = f"damped inverse (lambda={DAMPING:.2f})"
    else:
        raise ValueError(f"unknown inverse method: {inverse_method}")

    applied_qdot, safety_scale = rate_limit_for_cubic(proposed_qdot)
    predicted_twist = J @ applied_qdot

    print("Joint angles [rad]:", np.array2string(q_start, precision=3))
    print("Singular values:", np.array2string(singular_values, precision=5))
    print(f"Minimum singular value: {sigma_min:.6f}")
    print(f"Condition number: {condition_number:.1f}")
    print(f"Inverse method: {method_description}")
    print(f"Raw undamped joint-rate norm: {np.linalg.norm(undamped_qdot):.3f} rad/s")
    print(f"Raw undamped peak joint rate: {np.max(np.abs(undamped_qdot)):.3f} rad/s")
    if inverse_method == "damped":
        print(f"Damped joint-rate norm: {np.linalg.norm(damped_qdot):.3f} rad/s")
    print(f"Safety scale applied to selected command: {safety_scale:.3f}")
    print(f"Applied joint-rate-vector norm: {np.linalg.norm(applied_qdot):.3f} rad/s")
    print(f"Peak commanded joint rate: "
          f"{1.5 * np.max(np.abs(applied_qdot)):.3f} rad/s")
    print("Requested translation [m]:",
          np.array2string(desired_twist[:3] * TEST_DURATION, precision=4))
    print("Locally predicted applied translation [m]:",
          np.array2string(predicted_twist[:3] * TEST_DURATION, precision=4))

    measured_start = np.array(tool_position.getValues(), dtype=float)
    q_goal = q_start + applied_qdot * TEST_DURATION
    move_smoothly(q_goal, TEST_DURATION)
    hold(q_goal, SETTLE_DURATION)
    measured_end = np.array(tool_position.getValues(), dtype=float)
    measured_displacement = measured_end - measured_start
    print("Webots-measured translation [m]:",
          np.array2string(measured_displacement, precision=4))
    print(f"Measured translation magnitude: {np.linalg.norm(measured_displacement):.4f} m")


step_or_exit()
print("[LAB 4 SINGULARITY DEMONSTRATION]")
print("Three trials make the same 6 cm Cartesian request.")
print("The near-singular undamped command is rate-limited before execution.")
run_trial(
    "TRIAL 1: BENT ELBOW / UNDAMPED BASELINE",
    WELL_CONDITIONED_Q,
    "undamped",
)
run_trial(
    "TRIAL 2: ALMOST STRAIGHT ELBOW / UNDAMPED AND RATE-LIMITED",
    NEAR_SINGULAR_Q,
    "undamped",
)
run_trial(
    "TRIAL 3: ALMOST STRAIGHT ELBOW / DAMPED",
    NEAR_SINGULAR_Q,
    "damped",
)

print("\n[DEMONSTRATION COMPLETE]")
print("Compare joint motion and tool displacement in Trials 2 and 3.")
print("Reset Webots to run the demonstration again.")

q_hold = measured_joints()
while robot.step(time_step) != -1:
    command_joints(q_hold)
