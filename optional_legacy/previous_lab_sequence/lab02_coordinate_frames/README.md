# Lab 02 — Coordinate Frames

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

Robot geometry is meaningful only when every vector states where it is expressed and what it describes.

## Learning objectives

Draw a UR5e frame tree; distinguish active/passive transformations; transform points and directions; compose transforms; and validate a result against Webots measurements.

## Preparation

Review rotation matrices and homogeneous coordinates. Before simulation, predict why translation affects a point but not a free vector.

## Webots bridge: Tutorial 8 — The Supervisor

Before the investigation, complete [Webots Tutorial 8: The Supervisor](https://cyberbotics.com/doc/guide/tutorial-8-the-supervisor?version=R2025a) using Python. Focus on obtaining a node by `DEF`, reading its fields, and acquiring position/orientation measurements. Keep this tutorial in its own project.

For this lab, a Supervisor is measurement equipment: it may observe the simulated ground truth, but it must not compute your coordinate transformation. Record one example showing the difference between reading a Webots field and deriving a transformed point with your own NumPy matrices.
**Python prerequisite:** Before running this lab, complete [Lab 00 Section 1](../lab00_setup/README.md#1-required-student-environment), including the python.org CPython installation, Webots **Python command** configuration, minimal-controller test, and NumPy verification.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab02_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab02_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Inspect the UR5e hierarchy in the Webots Scene Tree and sketch base, joint, and tool frames.
2. Complete `src/transform_point.py` using NumPy only.
3. Complete `src/query_transform.py` to read a Supervisor node's position and orientation as validation data.
4. Transform a tool-frame point into the world frame by your own matrix composition.
5. Compare with Webots ground truth and report position/orientation error.

## Rule

Supervisor/GPS measurements are references, not transformation solvers. Your code must construct and multiply the matrices.

## Submission

Submit the Tutorial 8 Supervisor measurement example, your code, frame tree, one hand calculation, numerical comparison, and `answers.md`.

The former TF2 exercise is optional at `optional_advanced/ros2_gazebo/lab02_frames_tf/`.
