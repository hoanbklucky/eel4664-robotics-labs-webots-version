# Lab 09 — Manipulator Dynamics

## Purpose

Connect `M(q)qdd + C(q,qd)qd + g(q) = tau` to simulation behavior. Use a simplified dynamics model and design repeatable trials that vary speed and/or payload. Explain which terms dominate in slow motion, rapid acceleration, and static holding.

## Workflow

1. Read the complete lab before coding.
2. Reuse validated functions from earlier labs.
3. Keep frame/kinematic conventions explicit.
4. Run repeatable experiments.
5. Put generated data and figures in `results/`.

## Simulator health check

When Gazebo is required:

```bash
ros2 control list_controllers
ros2 topic list
ros2 action list
```

## Submission

Submit completed source code, `answers.md`, and evidence supporting your analysis.
