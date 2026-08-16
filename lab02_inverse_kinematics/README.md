# Lab 2 - Inverse Kinematics

## Mission

**Specify Cartesian tool poses, solve for UR5e joint configurations with your own inverse kinematics, and make the robot reach those poses in Webots.**

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Success Criteria

You are finished when:

- planar IK produces both branches and rejects unreachable points;
- pose error and the finite-difference Jacobian pass offline tests;
- guarded damped-least-squares IK converges from multiple seeds;
- an unreachable target returns an explicit failure;
- two accepted solutions execute safely in Webots; and
- solver, tracking, and model errors are reported separately.

## Learning Objectives

- Explain why IK can have zero, one, or multiple solutions.
- Solve and verify planar analytical IK.
- Define a consistent position/orientation error.
- Estimate a task Jacobian using the Lab 1 FK model.
- Implement damped-least-squares IK with convergence and safety guards.
- Compare seed-dependent solutions and safely execute accepted results.

## Prerequisites

Complete [Lab 1 - UR5e Frames and Forward Kinematics](../lab01_webots_ur5e_frames/README.md). Reuse its tested `forward_kinematics(q)`, fixed `T_6_tool`, device adapter, and smooth joint interpolation. Do not copy or reimplement FK.

Complete the Python/NumPy prerequisites in [Lab 00](../lab00_setup/README.md).

## Background

### What IK solves

Forward kinematics maps joints to a pose:

```text
q -> T_world_tool(q)
```

Inverse kinematics asks for a joint vector that produces a requested pose:

```text
T_target -> q
```

Unlike FK, IK may have no solution, one boundary solution, or several joint-space branches. A numerical solver normally finds one nearby solution, so its initial guess matters.

### Planar analytical IK

For a two-link planar arm,

```text
x = l1 cos(q1) + l2 cos(q1 + q2)
y = l1 sin(q1) + l2 sin(q1 + q2)
```

A target radius `r = sqrt(x^2 + y^2)` is reachable only if

```text
|l1 - l2| <= r <= l1 + l2
```

The two branches follow from

```text
c2 = (x^2 + y^2 - l1^2 - l2^2) / (2 l1 l2)
s2 = +/- sqrt(1 - c2^2)
q2 = atan2(s2, c2)
q1 = atan2(y, x) - atan2(l2 s2, l1 + l2 c2)
```

The signs give elbow-up and elbow-down configurations. Verify every returned branch by substituting it into FK. Reject unreachable targets rather than returning NaN.

### Tool-frame target and pose error

Lab 1 FK ends at DH frame `{6}`, whereas Webots measures the tool. Use the one fixed Lab 1 alignment:

```python
def fk_tool(q):
    return forward_kinematics(q) @ T_6_tool
```

The solver receives `fk_tool`, so its current pose, target pose, and Webots measurement refer to the same frame. Never refit `T_6_tool` for a new target.

At iteration `k`, form a six-dimensional base-frame error:

```text
e = [e_p; e_R]
e_p = p_target - p_current
e_R = 0.5 * sum_i cross(R_current[:, i], R_target[:, i])
```

The rotational expression is a small-angle approximation. A sign or frame mismatch between this error and the Jacobian usually causes divergence.

### Finite-difference Jacobian and IK update

The task Jacobian relates a small joint change to a small pose change:

```text
e approximately equals J delta_q
```

Estimate column `j` by perturbing only joint `j` and using centered differences:

```text
q_plus  = q + h e_j
q_minus = q - h e_j
J[:, j] approximately equals task_difference(T_minus, T_plus) / (2h)
```

Large `h` causes truncation error; extremely small `h` amplifies floating-point error. Lab 3 later derives the analytical Jacobian.

Near ill-conditioning, use damped least squares:

```text
delta_q = J^T (J J^T + lambda^2 I)^(-1) e
q_next = q + alpha delta_q
```

Implement the solve without an explicit inverse:

```python
y = np.linalg.solve(J @ J.T + damping**2 * np.eye(6), error)
delta_q = J.T @ y
```

`alpha` controls progress, damping suppresses large updates, and a maximum joint step prevents jumps. Declare success only when both position and orientation tolerances pass. All other exits must return `converged=False` and a reason.

### What the final errors mean

Keep three effects separate:

