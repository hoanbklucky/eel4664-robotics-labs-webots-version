# Lab 01 — Webots and the UR5e

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

Before deriving robot models, learn how commands and measurements cross the boundary between a Python controller and the official simulated UR5e.

## Learning objectives

Identify Webots worlds, PROTO models, controllers, devices, and time steps; read six joint sensors; command a repeatable pose; and explain the sense–compute–act loop.

## Preparation

Complete Lab 00, run its R2025a sample-preparation script, and inspect the official `ure.wbt` demonstration. Then use this lab's protected starter/work-world workflow. Predict how each named UR5e joint changes the robot.

**Python prerequisite:** Before running this lab, complete [Lab 00 Section 1](../lab00_setup/README.md#1-required-student-environment), including the python.org CPython installation, Webots **Python command** configuration, minimal-controller test, and NumPy verification.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab01_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab01_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. In `lab01_work.wbt`, select the `UR5e` robot and inspect its motors and sensors.
2. Preserve the device inventory produced by `diagnostic_devices` as the baseline.
3. Set only the UR5e `controller` field to `eel4664_ur5e`, then Reset.
4. Match each `RotationalMotor` with its `<joint>_sensor`.
5. Implement ordered sampling and CSV logging from `src/inspect_joint_states.py`.
6. Generate a smooth command from measured `q0` to a safe `qf` using `src/send_joint_goal.py`.
7. Reset and run two durations. Plot command and measurement versus simulation time.

Keep every persistent edit in `lab01_work.wbt`; restore from `lab01_starter.wbt` if a change makes the world unstable.

## Explain

Draw `world → robot/PROTO → controller → motor → physics → sensor → controller`. Explain why one `robot.step()` per loop synchronizes sensing, actuation, and physics.

## Submission

Submit both scripts, CSV/plot evidence, architecture sketch, maximum tracking error, and `answers.md`. Do not submit the downloaded Cyberbotics assets.

The former ROS action/controller exercise is optional at `optional_advanced/ros2_gazebo/lab01_ros2_gazebo_ur5e/`.
