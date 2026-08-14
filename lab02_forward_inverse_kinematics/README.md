# Lab 2 - Forward and Inverse Kinematics

**Do not save over the original starter world after running the simulation. Immediately save a working copy; reset/revert before preserving world changes.**

## Learning objectives

By the end of this lab, you should be able to:

1. implement and test homogeneous-transform utilities;
2. compute a UR5e end-effector pose from a measured joint vector using your own FK;
3. validate FK position and orientation against Webots ground truth;
4. solve planar analytical IK and iterative UR5e IK;
5. command a converged IK solution safely; and
6. quantify desired-versus-achieved pose error and explain failure cases.

## Prerequisites

Complete Lab 1. Bring your frame convention, ordered joint list, transformation functions, and working Webots device adapter. Review the FK/IK derivations completed in lecture, homework, or class.

## Background

For a six-joint serial chain,

```text
T_0_6(q) = T_0_1(q1) T_1_2(q2) ... T_5_6(q6)
```

Your FK must construct this ordered product using the instructor-approved UR5e parameters and explicitly stated base/tool offsets.

IK finds `q` such that the predicted pose matches a target. The analytical planar warm-up exposes branches and reachability. The UR5e solver uses your FK and a finite-difference task Jacobian constructed from that FK, with an explicit pose-error vector, convergence tolerance, iteration limit, and joint-limit handling. Lab 3 later derives and analyzes the geometric Jacobian.

Webots may supply measured tool pose only after your prediction is computed. Do not call a simulator, SciPy, MoveIt, or third-party FK/IK solver.

## Provided files

- `worlds/lab02_starter.wbt` - protected known-good world
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/transforms.py` and `src/test_transforms.py`
- `src/planar_fk.py` and `src/planar_ik.py`
- `src/ur5e_fk_starter.py`
- `src/read_configuration.py`
- `src/numerical_ik.py`
- `answers.md`

These files were consolidated from the former homogeneous-transform, FK, and IK labs.

## Required Webots workflow and recovery

1. **World:** open `worlds/lab02_starter.wbt` paused and use **File -> Save World As...** to create `worlds/lab02_work.wbt`; confirm `void` runs.
2. **Minimal controller:** assign `diagnostic_minimal`, Reset, and confirm startup.
3. **Devices:** assign `diagnostic_devices`, Reset, and confirm the six joints and validation sensors.
4. **One joint:** use the Lab 1 adapter to move one joint slightly and confirm ordered sensing.
5. **Full algorithm:** run FK/IK validation only after stages 1-4 pass.

Recover from `lab02_starter.wbt` and use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) if any earlier stage fails.

## Step-by-step instructions

1. Create `lab02_work.wbt` and complete the staged checks.
2. Complete and test the transformation utilities.
3. Complete planar FK/IK warm-ups and verify selected cases independently.
4. Enter the approved six-row UR5e parameter table and fixed frame offsets.
5. Record at least five Webots joint configurations, including home and a nonsymmetric pose.
6. Compute FK for every measured `q` before reading ground truth.
7. Define reachable target poses and solve IK from multiple initial guesses.
8. Command converged solutions with a smooth joint transition.
9. Measure final position and orientation error.

## Implementation tasks

1. Implement `rotx`, `roty`, `rotz`, `homogeneous`, and `invert_transform` in `transforms.py`.
2. Implement `planar_3r_fk` and both branches of `planar_2r_ik`, including reachability checks.
3. Implement `dh_transform` and `forward_kinematics` in `ur5e_fk_starter.py`.
4. Complete `numerical_ik.py` using a finite-difference Jacobian from your own FK (not Webots) and include:
   - position and orientation error;
   - pseudoinverse or damped least-squares update;
   - step-size control;
   - joint limits;
   - convergence and iteration limits; and
   - a recorded residual history.
5. Keep Webots sensing/actuation outside the mathematical functions.

## Required experiments

### Experiment A - FK validation

Evaluate at least five configurations. For each, report measured `q`, predicted tool transform, simulator reference, position error, and orientation error.

### Experiment B - IK convergence

Use at least three reachable targets and multiple initial guesses. Report convergence, iterations, final residual, and selected solution branch.

### Experiment C - execution accuracy and failure

Command at least two converged solutions and measure desired-versus-achieved pose error. Include one near-boundary or unreachable target and explain how the solver detects failure.

## Questions and reflection

1. Why does transform multiplication order matter?
2. Which fixed base/tool offset is required by your convention?
3. Why can multiple joint vectors represent the same tool pose?
4. How do initial guess, damping, and step size affect numerical IK?
5. Is a small IK residual sufficient to guarantee safe executable motion? Why?

## What to submit

Submit:

- completed transformation, FK, and IK source;
- parameter/convention table;
- unit-test output;
- FK comparison table/plots;
- IK convergence histories;
- commanded-versus-achieved pose errors;
- one failure analysis; and
- `answers.md`.

## Troubleshooting

If FK error is large at every configuration, check joint order, angle offsets, units, transform direction, and base/tool frames before changing parameters. If IK diverges, test the error vector and Jacobian independently. If Webots fails, return to the last staged validation boundary and consult the shared troubleshooting guide.