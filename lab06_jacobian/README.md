# Lab 06 — Jacobian and Differential Kinematics

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

The Jacobian predicts how joint motion becomes instantaneous tool motion and is the local bridge used by IK and control.

## Learning objectives

Derive and implement the geometric Jacobian; verify it by finite differences; test `Δx ≈ J Δq`; and compute joint velocity with an explicit pseudoinverse.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab06_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab06_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Complete `src/jacobian_starter.py` using transforms from Lab 04.
2. Verify each column with centered finite differences over several step sizes.
3. Predict tool velocity for a chosen `qdot` and compare with sampled Webots tool motion.
4. Compute `qdot = J⁺v` using NumPy SVD, apply a small integrated command, and quantify the achieved velocity.
5. Explain finite-step, frame, and sensor-sampling errors.

## Submission

Submit derivation, source, finite-difference study, Webots velocity comparison, and `answers.md`.
