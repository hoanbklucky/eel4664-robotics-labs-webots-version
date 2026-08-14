# Lab 3 - Jacobian, Differential Kinematics, and Singularities

**Do not save over the original starter world after running the simulation. Immediately save a working copy; reset/revert before preserving world changes.**

## Learning objectives

By the end of this lab, you should be able to:

1. derive and implement the UR5e geometric Jacobian from your FK chain;
2. verify Jacobian columns numerically;
3. validate the differential relationship between joint and tool velocity;
4. command a small Cartesian displacement using inverse/pseudoinverse methods;
5. measure rank, singular values, condition number, and manipulability; and
6. explain the physical loss of mobility near a singular configuration.

## Prerequisites

Complete Lab 2 and bring your tested FK, transform utilities, frame convention, and Webots adapter. Review Jacobian and singularity derivations from lecture/homework.

## Background

For small motion,

```text
twist = J(q) qdot
delta_x approximately J(q) delta_q
```

A pseudoinverse maps a requested Cartesian velocity to joint velocity. Near a singularity, one or more singular values approach zero, some Cartesian directions become difficult or impossible, and the requested joint velocity may become very large. Damped least squares trades exact tracking for bounded commands.

Use NumPy linear algebra to implement and inspect these relationships. Webots visualizes and measures the result; it must not compute the assigned Jacobian or Cartesian command.

## Provided files

- `worlds/lab03_starter.wbt`
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/jacobian_starter.py` - numerical checker and analytical starter
- `src/singularity_scan.py` - singular-value/condition-number starter
- `answers.md`

The singularity starter was moved from the former standalone singularities lab.

## Required Webots workflow and recovery

1. **World:** open `worlds/lab03_starter.wbt` paused and use **File -> Save World As...** to create `worlds/lab03_work.wbt`; verify `void`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm ordered joint sensing.
4. **One joint:** command one small joint displacement and verify the sign of measured tool motion.
5. **Full algorithm:** enable Cartesian motion and singularity experiments only after stages 1-4 pass.

Restore from `lab03_starter.wbt` after a bad edit. Use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) to separate world, Python, device, and motion failures.

## Step-by-step instructions

1. Import your Lab 2 FK without duplicating it.
2. Implement the geometric Jacobian in the frame specified by the instructor.
3. Verify every column with centered finite differences over several step sizes.
4. Select a well-conditioned configuration and compare predicted versus measured tool velocity.
5. Implement pseudoinverse and damped least-squares Cartesian motion.
6. Command a small Cartesian displacement with joint-rate and joint-limit checks.
7. Scan or approach a prescribed near-singular configuration safely.
8. Compare metrics and required joint velocities at well-conditioned and near-singular poses.

## Implementation tasks

1. Replace the analytical-Jacobian TODO in `jacobian_starter.py`.
2. Add centered finite-difference verification for both translational and rotational components.
3. Implement SVD-based pseudoinverse and damped least squares explicitly with NumPy.
4. Complete `singularity_scan.py` to record:
   - singular values;
   - numerical rank;
   - condition number;
   - manipulability measure; and
   - the joint configuration.
5. Enforce joint-position and joint-velocity limits before sending commands.
6. Log simulation time, `q`, `qdot`, requested twist, predicted twist, measured motion, and singularity metrics.

## Required experiments

### Experiment A - Jacobian verification

At several nonsymmetric configurations, plot finite-difference error versus perturbation size and explain truncation/roundoff behavior.

### Experiment B - differential Cartesian motion

At a well-conditioned pose, request a small displacement or velocity. Compare `J qdot` with measured tool motion and report translational/orientation error.

### Experiment C - near-singular behavior

Repeat a comparable Cartesian request near a singularity. Compare singular values, rank/condition number, joint-rate norm, tracking error, and damped versus undamped behavior.

## Questions and reflection

1. What physical tool direction corresponds to the smallest singular value?
2. Why can a modest Cartesian request produce extreme joint rates?
3. Why is the determinant alone an incomplete metric for a non-square or scaled Jacobian?
4. How does damping change tracking error and command magnitude?
5. Which safeguards prevented the singularity experiment from becoming unsafe?

## What to submit

Submit:

- Jacobian derivation and source;
- finite-difference validation plot;
- Cartesian-motion log and error metrics;
- singularity scan/approach data;
- well-conditioned versus near-singular comparison;
- physical interpretation; and
- `answers.md`.

## Troubleshooting

Validate FK first, then one Jacobian column, then all columns, then pseudoinverse motion. A sudden sign/frame error is not a singularity. Stop motion if joint-rate limits, joint limits, or conditioning thresholds are exceeded.