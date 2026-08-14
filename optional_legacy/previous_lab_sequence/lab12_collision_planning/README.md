# Lab 12 — Collision-Aware Planning

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

A kinematically valid goal can still be unsafe when the arm or swept path intersects the environment.

## Learning objectives

Represent obstacles; use your FK to approximate robot links; implement configuration/edge collision tests; build a waypoint planner; smooth a path; and validate it in Webots.

**Python prerequisite:** Before running this lab, complete [Lab 00 Section 1](../lab00_setup/README.md#1-required-student-environment), including the python.org CPython installation, Webots **Python command** configuration, minimal-controller test, and NumPy verification.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab12_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab12_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Add the instructor obstacle to `worlds/lab12_work.wbt` and document its frame and dimensions.
2. Complete `src/collision_planner.py`: compute link positions from your FK and test link capsules or segments against inflated obstacles.
3. Show a colliding straight-line joint path.
4. Implement the assigned sampling/waypoint search using your collision predicate; do not call a planning library.
5. Smooth only when every interpolated edge remains collision-free.
6. Execute with Lab 08 trajectories and report clearance, path length, computation time, and execution error.

## Submission

Explain discretization risk and why endpoint-only checks fail. Submit representation, pseudocode, source, failed/successful trials, metrics, and `answers.md`.

The former MoveIt exercise is optional at `optional_advanced/ros2_gazebo/lab12_moveit_collision_planning/`.
