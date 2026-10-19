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
    quintic_velocity = (
        30.0 * normalized_time**2
        - 60.0 * normalized_time**3
        + 30.0 * normalized_time**4
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

    figure, axis = plt.subplots(figsize=(8.2, 4.8))
    style_axes([axis])
    axis.plot(normalized_time, cubic_velocity, color=BLUE, linewidth=3.0,
              label="Cubic")
    axis.plot(normalized_time, quintic_velocity, color="#16833B", linewidth=3.0,
              label="Quintic")
    axis.plot(normalized_time, trapezoid_velocity, color=ORANGE, linewidth=3.0,
              linestyle="--", label="Trapezoidal (25%-50%-25%)")
    axis.axvline(0.25, color=GRAY, linewidth=1.0, alpha=0.6)
    axis.axvline(0.75, color=GRAY, linewidth=1.0, alpha=0.6)
    axis.set_xlim(0.0, 1.0)
    axis.set_ylim(0.0, 2.02)
    axis.set_xlabel(r"Normalized time  $u=t/T_f$")
    axis.set_ylabel(r"Normalized velocity  $(T_f/\Delta\theta)\dot{\theta}$")
    axis.set_title("Velocity profiles for the same distance and duration")
    axis.legend(loc="upper right")
    axis.text(
        0.02,
        0.94,
        "Area under every curve = 1",
        transform=axis.transAxes,
        color=GRAY,
        va="top",
    )
    figure.tight_layout()
    figure.savefig(
        OUTPUT_DIR / "velocity_profile_comparison.png",
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