1. **Solver error:** target versus `fk_tool(q_goal)`.
2. **Tracking effect:** `fk_tool(q_goal)` versus `fk_tool(q_measured)`.
3. **Model discrepancy:** `fk_tool(q_measured)` versus the Webots measurement.

Webots may measure and visualize the result. It may not solve FK or IK for the submitted work.

## Provided Files

- `worlds/lab02_starter.wbt` - protected UR5e world
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/planar_fk.py` and `src/planar_ik.py`
- `src/numerical_ik.py` - numerical IK scaffold
- `src/execute_pose_target.py` - safe execution scaffold
- `answers.md` - results template

## Part 1 - Setup / Validation

### Step 1 - Open, copy, and validate

1. From the repository root, verify the Lab 1 dependency:

   ```powershell
   python .\lab01_webots_ur5e_frames\src\test_transforms.py
   python -c "import numpy as np; from lab01_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; print(forward_kinematics(np.zeros(6)))"
   ```

2. Open `lab02_inverse_kinematics\worlds\lab02_starter.wbt` in Webots R2025a while paused.
3. Confirm the robot and floor render and the controller is `void`.
4. Immediately choose **File -> Save World As...** and create `lab02_work.wbt` beside the starter.
5. Validate the working copy in order:

   | Stage | Expected result |
   |---|---|
   | world with `void` | stable; no movement |
   | `diagnostic_minimal` | 10 completed steps; no movement |
   | `diagnostic_devices` | six motors, six sensors, and tool sensors; no movement |
   | **One joint:** Lab 1 controller | shoulder pan changes by only +0.05 rad |
   | **Full algorithm:** | wait until Steps 2-6 pass |

Record pass/fail in `answers.md`. Stop at the first failure.

**Never overwrite `lab02_starter.wbt`.** Discard a damaged working copy and recreate it from the starter.

## Part 2 - Core Implementation

### Step 2 - Solve the planar warm-up

Implement `planar_2r_fk` and `planar_2r_ik` using the Background equations. Test:

- one interior point, including both branches and FK reconstruction error;
- one workspace-boundary point; and
- one unreachable point that raises `ValueError`.

### Step 3 - Implement pose error and the task Jacobian

In `src/numerical_ik.py`:

1. Implement `pose_error(T_current, T_target)` and validate input shapes and finite values.
2. Test identical poses, a +0.01 m target-x change, and a small positive target-z rotation.
3. Implement a centered-difference `finite_difference_jacobian(fk_fn, q, h)`.
4. Confirm a finite `(6, 6)` result at a nonsymmetric `q`.
5. Compare `h = 1e-3, 1e-4, 1e-5, 1e-6` rad and justify one selection.

Use the same base-frame orientation convention in both functions.

### Step 4 - Implement guarded numerical IK

Complete `damped_least_squares_step` and `numerical_ik`. Each iteration must calculate `fk_fn(q)`, save position/orientation residuals, test both tolerances, calculate a damped update, limit the joint step, and enforce joint limits. Return an `IKResult` for success and every failure condition.

Use these starting values:

| Parameter | Initial value |
|---|---:|
| `alpha` | 0.3 |
| damping | 0.02 |
| finite-difference `h` | `1e-5` rad |
| maximum `|delta_q_i|` | 0.10 rad |
| position tolerance | 0.001 m |
| orientation tolerance | 0.5 degrees |
| maximum iterations | 500 |

Reject invalid inputs, NaN/Inf, limit violations, and iteration-limit exits. Change only one tuning parameter at a time.

### Step 5 - Test reachable targets, seeds, and failure

Create `fk_tool` with the fixed `T_6_tool`, then generate known-reachable targets:

```python
q_reference_a = np.array([0.20, -1.00, 1.10, -1.30, -1.00, 0.20])
q_reference_b = np.array([-0.40, -0.80, 0.90, -1.20, -1.20, -0.30])
T_target_a = fk_tool(q_reference_a)
T_target_b = fk_tool(q_reference_b)
```

The solver receives only a target and seed; it must not use `q_reference` internally. Solve each target from the measured Reset configuration, all zeros, and one nonsymmetric seed.

Test failure with:

```python
T_unreachable = T_target_a.copy()
T_unreachable[:3, 3] += np.array([1.5, 0.0, 0.0])
```

Save convergence, reason, iterations, residuals, final `q`, and residual history. Plot a fast run, a slower/different-seed run, and the unreachable run.

Select one solution per reachable target. Reject nonconverged, nonfinite, limit-violating, discontinuous, or path-unsafe candidates. Prefer a valid solution near measured `q0`. Do not use Webots, SciPy, MoveIt, or another library to solve FK/IK.

## Part 3 - Robot Experiment

### Step 6 - Connect the solver to Webots safely

1. Close Webots. If `controllers\lab02_controller` does not exist, run:

   ```powershell
   Copy-Item .\lab01_webots_ur5e_frames\controllers\eel4664_ur5e .\lab02_inverse_kinematics\controllers\lab02_controller -Recurse
   Rename-Item .\lab02_inverse_kinematics\controllers\lab02_controller\eel4664_ur5e.py lab02_controller.py
   ```

2. Add the repository root to `lab02_controller.py`:

   ```python
   from pathlib import Path
   import sys

   REPO_ROOT = Path(__file__).resolve().parents[3]
   sys.path.insert(0, str(REPO_ROOT))
   ```

3. Import Lab 1 FK/interpolation and the Lab 2 mission functions; do not copy the FK source.
4. Complete `prepare_pose_mission` so it accepts only converged, finite, limit-safe solutions and verifies the endpoint with `fk_tool`.
5. Complete `execute_pose_mission` so it interpolates from measured `q0`, commands all joints, holds the goal, and logs joints/tool pose.
6. First set `q_goal = q0`; confirm a finite pose prints and the robot does not move.

### Step 7 - Execute Target A and Target B

For each target:

1. Open `lab02_work.wbt` paused, assign `lab02_controller`, and **Reset**.
2. Read measured `q0` and select a validated solution near it.
3. Print convergence, `q_goal`, predicted endpoint, joint-limit check, and sampled-path check.
4. Stop without motion if any check fails.
5. Otherwise execute a smooth move lasting at least eight seconds and hold the goal.
6. Record measured final joints and Webots tool pose.
7. Reset and repeat once for reproducibility.

Never command the unreachable target or a failed result. Execute multiple branches only if assigned and both paths pass safety checks.

## Part 4 - Quantitative Analysis

### Step 8 - Separate and interpret the errors

For both targets and repeated trials, calculate:

```text
solver error:         T_target versus fk_tool(q_goal)
measured-joint error: T_target versus fk_tool(q_measured)
Webots error:         T_target versus T_webots_measured
```

For each comparison use

```text
position_error = ||p_target - p_achieved||
R_error = R_target^T R_achieved
orientation_error = acos(clamp((trace(R_error) - 1) / 2, -1, 1))
```

Report position in millimeters and orientation in degrees in one table. Identify the dominant error layer. Also state whether different seeds found the same joint vector or different branches and which accepted solution required less joint travel.

## Engineering Questions

1. Why must IK reuse an already validated FK model?
2. Why can different seeds produce different joint vectors for one pose?
3. How do `alpha`, damping, and maximum joint step affect convergence?
4. Why are position and orientation tolerances checked separately?
5. Why does endpoint convergence not guarantee safe execution?
6. How does an unreachable-target residual history differ from convergence?
7. How do the three error layers locate a problem?

## What to Submit

- completed four source scaffolds and the Lab 2 controller folder;
- completed `answers.md`;
- planar branch/reachability and numerical unit-test evidence;
- target/seed table and three residual plots, including failure;
- Webots logs for two targets and repeated trials;
- three-layer error table; and
- Engineering Question answers.

Do not submit `lab02_work.wbt`, vendor assets, or caches unless requested.

## Troubleshooting

| Last passing stage | First failing stage | Likely problem |
|---|---|---|
| Lab 1 tests | import | path or incomplete Lab 1 work |
| planar IK | pose error | transform direction, sign, or frame |
| pose error | Jacobian | perturbation, joint order, or rotation convention |
| Jacobian | convergence | seed, damping, step, limits, or target |
| offline solver | stationary controller | import boundary |
| stationary controller | motion | safety rejection, adapter, interpolation, or units |
| FK at measured joints | Webots pose | fixed tool transform or model discrepancy |

If IK diverges, inspect one residual history and one Jacobian column, then change one parameter at a time.

For Webots recovery, reopen the protected starter, create a fresh working copy, repeat `void -> minimal -> devices -> one joint`, and run the stationary import test before full motion. See [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) for repeated crashes.