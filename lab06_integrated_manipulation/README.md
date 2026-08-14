# Lab 6 - Integrated Manipulation / Final Project

**Do not save over the original starter world after running the simulation. Immediately save a working copy; reset/revert before preserving world changes.**

## Learning objectives

By the end of this project, you should be able to:

1. integrate coordinate transforms, FK/IK, trajectories, feedback, and quantitative evaluation;
2. use Jacobian or differential motion where it improves the task;
3. represent obstacles and implement collision checking/planning explicitly;
4. execute a repeatable manipulation-style task from a safe home configuration;
5. diagnose integration failures across model, planner, controller, and simulator boundaries; and
6. communicate system architecture, assumptions, evidence, and limitations.

## Prerequisites

Complete Labs 1-5. Reuse your tested mathematical modules rather than copying formulas into one monolithic controller. The project introduces system integration, not a new set of hidden simulator algorithms.

## Background

The baseline challenge is to move from home to a target object or pose, avoid an obstacle/forbidden region, complete a pick-and-place or equivalent manipulation sequence, and return safely. A full gripper is optional unless supplied by the instructor; reaching, approach/retreat, transport, and placement poses can demonstrate equivalent integration.

Simulator APIs may expose sensing and ground truth, but they must not replace submitted transformations, kinematics, Jacobian calculations, trajectory generation, collision predicates, planning, control, or evaluation.

## Provided files

- `worlds/lab06_starter.wbt`
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/collision_planner.py` - explicit collision-checking/planning starter
- `src/COLLISION_PLANNER_NOTES.md` - separation and reproducibility guidance
- `config/`, `results/`, `report/`, and `starter_code/` placeholders
- `answers.md`

Collision-planning material was merged from the former standalone collision-planning lab.

## Required Webots workflow and recovery

1. **World:** open `worlds/lab06_starter.wbt` paused and use **File -> Save World As...** to create `worlds/lab06_work.wbt`; verify `void` before adding an obstacle.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm the integration controller's required devices.
4. **One joint:** verify a conservative one-joint command through the final controller stack.
5. **Full algorithm:** add targets/obstacles and execute the integrated task only after stages 1-4 pass.

Keep a clean starter and a separate working world. After a crash, use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md), reopen a clean world, and reapply one known-good change at a time.

## Step-by-step instructions

1. Define the task, frames, home configuration, targets, obstacle model, limits, and metrics.
2. Draw the software/data-flow architecture before integrating code.
3. Validate each reused module with its earlier unit tests.
4. Create `lab06_work.wbt` and add only instructor-approved target/obstacle objects.
5. Demonstrate FK/IK reachability for approach, task, retreat, and home poses.
6. Show that a direct path collides or violates a forbidden region for at least one assigned case.
7. Plan a collision-free waypoint or sampled path with your own collision predicate.
8. Time-parameterize the path and execute it with feedback.
9. Log enough data to reproduce and quantify the complete run.
10. Repeat from Reset and analyze one controlled variation or failure.

## Implementation tasks

1. Complete `configuration_in_collision`, `edge_in_collision`, and `plan` in `collision_planner.py`.
2. Compute link geometry from your FK; do not use visual appearance as the collision predicate.
3. Inflate obstacles or otherwise state the safety margin.
4. Check every interpolated edge, not only path endpoints.
5. Smooth a path only if every replacement edge remains collision-free.
6. Integrate:
   - explicit transforms and FK/IK;
   - Jacobian/differential motion where used;
   - trajectory generation;
   - joint-limit and collision checks;
   - feedback/state estimates; and
   - deterministic logging and metrics.
7. Record random seeds, initial conditions, parameters, and controller gains.

## Required experiments

### Experiment A - module and path validation

Show target reachability, one colliding direct path, and one collision-free planned path. Report computation time, path length, minimum modeled clearance, and waypoint count.

### Experiment B - integrated task

Execute home -> approach -> task/transport -> retreat -> safe final/home. Report success criteria, pose/tracking error, completion time, and clearance.

### Experiment C - repeatability and failure analysis

Repeat the task from the same reset state and test one controlled variation, such as obstacle placement, target pose, payload/model condition, or planner seed. Include one failure, its boundary, and a mitigation.

## Questions and reflection

1. Which coordinate-frame interface caused the greatest integration risk?
2. How did collision-check resolution affect safety and computation time?
3. Which earlier lab module required the most modification, and why?
4. What evidence shows the task is repeatable rather than a single successful animation?
5. Which simulator ground-truth values were used only for validation?
6. What would have to change for transfer to a physical arm?

## What to submit

Submit:

- proposal and architecture diagram;
- source code with run instructions;
- configuration/parameter files and seeds;
- collision representation and planning pseudocode;
- successful demonstration video or instructor-approved live demo;
- CSV logs and at least two quantitative metrics;
- repeatability and failure analysis;
- final technical report; and
- `answers.md`.

## Milestones

1. **Proposal:** task, frames, metrics, risks, and module ownership.
2. **Model checkpoint:** validated geometry and reachable targets.
3. **Planning/control checkpoint:** safe offline and one-joint tests.
4. **Integrated demonstration:** repeatable Webots execution.
5. **Report:** prediction, evidence, discrepancy, failure, and mitigation.

## Optional physical-arm extension

With instructor approval, transfer selected modules to the course 3D-printed arm. Document interface, calibration, limits, and model differences. Hardware is optional and is not required to complete the simulation project successfully.

## Troubleshooting

Integrate one boundary at a time: world -> controller -> devices -> one joint -> one pose -> one segment -> full path. Preserve failing logs and worlds. If an endpoint is safe but motion collides, inspect edge interpolation and model clearance. If the planner succeeds but execution fails, separate planning, timing, and control errors.