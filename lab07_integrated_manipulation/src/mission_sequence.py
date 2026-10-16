#!/usr/bin/env python3
"""Provided state-machine mechanics for the integrated manipulation project."""

from dataclasses import dataclass
from enum import Enum, auto
import numpy as np


class MissionState(Enum):
    HOME = auto()
    PREGRASP = auto()
    GRASP = auto()
    TRANSPORT = auto()
    PLACE = auto()
    RETURN_HOME = auto()
    COMPLETE = auto()
    SAFE_ABORT = auto()


STATE_ORDER = (
    MissionState.HOME,
    MissionState.PREGRASP,
    MissionState.GRASP,
    MissionState.TRANSPORT,
    MissionState.PLACE,
    MissionState.RETURN_HOME,
    MissionState.COMPLETE,
)


@dataclass
class MissionContext:
    state: MissionState = MissionState.HOME
    state_started_s: float = 0.0
    failure_reason: str = ""


def validate_segment(plan, collision_checker, lower_limits, upper_limits):
    """Reject limit violations and colliding edges before execution."""
    plan = np.asarray(plan, dtype=float)
    lower_limits = np.asarray(lower_limits, dtype=float)
    upper_limits = np.asarray(upper_limits, dtype=float)
    if plan.ndim != 2 or plan.shape[1:] != lower_limits.shape:
        raise ValueError("plan must contain joint vectors matching the limits")
    if np.any(plan < lower_limits) or np.any(plan > upper_limits):
        raise ValueError("planned configuration violates a joint limit")
    for start, goal in zip(plan[:-1], plan[1:]):
        if collision_checker(start, goal):
            raise ValueError("planned edge is in collision")
    return True


def update_mission(context, observation, now_s, services):
    """Advance one state using project-supplied guards and actions."""
    if context.state in (MissionState.COMPLETE, MissionState.SAFE_ABORT):
        return context

    timeout_s = float(services["timeout_s"](context.state))
    if now_s - context.state_started_s > timeout_s:
        services["safe_hold"]()
        context.state = MissionState.SAFE_ABORT
        context.failure_reason = f"timeout in {context.state.name}"
        return context

    failure = services["failure_reason"](context.state, observation)
    if failure:
        services["safe_hold"]()
        context.state = MissionState.SAFE_ABORT
        context.failure_reason = str(failure)
        return context

    if services["state_complete"](context.state, observation):
        index = STATE_ORDER.index(context.state)
        context.state = STATE_ORDER[index + 1]
        context.state_started_s = now_s
        services["enter_state"](context.state)
    return context
