# Lab 4 - Trajectory Generation and Tracking

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Mission

Execute a smooth point-to-point motion and a straight-line Cartesian motion, then quantitatively compare them.

## Success Criteria

You succeed when the UR5e safely completes both motions, the point-to-point trajectory meets its endpoint constraints, the Cartesian path remains within the assigned straightness tolerance, and your logs support a comparison of duration, smoothness, tracking error, and maximum joint velocity.

## Learning Objectives

By the end of this lab, you should be able to:

1. implement cubic or quintic time scaling with explicit boundary conditions;
2. generate synchronized joint-space motion and Cartesian waypoint motion;
3. reuse your own FK, IK, and Jacobian-related checks from earlier labs;
4. execute sampled references through a small Webots adapter; and
5. compare trajectory geometry and tracking performance quantitatively.

## Prerequisites

Complete Labs 1-3 and the [setup prerequisites](../lab00_setup/README.md). Bring tested joint ordering, FK, IK, safe-motion checks, and logging. Webots Tutorials 2 and 3 remain optional enrichment; they are not prerequisites.

## Background

A trajectory is a time-parameterized reference, not merely a sequence of poses. A MoveJ-style motion interpolates in joint space and generally traces a curved Cartesian path. A practical MoveL-style motion samples a straight Cartesian segment, solves each waypoint with your own IK using continuity-aware initial guesses, and time-parameterizes the resulting joint path.

Use simulation time, not wall-clock time. At minimum compute

```text
e_i(t) = q_des,i(t) - q_meas,i(t)
RMSE_i = sqrt(mean(e_i(t)^2))
```

and a Cartesian straightness error measured from each FK position to the desired line segment.

## Provided Files

- `worlds/lab04_starter.wbt` - clean, known-good starter; never overwrite it
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/cubic_trajectory.py` - coefficient and sampling starter
- `src/send_trajectory.py` - Webots execution outline
- `src/cartesian_line.py` - straight-line waypoint scaffold
- `answers.md`

## Part 1 - Setup / Validation

1. **World:** open `worlds/lab04_starter.wbt` paused, verify it, and immediately use **File -> Save World As...** to create `worlds/lab04_work.wbt`.
2. **Minimal controller:** assign and run `diagnostic_minimal`.
3. **Devices:** assign `diagnostic_devices` and confirm all six motors and sensors.
4. **One joint:** run a low-speed polynomial on one joint and compare desired and measured position.
5. **Full algorithm:** proceed only after the first four stages pass.

Unit-test polynomial boundary conditions outside Webots before commanding the robot. Select instructor-approved start/end configurations and limits.

## Part 2 - Core Implementation

1. Complete `cubic_coefficients` and `sample_cubic`; add quintic timing if assigned.
2. Check endpoint position, velocity, and acceleration numerically.
3. Generate a synchronized MoveJ-style trajectory with explicit position, rate, and acceleration checks.
4. Complete `cartesian_line.py` to sample position—and orientation if assigned—between two poses.
5. Solve each Cartesian waypoint with your Lab 2 IK; reject failed, discontinuous, or unsafe solutions.
6. Keep trajectory generation, IK, metrics, and Webots device I/O in separate functions/modules.

Do not call a Webots, SciPy, MoveIt, or other library trajectory/IK solver for the submitted implementation.

## Part 3 - Robot Experiment

From the same reset state, execute:

1. a MoveJ-style joint-space motion from `q0` to `qf`; and
2. a practical MoveL-style Cartesian waypoint motion between the corresponding end-effector poses.

Log simulation time, desired/measured joint position, desired joint velocity, and FK end-effector position. Hold the final command safely. If a waypoint fails IK or a limit check, stop before motion rather than skipping it.

## Part 4 - Quantitative Analysis

For both motions report:

- commanded and measured duration;
- joint RMSE and maximum joint error;
- maximum desired/measured joint velocity;
- Cartesian path length;
- maximum and RMS distance from the desired Cartesian line; and
- a smoothness measure, such as peak acceleration or integrated squared acceleration.

Plot joint trajectories and the 3-D or projected end-effector paths on common axes. Explain the observed geometry/performance tradeoff rather than judging from animation alone.

## Engineering Questions

1. Why can a smooth joint-space trajectory produce a curved Cartesian path?
2. Why does increasing duration usually reduce velocity and acceleration demand?
3. Which IK continuity strategy prevented joint jumps along the Cartesian path?
4. How did waypoint spacing affect straightness, computation, and tracking?
5. Which metric most clearly distinguishes the two motions?

## What to Submit

- completed trajectory and Cartesian-line source;
- endpoint/unit tests and stated limits;
- Webots controller or adapter;
- desired/measured CSV logs for both motions;
- joint and Cartesian path plots;
- comparison table with all required metrics; and
- completed `answers.md`.

## Troubleshooting

If Webots repeatedly crashes, close it, follow [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md), and reopen the untouched starter world in safe mode before recreating a working copy. Revert a damaged starter with Git. A clean world that fails with `diagnostic_minimal` indicates a controller/Python problem; a clean world that opens with controller `void` but crashes after motion indicates command, units, timing, or limits. Retest one joint before the full trajectory.
