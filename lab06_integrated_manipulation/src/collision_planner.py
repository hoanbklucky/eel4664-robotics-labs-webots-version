#!/usr/bin/env python3
"""Explicit configuration-space collision checking and planning starter."""

def configuration_in_collision(q, obstacles):
    """TODO: use your FK link geometry and return a Boolean."""
    raise NotImplementedError

def edge_in_collision(q0, q1, obstacles, resolution=0.02):
    """TODO: interpolate joint space and check every sample."""
    raise NotImplementedError

def plan(q_start, q_goal, obstacles, rng):
    """TODO: implement the assigned waypoint or sampling planner."""
    raise NotImplementedError
