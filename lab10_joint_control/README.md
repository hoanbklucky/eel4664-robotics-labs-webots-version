# Lab 10 — Joint-Space Control

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

Feedback converts model mismatch and disturbances into measurable corrections, but gains trade speed against overshoot and effort.

## Learning objectives

Implement P and PD control; quantify rise time, overshoot, settling time, steady-state error, and effort; and transfer the same law from a NumPy plant to one Webots UR5e joint.

**Python prerequisite:** Before running this lab, complete [Lab 00 Section 1](../lab00_setup/README.md#1-required-student-environment), including the python.org CPython installation, Webots **Python command** configuration, minimal-controller test, and NumPy verification.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab10_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab10_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Complete `src/pd_control_sim.py` using your own numerical integration.
2. Predict responses for low, moderate, and excessive gains.
3. In a copied Webots world, isolate a safe joint trial and switch its motor to torque mode with `setPosition(float('inf'))` and `setTorque(tau)`.
4. Estimate velocity from position samples; apply your explicit `tau = Kp e - Kd qdot` law with saturation.
5. Compare Python-plant and Webots metrics; explain differences.

## Safety and submission

Use conservative torque limits, one joint first, and Reset between trials. Submit controller code, gains, plots/metrics, comparison, and `answers.md`.
