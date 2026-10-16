#!/usr/bin/env python3
"""Provided execution loop; hardware-specific details live in the adapter."""


def run_trajectory(adapter, trajectory, duration_s):
    """Execute a trajectory using Webots simulation time and return log rows."""
    if duration_s <= 0:
        raise ValueError("duration_s must be positive")
    start = adapter.get_time()
    rows = []
    while adapter.step():
        elapsed = adapter.get_time() - start
        q_des, qd_des, qdd_des = trajectory(min(elapsed, duration_s))
        adapter.command_positions(q_des)
        rows.append({
            "time": adapter.get_time(),
            "q_des": q_des.copy(),
            "qd_des": qd_des.copy(),
            "qdd_des": qdd_des.copy(),
            "q_measured": adapter.read_joint_positions().copy(),
        })
        if elapsed >= duration_s:
            break
    adapter.command_positions(trajectory(duration_s)[0])
    return rows
