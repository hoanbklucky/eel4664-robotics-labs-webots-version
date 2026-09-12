#!/usr/bin/env python3
"""Interactively compare Lab 2 FK predictions with Webots measurements."""

import numpy as np

from predict_fk_poses import POSES, predicted_tool_pose, rotation_to_rpy
from transforms import rotx, roty, rotz


def read_vector(prompt, length):
    """Read a comma- or space-separated vector, with optional brackets."""
    while True:
        text = input(prompt).strip().replace("[", " ").replace("]", " ").replace(",", " ")
        try:
            values = np.array([float(item) for item in text.split()], dtype=float)
        except ValueError:
            values = np.array([])
        if values.shape == (length,) and np.all(np.isfinite(values)):
            return values
        print(f"  Please enter exactly {length} finite numbers.")


def orientation_error_degrees(R_predicted, measured_rpy):
    """Return the angle of the relative predicted-to-measured rotation."""
    roll, pitch, yaw = measured_rpy
    R_measured = rotz(yaw) @ roty(pitch) @ rotx(roll)
    R_error = R_predicted.T @ R_measured
    cosine = np.clip((np.trace(R_error) - 1.0) / 2.0, -1.0, 1.0)
    return float(np.rad2deg(np.arccos(cosine)))


def main():
    print("Enter the vectors printed by the Webots fk_experiment controller.")
    print("You may include brackets and commas. Use the documented six-joint order.\n")
    position_errors = []
    orientation_errors = []

    for label, q_goal in POSES.items():
        try:
            T_predicted = predicted_tool_pose(q_goal)
        except NotImplementedError as error:
            print("[STOP] Complete the two marked modified-DH entries first.")
            print(f"       {error}")
            return 1
        p_predicted = T_predicted[:3, 3]
        rpy_predicted = rotation_to_rpy(T_predicted[:3, :3])

        print(f"--- Pose {label} ---")
        print("FK position [m]:", np.array2string(p_predicted, precision=6))
        print("FK RPY [rad]:   ", np.array2string(rpy_predicted, precision=6))
        q_measured = read_vector("Measured q [rad]: ", 6)
        p_measured = read_vector("Webots tool position [m]: ", 3)
        rpy_measured = read_vector("Webots tool RPY [rad]: ", 3)

        tracking_error = float(np.max(np.abs(q_measured - q_goal)))
        position_error = float(1000.0 * np.linalg.norm(p_predicted - p_measured))
        orientation_error = orientation_error_degrees(T_predicted[:3, :3], rpy_measured)
        position_errors.append(position_error)
        orientation_errors.append(orientation_error)

        print(f"Maximum joint tracking error: {tracking_error:.6f} rad")
        print(f"Tool position error:          {position_error:.3f} mm")
        print(f"Tool orientation error:       {orientation_error:.3f} deg\n")

    print("--- Summary ---")
    print(f"Mean position error:         {np.mean(position_errors):.3f} mm")
    print(f"Maximum position error:     {np.max(position_errors):.3f} mm")
    print(f"Mean orientation error:     {np.mean(orientation_errors):.3f} deg")
    print(f"Maximum orientation error:  {np.max(orientation_errors):.3f} deg")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())