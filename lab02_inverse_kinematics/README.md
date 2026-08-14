# Lab 2 - Inverse Kinematics

## Mission

**Move the UR5e to specified end-effector poses using your own inverse-kinematics solver and the FK model validated in Lab 1.**

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Success Criteria

You have completed the mission when:

- your planar IK returns both valid branches and rejects unreachable points;
- your numerical UR5e IK uses the Lab 1 FK rather than a simulator solver;
- at least two reachable target poses converge from multiple initial guesses;
- one unreachable target terminates with an explicit failure reason;
- a selected solution is checked for limits and executed smoothly in Webots;
- desired-versus-achieved position and orientation errors are reported; and
- you explain convergence, multiple solutions, damping, and failure behavior.

## Learning Objectives

- Solve planar analytical IK with branches and reachability checks.
- Define a six-dimensional pose-error vector.
- Construct a finite-difference task Jacobian from the Lab 1 FK.
- Implement pseudoinverse or damped least-squares IK with NumPy.
- Apply tolerances, step limits, joint limits, and iteration limits.
- Compare solutions from multiple initial guesses.
- Execute a safe IK solution and quantify achieved pose error.

## Prerequisites

Complete [Lab 1 - UR5e Frames and Forward Kinematics](../lab01_webots_ur5e_frames/README.md). Bring:

- passing transformation/FK tests;
- the finalized `forward_kinematics(q)` function;
- the fixed `T_6_tool` convention;
- the ordered UR5e device adapter;
- the tested smooth interpolation function; and
- the Lab 1 logger and pose-error calculations.

Do not reimplement FK in Lab 2. Import and reuse the tested Lab 1 module.

## Background

IK seeks `q` such that:

```text
T_world_tool(q) approximately equals T_target
```

At iteration `k`, form a six-dimensional task error:

```text
e = [p_target - p_current;
     orientation_error(R_current, R_target)]
```

Use the base-frame orientation-error convention assigned in lecture. One common small-angle form is:

```text
e_R = 0.5 * sum_i cross(R_current[:, i], R_target[:, i])
```

Construct a finite-difference task Jacobian from your Lab 1 FK, then compute a guarded update. For damped least squares:

```text
delta_q = J^T (J J^T + lambda^2 I)^(-1) e
q_next = q + alpha * delta_q
```

Use `numpy.linalg.solve` rather than explicitly forming a matrix inverse. Lab 3 later derives and studies the analytical geometric Jacobian; this lab uses finite differences only to support IK.

Webots may measure and visualize the result. It may not solve FK or IK for the submitted implementation.

## Provided Files

