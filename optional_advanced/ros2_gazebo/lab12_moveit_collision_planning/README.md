# Lab 12 — MoveIt 2 and Collision-Aware Planning

## Purpose

Launch the UR5e with MoveIt, use the RViz Motion Planning interface, add an obstacle, demonstrate collision-aware planning, and compare planning requests using a quantitative criterion. Explain what MoveIt automates that earlier labs implemented manually.

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
