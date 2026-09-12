#!/usr/bin/env python3
"""Print Lab 2 FK predictions for the three experiment configurations."""

import numpy as np

from ur5e_fk_starter import T_6_TOOL, forward_kinematics


POSES = {
    "A": np.array([0.0, -1.20, 1.20, -1.50, -1.57, 0.0]),
    "B": np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30]),
    "C": np.array([-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]),
}


def rotation_to_rpy(R):
    """Return roll, pitch, yaw for R = Rz(yaw) Ry(pitch) Rx(roll)."""
    R = np.asarray(R, dtype=float)
    horizontal = np.hypot(R[0, 0], R[1, 0])
    pitch = np.arctan2(-R[2, 0], horizontal)
    if horizontal > 1e-9:
        roll = np.arctan2(R[2, 1], R[2, 2])
        yaw = np.arctan2(R[1, 0], R[0, 0])
    else:
        roll = np.arctan2(-R[1, 2], R[1, 1])
        yaw = 0.0
    return np.array([roll, pitch, yaw])


def predicted_tool_pose(q_goal):
    """Return the student's predicted Webots tool transform."""
    return forward_kinematics(q_goal) @ T_6_TOOL


def main():
    print("Predicted Webots tool poses from your forward kinematics:")
    for label, q_goal in POSES.items():
        try:
            T_predicted = predicted_tool_pose(q_goal)
        except NotImplementedError as error:
            print("[STOP] Complete the two marked modified-DH entries first.")
            print(f"       {error}")
            return 1
        position = T_predicted[:3, 3]
        rpy = rotation_to_rpy(T_predicted[:3, :3])
        print(f"Pose {label}")
        print(f"  Position [m]: {np.array2string(position, precision=6)}")
        print(f"  RPY [rad]:    {np.array2string(rpy, precision=6)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())