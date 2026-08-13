# Lab 08 — Trajectory Generation

## Purpose

Derive cubic trajectory coefficients, optionally extend to quintic interpolation, plot position/velocity/acceleration, then execute sampled waypoints using `FollowJointTrajectory`. Compare commanded and measured joint motion.

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
