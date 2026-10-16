#!/usr/bin/env python3
"""Provided configuration-space edge checking and waypoint-planning helpers."""

import numpy as np


def configuration_in_collision(q, link_segments_fn, obstacles, segment_collision_fn):
    """Return True when any robot link segment intersects an obstacle."""
    segments = link_segments_fn(np.asarray(q, dtype=float))
    return any(
        segment_collision_fn(segment, obstacle)
        for segment in segments
        for obstacle in obstacles
    )


def interpolate_edge(q0, q1, resolution=0.02):
    """Sample a joint-space edge, including both endpoints."""
    q0 = np.asarray(q0, dtype=float)
    q1 = np.asarray(q1, dtype=float)
    if q0.shape != q1.shape or q0.ndim != 1:
        raise ValueError("q0 and q1 must be matching joint vectors")
    if resolution <= 0:
        raise ValueError("resolution must be positive")
    steps = max(1, int(np.ceil(np.max(np.abs(q1 - q0)) / resolution)))
    fractions = np.linspace(0.0, 1.0, steps + 1)[:, None]
    return q0 + fractions * (q1 - q0)


def edge_in_collision(q0, q1, collision_fn, resolution=0.02):
    """Check every sampled configuration on an edge."""
    return any(collision_fn(q) for q in interpolate_edge(q0, q1, resolution))


def plan(q_start, q_goal, collision_fn, waypoint_candidates, resolution=0.02):
    """Try the direct edge, then supplied candidate one-waypoint paths."""
    q_start = np.asarray(q_start, dtype=float)
    q_goal = np.asarray(q_goal, dtype=float)
    if not edge_in_collision(q_start, q_goal, collision_fn, resolution):
        return np.asarray([q_start, q_goal])
    for waypoint in waypoint_candidates:
        waypoint = np.asarray(waypoint, dtype=float)
        if (
            not edge_in_collision(q_start, waypoint, collision_fn, resolution)
            and not edge_in_collision(waypoint, q_goal, collision_fn, resolution)
        ):
            return np.asarray([q_start, waypoint, q_goal])
    raise RuntimeError("no collision-free direct or one-waypoint path was found")
