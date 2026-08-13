# Lab 02 ? Coordinate Frames

## Motivation

Robot geometry is meaningful only when every vector states where it is expressed and what it describes.

## Learning objectives

Draw a UR5e frame tree; distinguish active/passive transformations; transform points and directions; compose transforms; and validate a result against Webots measurements.

## Preparation

Review rotation matrices and homogeneous coordinates. Before simulation, predict why translation affects a point but not a free vector.

## Investigation

1. Inspect the UR5e hierarchy in the Webots Scene Tree and sketch base, joint, and tool frames.
2. Complete `src/transform_point.py` using NumPy only.
3. Complete `src/query_transform.py` to read a Supervisor node's position and orientation as validation data.
4. Transform a tool-frame point into the world frame by your own matrix composition.
5. Compare with Webots ground truth and report position/orientation error.

## Rule

Supervisor/GPS measurements are references, not transformation solvers. Your code must construct and multiply the matrices.

## Submission

Submit code, frame tree, one hand calculation, numerical comparison, and `answers.md`.

The former TF2 exercise is optional at `optional_advanced/ros2_gazebo/lab02_frames_tf/`.
