# Lab 5 - Trajectory Generation and Tracking

## Get the Latest Course Files

Before starting, save your work and close Webots. Follow [Updating the Course Repository](../docs/UPDATE_REPOSITORY.md). Do not force an update or discard local work when Git reports a conflict.

## Mission

Execute a smooth point-to-point motion and a straight-line Cartesian motion, then quantitatively compare them.

### Why track trajectories in Webots?

A generated trajectory is an ideal reference, not proof of the path a robot actually follows. Webots provides the experimental joint and tool measurements needed to compare the commanded and executed motions, including endpoint error, path straightness, smoothness, and maximum joint velocity.

This follows the same workflow used with hardware: **generate -> execute -> measure -> evaluate**. The visual path is useful for intuition, but the recorded data determine whether the trajectory meets its requirements.

## Success Criteria

You succeed when the UR5e safely completes both motions, the point-to-point trajectory meets its endpoint constraints, the Cartesian path remains within the assigned straightness tolerance, and your logs support a comparison of duration, smoothness, tracking error, and maximum joint velocity.

## Learning Objectives

By the end of this lab, you should be able to:

1. implement cubic or quintic time scaling with explicit boundary conditions;
2. generate synchronized joint-space motion and Cartesian sampled-reference motion;
3. reuse your own FK, IK, and Jacobian-related checks from earlier labs;
4. execute sampled references through a small Webots adapter; and
5. compare trajectory geometry and tracking performance quantitatively.

## Prerequisites

Complete Labs 1-4 and the [setup prerequisites](../lab00_setup/README.md). Bring tested joint ordering, FK, IK, safe-motion checks, and logging. Webots Tutorials 2 and 3 remain optional enrichment; they are not prerequisites.


**Platform note:** The required workflow supports Windows, macOS, and Ubuntu when configured through Lab 00. Terminal examples use `python`; on macOS or Ubuntu, use `python3` instead if `python` is not recognized.

## Background

A path describes where the robot moves; a trajectory also specifies when it reaches each point. The generated trajectory is only a reference. Webots measurements are needed to determine whether the robot followed that reference accurately and whether the motion respected its limits.

For a concepts-first explanation of cubic and quintic timing, duration scaling, synchronized joints, MoveJ versus MoveL, IK continuity, and tracking metrics, read [Lab 5 Optional Background](OPTIONAL_BACKGROUND.md). The required activity remains in this README.

Use simulation time, not wall-clock time. For every desired and measured comparison, use the same joint ordering, frame, and physical tool point. The starter's orange stylus tip is

```python
p_world_tip = transform_point(T_world_tool, [0, 0.13, 0])
```

Use that point for both desired and measured Cartesian straightness. The `TRAJECTORY_REFERENCE_BOARD` is a qualitative visual reference, not measurement data.

## Provided Files

