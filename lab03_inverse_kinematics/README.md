# Lab 3 - Inverse Kinematics

## Mission

**Choose Cartesian target poses, predict the required UR5e joint configurations with your own inverse-kinematics solver, command the robot in Webots, and measure how closely the stylus actually reaches each target pose.**

### Why measure in Webots?

On a physical UR5e, you would command the IK solution, measure the tool pose, and compare that measurement with the requested target. Because this course does not have access to a physical UR5e, Webots serves as the experimental robot. It preserves the same engineering workflow: **predict -> execute -> measure -> compare**.

A small target-to-measurement error supports the conclusion that the complete IK experiment worked. A large error does not automatically mean the IK mathematics is wrong; it may instead come from joint tracking, frame alignment, or a difference between your kinematic model and the Webots model. You will report these effects separately later in the lab. Webots is therefore a repeatable experimental reference, not a substitute for every source of uncertainty found on real hardware.

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
- Estimate a task Jacobian using the Lab 2 FK model.
- Implement damped-least-squares IK with convergence and safety guards.
- Compare seed-dependent solutions and safely execute accepted results.

## Prerequisites

Complete [Lab 2 - UR5e Frames and Forward Kinematics](../lab02_webots_ur5e_frames/README.md). Reuse its tested `forward_kinematics(q)`, fixed `T_6_tool`, device adapter, and smooth joint interpolation. Do not copy or reimplement FK.

Complete the Python/NumPy prerequisites in [Lab 00](../lab00_setup/README.md).


**Platform note:** The required workflow supports Windows, macOS, and Ubuntu when configured through Lab 00. Terminal examples use `python`; on macOS or Ubuntu, use `python3` instead if `python` is not recognized.

## Background

### 1. What inverse kinematics does

Suppose you want the stylus tip at a chosen location and orientation. You know the desired **tool pose**, but not the six joint angles that produce it.

| Problem | Given | Find |
|---|---|---|
| Forward kinematics (FK) | joint angles `q` | tool pose `T_world_tool(q)` |
| Inverse kinematics (IK) | desired pose `T_target` | joint angles `q` |

FK asks, "Where will the hand be if the joints have these angles?" IK asks, "How should the joints bend to put the hand here?"

IK can have no solution, one solution, or several solutions. For example, a target may be outside the workspace, or two different arm shapes may reach the same pose.

### 2. Start with a two-link arm

For a flat two-link arm,

```text
base --(q1)-- link l1 --(q2)-- link l2 --> target (x, y)
```

FK gives

```text
x = l1 cos(q1) + l2 cos(q1 + q2)
y = l1 sin(q1) + l2 sin(q1 + q2)
```

First calculate `r = sqrt(x^2 + y^2)`. The point is reachable only if

```text
|l1 - l2| <= r <= l1 + l2
```

For a reachable point,

```text
c2 = (x^2 + y^2 - l1^2 - l2^2) / (2 l1 l2)
s2 = +/- sqrt(1 - c2^2)
q2 = atan2(s2, c2)
q1 = atan2(y, x) - atan2(l2 s2, l1 + l2 c2)
```

The two signs of `s2` give elbow-up and elbow-down solutions. These are different IK **branches** that reach the same point. Check each answer by putting its angles back into FK. If the reachability test fails, report failure instead of returning NaN.

### 3. Solve the UR5e by improving a guess

Instead of deriving every UR5e branch, this lab uses a numerical loop:

```text
start with q
   -> calculate the current pose with FK
   -> measure the error to the target
   -> calculate a small joint correction
   -> update q and repeat
```

Because the process begins with a guess, different initial guesses can lead to different valid solutions.

### 4. Use the same tool frame everywhere

Lab 2 FK ends at DH frame `{6}`, while Webots measures the attached tool. Use the fixed Lab 2 alignment:

```python
def fk_tool(q):
    return forward_kinematics(q) @ T_6_tool
```

Use `fk_tool` for the current pose and target pose so they match the Webots tool frame. Never recalculate `T_6_tool` for a new target.

The tool-frame origin is at the stylus mount. The visible orange tip is the fixed point

```python
p_tool = np.array([0.0, 0.13, 0.0])
p_world_tip = transform_point(fk_tool(q), p_tool)
```

