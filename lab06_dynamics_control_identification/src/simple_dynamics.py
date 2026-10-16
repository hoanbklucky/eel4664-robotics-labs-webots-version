#!/usr/bin/env python3
"""One-joint inverse-dynamics equation for Lab 6."""

import numpy as np


def one_joint_torque(q, qd, qdd, inertia, damping, gravity_coeff):
    q, qd, qdd = np.broadcast_arrays(q, qd, qdd)
    torque = None  # TODO 1: inertia*qdd + damping*qd + gravity_coeff*np.sin(q)
    if torque is None:
        raise NotImplementedError("Complete TODO 1: the one-joint torque equation")
    return np.asarray(torque, dtype=float)
