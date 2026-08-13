# Lab 10 — Joint-Space Control

## Purpose

Simulate a one-joint plant in Python, implement P and PD control, and quantify rise time, overshoot, settling time, and steady-state error. Relate the experiment to the controllers used by `ros2_control`.

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
