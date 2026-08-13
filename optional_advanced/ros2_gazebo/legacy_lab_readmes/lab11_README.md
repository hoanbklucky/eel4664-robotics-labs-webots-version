# Lab 11 — State Estimation and Parameter Identification

## Purpose

Estimate joint velocity from sampled position, show how differentiation amplifies noise, filter the estimate, and identify one simple model parameter using least squares. Validate on data not used for fitting.

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
