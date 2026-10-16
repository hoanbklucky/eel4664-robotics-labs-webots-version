#!/usr/bin/env python3
"""Provided matched-condition experiment loop for Lab 6."""

from dataclasses import asdict, dataclass
import numpy as np


@dataclass(frozen=True)
class TrialConfig:
    condition: str
    kp: float
    kd: float
    ki: float
    duration_s: float
    command_limit: float


def validate_config(config):
    if not config.condition.strip():
        raise ValueError("condition label is required")
    if config.duration_s <= 0 or config.command_limit <= 0:
        raise ValueError("duration and command limit must be positive")


def run_trial(adapter, reference, controller, estimator, config):
    """Run one reset-state trial through small supplied interfaces."""
    validate_config(config)
    start = adapter.get_time()
    rows = []
    while adapter.step():
        elapsed = adapter.get_time() - start
        if elapsed > config.duration_s:
            break
        q_des, qd_des = reference(elapsed)
        q = float(adapter.read_position())
        qd_est = float(estimator.update(q, adapter.get_time()))
        command = float(controller.update(q_des, qd_des, q, qd_est))
        command = float(np.clip(command, -config.command_limit, config.command_limit))
        adapter.command_effort(command)
        rows.append({
            "time": adapter.get_time(),
            "q_des": q_des,
            "qd_des": qd_des,
            "q": q,
            "qd_est": qd_est,
            "error": q_des - q,
            "command": command,
            **asdict(config),
        })
    adapter.safe_hold()
    return rows


def require_matched_trials(a, b):
    """Verify that only the approved condition label differs."""
    comparable = ("kp", "kd", "ki", "duration_s", "command_limit")
    differences = [name for name in comparable if getattr(a, name) != getattr(b, name)]
    if differences:
        raise ValueError("trials are not matched: " + ", ".join(differences))
    if a.condition == b.condition:
        raise ValueError("condition labels must differ")
    return True
