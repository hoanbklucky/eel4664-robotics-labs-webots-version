# Final Project — Integrated Robotic Manipulation

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Goal

Integrate the semester's explicit algorithms into one reproducible Webots UR5e task.

At minimum use coordinate transformations, FK or IK, trajectory generation or collision-aware planning, feedback/state information, and quantitative evaluation.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/final_project_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/final_project_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## Baseline challenge

Using the supplied Webots project:

1. begin from a documented home configuration;
2. compute and reach a specified approach pose;
3. reach one or more targets while respecting joint limits;
4. avoid at least one obstacle or forbidden region;
5. return to a safe final configuration;
6. log enough data to evaluate execution quantitatively.

A gripper extension may be assigned. Simulator APIs may provide sensing and actuation, but must not replace submitted kinematics, planning, trajectory, control, estimation, or identification algorithms.

## Milestones

1. **Proposal:** task, frames, metric, risks.
2. **Model checkpoint:** validated geometry and reachable targets.
3. **Planning/control checkpoint:** collision-free offline tests.
4. **Integrated demonstration:** repeatable Webots execution and logs.
5. **Report:** prediction, evidence, discrepancy, failure, mitigation.

## Required evidence

Submit an architecture diagram, mathematical formulation, source and run instructions, at least two quantitative metrics, successful demonstration, and one failure analysis. Report seeds and initial conditions.

## Optional extensions

- add a Webots gripper or perception sensor;
- compare with the optional ROS 2/Gazebo track;
- transfer selected algorithms to the course arm and identify interface/model changes.
