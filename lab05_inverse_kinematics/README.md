# Lab 05 — Inverse Kinematics

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Motivation

Tool goals are Cartesian, but actuators accept joint commands; IK connects those descriptions and exposes reachability and nonuniqueness.

## Learning objectives

Derive analytical planar 2R IK; implement iterative UR5e IK from your Lab 04 FK/Jacobian; recognize unreachable and ill-conditioned targets; and validate solutions in Webots.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab05_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab05_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Investigation

1. Complete `src/planar_ik.py`, retaining both elbow branches and checking reachability.
2. Complete `src/numerical_ik.py` with explicit pose error, convergence criterion, joint limits, and iteration limit.
3. Test multiple initial guesses for reachable, near-boundary, and unreachable targets.
4. Command converged joint solutions through the Webots motor adapter using a smooth transition.
5. Compare predicted and measured final tool poses; report iterations and residuals.

## Rule

Do not use Webots, MoveIt, SciPy, or another IK solver. General linear algebra such as NumPy SVD is allowed.

## Submission

Submit derivations, source, convergence histories, Webots evidence, failure analysis, and `answers.md`.
