#!/usr/bin/env python3
"""Print Lab 2 FK predictions for the three experiment configurations."""

import numpy as np

from ur5e_fk_starter import T_6_TOOL, forward_kinematics


POSES = {
    "A": np.array([0.0, -1.20, 1.20, -1.50, -1.57, 0.0]),
    "B": np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30]),
    "C": np.array([-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]),
}


def main():
    print("Predicted Webots tool positions from your forward kinematics:")
    for label, q_goal in POSES.items():
        try:
            T_predicted = forward_kinematics(q_goal) @ T_6_TOOL
        except NotImplementedError as error:
            print("[STOP] Complete the two marked modified-DH entries first.")
            print(f"       {error}")
            return 1
        position = T_predicted[:3, 3]
        print(f"Pose {label}: {np.array2string(position, precision=6)} m")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())