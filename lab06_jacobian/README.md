# Lab 06 ? Jacobian and Differential Kinematics

## Motivation

The Jacobian predicts how joint motion becomes instantaneous tool motion and is the local bridge used by IK and control.

## Learning objectives

Derive and implement the geometric Jacobian; verify it by finite differences; test `dx ? J dq`; and compute joint velocity with an explicit pseudoinverse.

## Investigation

1. Complete `src/jacobian_starter.py` using transforms from Lab 04.
2. Verify each column with centered finite differences over several step sizes.
3. Predict tool velocity for a chosen `qdot` and compare with sampled Webots tool motion.
4. Compute `qdot = J?v` using NumPy SVD, apply a small integrated command, and quantify the achieved velocity.
5. Explain finite-step, frame, and sensor-sampling errors.

## Submission

Submit derivation, source, finite-difference study, Webots velocity comparison, and `answers.md`.
