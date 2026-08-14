# Lab 04 — Forward Kinematics of the UR5e

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

Given six encoder readings, predict where the tool is before asking the simulator where it appears.

## Learning objectives

Derive a planar warm-up, implement a DH-style transform, construct a six-link UR5e chain, read Webots joint sensors, and quantify FK position/orientation error.

## Webots bridge: Tutorials 5 and 6

Before deriving the UR5e chain, complete these tutorials in order:

1. [Tutorial 5: Compound Solid and Physics Attributes](https://cyberbotics.com/doc/guide/tutorial-5-compound-solid-and-physics-attributes?version=R2025a). Identify visual geometry, compound `boundingObject` geometry, mass, center of mass, contact properties, and `basicTimeStep`. Save the project because Tutorial 6 builds on it.
2. [Tutorial 6: 4-Wheels Robot](https://cyberbotics.com/doc/guide/tutorial-6-4-wheels-robot?version=R2025a). Complete the robot structure, `HingeJoint`, motor, sensor, and controller portions using Python.

The four-wheel robot is not a manipulator model; it is a compact exercise in building a robot as a tree of rigid bodies connected by joints. Draw one path from its root `Robot` node to a wheel, then draw the analogous path from the UR5e base to its tool. Label joint axes, parent/child solids, motors, and sensors. This structural comparison prepares the ordered transform product used in FK; it does not replace that derivation.
## Important rule

Do not call a simulator or library FK solver. Webots GPS/InertialUnit data is a reference only after your FK is computed. State any fixed base/tool-frame offset explicitly.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab04_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab04_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Complete `src/planar_fk.py` and validate hand-selected cases.
2. Complete `dh_transform` and the chain in `src/ur5e_fk_starter.py` using instructor-approved parameters.
3. Copy `src/read_configuration.py` into a Webots controller and record ordered joint positions.
4. Evaluate at least five configurations, including home and a nonsymmetric pose.
5. Compare predicted tool position and orientation with shared-world sensors.
6. Plot error and diagnose convention, parameter, discretization, or model-frame causes.

## Submission

Submit Tutorial 5–6 completion evidence, the wheel-to-UR5e structural comparison, FK derivation and code, parameter table with source, configuration data, error table/plot, and `answers.md`.
