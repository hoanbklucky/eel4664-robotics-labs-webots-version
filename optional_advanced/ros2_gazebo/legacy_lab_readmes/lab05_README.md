# Lab 05 — Inverse Kinematics

## Purpose

Implement analytical IK for a planar 2R arm, then iterative numerical IK for the UR5e. Use your own FK from Lab 04. Test reachable and problematic targets; report convergence, final error, and sensitivity to initial guess. Do not use MoveIt as the solver.

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
