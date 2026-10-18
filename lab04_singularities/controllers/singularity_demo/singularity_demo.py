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
    modified_dh_joint_axes,
    pose_difference,
)
from lab04_singularities.src.cartesian_path_controller import (  # noqa: E402
    cartesian_path_controller,
)


JOINT_NAMES = (
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
)

# Trials 1 and 2 demonstrate an elbow singularity. Trial 3 uses a different
# well-conditioned start and crosses a shoulder-singular region with the elbow
# still bent and wrist joint 2 away from zero.
ELBOW_START_Q = np.array([0.20, -0.80, 1.40, -1.10, -0.70, 0.30])
AWAY_FROM_SINGULARITY = np.array([-1.0, 0.0, 0.0], dtype=float)
TOWARD_SINGULARITY = np.array([1.0, 0.0, 0.0], dtype=float)
SHOULDER_START_Q = np.array(
    [-1.971137, -2.076381, 0.639429, 1.329040, 1.291846, -0.601321]
)
SHOULDER_DIRECTION = np.array([-0.39757, -0.91757, 0.00040], dtype=float)
SHOULDER_DIRECTION /= np.linalg.norm(SHOULDER_DIRECTION)
REQUESTED_SPEED = 0.02  # m/s; slow enough to watch conditioning deteriorate
ELBOW_PATH_LENGTH = 0.2006  # m; finishes about 1 degree past straight
SHOULDER_PATH_LENGTH = 0.242  # m; crosses the near-singular region
COMPLETION_ALLOWANCE = 3.0  # s; brief feedback-only finish after path motion
TARGET_TOLERANCE = 0.005  # m; precise relative to the 18-22 mm endpoint markers
ELBOW_CONDITION_THRESHOLD = 200.0
SHOULDER_CONDITION_THRESHOLD = 500.0
SHOULDER_BRANCH_SPEED = 5.0  # rad/s along the weak direction before limiting
DAMPING = 0.05
MAX_COMMANDED_JOINT_RATE = 3.00  # rad/s; below the Webots model's 3.14 limit
TRACKING_GAIN = 2.0  # 1/s; proportional pose-error correction
MOVE_DURATION = 2.5  # s; short reset between trials
SETTLE_DURATION = 0.25  # s
BOTTOM_PRIMARY_FONT = 0.075
BOTTOM_SECONDARY_FONT = BOTTOM_PRIMARY_FONT
BOTTOM_TEXT_COLOR = 0xFFF1A8
BOTTOM_SECONDARY_COLOR = 0xD00000
CORE_IDEA_TEXT = "SINGULARITY: SMALL CARTESIAN MOTION = LARGE JOINT MOTION"
CORE_IDEA_COLOR = 0x7A2600
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


