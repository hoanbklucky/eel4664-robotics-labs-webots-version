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


if __name__ == "__main__":
    save_linear_vs_cubic()
    save_duration_scaling()
