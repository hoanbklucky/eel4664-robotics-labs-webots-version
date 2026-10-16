#!/usr/bin/env python3
"""Least-squares parameter fit for Lab 6."""

import numpy as np


def fit_linear_parameter(phi, y):
    phi = np.asarray(phi, dtype=float)
    y = np.asarray(y, dtype=float)
    if phi.ndim == 1:
        phi = phi[:, None]
    if phi.ndim != 2 or y.ndim != 1 or phi.shape[0] != y.size:
        raise ValueError("phi and y have incompatible shapes")
    parameters = None  # TODO 3: np.linalg.lstsq(phi, y, rcond=None)[0]
    if parameters is None:
        raise NotImplementedError("Complete TODO 3: the least-squares solve")
    prediction = phi @ parameters
    residual = y - prediction
    return parameters, prediction, residual
