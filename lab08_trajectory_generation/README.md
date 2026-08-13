# Lab 08 ? Trajectory Generation

## Motivation

A goal pose says where to finish, not how to move safely and smoothly between samples.

## Learning objectives

Derive cubic coefficients; optionally derive quintic interpolation; evaluate position, velocity, and acceleration; sample a six-joint trajectory; and compare command with measured Webots motion.

## Investigation

1. Complete `src/cubic_trajectory.py` from endpoint constraints, not a library interpolator.
2. Plot `q`, `qdot`, and `qddot`; verify endpoint conditions numerically.
3. Complete `src/send_trajectory.py` to evaluate your polynomial at `robot.getTime()` and command each motor every Webots step.
4. Run two durations from the same reset state.
5. Log commands and position sensors; report maximum/RMS tracking error and observed smoothness.

## Submission

Submit derivation, source, plots, logged Webots comparison, and `answers.md`.