The stylus has no mass or collision geometry. It makes pose changes visible without changing the robot dynamics.

The starter also contains `TARGET_A` and `TARGET_B`. Each target has short red/green/blue pose axes at the tool-frame origin and a small translucent sphere at the desired stylus-tip point. These nodes are visual references only; the submitted solver must use the numerical `T_target`, not read target coordinates from Webots.

### 5. Describe the pose error

At each iteration, the solver compares the current tool pose with the target. Position error is

$$
\mathbf e_p = \mathbf p_{target} - \mathbf p_{current}.
$$

For example, suppose

```text
p_current = [0.50, 0.10, 0.30] m
p_target  = [0.52, 0.08, 0.31] m
```

Then

```text
e_p = [0.02, -0.02, 0.01] m
```

The tool must move 2 cm in world +x, 2 cm in world -y, and 1 cm in world +z.

Position alone is insufficient: the stylus may reach the correct point while pointing the wrong way. Use the small base-frame orientation error

$$
\mathbf e_R = \frac{1}{2}\sum_{i=1}^{3}
\left(\mathbf R_{current}[:,i] \times \mathbf R_{target}[:,i]\right).
$$

Each rotation-matrix column is one tool axis expressed in the base frame. If the target is rotated approximately 2 degrees about world +z from the current orientation, then

```text
e_R approximately equals [0, 0, 0.0349] rad
```

because 2 degrees is 0.0349 rad. Stack position and orientation vertically:

$$
\mathbf e =
\begin{bmatrix}
\mathbf e_p \\
\mathbf e_R
\end{bmatrix}
\in \mathbb R^6.
$$

Thus, `e[0:3]` describes translation and `e[3:6]` describes rotation. `pose_error` and the Jacobian must use the same frame and sign convention.

### 6. Estimate how each joint moves the tool

Let

$$
\Delta \mathbf q =
[\Delta q_1,\ldots,\Delta q_6]^T
$$

be a small change in the six joints. Let

$$
\Delta \mathbf x =
[\Delta p_x,\Delta p_y,\Delta p_z,
 \Delta \theta_x,\Delta \theta_y,\Delta \theta_z]^T
$$

be the resulting small tool-pose change. The task Jacobian gives the local linear approximation

$$
\boxed{\Delta \mathbf x \approx \mathbf J(\mathbf q)\,\Delta \mathbf q}.
$$

`J` is 6-by-6. Column `j` answers: "If only joint `j` changes by one small radian, how does the tool position and orientation change?"

Estimate that column by nudging joint `j` in both directions:

$$
\mathbf q^+ = \mathbf q + h\mathbf u_j,
\qquad
\mathbf q^- = \mathbf q - h\mathbf u_j,
$$

$$
\mathbf J[:,j] \approx
\frac{\mathbf e_{\mathrm{pose}}(T^-,T^+)}{2h},
\qquad
T^\pm = T_{\mathrm{tool}}(\mathbf q^\pm).
$$

Here, $\mathbf e_{\mathrm{pose}}$ is the pose difference calculated by `pose_error`, and $T_{\mathrm{tool}}(\mathbf q)$ is the transform returned by `fk_tool(q)`. The symbol `u_j` is zero except for a 1 at joint `j`. For example, if `h = 0.001` rad and the positive and negative evaluations differ by `0.0008` m in tool x, then that Jacobian entry is

```text
0.0008 / (2 * 0.001) = 0.4 m/rad
```

Repeat for all six joints. Large `h` gives a crude approximation; extremely small `h` exposes floating-point roundoff. Lab 4 derives the Jacobian directly.

### 7. Convert pose error into a joint correction

If the linear model were exact, we would solve

$$
\mathbf J\,\Delta\mathbf q = \mathbf e.
$$

Three common numerical choices are:

| Method | Basic idea | Limitation |
|---|---|---|
| Jacobian transpose | move along `J.T @ e` | simple but may converge slowly |
| pseudoinverse | use `pinv(J) @ e` | can create large changes near singularities |
| damped least squares | regularize the pseudoinverse | more stable; requires a damping value |

This lab uses damped least squares:

$$
\Delta\mathbf q =
\mathbf J^T\left(\mathbf J\mathbf J^T + \lambda^2\mathbf I\right)^{-1}\mathbf e,
$$

