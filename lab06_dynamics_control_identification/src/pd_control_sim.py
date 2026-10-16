#!/usr/bin/env python3
"""Provided one-joint simulation with one student PD equation."""

import numpy as np


def simulate_pd(kp, kd, q_des, duration=5.0, dt=0.001,
                inertia=1.0, damping=0.1, command_limit=20.0):
    if duration <= 0 or dt <= 0 or inertia <= 0 or command_limit <= 0:
        raise ValueError("duration, dt, inertia, and command_limit must be positive")
    times = np.arange(0.0, duration + dt, dt)
    q = np.zeros_like(times)
    qd = np.zeros_like(times)
    torque = np.zeros_like(times)

    for index in range(times.size - 1):
        error = q_des - q[index]
        velocity_error = -qd[index]
        command = None  # TODO 2: kp*error + kd*velocity_error
        if command is None:
            raise NotImplementedError("Complete TODO 2: the PD torque equation")
        torque[index] = np.clip(command, -command_limit, command_limit)
        qdd = (torque[index] - damping * qd[index]) / inertia
        qd[index + 1] = qd[index] + qdd * dt
        q[index + 1] = q[index] + qd[index + 1] * dt

    torque[-1] = torque[-2]
    return times, q, qd, torque
