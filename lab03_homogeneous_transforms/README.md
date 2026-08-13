# Lab 03 ? Homogeneous Transformations

## Motivation

A chain of simple rigid transformations can predict a complicated robot pose, but only when order and frame labels are correct.

## Learning objectives

Implement rotations and translations in NumPy; compose and invert homogeneous transforms; test invariants; and compare one composed UR5e transform with Webots ground truth.

## Investigation

1. Complete every TODO in `src/transforms.py` and run `src/test_transforms.py`.
2. Predict, then demonstrate, why `T1 @ T2` differs from `T2 @ T1`.
3. Verify `R.T @ R = I`, `det(R) = 1`, and `T @ inv(T) = I` numerically.
4. Use the UR5e frame sketch from Lab 02 to compose at least two adjacent transforms.
5. Read the tool GPS/InertialUnit only after computing your prediction; report discrepancies.

## Submission

Submit source, tests, one noncommutativity example, Webots comparison, and `answers.md`.
