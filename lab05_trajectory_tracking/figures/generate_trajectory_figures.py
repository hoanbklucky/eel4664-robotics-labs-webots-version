#!/usr/bin/env python3
"""Generate the explanatory trajectory figures used by Lab 5."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent
BLUE = "#2563EB"
ORANGE = "#D97706"
GRAY = "#64748B"
GREEN = "#16833B"


def style_axes(axes):
    for axis in axes:
        axis.grid(True, alpha=0.25)
        axis.spines[["top", "right"]].set_visible(False)


def save_linear_vs_cubic():
    time = np.linspace(-0.15, 1.15, 1001)
    inside = (time >= 0.0) & (time <= 1.0)
    progress = np.clip(time, 0.0, 1.0)

    linear_position = progress
    cubic_position = 3.0 * progress**2 - 2.0 * progress**3
    linear_velocity = np.where(inside, 1.0, 0.0)
    cubic_velocity = np.where(inside, 6.0 * progress - 6.0 * progress**2, 0.0)
    cubic_acceleration = np.where(inside, 6.0 - 12.0 * progress, 0.0)

    figure, axes = plt.subplots(3, 1, figsize=(8.2, 7.8), sharex=True)
    style_axes(axes)

    axes[0].plot(time, linear_position, color=ORANGE, linestyle="--", label="Linear")
    axes[0].plot(time, cubic_position, color=BLUE, label="Cubic rest-to-rest")
    axes[0].set_ylabel("Position / total move")
    axes[0].legend(loc="upper left")

    axes[1].plot(time, linear_velocity, color=ORANGE, linestyle="--", label="Linear")
    axes[1].plot(time, cubic_velocity, color=BLUE, label="Cubic rest-to-rest")
    axes[1].set_ylabel("Normalized velocity")
    axes[1].annotate("instantaneous jump", xy=(0.0, 1.0), xytext=(0.11, 1.25),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)

    axes[2].plot(time, np.zeros_like(time), color=ORANGE, linestyle="--",
                 label="Linear: zero only between jumps")
    axes[2].plot(time, cubic_acceleration, color=BLUE, label="Cubic")
    axes[2].axvline(0.0, color=ORANGE, linewidth=2.0, alpha=0.75)
    axes[2].axvline(1.0, color=ORANGE, linewidth=2.0, alpha=0.75)
    axes[2].annotate("ideal acceleration impulses", xy=(0.0, 4.8), xytext=(0.12, 3.7),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axes[2].set_ylabel("Normalized acceleration")
    axes[2].set_xlabel("Normalized physical time, t / Tf")

    for axis in axes:
        axis.axvline(0.0, color=GRAY, linewidth=0.8, alpha=0.5)
        axis.axvline(1.0, color=GRAY, linewidth=0.8, alpha=0.5)

    figure.suptitle("Linear interpolation starts abruptly; a cubic starts and ends at rest")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "linear_vs_cubic.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def cubic_motion(time, duration):
    progress = np.clip(time / duration, 0.0, 1.0)
    active = (time >= 0.0) & (time <= duration)
    position = 3.0 * progress**2 - 2.0 * progress**3
    velocity = np.where(active, (6.0 * progress - 6.0 * progress**2) / duration, 0.0)
    acceleration = np.where(active, (6.0 - 12.0 * progress) / duration**2, 0.0)
    return position, velocity, acceleration


def save_duration_scaling():
    time = np.linspace(0.0, 2.0, 1001)
    figure, axes = plt.subplots(3, 1, figsize=(8.2, 7.8), sharex=True)
    style_axes(axes)

    for duration, color, linestyle in [(1.0, ORANGE, "--"), (2.0, BLUE, "-")]:
        position, velocity, acceleration = cubic_motion(time, duration)
        label = f"Tf = {duration:g} s"
        axes[0].plot(time, position, color=color, linestyle=linestyle, label=label)
        axes[1].plot(time, velocity, color=color, linestyle=linestyle, label=label)
        axes[2].plot(time, acceleration, color=color, linestyle=linestyle, label=label)

    axes[0].set_ylabel("Position / total move")
    axes[0].legend(loc="lower right")
    axes[1].set_ylabel("Velocity / total move")
    axes[2].set_ylabel("Acceleration / total move")
    axes[2].set_xlabel("Physical time t (s)")

    axes[1].annotate("peak 1.50", xy=(0.5, 1.5), xytext=(0.62, 1.63),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axes[1].annotate("peak 0.75", xy=(1.0, 0.75), xytext=(1.12, 1.02),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axes[2].annotate("magnitude 6", xy=(0.0, 6.0), xytext=(0.20, 4.5),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axes[2].annotate("magnitude 1.5", xy=(0.0, 1.5), xytext=(0.40, 2.2),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)

    figure.suptitle("Doubling duration halves peak velocity and quarters peak acceleration")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "duration_scaling.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def save_cubic_progress():
    normalized_time = np.linspace(0.0, 1.0, 501)
    path_progress = 3.0 * normalized_time**2 - 2.0 * normalized_time**3

    figure, axis = plt.subplots(figsize=(8.2, 4.8))
    style_axes([axis])
    axis.plot(normalized_time, path_progress, color=BLUE, linewidth=3.0)
    axis.scatter([0.0, 0.5, 1.0], [0.0, 0.5, 1.0], color=ORANGE, zorder=3)
    axis.annotate("start at rest", xy=(0.0, 0.0), xytext=(0.12, 0.12),
                  arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axis.annotate("halfway", xy=(0.5, 0.5), xytext=(0.58, 0.36),
                  arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axis.annotate("finish at rest", xy=(1.0, 1.0), xytext=(0.68, 0.82),
                  arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axis.set_xlim(-0.03, 1.03)
    axis.set_ylim(-0.03, 1.03)
    axis.set_xlabel("Normalized time  s = t / Tf")
    axis.set_ylabel("Path progress  3s² - 2s³")
    axis.set_title("Cubic path progress starts and ends smoothly")
    figure.tight_layout()
    figure.savefig(OUTPUT_DIR / "cubic_progress.png", dpi=180, bbox_inches="tight")
    plt.close(figure)


def save_cubic_derivative_shapes():
    normalized_time = np.linspace(0.0, 1.0, 501)
    velocity_factor = 6.0 * normalized_time - 6.0 * normalized_time**2
    acceleration_factor = 6.0 - 12.0 * normalized_time

    figure, axes = plt.subplots(2, 1, figsize=(8.2, 6.4), sharex=True)
    style_axes(axes)

    axes[0].plot(normalized_time, velocity_factor, color=BLUE, linewidth=3.0)
    axes[0].scatter([0.0, 0.5, 1.0], [0.0, 1.5, 0.0], color=ORANGE, zorder=3)
    axes[0].annotate("maximum = 1.5", xy=(0.5, 1.5), xytext=(0.62, 1.18),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axes[0].set_ylabel(r"Velocity factor  $6s-6s^2$")

    axes[1].plot(normalized_time, acceleration_factor, color=ORANGE, linewidth=3.0)
    axes[1].axhline(0.0, color=GRAY, linewidth=1.0)
    axes[1].scatter([0.0, 0.5, 1.0], [6.0, 0.0, -6.0], color=BLUE, zorder=3)
    axes[1].annotate("sign changes at halfway", xy=(0.5, 0.0),
                     xytext=(0.58, 2.2),
                     arrowprops={"arrowstyle": "->", "color": GRAY}, color=GRAY)
    axes[1].set_ylabel(r"Acceleration factor  $6-12s$")
    axes[1].set_xlabel(r"Normalized time  $s=t/T_f$")

    figure.suptitle("Normalized velocity and acceleration shapes of the cubic")
    figure.tight_layout()
    figure.savefig(
        OUTPUT_DIR / "cubic_velocity_acceleration_shapes.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(figure)


def save_velocity_profile_comparison():
    normalized_time = np.linspace(0.0, 1.0, 1001)
    cubic_velocity = 6.0 * normalized_time - 6.0 * normalized_time**2
    cubic_acceleration = 6.0 - 12.0 * normalized_time
    quintic_velocity = (
        30.0 * normalized_time**2
        - 60.0 * normalized_time**3
        + 30.0 * normalized_time**4
    )
    quintic_acceleration = (
        60.0 * normalized_time
        - 180.0 * normalized_time**2
        + 120.0 * normalized_time**3
    )

    acceleration_fraction = 0.25
    trapezoid_peak = 1.0 / (1.0 - acceleration_fraction)
    trapezoid_velocity = np.piecewise(
        normalized_time,
        [
            normalized_time < acceleration_fraction,
            (normalized_time >= acceleration_fraction)
            & (normalized_time <= 1.0 - acceleration_fraction),
            normalized_time > 1.0 - acceleration_fraction,
        ],
        [
            lambda value: trapezoid_peak * value / acceleration_fraction,
            trapezoid_peak,
            lambda value: trapezoid_peak * (1.0 - value) / acceleration_fraction,
        ],
    )
    trapezoid_acceleration_level = trapezoid_peak / acceleration_fraction
    trapezoid_acceleration = np.piecewise(
        normalized_time,
        [
            normalized_time < acceleration_fraction,
            (normalized_time >= acceleration_fraction)
            & (normalized_time <= 1.0 - acceleration_fraction),
            normalized_time > 1.0 - acceleration_fraction,
        ],
        [trapezoid_acceleration_level, 0.0, -trapezoid_acceleration_level],
    )

    figure, axes = plt.subplots(2, 1, figsize=(8.4, 7.2), sharex=True)
    style_axes(axes)
    velocity_axis, acceleration_axis = axes

    velocity_axis.plot(normalized_time, cubic_velocity, color=BLUE,
                       linewidth=3.0, label="Cubic")
    velocity_axis.plot(normalized_time, quintic_velocity, color="#16833B",
                       linewidth=3.0, label="Quintic")
    velocity_axis.plot(normalized_time, trapezoid_velocity, color=ORANGE,
                       linewidth=3.0, linestyle="--",
                       label="Trapezoidal (25%-50%-25%)")
    velocity_axis.set_ylim(0.0, 2.02)
    velocity_axis.set_ylabel(
        r"Normalized velocity  $(T_f/\Delta\theta)\dot{\theta}$"
    )
    velocity_axis.set_title("Profiles for the same distance and duration")
    velocity_axis.legend(loc="upper right")
    velocity_axis.text(
        0.02,
        0.94,
        "Area under every curve = 1",
        transform=velocity_axis.transAxes,
        color=GRAY,
        va="top",
    )

    acceleration_axis.plot(normalized_time, cubic_acceleration, color=BLUE,
                           linewidth=3.0, label="Cubic")
    acceleration_axis.plot(normalized_time, quintic_acceleration,
                           color="#16833B", linewidth=3.0, label="Quintic")
    acceleration_axis.plot(normalized_time, trapezoid_acceleration,
                           color=ORANGE, linewidth=3.0, linestyle="--",
                           drawstyle="steps-post", label="Trapezoidal")
    acceleration_axis.axhline(0.0, color=GRAY, linewidth=1.0)
    acceleration_axis.set_ylabel(
        r"Normalized acceleration  $(T_f^2/\Delta\theta)\ddot{\theta}$"
    )
    acceleration_axis.set_xlabel(r"Normalized time  $u=t/T_f$")

    for axis in axes:
        axis.axvline(0.25, color=GRAY, linewidth=1.0, alpha=0.5)
        axis.axvline(0.75, color=GRAY, linewidth=1.0, alpha=0.5)
        axis.set_xlim(0.0, 1.0)

    figure.tight_layout()
    figure.savefig(
        OUTPUT_DIR / "velocity_profile_comparison.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(figure)


def save_joint_space_motion():
    normalized_time = np.linspace(0.0, 1.0, 501)
    progress = 3.0 * normalized_time**2 - 2.0 * normalized_time**3

    start_angles = np.deg2rad([15.0, 100.0])
    final_angles = np.deg2rad([95.0, -20.0])
    joint_angles = (
        start_angles[:, None]
        + (final_angles - start_angles)[:, None] * progress
    )

    link_1 = 1.0
    link_2 = 0.75
    q1 = joint_angles[0]
    q2 = joint_angles[1]
    tool_x = link_1 * np.cos(q1) + link_2 * np.cos(q1 + q2)
    tool_y = link_1 * np.sin(q1) + link_2 * np.sin(q1 + q2)

    figure, axes = plt.subplots(1, 2, figsize=(10.2, 4.5))
    style_axes(axes)

    axes[0].plot(normalized_time, np.rad2deg(q1), color=BLUE,
                 linewidth=3.0, label=r"Joint 1, $q_1$")
    axes[0].plot(normalized_time, np.rad2deg(q2), color=ORANGE,
                 linewidth=3.0, label=r"Joint 2, $q_2$")
    axes[0].set_xlabel(r"Normalized time  $u=t/T_f$")
    axes[0].set_ylabel("Joint angle [deg]")
    axes[0].set_title("MoveJ interpolates joint angles")
    axes[0].legend()

    axes[1].plot(tool_x, tool_y, color=BLUE, linewidth=3.0,
                 label="Tool path from FK")
    axes[1].plot([tool_x[0], tool_x[-1]], [tool_y[0], tool_y[-1]],
                 color=GRAY, linewidth=2.0, linestyle="--",
                 label="Straight line between endpoints")
    axes[1].scatter(tool_x[0], tool_y[0], color=GREEN, s=70,
                    zorder=4, label="Start")
    axes[1].scatter(tool_x[-1], tool_y[-1], color="#DC2626", s=70,
                    zorder=4, label="End")
    axes[1].set_xlabel("Tool x position")
    axes[1].set_ylabel("Tool y position")
    axes[1].set_title("The resulting tool path is generally curved")
    axes[1].axis("equal")
    axes[1].legend(fontsize=9)

    figure.tight_layout()
    figure.savefig(
        OUTPUT_DIR / "joint_space_motion.png", dpi=180, bbox_inches="tight"
    )
    plt.close(figure)


def save_cartesian_sampling():
    path_progress = np.linspace(0.0, 1.0, 501)
    start = np.array([0.0, 0.0])
    end = np.array([2.4, 1.2])
    path = start[:, None] + (end - start)[:, None] * path_progress
    waypoint_progress = np.linspace(0.0, 1.0, 9)
    waypoints = start[:, None] + (end - start)[:, None] * waypoint_progress

    time = np.linspace(0.0, 1.0, 1001)
    joint_reference = (
        15.0
        + 55.0 * (3.0 * time**2 - 2.0 * time**3)
        + 7.0 * np.sin(np.pi * time) ** 2
    )
    sample_times = np.linspace(0.0, 1.0, 6)
    sample_angles = (
        15.0
        + 55.0 * (3.0 * sample_times**2 - 2.0 * sample_times**3)
        + 7.0 * np.sin(np.pi * sample_times) ** 2
    )

    figure, axes = plt.subplots(1, 2, figsize=(10.4, 4.4))
    style_axes(axes)

    axes[0].plot(path[0], path[1], color=BLUE, linewidth=3.0,
                 label="Desired Cartesian line")
    axes[0].scatter(waypoints[0], waypoints[1], color=ORANGE, s=55,
                    zorder=4, label="Sampled references")
    axes[0].scatter(start[0], start[1], color=GREEN, s=75, zorder=5)
    axes[0].scatter(end[0], end[1], color="#DC2626", s=75, zorder=5)
    axes[0].set_xlabel("Cartesian x position")
    axes[0].set_ylabel("Cartesian y position")
    axes[0].set_title("MoveL samples one Cartesian path")
    axes[0].axis("equal")
    axes[0].legend()

    axes[1].plot(time, joint_reference, color=BLUE, linewidth=3.0,
                 label="Continuously evaluated reference")
    axes[1].plot(time, np.interp(time, sample_times, sample_angles),
                 color=GREEN, linewidth=2.2, linestyle=":",
                 label="Linear interpolation")
    axes[1].step(sample_times, sample_angles, where="post", color=GRAY,
                 linewidth=2.0, linestyle="--",
                 label="Held command (coarse updates)")
    axes[1].scatter(sample_times, sample_angles, color=ORANGE, s=48,
                    zorder=4, label="Joint angles from IK")
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel(r"Joint angle  $q_j$")
    axes[1].set_title("Joint commands from the Cartesian samples")
    axes[1].legend(fontsize=8.5)

    figure.tight_layout()
    figure.savefig(
        OUTPUT_DIR / "cartesian_waypoints.png", dpi=180, bbox_inches="tight"
    )
    plt.close(figure)


def save_via_point_segments():
    normalized_time = np.linspace(0.0, 1.0, 1201)
    continuous_speed = 6.0 * normalized_time - 6.0 * normalized_time**2
    segment_count = 3
    local_progress = np.mod(normalized_time * segment_count, 1.0)
    local_progress[-1] = 1.0
    stop_at_waypoint_speed = 6.0 * local_progress * (1.0 - local_progress)

    via_times = np.array([0.0, 1.0, 2.0, 3.0])
    via_angles = np.array([0.0, 0.9, -0.25, 1.05])
    via_slopes = np.array([
        0.0,
        (via_angles[2] - via_angles[0]) / (via_times[2] - via_times[0]),
        (via_angles[3] - via_angles[1]) / (via_times[3] - via_times[1]),
        0.0,
    ])

    spline_time_parts = []
    spline_angle_parts = []
    for index in range(len(via_times) - 1):
        t0, t1 = via_times[index:index + 2]
        y0, y1 = via_angles[index:index + 2]
        m0, m1 = via_slopes[index:index + 2]
        segment_time = np.linspace(t0, t1, 151, endpoint=index == len(via_times) - 2)
        duration = t1 - t0
        u = (segment_time - t0) / duration
        h00 = 2.0 * u**3 - 3.0 * u**2 + 1.0
        h10 = u**3 - 2.0 * u**2 + u
        h01 = -2.0 * u**3 + 3.0 * u**2
        h11 = u**3 - u**2
        segment_angle = (
            h00 * y0 + h10 * duration * m0
            + h01 * y1 + h11 * duration * m1
        )
        spline_time_parts.append(segment_time)
        spline_angle_parts.append(segment_angle)

    spline_time = np.concatenate(spline_time_parts)
    spline_angle = np.concatenate(spline_angle_parts)

    figure, axes = plt.subplots(1, 2, figsize=(10.6, 4.5))
    style_axes(axes)

    axes[0].plot(normalized_time, continuous_speed, color=BLUE,
                 linewidth=3.0, label="One continuous path schedule")
    axes[0].plot(normalized_time, stop_at_waypoint_speed, color=ORANGE,
                 linewidth=2.5, linestyle="--",
                 label="Independent rest-to-rest segments")
    for boundary in [1.0 / 3.0, 2.0 / 3.0]:
        axes[0].axvline(boundary, color=GRAY, linewidth=1.0, alpha=0.7)
    axes[0].set_xlim(0.0, 1.0)
    axes[0].set_ylim(bottom=0.0)
    axes[0].set_xlabel(r"Normalized time  $u=t/T_f$")
    axes[0].set_ylabel("Relative path speed")
    axes[0].set_title(
        "Stop at or pass through\nuser-defined via points",
        fontsize=14,
    )
    axes[0].legend(fontsize=8.5)

    axes[1].plot(spline_time, spline_angle, color=BLUE, linewidth=3.0,
                 label="Piecewise cubic trajectory")
    axes[1].scatter(via_times, via_angles, color=ORANGE, s=60,
                    zorder=4, label="User-defined via points")
    for index in [1, 2]:
        axes[1].axvline(via_times[index], color=GRAY, linewidth=1.0,
                        linestyle="--", alpha=0.7)
        tangent_time = np.array([via_times[index] - 0.22,
                                 via_times[index] + 0.22])
        tangent_angle = (
            via_angles[index]
            + via_slopes[index] * (tangent_time - via_times[index])
        )
        axes[1].plot(tangent_time, tangent_angle, color=GREEN,
                     linewidth=2.0)
    axes[1].annotate("same slope from both segments",
                     xy=(1.0, via_angles[1]), xytext=(1.22, 0.67),
                     arrowprops={"arrowstyle": "->", "color": GRAY},
                     color=GRAY, fontsize=9)
    axes[1].set_xlabel("Time")
    axes[1].set_ylabel(r"Joint angle  $q_j$")
    axes[1].set_title(
        "Polynomial segments joined at\nuser-defined via points",
        fontsize=14,
    )
    axes[1].legend(fontsize=8.5, loc="lower right")

    figure.tight_layout()
    figure.savefig(
        OUTPUT_DIR / "via_point_segments.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close(figure)


if __name__ == "__main__":
    save_linear_vs_cubic()
    save_duration_scaling()
    save_cubic_progress()
    save_cubic_derivative_shapes()
    save_velocity_profile_comparison()
    save_joint_space_motion()
    save_cartesian_sampling()
    save_via_point_segments()
