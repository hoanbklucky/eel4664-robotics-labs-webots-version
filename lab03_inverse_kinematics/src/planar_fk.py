#!/usr/bin/env python3
"""Provided planar FK helpers used to demonstrate analytical IK branches."""
import numpy as np


def planar_2r_fk(q, lengths):
    q, lengths = np.asarray(q, float), np.asarray(lengths, float)
    if q.shape != (2,) or lengths.shape != (2,) or np.any(lengths <= 0):
        raise ValueError("expected two joints and two positive link lengths")
    q1, q2 = q
    l1, l2 = lengths
    return np.array([l1*np.cos(q1)+l2*np.cos(q1+q2),
                     l1*np.sin(q1)+l2*np.sin(q1+q2)])


def planar_3r_fk(q, lengths):
    q, lengths = np.asarray(q, float), np.asarray(lengths, float)
    if q.shape != (3,) or lengths.shape != (3,) or np.any(lengths <= 0):
        raise ValueError("expected three joints and three positive link lengths")
    angles = np.cumsum(q)
    position = np.array([np.sum(lengths*np.cos(angles)), np.sum(lengths*np.sin(angles))])
    return np.r_[position, angles[-1]]


if __name__ == "__main__":
    print(planar_3r_fk(np.deg2rad([20, -30, 15]), [0.5, 0.4, 0.2]))