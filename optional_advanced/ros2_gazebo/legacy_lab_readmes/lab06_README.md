# Lab 06 — Jacobian and Differential Kinematics

## Purpose

Derive and implement a manipulator Jacobian. Verify it with finite differences, test `dx ≈ J dq`, and use a pseudoinverse to compute joint velocity for a requested Cartesian velocity.

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
