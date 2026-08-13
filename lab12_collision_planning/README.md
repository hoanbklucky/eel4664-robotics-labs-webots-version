# Lab 12 ? Collision-Aware Planning

## Motivation

A kinematically valid goal can still be unsafe when the arm or swept path intersects the environment.

## Learning objectives

Represent obstacles; use your FK to approximate robot links; implement configuration/edge collision tests; build a waypoint planner; smooth a path; and validate it in Webots.

## Investigation

1. Add the instructor obstacle to a copy of the shared world and document its frame and dimensions.
2. Complete `src/collision_planner.py`: compute link positions from your FK and test link capsules or segments against inflated obstacles.
3. Show a colliding straight-line joint path.
4. Implement the assigned sampling/waypoint search using your collision predicate; do not call a planning library.
5. Smooth only when every interpolated edge remains collision-free.
6. Execute with Lab 08 trajectories and report clearance, path length, computation time, and execution error.

## Submission

Explain discretization risk and why endpoint-only checks fail. Submit representation, pseudocode, source, failed/successful trials, metrics, and `answers.md`.

The former MoveIt exercise is optional at `optional_advanced/ros2_gazebo/lab12_moveit_collision_planning/`.