def show_core_idea(enabled=True):
    """Show the central physical meaning only during singularity trials."""
    if enabled:
        robot.setLabel(
            6, CORE_IDEA_TEXT, 0.02, 0.105, 0.06,
            CORE_IDEA_COLOR, 0.0, "Arial"
        )
    else:
        robot.setLabel(6, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")


def show_preparing_label(label, pose_name):
    show_core_idea()
    robot.setLabel(0, label, 0.02, 0.02, 0.065, 0x102030, 0.0, "Arial")
    robot.setLabel(
        1, f"MOVING TO THE {pose_name} START POSE", 0.02, 0.18, 0.06,
        0x087830, 0.0, "Arial"
    )
    for label_id in (2, 3, 4, 5, 7):
        robot.setLabel(label_id, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")


def show_trial_label(
        label, sigma_min, condition_number, configuration_text, request_text,
        show_banner):
    show_core_idea(show_banner)
    robot.setLabel(0, label, 0.02, 0.02, 0.065, 0x102030, 0.0, "Arial")
    status_y = 0.18 if show_banner else 0.115
    metrics_y = 0.255 if show_banner else 0.205
    request_y = 0.325 if show_banner else 0.275
    robot.setLabel(
        1,
        ">>> WELL-CONDITIONED START POSE <<<",
        0.02,
        status_y,
        0.06,
        0x087830,
        0.0,
        "Arial",
    )
    robot.setLabel(
        2,
        (f"START: sigma_min={sigma_min:.3f} | condition={condition_number:.1f} | "
         f"{configuration_text}"),
        0.02,
        metrics_y,
        0.05,
        0x202020,
        0.0,
        "Arial",
    )
    robot.setLabel(
        3,
        request_text,
        0.02,
        request_y,
        0.05,
        0x5C4800,
        0.0,
        "Arial",
    )
    for label_id in (4, 5, 7):
        robot.setLabel(label_id, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")


def show_singularity_checkpoint(
        family, sigma_min, condition_number, configuration_text,
        peak_applied_rate, peak_raw_rate):
    """Replace the compact HUD with the metrics at the singularity threshold."""
    show_core_idea()
    robot.setLabel(
        1, f">>> {family.upper()} SINGULARITY THRESHOLD REACHED <<<",
        0.02, 0.18, 0.065,
        0xD00000, 0.0, "Arial"
    )
    robot.setLabel(
        2,
        (f"NOW: sigma_min={sigma_min:.4f} | condition={condition_number:.0f} | "
         f"{configuration_text}"),
        0.02, 0.255, 0.05, 0x202020, 0.0, "Arial"
    )
    robot.setLabel(
        3,
        (f"PEAK RAW REQUEST = {peak_raw_rate:.2f} rad/s | "
         f"PEAK AFTER LIMIT = {peak_applied_rate:.2f} rad/s"),
        0.02, 0.325, 0.052, 0xD00000, 0.0, "Arial"
    )


def show_approach_result(
        family, sigma_min, condition_number, configuration_text,
        peak_applied_rate, peak_raw_rate, reached_target):
    """Show the final near-singular metrics without adding more overlay lines."""
    status = (
        f">>> {family.upper()} NEAR-SINGULAR ENDPOINT REACHED <<<"
        if reached_target else
        f">>> {family.upper()} APPROACH ENDED - TARGET NOT REACHED <<<"
    )
    show_core_idea()
    robot.setLabel(
        1, status, 0.02, 0.18, 0.06,
        0xD00000, 0.0, "Arial"
    )
    robot.setLabel(
        2,
        (f"END: sigma_min={sigma_min:.4f} | condition={condition_number:.0f} | "
         f"{configuration_text}"),
        0.02, 0.255, 0.05, 0x202020, 0.0, "Arial"
    )
    robot.setLabel(
        3,
        (f"PEAK RAW REQUEST = {peak_raw_rate:.2f} rad/s | "
         f"PEAK AFTER LIMIT = {peak_applied_rate:.2f} rad/s"),
        0.02, 0.325, 0.052, 0xD00000, 0.0, "Arial"
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


def wait_for_space(q, message, hint="", extra_hint=""):
    """Hold the robot until the student presses Space in the 3D view."""
    robot.setLabel(
        7, extra_hint, 0.02, 0.70, 0.06,
        BOTTOM_TEXT_COLOR, 0.0, "Arial"
    )
    robot.setLabel(
        4, message, 0.02, 0.80, BOTTOM_PRIMARY_FONT,
        BOTTOM_TEXT_COLOR, 0.0, "Arial"
    )
    robot.setLabel(
        5, hint, 0.02, 0.90, BOTTOM_SECONDARY_FONT,
        BOTTOM_SECONDARY_COLOR, 0.0, "Arial"
    )
    if extra_hint:
        print(extra_hint)
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
                robot.setLabel(7, "", 0, 0, 0.01, 0x000000, 0.0, "Arial")
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


def shoulder_radius(q):
    """Return horizontal distance from the wrist center to the base axis."""
    origins, _, _ = modified_dh_joint_axes(q)
    return float(np.linalg.norm(origins[3, :2]))


def configuration_text(q, family):
    """Return the geometry students should watch for this singularity."""
    if family == "shoulder":
        return f"wrist-center radius={100.0 * shoulder_radius(q):.1f} cm"
    return f"elbow={np.degrees(q[2]):.1f} deg"


def write_rate_plot():
    """Write a dependency-free SVG comparing peak joint rate over time."""
    width, height = 1000, 650
    left, right, top, bottom = 95, 35, 70, 80
    plot_width = width - left - right
    plot_height = height - top - bottom
    default_duration = ELBOW_PATH_LENGTH / REQUESTED_SPEED
    maximum_time = max(
        default_duration,
        max((samples[-1][0] for samples in RATE_HISTORIES.values() if samples),
            default=default_duration),
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
    for index, (name, (event_time, threshold)) in enumerate(
            SINGULARITY_TIMES.items()):
        event_x = x_pixel(event_time)
        svg.extend([
            f'<line x1="{event_x:.1f}" y1="{top}" x2="{event_x:.1f}" '
            f'y2="{height-bottom}" stroke="#d4a500" stroke-width="2" '
            'stroke-dasharray="5 5"/>',
            f'<text x="{event_x+7:.1f}" y="{top+42+18*index}" font-family="Arial" '
            f'font-size="13" fill="#7a5c00">{name}: condition = '
            f'{threshold:.0f}</text>',
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
        path_length, singularity_family=None, condition_threshold=None):
    """Track the line and pause when an approaching trial becomes ill conditioned."""
    nominal_duration = path_length / REQUESTED_SPEED
    q_command = q_start.copy()
    starting_pose = stylus_fk(q_start)
    previous_time = robot.getTime()
    motion_time = 0.0
    peak_raw_rate = 0.0
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
        _, singular_values, v_transpose = np.linalg.svd(J, full_matrices=False)
        sigma_min = float(singular_values[-1])
        condition_number = float(singular_values[0] / sigma_min)

        if motion_time >= nominal_duration:
            target_error = np.linalg.norm(requested_target - current_position)
            if target_error < TARGET_TOLERANCE:
                reached_target = True
                break
            if motion_time >= nominal_duration + COMPLETION_ALLOWANCE:
                break

        # Follow a moving reference on the yellow line. Feedback removes both
        # along-path lag and cross-track error while holding orientation.
        reference_pose = starting_pose.copy()
        reference_distance = min(REQUESTED_SPEED * motion_time, path_length)
        reference_pose[:3, 3] = measured_start + reference_distance * direction
        pose_error = pose_difference(current_pose, reference_pose)
        feedforward_twist = np.zeros(6)
        if motion_time < nominal_duration:
            feedforward_twist[:3] = REQUESTED_SPEED * direction
        if inverse_method == "undamped":
            proposed_qdot = cartesian_path_controller(
                J, pose_error, feedforward_twist, TRACKING_GAIN
            )
        else:
            desired_twist = feedforward_twist + TRACKING_GAIN * pose_error
            proposed_qdot = inverse_rate(J, desired_twist, inverse_method)
        if (singularity_family == "shoulder" and
                condition_number >= SHOULDER_CONDITION_THRESHOLD):
            # At the shoulder singularity, two IK branches meet. Numerical and
            # physics noise can otherwise select either branch from run to run.
            # Orient the weakest joint-space direction toward decreasing joint
            # 1 and require a consistent component along it. Because J maps
            # this direction to almost zero Cartesian motion, the bias selects
            # the visibly large shoulder-rotation branch without changing the
            # requested straight Cartesian path.
            weak_direction = v_transpose[-1].copy()
            if weak_direction[0] > 0.0:
                weak_direction *= -1.0
            weak_component = float(proposed_qdot @ weak_direction)
            proposed_qdot += (
                max(SHOULDER_BRANCH_SPEED, weak_component) - weak_component
            ) * weak_direction
        applied_qdot, safety_scale = rate_limit(proposed_qdot)
        raw_peak = float(np.max(np.abs(proposed_qdot)))
        commanded_peak = float(np.max(np.abs(applied_qdot)))
        peak_raw_rate = max(peak_raw_rate, raw_peak)
        peak_commanded_rate = max(peak_commanded_rate, commanded_peak)
        if singularity_family == "shoulder":
            robot.setLabel(
                4,
                "WATCH: RATE SPIKE, LIMITING, AND LARGE SHOULDER ROTATION",
                0.02, 0.80, BOTTOM_PRIMARY_FONT,
                BOTTOM_TEXT_COLOR, 0.0, "Arial"
            )
        robot.setLabel(
            5,
            (f"CURRENT = {commanded_peak:.2f} | PEAK RAW = {peak_raw_rate:.2f} | "
             f"PEAK LIMITED = {peak_commanded_rate:.2f} rad/s"),
            0.02, 0.90, BOTTOM_SECONDARY_FONT,
            BOTTOM_SECONDARY_COLOR, 0.0, "Arial",
        )

        if (singularity_family is not None and singularity_time is None and
                condition_number >= condition_threshold):
            singularity_time = motion_time
            print("SINGULARITY CHECKPOINT")
            print(f"  active motion time: {motion_time:.3f} s")
            print(f"  minimum singular value: {sigma_min:.6f}")
            print(f"  condition number: {condition_number:.1f}")
            print(f"  {configuration_text(current_q, singularity_family)}")
            print(f"  peak raw requested joint rate so far: {peak_raw_rate:.3f} rad/s")
            print(f"  peak joint rate after limit so far: {peak_commanded_rate:.3f} rad/s")
            show_singularity_checkpoint(
                singularity_family, sigma_min, condition_number,
                configuration_text(current_q, singularity_family),
                peak_commanded_rate, peak_raw_rate,
            )
        q_command += applied_qdot * dt
        command_joints(q_command)
        update_actual_trace(measured_start)
        rate_history.append((motion_time, commanded_peak))
        minimum_safety_scale = min(minimum_safety_scale, safety_scale)

    return (
        q_command,
        peak_raw_rate,
        peak_commanded_rate,
        minimum_safety_scale,
        reached_target,
        rate_history,
        singularity_time,
    )


def run_trial(
        label, q_pose, direction, path_length, inverse_method,
        singularity_family=None, condition_threshold=None, next_hint="",
        reposition=True):
    print(f"\n=== {label} ===")
    if reposition:
        print("Moving to the test pose...")
        pose_name = "SHOULDER-TEST" if singularity_family == "shoulder" else "BENT-ELBOW"
        show_preparing_label(label, pose_name)
        move_smoothly(q_pose, MOVE_DURATION)
    else:
        print("The world starts at the bent-elbow Trial 1 pose.")
    hold(q_pose, SETTLE_DURATION)

    q_start = measured_joints()
    J = analytic_jacobian(q_start, endpoint_fk=stylus_fk)
    singular_values = np.linalg.svd(J, compute_uv=False)
    sigma_min = float(singular_values[-1])
    condition_number = float(singular_values[0] / sigma_min)

    desired_twist = np.zeros(6)
    desired_twist[:3] = REQUESTED_SPEED * direction

    undamped_qdot = cartesian_path_controller(
        J, np.zeros(6), desired_twist, TRACKING_GAIN
    )
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
    requested_translation = path_length * direction
    requested_target = measured_start + requested_translation
    show_request(measured_start, requested_target)
    geometry_family = singularity_family or "elbow"
    if singularity_family == "shoulder":
        request_text = (
            f"{100 * path_length:.1f} cm THROUGH SHOULDER REGION | undamped inverse"
        )
    elif singularity_family == "elbow":
        request_text = (
            f"{100 * path_length:.0f} cm TOWARD STRAIGHT ELBOW | undamped inverse"
        )
    else:
        request_text = (
            f"{100 * path_length:.0f} cm AWAY FROM STRAIGHT ELBOW | undamped inverse"
        )
    show_trial_label(
        label, sigma_min, condition_number,
        configuration_text(q_start, geometry_family), request_text,
        singularity_family is not None,
    )
    if singularity_family == "elbow":
        wait_for_space(
            q_start,
            "WATCH: CURRENT AND PEAK JOINT RATES RISE NEAR THE GREEN TARGET",
            "MOTION WILL NOT PAUSE | PRESS SPACE TO RUN TRIAL 2",
            "ELBOW STRAIGHTENS; sigma_min FALLS AND CONDITION NUMBER RISES",
        )
    elif singularity_family == "shoulder":
        wait_for_space(
            q_start,
            "WATCH: RAW RATE SPIKES AS THE WRIST CENTER CROSSES THE BASE AXIS",
            "3 rad/s LIMIT CAUSES JERK + LARGE SHOULDER TURN | PRESS SPACE TO RUN",
            "FIRST HALF APPROACHES THE AXIS; SECOND HALF CROSSES AND MOVES AWAY",
        )
    else:
        wait_for_space(
            q_start,
            "PRESS SPACE TO RUN THIS TRIAL",
            (
                (f"WATCH {singularity_family.upper()} SINGULARITY; PAUSE AT "
                 f"CONDITION {condition_threshold:.0f}")
                if singularity_family is not None
                else "BASELINE MOVES AWAY FROM THE SINGULARITY"
            ),
        )
    robot.setLabel(
        4,
        (f"RUNNING TOWARD {singularity_family.upper()} SINGULARITY - WATCH THE RATE"
         if singularity_family is not None else
         "RUNNING AWAY FROM STRAIGHT ELBOW - MODERATE RATE"),
        0.02,
        0.80,
        BOTTOM_PRIMARY_FONT,
        BOTTOM_TEXT_COLOR,
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

    (q_goal, peak_raw_rate, peak_commanded_rate, minimum_safety_scale,
     reached_target, rate_history, singularity_time) = (
        execute_cartesian_motion(
            q_start, direction, inverse_method, measured_start, requested_target,
            path_length, singularity_family, condition_threshold,
        )
    )
    short_label = label.split(":", 1)[0]
    RATE_HISTORIES[short_label] = rate_history
    if singularity_time is not None:
        SINGULARITY_TIMES[short_label] = (
            singularity_time, condition_threshold
        )
    try:
        write_rate_plot()
        print(f"Joint-rate plot saved to: {RATE_PLOT_PATH}")
    except OSError as error:
        print(f"WARNING: could not write joint-rate plot: {error}")
    hold(q_goal, SETTLE_DURATION)
    measured_end = np.array(tool_position.getValues(), dtype=float)
    update_actual_trace(measured_start)
    measured_displacement = measured_end - measured_start
    final_target_error = float(np.linalg.norm(requested_target - measured_end))
    # The joints can finish settling during the short post-motion hold, so use
    # the final measured stylus position for the result shown to students.
    reached_target = reached_target or final_target_error < TARGET_TOLERANCE
    final_q = measured_joints()
    final_singular_values = np.linalg.svd(
        analytic_jacobian(final_q, endpoint_fk=stylus_fk), compute_uv=False
    )
    final_sigma_min = float(final_singular_values[-1])
    final_condition_number = float(final_singular_values[0] / final_sigma_min)
    if singularity_family is not None:
        show_approach_result(
            singularity_family, final_sigma_min, final_condition_number,
            configuration_text(final_q, singularity_family),
            peak_commanded_rate, peak_raw_rate, reached_target,
        )
    print("Webots-measured translation [m]:",
          np.array2string(measured_displacement, precision=4))
    print(f"Measured translation magnitude: {np.linalg.norm(measured_displacement):.4f} m")
    print(f"Peak raw requested joint rate during trial: {peak_raw_rate:.3f} rad/s")
    print(f"Peak joint rate after limit during trial: {peak_commanded_rate:.3f} rad/s")
    print(f"Minimum safety scale during trial: {minimum_safety_scale:.3f}")
    print(f"Final minimum singular value: {final_sigma_min:.6f}")
    print(f"Final condition number: {final_condition_number:.1f}")
    print(f"Final {configuration_text(final_q, geometry_family)}")
    print(
        f"Final target error: {1000.0 * final_target_error:.1f} mm "
        f"(success tolerance: {1000.0 * TARGET_TOLERANCE:.1f} mm)"
    )
    print("Target reached:", "YES" if reached_target else "NO (completion allowance ended)")
    if not reached_target:
        print("The finite joint-rate limit prevented full tracking before the completion allowance ended.")
    if next_hint:
        result_y = 0.18 if singularity_family is not None else 0.115
        rate_y = 0.325 if singularity_family is not None else 0.275
        robot.setLabel(
            1, f">>> {short_label} COMPLETE - RECORD THE RESULT <<<",
            0.02, result_y, 0.06, 0x087830, 0.0, "Arial",
        )
        robot.setLabel(
            3,
            (f"PEAK RAW REQUEST = {peak_raw_rate:.2f} rad/s | "
             f"PEAK AFTER LIMIT = {peak_commanded_rate:.2f} rad/s"),
            0.02, rate_y, 0.052, 0xD00000, 0.0, "Arial",
        )
        wait_for_space(
            q_goal,
            "PRESS SPACE TO MOVE TO THE NEXT TRIAL",
            next_hint,
        )


step_or_exit()
print("[LAB 4 SINGULARITY DEMONSTRATION]")
print("Trial 1 is a baseline. Trial 2 approaches an elbow singularity.")
print("Trial 3 crosses a shoulder-singular region with the elbow still bent.")
run_trial(
    "TRIAL 1: MOVE AWAY / UNDAMPED BASELINE",
    ELBOW_START_Q,
    AWAY_FROM_SINGULARITY,
    ELBOW_PATH_LENGTH,
    "undamped",
    next_hint="NEXT: TRIAL 2 APPROACHES AN ELBOW SINGULARITY",
    reposition=False,
)
run_trial(
    "TRIAL 2: APPROACH ELBOW SINGULARITY / UNDAMPED",
    ELBOW_START_Q,
    TOWARD_SINGULARITY,
    ELBOW_PATH_LENGTH,
    "undamped",
    singularity_family="elbow",
    condition_threshold=ELBOW_CONDITION_THRESHOLD,
    next_hint="NEXT: TRIAL 3 APPROACHES A SHOULDER SINGULARITY",
)
run_trial(
    "TRIAL 3: APPROACH SHOULDER SINGULARITY / UNDAMPED",
    SHOULDER_START_Q,
    SHOULDER_DIRECTION,
    SHOULDER_PATH_LENGTH,
    "undamped",
    singularity_family="shoulder",
    condition_threshold=SHOULDER_CONDITION_THRESHOLD,
)

print("\n[DEMONSTRATION COMPLETE]")
print("Compare the baseline with the elbow and shoulder singularity trials.")
print(f"Joint-rate comparison plot: {RATE_PLOT_PATH}")
print("Reset Webots to run the demonstration again.")

q_hold = measured_joints()
while robot.step(time_step) != -1:
    command_joints(q_hold)
