#!/usr/bin/env python3
"""Generate the 2R Jacobian-column schematic used by the Lab 4 background."""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUTPUT = Path(__file__).resolve().parent / "planar_2r_jacobian_columns.png"
LINK_1 = "#334155"
LINK_2 = "#2563EB"
COLUMN_1 = "#059669"
COLUMN_2 = "#D97706"
LOST = "#DC2626"


def endpoint_and_columns(length_1, length_2, theta_1, theta_2):
    elbow = np.array([
        length_1 * np.cos(theta_1),
        length_1 * np.sin(theta_1),
    ])
    endpoint = elbow + np.array([
        length_2 * np.cos(theta_1 + theta_2),
        length_2 * np.sin(theta_1 + theta_2),
    ])
    column_1 = np.array([
        -length_1 * np.sin(theta_1) - length_2 * np.sin(theta_1 + theta_2),
        length_1 * np.cos(theta_1) + length_2 * np.cos(theta_1 + theta_2),
    ])
    column_2 = np.array([
        -length_2 * np.sin(theta_1 + theta_2),
        length_2 * np.cos(theta_1 + theta_2),
    ])
    return elbow, endpoint, column_1, column_2


def draw_arm(axis, theta_1, theta_2, title, singular=False):
    elbow, endpoint, column_1, column_2 = endpoint_and_columns(
        4.0, 3.0, theta_1, theta_2
    )
    axis.plot([0.0, elbow[0]], [0.0, elbow[1]], color=LINK_1, linewidth=5)
    axis.plot([elbow[0], endpoint[0]], [elbow[1], endpoint[1]], color=LINK_2, linewidth=5)
    axis.scatter([0.0, elbow[0], endpoint[0]], [0.0, elbow[1], endpoint[1]],
                 s=[55, 55, 75], color=[LINK_1, LINK_1, LINK_2], zorder=3)

    arrow_scale = 0.32
    axis.arrow(endpoint[0], endpoint[1], *(arrow_scale * column_1),
               color=COLUMN_1, width=0.035, head_width=0.24,
               length_includes_head=True, label="Column 1")
    axis.arrow(endpoint[0], endpoint[1], *(arrow_scale * column_2),
               color=COLUMN_2, width=0.035, head_width=0.24,
               length_includes_head=True, label="Column 2")

    axis.text(endpoint[0] + arrow_scale * column_1[0],
              endpoint[1] + arrow_scale * column_1[1] + 0.18,
              "J column 1", color=COLUMN_1, ha="center")
    axis.text(endpoint[0] + arrow_scale * column_2[0],
              endpoint[1] + arrow_scale * column_2[1] - 0.32,
              "J column 2", color=COLUMN_2, ha="center")

    if singular:
        axis.annotate("lost instantaneous x direction", xy=(endpoint[0], endpoint[1]),
                      xytext=(2.2, -1.2), color=LOST,
                      arrowprops={"arrowstyle": "-|>", "color": LOST, "lw": 2})
        axis.text(3.6, 1.15, "columns are parallel", color=LOST, ha="center")
    else:
        axis.text(1.6, -1.1, "independent column directions", color=COLUMN_1)

    axis.set_title(title)
    axis.set_xlabel("x")
    axis.set_ylabel("y")
    axis.set_aspect("equal", adjustable="box")
    axis.set_xlim(-1.6, 8.2)
    axis.set_ylim(-1.6, 7.8)
    axis.grid(True, alpha=0.25)
    axis.spines[["top", "right"]].set_visible(False)


figure, axes = plt.subplots(1, 2, figsize=(11.5, 5.2))
draw_arm(
    axes[0],
    np.deg2rad(30.0),
    np.deg2rad(60.0),
    "Bent configuration: two independent velocity directions",
)
draw_arm(
    axes[1],
    0.0,
    0.0,
    "Stretched configuration: one instantaneous direction is lost",
    singular=True,
)
figure.suptitle("Each Jacobian column is the end-effector velocity caused by one joint")
figure.tight_layout()
figure.savefig(OUTPUT, dpi=180, bbox_inches="tight")
plt.close(figure)