- `worlds/lab05_starter.wbt` - clean starter with stylus, grid, and trajectory reference board; never overwrite it
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/cubic_trajectory.py` - coefficient and sampling starter
- `src/send_trajectory.py` - Webots execution outline
- `src/cartesian_line.py` - straight-line sampling and sequential-IK scaffold
- `Lab05_Report_Template.docx`



## Open the Word report template

Follow [Opening a Word Report Template](../docs/OPEN_WORD_REPORT.md) and create a personal copy of `Lab05_Report_Template.docx` before entering results.

## Part 1 - Setup / Validation

> **Why this part matters:** Testing the world, devices, one joint, and polynomial boundary conditions first prevents setup or interpolation errors from contaminating a full trajectory experiment.

1. **World:** open `worlds/lab05_starter.wbt` paused; verify the grid, stylus, and `TRAJECTORY_REFERENCE_BOARD`; then immediately use **File -> Save World As...** to create `worlds/lab05_work.wbt`.
2. **Minimal controller:** assign and run `diagnostic_minimal`.
3. **Devices:** assign `diagnostic_devices` and confirm all six motors and sensors.
4. **One joint:** run a low-speed polynomial on one joint and compare desired and measured position.
5. **Full algorithm:** proceed only after the first four stages pass.

Unit-test polynomial boundary conditions outside Webots before commanding the robot. Select instructor-approved start/end configurations and limits.

## Part 2 - MoveJ Implementation

> **Why this part matters:** MoveJ is generated directly in joint space. The three cubic equations show how the initial and final joint conditions become a synchronized, timed joint trajectory.

1. Open `src/cubic_trajectory.py`.
2. Complete only `TODO 1`, `TODO 2`, and `TODO 3`: final position change, the quadratic coefficient, and the cubic coefficient.
3. Run endpoint checks confirming the requested initial/final position and velocity.
4. Use the same duration and normalized clock for all six joints so they start and finish together.
5. Generate the MoveJ-style joint reference and check every sampled joint position, velocity, and acceleration against the assigned limits.

Do not call a Webots, SciPy, MoveIt, or other library trajectory solver for the three assigned equations.

## Part 3 - MoveL Implementation

> **Why this part matters:** MoveL starts with a timed Cartesian line rather than a joint polynomial. Each Cartesian sample must be converted to a continuous and feasible sequence of joint commands.

1. Read the supplied `src/cartesian_line.py` and identify where each accepted IK solution becomes the seed for the next IK solve.
2. Use the provided helper to sample the straight Cartesian path between the MoveJ endpoint poses.
3. Solve the samples in order. Do not solve each sample from the same fixed seed.
4. Before motion, confirm that every IK solve converged and that no joint-limit or branch-jump check failed.
5. Associate the joint solutions with the Cartesian trajectory times and use the same limits and timing conventions as in Part 2.

The execution loop sends the current joint target once per Webots simulation step. It does not create an independent rest-to-rest motion between every two samples. See [What happens between two IK samples?](OPTIONAL_BACKGROUND.md#what-happens-between-two-ik-samples) for the Webots and physical-robot interpretation.

Do not rewrite the supplied Cartesian-sampling, line-distance, logging, or execution helpers, and do not call a Webots, SciPy, MoveIt, or other library IK solver for the assigned work.

## Part 4 - Robot Experiment

> **Why this part matters:** Running both motions from the same reset state reveals the difference between a smooth joint-space path and a geometrically straight Cartesian path.

From the same reset state, execute:

1. a MoveJ-style joint-space motion from `q0` to `qf`; and
2. a practical MoveL-style Cartesian sampled-reference motion between the corresponding end-effector poses.

Log simulation time, desired/measured joint position, desired joint velocity, and FK end-effector position. Hold the final command safely. If a Cartesian sample fails IK or a limit check, stop before motion rather than skipping it.

## Part 5 - Quantitative Analysis

> **Why this part matters:** Tracking error, straightness, velocity, and smoothness measurements show the tradeoffs that animation alone cannot establish.

For both motions report:

- commanded and measured duration;
- joint RMSE and maximum joint error;
- maximum desired/measured joint velocity;
- Cartesian path length;
- maximum and RMS distance from the desired Cartesian line; and
- a smoothness measure, such as peak acceleration or integrated squared acceleration.

Plot joint trajectories and the 3-D or projected end-effector paths on common axes. Explain the observed geometry/performance tradeoff rather than judging from animation alone.

## Engineering Question

Answer in 2-3 sentences.

Why can a smooth joint-space trajectory produce a curved Cartesian tool path, while a Cartesian sampled-reference trajectory can remain approximately straight? Refer to your measured paths.

## What to Submit

1. Completed `src/cubic_trajectory.py` containing the three equation lines.
2. Completed `Lab05_Report_Template.docx` containing endpoint checks, MoveJ and MoveL logs and plots, the metric comparison, and the Engineering Question response.

Do not submit supplied helper code, `lab05_work.wbt`, vendor assets, or caches unless requested.

## Troubleshooting

If Webots repeatedly crashes, close it, follow [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md), and reopen the untouched starter world in safe mode before recreating a working copy. Revert a damaged starter with Git. A clean world that fails with `diagnostic_minimal` indicates a controller/Python problem; a clean world that opens with controller `void` but crashes after motion indicates command, units, timing, or limits. Retest one joint before the full trajectory.
