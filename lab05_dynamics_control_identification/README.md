# Lab 09 — Manipulator Dynamics

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

Kinematics predicts motion; dynamics explains the effort required and why payload and acceleration matter.

## Learning objectives

Interpret `M(q)qdd + C(q,qd)qd + g(q) = tau`; implement a simplified model; separate gravity, inertia, and velocity effects; and compare predictions with Webots physics trials.

## Webots bridge: Tutorial 7 — Your First PROTO

Complete [Webots Tutorial 7: Your First PROTO](https://cyberbotics.com/doc/guide/tutorial-7-your-first-proto?version=R2025a) using the four-wheel robot saved in Lab 04. Confirm that a PROTO packages a node hierarchy and exposes selected fields with `IS`; it does not supply robot dynamics or control algorithms.

Expose and vary the tutorial robot's `bodyMass`, then connect that experiment to Tutorial 5's `Physics.mass`, `density`, `centerOfMass`, and inertia concepts. For the UR5e trials below, use the same idea to define payload conditions as explicit model parameters. Do not edit or replace Cyberbotics' installed UR5e PROTO; work in a saved course-world copy or a small course-owned wrapper/payload PROTO.
**Python prerequisite:** Before running this lab, complete [Lab 00 Section 1](../lab00_setup/README.md#1-required-student-environment), including the python.org CPython installation, Webots **Python command** configuration, minimal-controller test, and NumPy verification.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab09_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab09_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Complete `src/simple_dynamics.py` and validate units/limiting cases.
2. Predict which term dominates static holding, slow motion, and rapid acceleration.
3. In a copied world/controller, use motor torque feedback when available or prescribed experiment data.
4. Repeat matched trajectories at two durations and two payload conditions.
5. Compare predicted trends and measured torque; explain unmodeled friction and multi-link coupling.

## Rule and submission

Do not use a simulator inverse-dynamics function. Submit the Tutorial 7 PROTO, evidence that `bodyMass` changes through its exposed field, equations, source, payload definition, trial table/plots, residual analysis, and `answers.md`.
