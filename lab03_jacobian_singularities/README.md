# Lab 3 - Jacobian, Differential Kinematics, and Singularities

## Mission

**Move the end effector along a Cartesian direction and experimentally demonstrate what happens near a singularity.**

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

Open `worlds/lab03_starter.wbt` paused and immediately use **File -> Save World As...** to create `worlds/lab03_work.wbt`.

## Success Criteria

You have completed the mission when:

- your geometric Jacobian agrees with finite differences;
- the UR5e executes a commanded Cartesian-direction motion away from singularity;
- singularity metrics are plotted or tabulated along an approach;
- normal and near-singular behavior are compared quantitatively; and
- you identify the physical Cartesian motion direction that is lost or degraded.

## Learning Objectives

- Derive and implement the UR5e geometric Jacobian.
- Verify `twist = J(q) qdot` using finite differences and Webots motion.
- Implement pseudoinverse and damped least-squares Cartesian motion.
- Measure minimum singular value, rank, condition number, and manipulability.
- Relate numerical conditioning to joint-rate amplification and physical mobility.
- Enforce safe joint, rate, and conditioning limits.

## Prerequisites

Complete Lab 2 and the [setup prerequisites](../lab00_setup/README.md). Bring tested FK, transform utilities, frame convention, and Webots adapter. Review Jacobians and singularities from lecture/homework.

## Background

For small motion:

```text
twist = J(q) qdot
delta_x approximately J(q) delta_q
```

A pseudoinverse maps Cartesian velocity to joint velocity. Near a singularity, at least one singular value approaches zero, some Cartesian motion direction becomes difficult or impossible, and requested joint rates may grow sharply. Damped least squares bounds commands by accepting task-space error.

Webots measures the resulting motion; it must not compute the assigned Jacobian or inverse differential solution.

## Provided Files

- `worlds/lab03_starter.wbt`
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/jacobian_starter.py`
- `src/singularity_scan.py`
- `src/cartesian_direction_motion.py` - mission integration scaffold
- `answers.md`

## Part 1 - Setup / Validation

1. **World:** create `lab03_work.wbt` and verify controller `void`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm ordered joint sensing.
4. **One joint:** move one joint slightly and verify predicted tool-motion direction.
5. **Full algorithm:** enable Cartesian and near-singular experiments only after stages 1-4 pass.

Import your Lab 2 FK rather than duplicating it. Establish conservative joint-rate, joint-limit, and condition-number stop thresholds before motion.

## Part 2 - Core Implementation

1. Implement the geometric Jacobian in the assigned frame.
2. Add centered finite-difference verification for translational and rotational columns.
3. Implement an SVD pseudoinverse and damped least squares explicitly with NumPy.
4. Complete `singularity_scan.py` to record `sigma_min`, rank, condition number, manipulability, and `q`.
5. Complete `cartesian_direction_motion.py` with step size, damping, saturation, and stop conditions.
6. Keep Webots sensing/actuation separate from Jacobian mathematics.

## Part 3 - Robot Experiment

1. Select a well-conditioned starting pose.
2. Command a small tool displacement or velocity along the assigned Cartesian direction.
3. Log requested, predicted, and measured motion.
4. Approach an instructor-approved near-singular configuration in conservative increments.
5. Repeat a comparable Cartesian request.
6. Stop before rate/conditioning thresholds are violated.
7. Repeat near-singular motion with damping and compare behavior.

The final robotic outcome is a visible Cartesian-direction motion whose degradation near singularity is predicted by your metrics.

## Part 4 - Quantitative Analysis

- Plot finite-difference Jacobian error versus perturbation size.
- Plot `sigma_min` and condition number versus time or approach parameter.
- Compare normal and near-singular joint-rate norm.
- Compare predicted and measured Cartesian velocity/displacement.
- Compare damped and undamped tracking error and command magnitude.
- Identify the singular-vector direction associated with degraded mobility.

## Engineering Questions

1. What physical tool direction corresponds to the smallest singular value?
2. Why can a modest Cartesian request demand extreme joint rates?
3. Why is determinant alone inadequate for many Jacobians?
4. How does damping trade Cartesian accuracy for numerical safety?
5. How do you distinguish a frame/sign error from a real singularity?
6. Which safeguards prevented unsafe motion?

## What to Submit

- Jacobian derivation and implementation;
- finite-difference validation;
- Cartesian-direction controller and logs;
- singularity metric plot/table;
- normal versus near-singular comparison;
- damped versus undamped result;
- physical interpretation; and
- `answers.md`.

## Troubleshooting

Validate FK first, then one Jacobian column, then all columns, then a tiny Cartesian command. A sudden sign/frame discrepancy is not evidence of singularity. Stop if joint-rate, joint-limit, or conditioning thresholds are exceeded. Recover from `lab03_starter.wbt` after world/controller failures.