#!/usr/bin/env python3
"""Scaffold for reproducible matched-condition tracking trials."""

from dataclasses import dataclass


@dataclass(frozen=True)
class TrialConfig:
    condition: str
    kp: float
    kd: float
    ki: float
    duration_s: float
    command_limit: float


def validate_config(config):
    """Reject incomplete or unsafe experiment metadata before motion."""
    if not config.condition.strip():
        raise ValueError("condition label is required")
    if config.duration_s <= 0 or config.command_limit <= 0:
        raise ValueError("duration and command limit must be positive")


def run_trial(adapter, reference, controller, estimator, config):
    """Run one reset-state trial and return raw, analysis-ready rows."""
    validate_config(config)
    # TODO: log time, q_des, q, raw/filtered velocity, error, command,
    # gains, and condition. Enforce timeout, saturation, and safe hold.
    raise NotImplementedError


def require_matched_trials(a, b):
    """Check that only the approved dynamic condition differs."""
    # TODO: verify reference, gains, limits, and controlled variables match.
    raise NotImplementedError
