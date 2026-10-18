#!/usr/bin/env python3
"""Two-line Cartesian path controller for Lab 4."""

import numpy as np


def cartesian_path_controller(J, pose_error, feedforward_twist, gain):
    """Return the undamped joint rate that tracks a moving Cartesian pose."""
    J = np.asarray(J, dtype=float)
    pose_error = np.asarray(pose_error, dtype=float)
    feedforward_twist = np.asarray(feedforward_twist, dtype=float)
    if J.shape != (6, 6):
        raise ValueError("J must be a 6-by-6 Jacobian")
    if pose_error.shape != (6,) or feedforward_twist.shape != (6,):
        raise ValueError("pose_error and feedforward_twist must have six elements")
    if not np.isfinite(gain) or gain < 0.0:
        raise ValueError("gain must be finite and nonnegative")

    # TODO 1: commanded twist = supplied feedforward twist + gain * pose error
    # TODO 2: solve J @ joint_rate = commanded twist, then return joint_rate
    raise NotImplementedError(
        "Complete the two controller lines using the Lab 4 README hints."
    )
