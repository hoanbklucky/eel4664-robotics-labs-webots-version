# Lab 4 - Trajectory Generation and Tracking

**Do not save over the original starter world after running the simulation. Immediately save a working copy; reset/revert before preserving world changes.**

## Learning objectives

By the end of this lab, you should be able to:

1. implement cubic and/or quintic joint-space interpolation;
2. evaluate desired joint position, velocity, and acceleration at simulation timestamps;
3. execute a synchronized six-joint trajectory in Webots;
4. compare desired and measured motion quantitatively;
5. evaluate smoothness, duration, limits, and sampling effects; and
6. optionally compare joint-space motion with a Cartesian waypoint strategy.

## Prerequisites

Complete Labs 1-3. Bring the UR5e joint ordering, device adapter, FK, and safe motion checks. The polynomial coefficient derivations may be completed in lecture, homework, or class; this lab focuses on implementation and experimental behavior.

## Background

A trajectory is a time-parameterized reference, not just a sequence of poses. Endpoint position/velocity/acceleration constraints determine polynomial coefficients. The controller must sample the reference using `robot.getTime()` and command all joints consistently.

At minimum evaluate tracking with:

```text
e_i(t) = q_des,i(t) - q_meas,i(t)
RMSE = sqrt(mean(e_i(t)^2))
```

Also inspect maximum error and whether requested velocity/acceleration violates stated limits.

## Provided files

- `worlds/lab04_starter.wbt`
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/cubic_trajectory.py` - coefficient/evaluation starter
- `src/send_trajectory.py` - Webots execution outline
- `answers.md`

## Required Webots workflow and recovery

1. **World:** open `worlds/lab04_starter.wbt` paused and use **File -> Save World As...** to create `worlds/lab04_work.wbt`; verify `void`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm motors/sensors.
4. **One joint:** execute a low-speed one-joint polynomial and compare desired/measured position.
5. **Full algorithm:** run synchronized six-joint trajectories only after stages 1-4 pass.

Recover from `lab04_starter.wbt` after a bad edit and use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) to isolate world, controller, device, or motion failures.

## Step-by-step instructions

1. Implement and unit-test the polynomial generator without Webots.
2. Check endpoint constraints numerically.
3. Select safe `q0`, `qf`, duration, and joint limits.
4. Create `lab04_work.wbt` and complete staged validation.
5. Execute the same motion with at least two durations.
6. Log desired/measured `q` and desired `qdot`/`qddot` at simulation timestamps.
7. Plot each joint's position and velocity; include acceleration when required.
8. Compute tracking and smoothness metrics.
9. If assigned, compare the joint-space trajectory with Cartesian waypoints generated using your Lab 2/3 algorithms.

## Implementation tasks

1. Complete `cubic_coefficients` and `sample_cubic`.
2. Implement a quintic alternative or justify the instructor-approved cubic boundary conditions.
3. Complete `send_trajectory.py` as a Webots controller.
4. Clamp time before/after the motion and hold the final command safely.
5. Check joint position, velocity, and acceleration limits before execution.
6. Log commands and measurements separately; do not infer measured motion from commands.
7. Keep polynomial generation independent of Webots I/O.

## Required experiments

### Experiment A - endpoint and sampling validation

Demonstrate that the implemented trajectory satisfies its boundary conditions and compare at least two sampling periods offline.

### Experiment B - duration comparison

Execute the same `q0 -> qf` motion at two durations. Compare peak desired velocity/acceleration, RMSE, maximum error, and completion time.

### Experiment C - trajectory style or constraints

Compare cubic versus quintic smoothness, or compare MoveJ-style joint interpolation with an instructor-approved Cartesian/MoveL-style waypoint experiment. Identify any joint-limit, rate, or Cartesian-path tradeoff.

## Questions and reflection

1. Why does increasing duration usually reduce velocity and acceleration demand?
2. Which metric best exposes tracking performance in your experiment, and why?
3. How does discrete sampling change a continuous polynomial reference?
4. Why can a smooth joint trajectory produce a curved Cartesian path?
5. What must be checked before executing a Cartesian waypoint sequence?

## What to submit

Submit:

- polynomial source and endpoint tests;
- Webots trajectory controller;
- desired/measured CSV logs;
- position, velocity, and acceleration plots;
- RMSE and at least one additional metric;
- duration and smoothness comparison;
- constraint discussion; and
- `answers.md`.

## Troubleshooting

Test the polynomial without Webots first. Then run one joint at low speed. If all joints jump, verify time origin, units, joint order, and endpoint clamping. If tracking error is inconsistent between trials, confirm identical Reset state and simulation-time logging.