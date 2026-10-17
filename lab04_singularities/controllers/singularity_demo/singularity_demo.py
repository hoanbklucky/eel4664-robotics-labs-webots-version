#!/usr/bin/env python3
"""Run supplied baseline and singularity-approach trials."""

from pathlib import Path
import sys

import numpy as np
from controller import Supervisor


REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from lab02_webots_ur5e_frames.src.ur5e_fk_starter import (  # noqa: E402
    T_6_TOOL,
    forward_kinematics,
)
from lab04_singularities.src.jacobian_starter import (  # noqa: E402
    analytic_jacobian,
    pose_difference,
)


JOINT_NAMES = (
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
)

# Both trials begin with a visibly bent, well-conditioned elbow. Trial 1 moves
# away from the straight-elbow singularity. Trial 2 reverses the same
# horizontal request and approaches the singularity from the safe side.
START_Q = np.array([0.20, -0.80, 1.40, -1.10, -0.70, 0.30])
AWAY_FROM_SINGULARITY = np.array([-1.0, 0.0, 0.0], dtype=float)
TOWARD_SINGULARITY = np.array([1.0, 0.0, 0.0], dtype=float)
REQUESTED_SPEED = 0.02  # m/s; slow enough to watch conditioning deteriorate
PATH_LENGTH = 0.20  # m
NOMINAL_DURATION = PATH_LENGTH / REQUESTED_SPEED
COMPLETION_ALLOWANCE = 3.0  # s; brief feedback-only finish after path motion
TARGET_TOLERANCE = 0.001  # m
SINGULARITY_CONDITION_THRESHOLD = 200.0
DAMPING = 0.05
MAX_COMMANDED_JOINT_RATE = 3.00  # rad/s; below the Webots model's 3.14 limit
POSITION_FEEDBACK_GAIN = 2.0  # 1/s
ORIENTATION_FEEDBACK_GAIN = 2.0  # 1/s
MOVE_DURATION = 2.5  # s; short reset between the two trials
SETTLE_DURATION = 0.25  # s
RATE_PLOT_PATH = REPO_ROOT / "lab04_singularities" / "joint_rate_comparison.svg"
RATE_HISTORIES = {}
SINGULARITY_TIMES = {}


def cubic_blend(progress):
    """Return a smooth interpolation fraction for 0 <= progress <= 1."""
    progress = np.clip(progress, 0.0, 1.0)
    return float(3.0 * progress**2 - 2.0 * progress**3)


robot = Supervisor()
time_step = int(robot.getBasicTimeStep())
motors = [robot.getDevice(name) for name in JOINT_NAMES]
sensors = [robot.getDevice(f"{name}_sensor") for name in JOINT_NAMES]
# The commanded motion holds orientation fixed, so the flange and the rigidly
# attached stylus tip undergo the same translation. Use the tip GPS to place
# the path where students actually see the stylus.
tool_position = robot.getDevice("tool_test_point_position")

request_start_node = robot.getFromDef("REQUEST_START_MARKER")
if request_start_node is None:
    raise SystemExit(
        "LAB 4 SETUP ERROR: this world does not provide supervisor access and "
        "the visual markers. Create a fresh lab04_work.wbt from the updated "
        "lab04_starter.wbt, then select the singularity_demo controller."
    )

request_start_marker = request_start_node.getField("translation")
request_goal_marker = robot.getFromDef("REQUEST_GOAL_MARKER").getField("translation")
request_dot_fields = [
    robot.getFromDef(f"REQUEST_DOT_{index}").getField("translation")
    for index in range(1, 5)
]
requested_path_points = robot.getFromDef("REQUESTED_PATH_COORD").getField("point")
actual_path_points = robot.getFromDef("ACTUAL_PATH_COORD").getField("point")
actual_end_marker = robot.getFromDef("ACTUAL_END_MARKER").getField("translation")

for sensor in sensors:
    sensor.enable(time_step)
tool_position.enable(time_step)
keyboard = robot.getKeyboard()
keyboard.enable(time_step)