- `worlds/lab02_starter.wbt` - protected clean world with tool sensors
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/planar_fk.py` and `src/planar_ik.py` - analytical warm-up
- `src/numerical_ik.py` - pose error, finite-difference Jacobian, and IK scaffold
- `src/execute_pose_target.py` - mission integration scaffold
- `answers.md`

The transformation utilities, configuration reader, and UR5e FK starter were moved to Lab 1 with Git history preserved.

## Part 1 - Setup / Validation

Complete every checkpoint in order.

### Step 1 - Recheck the Lab 1 mathematical dependency

From the repository root:

```powershell
python .\lab01_webots_ur5e_frames\src\test_transforms.py
python -c "import numpy as np; from lab01_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; T=forward_kinematics(np.zeros(6)); print(T)"
```

Both commands must run successfully. If FK is incomplete or fails structural checks, return to Lab 1.

### Step 2 - Open and copy the Lab 2 world

1. Start Webots R2025a and keep it paused.
2. Select **File -> Open World...**.
3. Open `C:\eel4664-robotics-labs\lab02_inverse_kinematics\worlds\lab02_starter.wbt`.
4. Confirm the robot and floor render and the UR5e controller is `void`.
5. Immediately select **File -> Save World As...**.
6. Save beside the starter as `lab02_work.wbt`.
7. Confirm the title bar shows the working copy.

Never overwrite `lab02_starter.wbt`.

### Step 3 - Validate staged controller boundaries

1. **World:** Reset and run `void` for about two seconds.
2. **Minimal controller:** assign `diagnostic_minimal`, Reset, and confirm 10 completed steps.
3. **Devices:** assign `diagnostic_devices` and confirm all six motors, six joint sensors, `tool_position`, and `tool_orientation`.
4. **One joint:** repeat a conservative +0.05 rad shoulder-pan motion with the Lab 1 adapter.
5. **Full algorithm:** do not execute IK until offline convergence, limits, and all earlier stages pass.

Record pass/fail evidence in `answers.md`.

### Step 4 - Create the Lab 2 execution controller

Close Webots and run:

```powershell
Copy-Item .\lab01_webots_ur5e_frames\controllers\eel4664_ur5e .\lab02_inverse_kinematics\controllers\lab02_controller -Recurse
Rename-Item .\lab02_inverse_kinematics\controllers\lab02_controller\eel4664_ur5e.py lab02_controller.py
```

If `lab02_controller` already exists, do not copy again.

At the top of `lab02_controller.py`, add:

```python
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from lab01_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics
from lab01_webots_ur5e_frames.src.send_joint_goal import interpolate
```

This imports the tested Lab 1 implementation directly. Do not make a second FK copy in Lab 2.

### Step 5 - Confirm the controller import before motion

Temporarily leave the controller target equal to measured `q0` and print:

```python
print("FK import check:")
print(forward_kinematics(q0))
```

Assign `lab02_controller`, Reset, and run. Pass: a finite 4-by-4 matrix prints and the robot does not move.

### Step 6 - Record the setup checkpoint table

| Stage | Expected | Actual | Pass? |
|---|---|---|---|
| Lab 1 transforms/FK | offline tests pass | | |
| `void` world | stable world | | |
| `diagnostic_minimal` | 10 steps | | |
| `diagnostic_devices` | required devices listed | | |
| **One joint:** | +0.05 rad at joint 0 | | |
| FK import | finite 4-by-4 matrix, no motion | | |
| **Full algorithm:** | wait for Parts 2-3 | | |

## Part 2 - Core Implementation

### Step 7 - Complete the planar analytical warm-up

Implement `planar_3r_fk` and `planar_2r_ik`.

`planar_2r_ik(x, y, l1, l2)` must:

- check `|l1-l2| <= sqrt(x^2+y^2) <= l1+l2`;
- return both elbow-up and elbow-down branches when distinct;
- reconstruct the requested point with planar FK; and
- raise `ValueError` for an unreachable point.

Test at least:

1. a point strictly inside the workspace;
2. a point on a workspace boundary; and
3. an unreachable point.

Report both branches in radians and verify each with FK.

### Step 8 - Implement and unit-test pose error

In `src/numerical_ik.py`, implement `pose_error(T_current, T_target)`.

Pass these tests before continuing:

- identical transforms produce six zeros;
- +0.01 m target x translation produces the expected translational sign;
- a small positive target z rotation produces the expected rotational sign; and
- inputs not shaped `(4, 4)` are rejected.

State whether the rotational error is expressed in the base or body frame and keep that convention consistent with the Jacobian.

### Step 9 - Implement the finite-difference task Jacobian

Implement `finite_difference_jacobian(fk_fn, q, h)` using your Lab 1 FK.

Requirements:

- output shape `(6, 6)`;
- one column per joint in the required order;
- centered differences unless otherwise approved;
- translational and rotational rows use the same frame convention as `pose_error`; and
- `h` is configurable.

Evaluate at `h = 1e-3, 1e-4, 1e-5, 1e-6` rad. Select a value that balances truncation and floating-point error and justify it.

### Step 10 - Implement a guarded IK iteration

Complete `numerical_ik` with:

1. current pose from Lab 1 FK;
2. six-dimensional pose error;
3. finite-difference Jacobian;
4. damped least-squares update using `numpy.linalg.solve`;
5. step scale `alpha`;
6. maximum per-iteration joint step;
7. joint-limit enforcement;
8. separate position/orientation stopping tolerances;
9. maximum iteration count; and
10. returned residual history and failure reason.

Recommended starting values:

| Parameter | Initial value |
|---|---:|
| `alpha` | 0.3 |
| `lambda` | 0.02 |
| finite-difference `h` | `1e-5` rad |
| maximum `|delta_q_i|` | 0.10 rad/iteration |
| position tolerance | 0.001 m |
| orientation tolerance | 0.5 degrees |
| maximum iterations | 500 |

These are starting values, not guaranteed optimal values. Never allow NaN/Inf, silent nonconvergence, or unlimited iterations.

### Step 11 - Define reproducible reachable targets

Generate targets with the tested Lab 1 FK so their reachability is known:

```python
q_reference_a = np.array([0.20, -1.00, 1.10, -1.30, -1.00, 0.20])
q_reference_b = np.array([-0.40, -0.80, 0.90, -1.20, -1.20, -0.30])

