# Lab 01 ? Webots and the UR5e

## Motivation

Before deriving robot models, learn how commands and measurements cross the boundary between your Python program and a simulated mechanism.

## Learning objectives

Launch a UR5e world; identify Webots worlds, PROTO models, controllers, devices, and time steps; read six joint sensors; command a repeatable pose; and explain the sense?compute?act loop.

## Preparation

Complete Lab 00. Copy the shared controller before modifying it. Predict how each named joint changes the robot.

## Investigation

1. Open `webots/worlds/eel4664_ur5e.wbt` and inspect the Scene Tree.
2. Match each `RotationalMotor` with its `<joint>_sensor`.
3. In `src/inspect_joint_states.py`, implement ordered sensor sampling and CSV logging.
4. In `src/send_joint_goal.py`, generate commands from measured `q0` to a safe `qf`; do not jump directly to `qf`.
5. Reset and run two durations. Plot command and measurement versus simulation time.

## Explain

Draw `world ? robot/PROTO ? controller ? motor ? physics ? sensor ? controller`. Explain why one `robot.step()` per loop synchronizes sensing, actuation, and physics.

## Submission

Submit both scripts, CSV/plot evidence, architecture sketch, maximum tracking error, and `answers.md`.

The former ROS action/controller exercise is optional at `optional_advanced/ros2_gazebo/lab01_ros2_gazebo_ur5e/`.