def step_or_exit():
    if robot.step(time_step) == -1:
        raise SystemExit


def measured_joints():
    return np.array([sensor.getValue() for sensor in sensors], dtype=float)


def command_joints(q):
    for motor, value in zip(motors, q):
        motor.setPosition(float(value))


def set_line(field, start, end):
    field.setMFVec3f(0, np.asarray(start, dtype=float).tolist())
    field.setMFVec3f(1, np.asarray(end, dtype=float).tolist())


def show_request(start, target):
    """Draw the exact Cartesian translation requested in the current trial."""
    request_start_marker.setSFVec3f(start.tolist())
    request_goal_marker.setSFVec3f(target.tolist())
    set_line(requested_path_points, start, target)
    for fraction, field in zip((0.2, 0.4, 0.6, 0.8), request_dot_fields):
        field.setSFVec3f((start + fraction * (target - start)).tolist())
    set_line(actual_path_points, start, start)
    actual_end_marker.setSFVec3f(start.tolist())


def update_actual_trace(start):
    current = np.array(tool_position.getValues(), dtype=float)
    set_line(actual_path_points, start, current)
    actual_end_marker.setSFVec3f(current.tolist())


def show_preparing_label(label):
    robot.setLabel(0, label, 0.02, 0.02, 0.075, 0x102030, 0.0, "Arial")
    robot.setLabel(
        1, "MOVING TO THE BENT START POSE", 0.02, 0.115, 0.07,
        0x087830, 0.0, "Arial"
    )
    for label_id in (2, 3, 4, 5, 6, 7):
        robot.setLabel(label_id, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")


def show_trial_label(
        label, sigma_min, condition_number, inverse_method, elbow_angle,
        approach_singularity):
    robot.setLabel(0, label, 0.02, 0.02, 0.075, 0x102030, 0.0, "Arial")
    robot.setLabel(
        1,
        ">>> WELL-CONDITIONED START: ELBOW IS BENT <<<",
        0.02,
        0.115,
        0.07,
        0x087830,
        0.0,
        "Arial",
    )
    robot.setLabel(
        2,
        (f"START: sigma_min={sigma_min:.3f} | condition={condition_number:.1f} | "
         f"elbow={np.degrees(elbow_angle):.1f} deg"),
        0.02,
        0.205,
        0.055,
        0x202020,
        0.0,
        "Arial",
    )
    robot.setLabel(
        3,
        (f"20 cm {'TOWARD' if approach_singularity else 'AWAY FROM'} STRAIGHT ELBOW | "
         f"{inverse_method}"),
        0.02,
        0.275,
        0.055,
        0x5C4800,
        0.0,
        "Arial",
    )
    for label_id in (4, 5, 6, 7):
        robot.setLabel(label_id, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")


def show_singularity_checkpoint(
        sigma_min, condition_number, elbow_angle, applied_rate, raw_rate):
    """Replace the compact HUD with the metrics at the singularity threshold."""
    robot.setLabel(
        1, ">>> SINGULARITY THRESHOLD REACHED <<<", 0.02, 0.115, 0.075,
        0xD00000, 0.0, "Arial"
    )
    robot.setLabel(
        2,
        (f"NOW: sigma_min={sigma_min:.4f} | condition={condition_number:.0f} | "
         f"elbow={np.degrees(elbow_angle):.1f} deg"),
        0.02, 0.205, 0.055, 0x202020, 0.0, "Arial"
    )
    robot.setLabel(
        3,
        (f"JOINT RATE NOW = {applied_rate:.2f} rad/s | "
         f"RAW REQUEST = {raw_rate:.2f} rad/s | LIMIT = 3.00"),
        0.02, 0.275, 0.06, 0xD00000, 0.0, "Arial"
    )


def show_approach_result(
        sigma_min, condition_number, elbow_angle, peak_rate, reached_target):
    """Show the final near-singular metrics without adding more overlay lines."""
    status = (
        ">>> NEAR-SINGULAR ENDPOINT REACHED <<<"
        if reached_target else
        ">>> RATE-LIMITED NEAR SINGULARITY - TARGET NOT REACHED <<<"
    )
    robot.setLabel(
        1, status, 0.02, 0.115, 0.065,
        0xD00000, 0.0, "Arial"
    )
    robot.setLabel(
        2,
        (f"END: sigma_min={sigma_min:.4f} | condition={condition_number:.0f} | "
         f"elbow={np.degrees(elbow_angle):.1f} deg"),
        0.02, 0.205, 0.055, 0x202020, 0.0, "Arial"
    )
    robot.setLabel(
        3, f"PEAK COMMANDED JOINT RATE = {peak_rate:.2f} rad/s",
        0.02, 0.275, 0.055, 0xD00000, 0.0, "Arial"
    )


def move_smoothly(q_goal, duration, observer=None):
    """Move from the measured pose to q_goal using a cubic blend."""
    q_start = measured_joints()
    start_time = robot.getTime()
    while True:
        step_or_exit()
        elapsed = robot.getTime() - start_time
        blend = cubic_blend(elapsed / duration)
        command_joints(q_start + blend * (q_goal - q_start))
        if observer is not None:
            observer()
        if elapsed >= duration:
            break


def hold(q, duration):
    start_time = robot.getTime()
    while robot.getTime() - start_time < duration:
        step_or_exit()
        command_joints(q)


def wait_for_space(q, message, hint=""):
    """Hold the robot until the student presses Space in the 3D view."""
    robot.setLabel(4, message, 0.02, 0.81, 0.06, 0xFFF1A8, 0.0, "Arial")
    robot.setLabel(5, hint, 0.02, 0.89, 0.052, 0xF1C4FF, 0.0, "Arial")
    print(message)
    if hint:
        print(hint)
    while keyboard.getKey() != -1:
        pass
    while True:
        step_or_exit()
        command_joints(q)
        key = keyboard.getKey()
        while key != -1:
            if key & 0xFFFF == ord(" "):
                return
            key = keyboard.getKey()


def rate_limit(qdot):
    """Uniformly scale a velocity command to the demonstration limit."""
    qdot = np.asarray(qdot, dtype=float)
    peak_rate = float(np.max(np.abs(qdot)))
    if peak_rate <= MAX_COMMANDED_JOINT_RATE:
        return qdot, 1.0
    scale = MAX_COMMANDED_JOINT_RATE / peak_rate
    return scale * qdot, scale


def stylus_fk(q):
    """Return the pose of the visible stylus tip controlled in this demo."""
    T_tool = forward_kinematics(q) @ T_6_TOOL
    T_tip = T_tool.copy()
    T_tip[:3, 3] += T_tool[:3, :3] @ np.array([0.0, 0.13, 0.0])
    return T_tip


def write_rate_plot():
    """Write a dependency-free SVG comparing peak joint rate over time."""
    width, height = 1000, 650
    left, right, top, bottom = 95, 35, 70, 80
    plot_width = width - left - right
    plot_height = height - top - bottom
    maximum_time = max(
        NOMINAL_DURATION,
        max((samples[-1][0] for samples in RATE_HISTORIES.values() if samples),
            default=NOMINAL_DURATION),
    )
    maximum_rate = max(
        MAX_COMMANDED_JOINT_RATE * 1.08,
        max(
            (rate for samples in RATE_HISTORIES.values() for _, rate in samples),
            default=0.0,
        ),
    )
    colors = ("#16833b", "#d7191c", "#6a1b9a")

    def x_pixel(time_value):
        return left + plot_width * time_value / maximum_time

    def y_pixel(rate_value):
        return top + plot_height * (1.0 - rate_value / maximum_rate)

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="500" y="36" text-anchor="middle" font-family="Arial" '
        'font-size="25" font-weight="bold">Lab 4 Joint Rate Comparison</text>',
        '<text x="500" y="61" text-anchor="middle" font-family="Arial" '
        'font-size="15">Maximum absolute commanded rate among the six joints</text>',
    ]
    for fraction in np.linspace(0.0, 1.0, 6):
        rate = maximum_rate * fraction
        y = y_pixel(rate)
        svg.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" '
            'stroke="#dddddd" stroke-width="1"/>'
        )
        svg.append(
            f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end" '
            f'font-family="Arial" font-size="14">{rate:.2f}</text>'
        )
    for fraction in np.linspace(0.0, 1.0, 6):
        time_value = maximum_time * fraction
        x = x_pixel(time_value)
        svg.append(
            f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" '
            'stroke="#eeeeee" stroke-width="1"/>'
        )
        svg.append(
            f'<text x="{x:.1f}" y="{height-bottom+25}" text-anchor="middle" '
            f'font-family="Arial" font-size="14">{time_value:.1f}</text>'
        )
    limit_y = y_pixel(MAX_COMMANDED_JOINT_RATE)
    svg.extend([
        f'<line x1="{left}" y1="{limit_y:.1f}" x2="{width-right}" y2="{limit_y:.1f}" '
        'stroke="#555555" stroke-width="2" stroke-dasharray="8 6"/>',
        f'<text x="{width-right-4}" y="{limit_y-8:.1f}" text-anchor="end" '
        'font-family="Arial" font-size="14">3.00 rad/s safety limit</text>',
    ])
    for index, (name, event_time) in enumerate(SINGULARITY_TIMES.items()):
        event_x = x_pixel(event_time)
        svg.extend([
            f'<line x1="{event_x:.1f}" y1="{top}" x2="{event_x:.1f}" '
            f'y2="{height-bottom}" stroke="#d4a500" stroke-width="2" '
            'stroke-dasharray="5 5"/>',
            f'<text x="{event_x+7:.1f}" y="{top+42+18*index}" font-family="Arial" '
            f'font-size="13" fill="#7a5c00">{name}: condition = '
            f'{SINGULARITY_CONDITION_THRESHOLD:.0f}</text>',
        ])
    for (name, samples), color in zip(RATE_HISTORIES.items(), colors):
        points = " ".join(
            f"{x_pixel(time_value):.1f},{y_pixel(rate):.1f}"
            for time_value, rate in samples
        )
        svg.append(
            f'<polyline points="{points}" fill="none" stroke="{color}" '
            'stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>'
        )
    svg.extend([
        f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" '
        f'y2="{height-bottom}" stroke="#222222" stroke-width="2"/>',
        f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" '
        'stroke="#222222" stroke-width="2"/>',
        f'<text x="{left + plot_width/2:.1f}" y="{height-22}" text-anchor="middle" '
        'font-family="Arial" font-size="18">Active motion time [s]</text>',
        f'<text x="26" y="{top + plot_height/2:.1f}" text-anchor="middle" '
        'font-family="Arial" font-size="18" '
        f'transform="rotate(-90 26 {top + plot_height/2:.1f})">max |joint rate| [rad/s]</text>',
    ])
    legend_x = left + 365
    for index, ((name, _), color) in enumerate(zip(RATE_HISTORIES.items(), colors)):
        x = legend_x + 175 * index
        svg.extend([
            f'<line x1="{x}" y1="{top+18}" x2="{x+32}" y2="{top+18}" '
            f'stroke="{color}" stroke-width="5"/>',
            f'<text x="{x+39}" y="{top+23}" font-family="Arial" '
            f'font-size="14">{name}</text>',
        ])
    svg.append('</svg>')
    RATE_PLOT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RATE_PLOT_PATH.write_text("\n".join(svg), encoding="utf-8")