$$
\mathbf q_{next}=\mathbf q+\alpha\,\Delta\mathbf q.
$$

- `lambda` (`damping`) stabilizes difficult configurations.
- `alpha` controls how much of the proposed correction is applied.
- `max_joint_step` prevents any joint from changing too much in one iteration.

Do not form the inverse explicitly. Solve the linear system:

```python
y = np.linalg.solve(J @ J.T + damping**2 * np.eye(6), error)
delta_q = alpha * (J.T @ y)
delta_q = np.clip(delta_q, -max_joint_step, max_joint_step)
q_next = q + delta_q
```

Too little damping may produce large updates; too much damping may make convergence slow.

### 8. Put the numerical IK loop together

The complete idea is:

```python
q = q_seed.copy()

for iteration in range(max_iterations):
    T_current = fk_tool(q)
    error = pose_error(T_current, T_target)

    if position_error_passes and orientation_error_passes:
        return IKResult(q=q, converged=True, ...)

    J = finite_difference_jacobian(fk_tool, q, h)
    delta_q = alpha * damped_least_squares_step(J, error, damping)
    delta_q = limit_each_joint_step(delta_q)
    q = enforce_joint_limits(q + delta_q)

return IKResult(q=q, converged=False, reason="iteration limit", ...)
```

An illustrative residual history might look like this:

| Iteration | Position error | Orientation error | Largest proposed joint change |
|---:|---:|---:|---:|
| 0 | 90 mm | 12.0 deg | 0.10 rad |
| 10 | 31 mm | 4.2 deg | 0.08 rad |
| 25 | 6 mm | 1.1 deg | 0.04 rad |
| 42 | 0.7 mm | 0.3 deg | 0.01 rad |

With tolerances of 1 mm and 0.5 degrees, the last row converges because **both** errors pass. Real results will differ; the important pattern is that the residuals decrease without unstable jumps.

### 9. Stop safely and interpret the result

Return `converged=False` with a clear reason if the iteration limit is reached, a value becomes NaN/Inf, or joint limits prevent progress. Never command a failed result in Webots. Even a converged endpoint must pass joint-limit and sampled-path safety checks.

After execution, separate:

1. **solver error:** `T_target` versus `fk_tool(q_goal)`;
2. **tracking effect:** `fk_tool(q_goal)` versus `fk_tool(q_measured)`; and
3. **model discrepancy:** `fk_tool(q_measured)` versus the Webots tool measurement.

For example, a tiny solver error but a large Webots error suggests that the numerical IK converged and the remaining problem lies in tracking, frame alignment, or model mismatch. Webots may measure and visualize the result, but it may not solve FK or IK for you.

## Provided Files

- `worlds/lab03_starter.wbt` - protected UR5e world with stylus and two compact visual pose targets
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/planar_fk.py` and `src/planar_ik.py`
- `src/numerical_ik.py` - numerical IK scaffold
- `src/execute_pose_target.py` - safe execution scaffold
- `answers.md` - results template

## Part 1 - Setup / Validation

### Step 1 - Open, copy, and validate

1. From the repository root, verify the Lab 2 dependency:

   ```bash
   python lab02_webots_ur5e_frames/src/test_transforms.py
   python -c "import numpy as np; from lab02_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; print(forward_kinematics(np.zeros(6)))"
   ```

2. Open `lab03_inverse_kinematics/worlds/lab03_starter.wbt` in Webots R2025a while paused.
3. Confirm the robot, stylus, `TARGET_A`, and `TARGET_B` render and the controller is `void`. The target markers should appear as small colored axes with faint tip spheres, not as physical scene objects.
4. Immediately choose **File -> Save World As...** and create `lab03_work.wbt` beside the starter.
5. Validate the working copy in order:

   | Stage | Expected result |
   |---|---|
   | world with `void` | stable; no movement |
   | `diagnostic_minimal` | 10 completed steps; no movement |
   | `diagnostic_devices` | six motors, six sensors, and tool sensors; no movement |
   | **One joint:** Lab 2 controller | shoulder pan changes by only +0.05 rad |
   | **Full algorithm:** | wait until Steps 2-6 pass |

Record pass/fail in `answers.md`. Stop at the first failure.

**Never overwrite `lab03_starter.wbt`.** Discard a damaged working copy and recreate it from the starter.

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
q_reference_a = np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30])
q_reference_b = np.array([-0.30, -0.90, 1.10, -1.40, -1.20, -0.20])
T_target_a = fk_tool(q_reference_a)
T_target_b = fk_tool(q_reference_b)
```

