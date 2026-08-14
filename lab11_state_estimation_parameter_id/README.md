# Lab 11 — State Estimation and Parameter Identification

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

Sensors provide samples, not perfect state; useful models must be estimated and then tested on data they did not fit.

## Learning objectives

Estimate velocity from sampled position; explain noise amplification; implement filtering; identify a simple parameter by least squares; and validate on held-out Webots data.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab11_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab11_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Generate repeatable Webots position/command/torque logs using simulation timestamps.
2. Complete `src/estimate_velocity.py` with backward and centered differences plus an explicit filter.
3. Compare estimates with a known trajectory derivative or simulator reference reserved for validation.
4. Complete `src/least_squares_id.py`; state the regressor and parameter meaning.
5. Fit on one trial and validate on another speed or payload. Report residuals, not only fitted parameters.

## Submission

Submit source, raw-data description, velocity plots/errors, regression derivation, held-out validation, and `answers.md`.