def inverse_rate(J, desired_twist, inverse_method):
    if inverse_method == "undamped":
        return np.linalg.solve(J, desired_twist)
    if inverse_method == "damped":
        system = J @ J.T + DAMPING**2 * np.eye(6)
        return J.T @ np.linalg.solve(system, desired_twist)
    raise ValueError(f"unknown inverse method: {inverse_method}")


def execute_cartesian_motion(
        q_start, direction, inverse_method, measured_start, requested_target,
        approach_singularity):
    """Track the line and pause when an approaching trial becomes ill conditioned."""
    q_command = q_start.copy()
    starting_pose = stylus_fk(q_start)
    previous_time = robot.getTime()
    motion_time = 0.0
    peak_commanded_rate = 0.0
    minimum_safety_scale = 1.0
    rate_history = []
    reached_target = False
    singularity_time = None

    while True:
        step_or_exit()
        now = robot.getTime()
        dt = now - previous_time
        previous_time = now
        motion_time += dt

        current_position = np.array(tool_position.getValues(), dtype=float)
        current_q = measured_joints()
        current_pose = stylus_fk(current_q)
        J = analytic_jacobian(current_q, endpoint_fk=stylus_fk)
        singular_values = np.linalg.svd(J, compute_uv=False)
        sigma_min = float(singular_values[-1])
        condition_number = float(singular_values[0] / sigma_min)

        if motion_time >= NOMINAL_DURATION:
            target_error = np.linalg.norm(requested_target - current_position)
            if target_error < TARGET_TOLERANCE:
                reached_target = True
                break
            if motion_time >= NOMINAL_DURATION + COMPLETION_ALLOWANCE:
                break

        # Follow a moving reference on the yellow line. Feedback removes both
        # along-path lag and cross-track error while holding orientation.
        reference_pose = starting_pose.copy()
        reference_distance = min(REQUESTED_SPEED * motion_time, PATH_LENGTH)
        reference_pose[:3, 3] = measured_start + reference_distance * direction
        pose_error = pose_difference(current_pose, reference_pose)
        tracking_twist = np.zeros(6)
        if motion_time < NOMINAL_DURATION:
            tracking_twist[:3] = REQUESTED_SPEED * direction
        tracking_twist[:3] += POSITION_FEEDBACK_GAIN * pose_error[:3]
        tracking_twist[3:] = ORIENTATION_FEEDBACK_GAIN * pose_error[3:]

        proposed_qdot = inverse_rate(J, tracking_twist, inverse_method)
        applied_qdot, safety_scale = rate_limit(proposed_qdot)
        raw_peak = float(np.max(np.abs(proposed_qdot)))
        commanded_peak = float(np.max(np.abs(applied_qdot)))
        peak_commanded_rate = max(peak_commanded_rate, commanded_peak)
        robot.setLabel(
            5,
            (f"JOINT RATE NOW = {commanded_peak:.2f} rad/s | "
             f"PEAK SO FAR = {peak_commanded_rate:.2f} rad/s"),
            0.02, 0.89, 0.06, 0x6A1B9A, 0.0, "Arial",
        )

        if (approach_singularity and singularity_time is None and
                condition_number >= SINGULARITY_CONDITION_THRESHOLD):
            singularity_time = motion_time
            print("SINGULARITY CHECKPOINT")
            print(f"  active motion time: {motion_time:.3f} s")
            print(f"  minimum singular value: {sigma_min:.6f}")
            print(f"  condition number: {condition_number:.1f}")
            print(f"  elbow angle: {np.degrees(current_q[2]):.2f} deg")
            print(f"  raw requested peak joint rate: {raw_peak:.3f} rad/s")
            print(f"  applied peak joint rate: {commanded_peak:.3f} rad/s")
            print(f"  peak commanded joint rate so far: {peak_commanded_rate:.3f} rad/s")
            show_singularity_checkpoint(
                sigma_min, condition_number, current_q[2], commanded_peak,
                raw_peak,
            )
            wait_for_space(
                q_command,
                f"PAUSED AT CONDITION = {SINGULARITY_CONDITION_THRESHOLD:.0f}",
                "READ THE JOINT RATE ABOVE, THEN PRESS SPACE TO CONTINUE.",
            )
            robot.setLabel(
                4, "RUNNING TOWARD THE GREEN SINGULARITY TARGET", 0.02, 0.81,
                0.06, 0xFFF1A8, 0.0, "Arial"
            )
            robot.setLabel(5, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")
            previous_time = robot.getTime()

        q_command += applied_qdot * dt
        command_joints(q_command)
        update_actual_trace(measured_start)
        rate_history.append((motion_time, commanded_peak))
        minimum_safety_scale = min(minimum_safety_scale, safety_scale)

    return (
        q_command,
        peak_commanded_rate,
        minimum_safety_scale,
        reached_target,
        rate_history,
        singularity_time,
    )


def run_trial(
        label, direction, inverse_method, approach_singularity, reposition=True):
    print(f"\n=== {label} ===")
    if reposition:
        print("Moving to the test pose...")
        show_preparing_label(label)
        move_smoothly(START_Q, MOVE_DURATION)
    else:
        print("The world starts at the bent-elbow Trial 1 pose.")
    hold(START_Q, SETTLE_DURATION)

    q_start = measured_joints()
    J = analytic_jacobian(q_start, endpoint_fk=stylus_fk)
    singular_values = np.linalg.svd(J, compute_uv=False)
    sigma_min = float(singular_values[-1])
    condition_number = float(singular_values[0] / sigma_min)

    desired_twist = np.zeros(6)
    desired_twist[:3] = REQUESTED_SPEED * direction

    undamped_qdot = np.linalg.solve(J, desired_twist)
    damped_qdot = inverse_rate(J, desired_twist, "damped")
    proposed_qdot = inverse_rate(J, desired_twist, inverse_method)
    method_description = (
        "undamped inverse"
        if inverse_method == "undamped"
        else f"damped inverse (lambda={DAMPING:.2f})"
    )
    applied_qdot, safety_scale = rate_limit(proposed_qdot)
    predicted_twist = J @ applied_qdot

    measured_start = np.array(tool_position.getValues(), dtype=float)
    requested_translation = PATH_LENGTH * direction
    requested_target = measured_start + requested_translation
    show_request(measured_start, requested_target)
    show_trial_label(
        label, sigma_min, condition_number, method_description, q_start[2],
        approach_singularity,
    )
    wait_for_space(
        q_start,
        "PRESS SPACE TO RUN THIS TRIAL",
        (
            ("WATCH JOINT RATE GROW; PAUSE WHEN CONDITION REACHES "
             f"{SINGULARITY_CONDITION_THRESHOLD:.0f}")
            if approach_singularity
            else "BASELINE MOVES AWAY FROM THE SINGULARITY"
        ),
    )
    robot.setLabel(
        4,
        ("RUNNING TOWARD STRAIGHT ELBOW - WATCH THE RATE GROW"
         if approach_singularity else
         "RUNNING AWAY FROM STRAIGHT ELBOW - MODERATE RATE"),
        0.02,
        0.81,
        0.06,
        0xFFF1A8,
        0.0,
        "Arial",
    )
    robot.setLabel(5, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")

    print("Joint angles [rad]:", np.array2string(q_start, precision=3))
    print("Singular values:", np.array2string(singular_values, precision=5))
    print(f"Minimum singular value: {sigma_min:.6f}")
    print(f"Condition number: {condition_number:.1f}")
    print(f"Inverse method: {method_description}")
    print(f"Raw undamped joint-rate norm: {np.linalg.norm(undamped_qdot):.3f} rad/s")
    print(f"Raw undamped peak joint rate: {np.max(np.abs(undamped_qdot)):.3f} rad/s")
    if inverse_method == "damped":
        print(f"Damped joint-rate norm: {np.linalg.norm(damped_qdot):.3f} rad/s")
    print(f"Initial safety scale: {safety_scale:.3f}")
    print(f"Initial applied joint-rate-vector norm: {np.linalg.norm(applied_qdot):.3f} rad/s")
    print("Requested translation [m]:",
          np.array2string(requested_translation, precision=4))
    print("Initial locally predicted velocity [m/s]:",
          np.array2string(predicted_twist[:3], precision=4))

    (q_goal, peak_commanded_rate, minimum_safety_scale, reached_target,
     rate_history, singularity_time) = (
        execute_cartesian_motion(
            q_start, direction, inverse_method, measured_start, requested_target,
            approach_singularity,
        )
    )
    short_label = label.split(":", 1)[0]
    RATE_HISTORIES[short_label] = rate_history
    if singularity_time is not None:
        SINGULARITY_TIMES[short_label] = singularity_time
    try:
        write_rate_plot()
        print(f"Joint-rate plot saved to: {RATE_PLOT_PATH}")
    except OSError as error:
        print(f"WARNING: could not write joint-rate plot: {error}")
    hold(q_goal, SETTLE_DURATION)
    measured_end = np.array(tool_position.getValues(), dtype=float)
    update_actual_trace(measured_start)
    measured_displacement = measured_end - measured_start
    final_q = measured_joints()
    final_singular_values = np.linalg.svd(
        analytic_jacobian(final_q, endpoint_fk=stylus_fk), compute_uv=False
    )
    final_sigma_min = float(final_singular_values[-1])
    final_condition_number = float(final_singular_values[0] / final_sigma_min)
    if approach_singularity:
        show_approach_result(
            final_sigma_min, final_condition_number, final_q[2],
            peak_commanded_rate, reached_target,
        )
    print("Webots-measured translation [m]:",
          np.array2string(measured_displacement, precision=4))
    print(f"Measured translation magnitude: {np.linalg.norm(measured_displacement):.4f} m")
    print(f"Peak commanded joint rate during trial: {peak_commanded_rate:.3f} rad/s")
    print(f"Minimum safety scale during trial: {minimum_safety_scale:.3f}")
    print(f"Final minimum singular value: {final_sigma_min:.6f}")
    print(f"Final condition number: {final_condition_number:.1f}")
    print(f"Final elbow angle: {np.degrees(final_q[2]):.2f} deg")
    print("Target reached:", "YES" if reached_target else "NO (completion allowance ended)")
    if not reached_target:
        print(
            "The red trace stopped short because the requested constant-speed "
            "path reaches the straight-elbow workspace boundary. The finite "
            "joint-rate limit prevents the unbounded undamped rate demand."
        )
    if not approach_singularity:
        robot.setLabel(
            1, ">>> TRIAL 1 COMPLETE - BASELINE RECORDED <<<",
            0.02, 0.115, 0.065, 0x087830, 0.0, "Arial",
        )
        robot.setLabel(
            3, f"TRIAL 1 PEAK COMMANDED JOINT RATE = {peak_commanded_rate:.2f} rad/s",
            0.02, 0.275, 0.06, 0xD00000, 0.0, "Arial",
        )
        wait_for_space(
            q_goal,
            "PRESS SPACE TO RETURN TO THE BENT START POSE",
            "NEXT: TRIAL 2 APPROACHES THE SINGULARITY",
        )


step_or_exit()
print("[LAB 4 SINGULARITY DEMONSTRATION]")
print("Both trials start from the same bent, well-conditioned pose.")
print("Trial 1 moves away; Trial 2 moves 20 cm toward a singularity.")
run_trial(
    "TRIAL 1: MOVE AWAY / UNDAMPED BASELINE",
    AWAY_FROM_SINGULARITY,
    "undamped",
    approach_singularity=False,
    reposition=False,
)
run_trial(
    "TRIAL 2: APPROACH SINGULARITY / UNDAMPED",
    TOWARD_SINGULARITY,
    "undamped",
    approach_singularity=True,
)

print("\n[DEMONSTRATION COMPLETE]")
print("Compare the moderate Trial 1 rate with the sharp Trial 2 increase.")
print(f"Joint-rate comparison plot: {RATE_PLOT_PATH}")
print("Reset Webots to run the demonstration again.")

q_hold = measured_joints()
while robot.step(time_step) != -1:
    command_joints(q_hold)
