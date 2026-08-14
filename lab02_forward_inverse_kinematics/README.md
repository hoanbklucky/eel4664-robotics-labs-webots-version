# Lab 2 - Forward and Inverse Kinematics

## Mission

**Move the UR5e to a specified end-effector pose using your own kinematics.**

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

Open `worlds/lab02_starter.wbt` paused and immediately use **File -> Save World As...** to create `worlds/lab02_work.wbt`.

## Success Criteria

You have completed the mission when:

- your FK passes unit tests and predicts Webots tool pose with quantified error;
- your IK solver reaches at least one assigned target without a built-in solver;
- the UR5e executes the computed joint solution safely;
- desired-versus-achieved position and orientation errors are reported; and
- you explain multiple solutions, joint limits, reachability, and one failure case.

## Learning Objectives

- Implement homogeneous transforms and a six-link UR5e FK chain.
- Validate FK against simulator ground truth.
- Implement analytical planar IK and numerical UR5e IK.
- Handle pose error, convergence, reachability, joint limits, and multiple solutions.
- Command an IK solution through the Lab 1 device adapter.
- Interpret model-versus-simulation discrepancy quantitatively.

## Prerequisites

Complete Lab 1 and the [setup prerequisites](../setup/README.md). Bring your ordered joint list, frame convention, transform functions, and working Webots adapter. Review FK/IK derivations completed in lecture, homework, or class.

## Background

For a serial chain:

```text
T_0_6(q) = T_0_1(q1) T_1_2(q2) ... T_5_6(q6)
```

Your FK constructs this ordered product with the instructor-approved parameters and explicit base/tool offsets.

IK seeks `q` whose predicted pose matches a target. In this lab, the iterative UR5e solver uses your FK and a finite-difference task Jacobian constructed from that FK. Lab 3 later derives the geometric Jacobian. Webots may measure the final pose but may not solve FK or IK.

## Provided Files

- `worlds/lab02_starter.wbt`
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/transforms.py` and `src/test_transforms.py`
- `src/planar_fk.py` and `src/planar_ik.py`
- `src/ur5e_fk_starter.py`
- `src/read_configuration.py`
- `src/numerical_ik.py`
- `src/execute_pose_target.py` - mission integration scaffold
- `answers.md`

## Part 1 - Setup / Validation

1. **World:** create `lab02_work.wbt` and verify it with controller `void`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm the six joints and validation devices.
4. **One joint:** move one joint slightly and confirm ordered sensing and tool-motion sign.
5. **Full algorithm:** run the pose mission only after stages 1-4 pass.

Run `test_transforms.py` and planar warm-up cases before connecting Webots.

## Part 2 - Core Implementation

1. Implement `rotx`, `roty`, `rotz`, `homogeneous`, and `invert_transform`.
2. Implement planar FK and both planar 2R IK branches with reachability checks.
3. Enter the approved UR5e parameter table and implement `dh_transform` and `forward_kinematics`.
4. Complete `numerical_ik.py` with:
   - position and orientation error;
   - finite-difference task Jacobian;
   - pseudoinverse or damped least-squares update;
   - step size, tolerance, and iteration limit;
   - joint-limit handling; and
   - residual history.
5. Complete `execute_pose_target.py` without placing mathematics inside the Webots adapter.

Do not call Webots, SciPy, MoveIt, or another library's FK/IK solver.

## Part 3 - Robot Experiment

1. Record at least five Webots joint configurations, including a nonsymmetric pose.
2. Predict each end-effector transform with FK before reading ground truth.
3. Define the assigned target pose and check workspace/joint-limit feasibility.
4. Run IK from multiple initial guesses and select a valid solution.
5. Command the chosen `q` with a smooth transition.
6. Hold the final pose and record measured joint and tool state.
7. Repeat for a second target or branch when assigned.
8. Include one near-boundary or unreachable target to demonstrate correct failure handling.

The final robotic outcome is a UR5e that reaches a Cartesian target because of your own FK/IK implementation.

## Part 4 - Quantitative Analysis

- Tabulate FK position/orientation error for at least five configurations.
- Plot IK residual versus iteration.
- Report iterations, final residual, and selected solution for each target.
- Compute target-versus-achieved position and orientation error.
- Compare multiple initial guesses or solution branches.
- Diagnose errors from parameters, offsets, joint tracking, and conventions.

## Engineering Questions

1. Why does transform multiplication order matter?
2. Which base/tool offset is required by your model?
3. Why can multiple joint configurations reach the same pose?
4. How do initial guess, damping, and step size affect convergence?
5. Why does a small IK residual not guarantee a safe executable path?
6. Which discrepancy most likely indicates a frame-convention error?

## What to Submit

- transformation, FK, IK, and mission-adapter source;
- convention and parameter table;
- unit-test output and FK validation table;
- IK convergence histories and solution comparison;
- Webots evidence that the robot reaches the target;
- desired-versus-achieved pose errors;
- failure analysis; and
- `answers.md`.

## Troubleshooting

Validate transforms, then FK, then the finite-difference Jacobian, then IK, and only then Webots execution. Large error at every pose usually indicates joint order, units, offsets, or transform direction. Restore `lab02_starter.wbt` and use the shared troubleshooting guide for simulator failures.