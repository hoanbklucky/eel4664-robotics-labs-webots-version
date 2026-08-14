#!/usr/bin/env python3
"""Planar FK warm-ups used to verify analytical IK branches."""
import numpy as np


def planar_2r_fk(q, lengths):
    """Return [x, y] for two revolute joints; student implementation."""
    raise NotImplementedError


def planar_3r_fk(q, lengths):
    """Return [x, y, phi] for three revolute joints; student implementation."""
    raise NotImplementedError


if __name__ == "__main__":
    print(planar_3r_fk(np.deg2rad([20, -30, 15]), [0.5, 0.4, 0.2]))