The displayed `TARGET_A` and `TARGET_B` frames correspond to these two known-reachable configurations. They let you see whether the stylus reaches the requested pose, but they are not solver inputs. The solver receives only a target and seed; it must not use `q_reference` internally. Solve each target from the measured Reset configuration, all zeros, and one nonsymmetric seed.

Test failure with:

```python
T_unreachable = T_target_a.copy()
T_unreachable[:3, 3] += np.array([1.5, 0.0, 0.0])
```

Save convergence, reason, iterations, residuals, final `q`, and residual history. Plot a fast run, a slower/different-seed run, and the unreachable run.

Select one solution per reachable target. Reject nonconverged, nonfinite, limit-violating, discontinuous, or path-unsafe candidates. Prefer a valid solution near measured `q0`. Do not use Webots, SciPy, MoveIt, or another library to solve FK/IK.

## Part 3 - Robot Experiment

### Step 6 - Connect the solver to Webots safely

1. Close Webots. If `controllers/lab03_controller` does not exist, run this cross-platform command from the repository root:

   ```bash
   python -c "from pathlib import Path; import shutil; src=Path('lab02_webots_ur5e_frames/controllers/eel4664_ur5e'); dst=Path('lab03_inverse_kinematics/controllers/lab03_controller'); shutil.copytree(src,dst); (dst/'eel4664_ur5e.py').rename(dst/'lab03_controller.py')"
   ```

2. Add the repository root to `lab03_controller.py`:

   ```python
   from pathlib import Path
   import sys

   REPO_ROOT = Path(__file__).resolve().parents[3]
   sys.path.insert(0, str(REPO_ROOT))
   ```

3. Import Lab 2 FK/interpolation and the Lab 3 mission functions; do not copy the FK source.
4. Complete `prepare_pose_mission` so it accepts only converged, finite, limit-safe solutions and verifies the endpoint with `fk_tool`.
5. Complete `execute_pose_mission` so it interpolates from measured `q0`, commands all joints, holds the goal, and logs joints/tool pose.
6. First set `q_goal = q0`; confirm a finite pose prints and the robot does not move.

### Step 7 - Execute Target A and Target B

For each target:

1. Open `lab03_work.wbt` paused, assign `lab03_controller`, and **Reset**.
2. Read measured `q0` and select a validated solution near it.
3. Print convergence, `q_goal`, predicted endpoint, joint-limit check, and sampled-path check.
4. Stop without motion if any check fails.
5. Otherwise execute a smooth move lasting at least eight seconds and hold the goal.
6. Confirm visually that the orange stylus tip enters the corresponding translucent target sphere and its orientation aligns with the target axes; then record measured final joints and Webots tool pose.
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

- completed four source scaffolds and the Lab 3 controller folder;
- completed `answers.md`;
- planar branch/reachability and numerical unit-test evidence;
- target/seed table and three residual plots, including failure;
- Webots logs for two targets and repeated trials;
- three-layer error table; and
- Engineering Question answers.

Do not submit `lab03_work.wbt`, vendor assets, or caches unless requested.

## Troubleshooting

| Last passing stage | First failing stage | Likely problem |
|---|---|---|
| Lab 2 tests | import | path or incomplete Lab 2 work |
| planar IK | pose error | transform direction, sign, or frame |
| pose error | Jacobian | perturbation, joint order, or rotation convention |
| Jacobian | convergence | seed, damping, step, limits, or target |
| offline solver | stationary controller | import boundary |
| stationary controller | motion | safety rejection, adapter, interpolation, or units |
| FK at measured joints | Webots pose | fixed tool transform or model discrepancy |

If IK diverges, inspect one residual history and one Jacobian column, then change one parameter at a time.

For Webots recovery, reopen the protected starter, create a fresh working copy, repeat `void -> minimal -> devices -> one joint`, and run the stationary import test before full motion. See [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) for repeated crashes.