T_target_a = forward_kinematics(q_reference_a)
T_target_b = forward_kinematics(q_reference_b)
```

The solver receives only `T_target` and an initial guess; it must not use `q_reference` internally.

For each target, solve from at least three seeds:

- measured Reset configuration;
- all zeros; and
- one instructor-approved nonsymmetric seed.

Save convergence flag, iterations, final position/orientation residual, final `q`, maximum step, and residual history.

### Step 12 - Test explicit failure

Create an unreachable target without changing its orientation:

```python
T_unreachable = T_target_a.copy()
T_unreachable[:3, 3] += np.array([1.5, 0.0, 0.0])
```

Pass: the solver stops at the iteration limit or an explicit guard and returns `converged=False` with a useful reason. It must not return the last iterate as though it were a valid solution.

### Step 13 - Select an executable solution

Before Webots motion, reject any candidate that:

- did not meet both tolerances;
- contains a nonfinite value;
- violates the stated joint limits;
- makes a discontinuous branch jump from measured `q0`; or
- fails the sampled joint-space path checks.

Among valid candidates, justify a selection criterion such as minimum wrapped joint distance from `q0`. IK endpoint convergence alone does not prove the path is safe.

Do not call Webots, SciPy, MoveIt, or another library's FK/IK solver.

## Part 3 - Robot Experiment

### Step 14 - Freeze the offline solver results

Before opening Webots motion, save a table containing every target/seed result. Mark each candidate accepted or rejected and give the reason. Preserve residual histories for all accepted solutions and at least one failed run.

### Step 15 - Integrate the selected solution

Complete `src/execute_pose_target.py` so it:

1. receives a target transform and measured `q0`;
2. calls your IK solver;
3. rejects nonconvergence or unsafe candidates;
4. verifies the endpoint with Lab 1 FK;
5. sends only an accepted `q_goal` to the Webots adapter;
6. uses the tested Lab 1 interpolation; and
7. logs desired/measured joints and measured tool pose.

Keep IK mathematics outside Webots device-I/O functions.

### Step 16 - Execute Target A

1. Open `lab02_work.wbt` paused.
2. Repeat `void -> diagnostic_minimal -> diagnostic_devices -> one joint` if the world or controller changed.
3. Assign `lab02_controller`.
4. Reset and read measured `q0`.
5. Recompute/select the valid Target A solution from that `q0`.
6. Print target pose, selected `q_goal`, predicted final pose, and safety checks.
7. Execute over at least 8 seconds.
8. Hold the final command.
9. Record measured final joints and tool pose.
10. Reset and repeat once to check reproducibility.

### Step 17 - Execute Target B or a second branch

Repeat Step 16 for Target B. If two valid IK solutions for one target are available and both paths are safe, the instructor may instead require execution of both branches.

Never send `T_unreachable` or any nonconverged result to the robot.

### Step 18 - Record achieved task-space error

For each executed trial:

1. evaluate Lab 1 FK at measured final `q`;
2. apply fixed `T_world_0` and `T_6_tool`;
3. compare predicted pose with the requested target;
4. compare the measured Webots tool pose with the target; and
5. distinguish solver residual, joint-tracking error, and model/simulator discrepancy.

The outcome is a UR5e that reaches Cartesian targets because of your own IK solver and previously validated FK model.

## Part 4 - Quantitative Analysis

For every target/seed pair, report:

- convergence status and failure reason;
- iteration count;
- final position and orientation residual;
- final joint vector;
- distance from the initial guess;
- maximum per-iteration joint step; and
- whether the candidate passed execution checks.

Plot residual norm versus iteration for at least:

1. a fast converging run;
2. a slower or differently seeded run; and
3. the unreachable target.

For each executed target, report:

```text
position_error = ||p_target - p_achieved||_2
R_error = R_target^T R_achieved
orientation_error = acos(clamp((trace(R_error)-1)/2, -1, 1))
```

Provide separate values using:

- the FK pose at the solver's `q_goal`;
- FK at measured final joints; and
- Webots measured tool pose.

This separates numerical convergence, joint tracking, and model discrepancy. Compare repeated trials and any multiple branches.

## Engineering Questions

1. Why does IK depend on an already validated FK model?
2. Why can different initial guesses converge to different joint vectors?
3. How do `alpha`, damping, and maximum step affect stability and speed?
4. Why are position and orientation tolerances reported separately?
5. Why is a small endpoint residual insufficient to guarantee safe execution?
6. How does the unreachable-target residual history differ from convergence?
7. Why must the finite-difference Jacobian use the same error-frame convention?
8. Which errors come from IK, tracking, and the nominal Webots model?

## What to Submit

- completed planar and numerical IK source;
- completed `execute_pose_target.py` and `lab02_controller`;
- checkpoint table and direct Lab 1 FK import evidence;
- planar branch/reachability tests;
- pose-error and finite-difference Jacobian tests;
- solver parameter table and safety limits;
- target/seed convergence table;
- residual-history plots including failure;
- Webots logs for both targets and the repeated trial;
- desired-versus-achieved position/orientation errors;
- multiple-solution and failure analysis; and
- completed `answers.md`.

Do not submit `lab02_work.wbt` unless requested.

## Troubleshooting

| Last passing stage | First failing stage | Likely problem |
|---|---|---|
| Lab 1 FK | Lab 2 import | repository path or module import |
| planar IK | pose-error tests | transform direction or error sign |
| pose error | Jacobian test | perturbation size, column order, or frame |
| Jacobian | IK convergence | damping, step, limits, or target |
| offline convergence | one-joint Webots check | controller/device boundary |
| one joint | full IK motion | unsafe selection, interpolation, or units |
| predicted endpoint | measured endpoint | tracking or model/tool-frame discrepancy |

If IK diverges, do not tune every parameter simultaneously. Save the failing residual history, test one target/seed offline, inspect one Jacobian column, and change one parameter at a time.

For a Webots failure, recover from `lab02_starter.wbt` and repeat `void -> minimal -> devices -> one joint`. Use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) for repeated crashes.
