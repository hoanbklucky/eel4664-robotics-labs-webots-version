#!/usr/bin/env python3
"""Explicit state-machine scaffold for the pick-and-place mission."""

from dataclasses import dataclass
from enum import Enum, auto


class MissionState(Enum):
    HOME = auto()
    PREGRASP = auto()
    GRASP = auto()
    TRANSPORT = auto()
    PLACE = auto()
    RETURN_HOME = auto()
    COMPLETE = auto()
    SAFE_ABORT = auto()


@dataclass
class MissionContext:
    state: MissionState = MissionState.HOME
    state_started_s: float = 0.0
    failure_reason: str = ""


def validate_segment(plan, collision_checker, limits):
    """Reject an unsafe segment before it reaches the Webots adapter."""
    # TODO: check every edge, limits, IK continuity, and clearance.
    raise NotImplementedError


def update_mission(context, observation, now_s, services):
    """Advance one state using explicit guards, timeouts, and safe failures."""
    # TODO: implement home -> pregrasp -> grasp/equivalent -> transport ->
    # place -> return-home. Unsafe plans and timeouts enter SAFE_ABORT.
    raise NotImplementedError
