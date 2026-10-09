# Lab 3 - Inverse Kinematics

## Get the Latest Course Files

Before starting the lab, save your work, close Webots, and update the course repository. Open a terminal and use the commands for your operating system.

**Windows PowerShell:**

```powershell
cd C:\eel4664-robotics-labs
git status --short
git pull --rebase
```

**macOS or Ubuntu Terminal:**

```bash
cd ~/eel4664-robotics-labs
git status --short
git pull --rebase
```

A successful update reports either `Already up to date.` or the files that Git updated.

`git status --short` lists local file changes; no output means there are none. `git pull --rebase` downloads new course commits from GitHub and then reapplies any of your local commits after them. It does not submit your work to GitHub. See [What these Git commands mean](../lab00_setup/README.md#what-these-git-commands-mean) for an explanation of Git terminology.

If `git pull --rebase` reports local changes, a conflict, or another error, do not force the update or discard your work. Follow [If the repository cannot update cleanly](../lab00_setup/README.md#if-the-repository-cannot-update-cleanly).

## Mission

**Choose Cartesian target poses, predict the required UR5e joint configurations with your own inverse-kinematics solver, command the robot in Webots, and measure how closely the stylus actually reaches each target pose.**

### Why measure in Webots?

On a physical UR5e, you would command the IK solution, measure the tool pose, and compare that measurement with the requested target. Because this course does not have access to a physical UR5e, Webots serves as the experimental robot. It preserves the same engineering workflow: **predict -> execute -> measure -> compare**.

A small target-to-measurement error supports the conclusion that the complete IK experiment worked. A large error does not automatically mean the IK mathematics is wrong; it may instead come from joint tracking, frame alignment, or a difference between your kinematic model and the Webots model. You will report these effects separately later in the lab. Webots is therefore a repeatable experimental reference, not a substitute for every source of uncertainty found on real hardware.

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Success Criteria

You are finished when:

- the two marked IK equations are complete;
- the provided offline program converges for Targets A and B and rejects an unreachable target;
- the provided controller executes both accepted solutions in Webots; and
- the report compares the predicted and measured tool poses.
## Learning Objectives

- Explain numerical IK as repeated small corrections from the current pose toward a desired pose.
- Connect the damped-least-squares equation to one joint correction.
- Explain how the seed, damping, and step size affect convergence.
- Compare an FK-predicted tool pose with the pose measured in Webots.
## Prerequisites

Complete [Lab 2 - UR5e Frames and Forward Kinematics](../lab02_webots_ur5e_frames/README.md). Reuse its tested `forward_kinematics(q)`, fixed `T_6_TOOL`, device adapter, and smooth joint interpolation. Do not copy or reimplement FK.

Complete the Python/NumPy prerequisites in [Lab 00](../lab00_setup/README.md).


**Platform note:** The required workflow supports Windows, macOS, and Ubuntu when configured through Lab 00. Terminal examples use `python`; on macOS or Ubuntu, use `python3` instead if `python` is not recognized.

### Optional planar IK warm-up

Use the [Planar Robot FK and IK Simulator Activities](../docs/PLANAR_3R_SIMULATOR_ACTIVITIES.md) to explore elbow-up and elbow-down branches, verify IK by substituting each solution into FK, find unreachable and singular targets, and compare analytical IK with an iterative solver. This external-browser activity is optional unless assigned by the instructor.

<details>
<summary><strong>Optional background: analytical IK, pose error, Jacobians, and numerical methods</strong></summary>

The core activity begins in Part 2. Expand this section when you want the derivations, examples, or more detail about why the provided code works.

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

Lab 2 FK ends at DH frame `{6}`, while Webots measures the attached tool frame. This lab follows Craig's frame notation:

${}^{A}_{B}T$

means "the pose of frame `{B}` expressed relative to frame `{A}`." The same matrix converts coordinates written in frame `{B}` into coordinates written in frame `{A}`.

The robot base is placed at the Webots world origin, so DH frame `{0}` and the Webots world frame coincide in this course world. Therefore:

- ${}^{0}_{6}T(\mathbf q)$ is the pose of DH frame `{6}` relative to frame `{0}`, calculated by Lab 2 FK;
- ${}^{6}_{tool}T$ is the fixed pose of the tool frame relative to frame `{6}`; and
- ${}^{0}_{tool}T(\mathbf q)$ is the resulting tool pose relative to frame `{0}`.

Chain the two transforms in this order:

${}^{0}_{tool}T(\mathbf q) = {}^{0}_{6}T(\mathbf q) \cdot {}^{6}_{tool}T.$

Read the chain from right to left when transforming a point: first go from the tool frame to frame `{6}`, and then from frame `{6}` to frame `{0}`. Transformation order matters; reversing the two matrices describes a different frame relationship.

In the code, `forward_kinematics(q)` returns the first transform on the right side of the equation above. The supplied `T_6_TOOL` stores the second, fixed transform. The wrapper `fk_tool(q)` multiplies them and returns the tool pose on the left side. Use this same wrapper for the current and target poses. Never recalculate `T_6_TOOL` for a new target.

The tool-frame origin is at the stylus mount. In tool coordinates, the visible orange tip is the fixed point

${}^{tool}\mathbf p_{tip}=\begin{bmatrix}0 & 0.13 & 0\end{bmatrix}^{T}\ \text{m}.$

Its frame-`{0}` position is found by transforming this point with ${}^{0}_{tool}T(\mathbf q)$.

The stylus has no mass or collision geometry. It makes pose changes visible without changing the robot dynamics.

The starter also contains `TARGET_A` and `TARGET_B`. Each target has short red/green/blue pose axes at the tool-frame origin and a small translucent sphere at the desired stylus-tip point. These nodes are visual references only; the submitted solver must use the numerical `T_target`, not read target coordinates from Webots.

### 5. Describe the pose error

At each iteration, the solver compares the current tool pose with the target. Position error is

$\mathbf e_p = \mathbf p_{target} - \mathbf p_{current}.$

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

$\mathbf e_R = \frac{1}{2}\sum_{i=1}^{3} \left(\mathbf R_{current}[:,i] \times \mathbf R_{target}[:,i]\right).$

Each rotation-matrix column is one tool axis expressed in the base frame. If the target is rotated approximately 2 degrees about world +z from the current orientation, then

```text
e_R approximately equals [0, 0, 0.0349] rad
```

because 2 degrees is 0.0349 rad. Stack position and orientation vertically:

$\mathbf e = \begin{bmatrix} \mathbf e_p \\ \mathbf e_R \end{bmatrix} \in \mathbb R^6.$

Thus, `e[0:3]` describes translation and `e[3:6]` describes rotation. `pose_error` and the Jacobian must use the same frame and sign convention.

### 6. Estimate how each joint moves the tool

Let

$\Delta \mathbf q = [\Delta q_1,\ldots,\Delta q_6]^T$

be a small change in the six joints. Let

$\Delta \mathbf x = [\Delta p_x,\Delta p_y,\Delta p_z, \Delta \theta_x,\Delta \theta_y,\Delta \theta_z]^T$

be the resulting small tool-pose change. The task Jacobian gives the local linear approximation

$\boxed{\Delta \mathbf x \approx \mathbf J(\mathbf q)\Delta \mathbf q}.$

`J` is 6-by-6. Column `j` answers: "If only joint `j` changes by one small radian, how does the tool position and orientation change?"

Estimate that column by nudging joint `j` in both directions:

$\mathbf q^+ = \mathbf q + h\mathbf u_j, \qquad \mathbf q^- = \mathbf q - h\mathbf u_j,$

$\mathbf J[:,j] \approx \frac{ \mathbf e_{\mathrm{pose}} \left({}^{0}_{tool}T^{-},{}^{0}_{tool}T^{+}\right) }{2h}, \qquad {}^{0}_{tool}T^{\pm} = {}^{0}_{tool}T(\mathbf q^{\pm}).$

Here, $\mathbf e_{\mathrm{pose}}$ is the pose difference calculated by `pose_error`, and ${}^{0}_{tool}T(\mathbf q)$ is the frame-`{0}` tool transform returned by `fk_tool(q)`. The symbol `u_j` is zero except for a 1 at joint `j`. For example, if `h = 0.001` rad and the positive and negative evaluations differ by `0.0008` m in tool x, then that Jacobian entry is

```text
0.0008 / (2 * 0.001) = 0.4 m/rad
```

Repeat for all six joints. Large `h` gives a crude approximation; extremely small `h` exposes floating-point roundoff. Lab 4 derives the Jacobian directly.

### 7. From local tool motion to numerical IK

The numerical IK update follows directly from the local relationship between a small joint change and the resulting small tool motion. No prior knowledge of Newton's method is required.

#### 7.1 Use small motions to reduce the pose error

At iteration $k$, the current joint estimate is $\mathbf q_k$, and forward kinematics gives the current tool pose. The **pose_error** function compares that pose with the desired pose and constructs

$\mathbf e_k=\begin{bmatrix}\mathbf p_d-\mathbf p_k\\\mathbf e_R\end{bmatrix},$

where the first three entries are position error and the last three entries form a small orientation-error vector.

The IK goal is to find joint angles $\mathbf q^*$ for which

$\mathbf e(\mathbf q^*)=\mathbf 0.$

That makes IK a root-finding problem: the function whose root we seek is the pose-error function.

The easiest way to derive the joint update is to ask how a small joint change affects the tool. For a one-variable function, the derivative converts a small input change into an approximate output change:

$\Delta y\approx f'(q_k)\Delta q.$

A robot has several joint inputs and several tool-motion outputs, so the derivatives are collected in the Jacobian matrix. Near the current joint estimate, a first-order Taylor approximation gives

$\mathbf f(\mathbf q_k+\Delta\mathbf q)\approx\mathbf f(\mathbf q_k)+\mathbf J(\mathbf q_k)\Delta\mathbf q.$

Subtract the current pose $\mathbf f(\mathbf q_k)$. The resulting local tool-pose change is approximately

$\Delta\mathbf x\approx\mathbf J(\mathbf q_k)\Delta\mathbf q.$

Here, $\Delta\mathbf x$ is not the subtraction of two homogeneous matrices. It is a six-component local motion: three small position changes and three small orientation changes. Column $j$ of the Jacobian answers: “If joint $j$ changes slightly, how does that six-component tool motion change?”

The tool change we want is exactly the remaining pose correction:

$\Delta\mathbf x_{\mathrm{desired}}=\mathbf e_k.$

Require the joint correction to produce that desired tool change:

$\mathbf J(\mathbf q_k)\Delta\mathbf q\approx\mathbf e_k.$

If the Jacobian is square and safely invertible, solve for the joint correction:

$\Delta\mathbf q\approx\mathbf J^{-1}(\mathbf q_k)\mathbf e_k.$

Then update the joint estimate:

$\mathbf q_{k+1}=\mathbf q_k+\Delta\mathbf q.$

This local correction is closely related to multivariable Newton's method, but that connection is not required to apply the IK update. The optional reading below explains the relationship.

The approximation is accurate only for small changes near $\mathbf q_k$. One correction usually does not reach the target exactly. The solver therefore repeats the cycle: evaluate FK, calculate the remaining pose error, calculate the Jacobian, solve for another joint correction, and update the joint estimate.

<details>
<summary><strong>Optional reading: Connection to Newton's root-finding method</strong></summary>

For one variable, Newton's method seeks a value $x$ that makes $g(x)=0$. Starting from $x_k$, it replaces the curved function locally by its tangent line and uses the tangent's zero crossing as the next estimate.

The scalar correction is $\Delta x=-g(x_k)/g'(x_k)$, followed by $x_{k+1}=x_k+\Delta x$. The numerator measures how far the function is from zero, and the derivative predicts how strongly the function changes when $x$ changes.

For IK, define the root function as the pose error: $\mathbf g(\mathbf q)=\mathbf e(\mathbf q)=\mathbf x_d-\mathbf f(\mathbf q)$. An IK solution is a root because it satisfies $\mathbf e(\mathbf q^*)=\mathbf 0$.

The minus sign comes from the definition of the error. Differentiate $\mathbf e(\mathbf q)=\mathbf x_d-\mathbf f(\mathbf q)$ with respect to $\mathbf q$: $\partial\mathbf e/\partial\mathbf q=\partial\mathbf x_d/\partial\mathbf q-\partial\mathbf f/\partial\mathbf q$.

The desired pose does not change when the joint estimate changes, so $\partial\mathbf x_d/\partial\mathbf q=\mathbf 0$. The derivative of forward kinematics is the Jacobian, $\partial\mathbf f/\partial\mathbf q=\mathbf J(\mathbf q)$. Therefore, $\partial\mathbf e/\partial\mathbf q\approx-\mathbf J(\mathbf q)$.

For the position error, this negative sign is exact: moving the current tool position toward the target decreases the remaining position error by the same amount. For orientation, the lab represents the difference between two rotations with the small vector $\mathbf e_R$. A small current-tool rotation $\Delta\boldsymbol\phi\approx\mathbf J_\omega\Delta\mathbf q$ changes the remaining orientation error in the opposite direction, so $\Delta\mathbf e_R\approx-\mathbf J_\omega\Delta\mathbf q$. This local small-angle step is why the combined six-component relation uses approximately equal rather than exactly equal.

The vector Newton correction is $\Delta\mathbf q=-[\partial\mathbf e/\partial\mathbf q]^{-1}\mathbf e_k$. Substituting the local error derivative gives $\Delta\mathbf q\approx-[-\mathbf J(\mathbf q_k)]^{-1}\mathbf e_k$.

Since $(-\mathbf J)^{-1}=-\mathbf J^{-1}$, the two minus signs cancel, leaving $\Delta\mathbf q\approx\mathbf J^{-1}(\mathbf q_k)\mathbf e_k$.

Thus, $\mathbf e_k$ corresponds to $g(x_k)$, while $\mathbf J^{-1}$ includes the sign that comes from $-1/g'(x_k)$. Newton's method can converge quickly from a good initial guess, but it can fail when the derivative or Jacobian is singular, poorly conditioned, or evaluated too far from the solution.

</details>

A direct inverse is not reliable for general robot IK. Some robots have a non-square Jacobian, and even the UR5e's 6-by-6 task Jacobian becomes singular or poorly conditioned at certain configurations. Near those configurations, a small pose error can produce a very large joint correction.

#### 7.2 Replace the inverse with a pseudoinverse

The Moore-Penrose pseudoinverse generalizes the inverse. It is written as `J+` in plain text and with a superscript `+` on `J` in the equation below. The update becomes

$\Delta\mathbf q=\mathbf J^{+}(\mathbf q_k)\mathbf e_k,\qquad \mathbf q_{k+1}=\mathbf q_k+\Delta\mathbf q.$

When the task rows are independent, one useful form is

$\mathbf J^{+}=\mathbf J^T\left(\mathbf J\mathbf J^T\right)^{-1}.$

The pseudoinverse chooses a least-squares correction: if no joint change produces the requested tool change exactly, it chooses one whose predicted tool motion is as close as possible. For redundant robots, it also selects a minimum-norm solution.

A basic pseudoinverse IK loop is:

1. Choose an initial joint estimate `q0`, error tolerances, and a maximum iteration count.
2. Calculate the current pose with FK.
3. Calculate the six-component pose error.
4. Stop successfully if both position and orientation errors pass their tolerances.
5. Calculate the Jacobian.
6. Calculate a joint correction using the pseudoinverse.
7. Update the joint estimate.
8. Repeat, or report failure if the iteration limit is reached.

The pseudoinverse is more general than a direct inverse, but it can still request extremely large joint changes near a singularity.

#### 7.3 Add damping for stability

Damped least squares modifies the pseudoinverse so the solver does not react too aggressively near a singularity:

$\Delta\mathbf q_{DLS}=\mathbf J^T\left(\mathbf J\mathbf J^T+\lambda^2\mathbf I\right)^{-1}\mathbf e_k.$

It balances two goals:

1. make the predicted tool motion match the requested pose correction; and
2. keep the joint correction reasonably small.

This balance can be written as

$\min_{\Delta\mathbf q}\quad \left\|\mathbf J\Delta\mathbf q-\mathbf e_k\right\|^2+\lambda^2\left\|\Delta\mathbf q\right\|^2.$

The first term penalizes remaining pose error. The second term penalizes a large joint correction. The damping value `lambda` controls how strongly large joint changes are discouraged.

A useful analogy is steering a shopping cart through a narrow doorway. An undamped solver may react to a small alignment error with a large steering change. Damping prefers a smaller, steadier correction, even if several iterations are needed.

This lab also applies only a fraction `alpha` of the DLS proposal:

$\mathbf q_{k+1}=\mathbf q_k+\alpha\Delta\mathbf q_{DLS}.$

The safeguards have different jobs:

- `damping` reduces sensitivity to singular or poorly conditioned Jacobians;
- `alpha` controls how cautiously the solver follows the proposed correction;
- `max_joint_step` places a hard limit on each joint's change during one iteration; and
- the joint limits prevent the estimate from leaving the permitted range.

Too little damping can allow very large or unstable corrections. Too much damping makes the updates conservative and may slow convergence. A small `alpha` is cautious but slow, while a large `alpha` moves faster but can overshoot.

Do not form the inverse in the displayed DLS equation explicitly. First solve

$\left(\mathbf J\mathbf J^T+\lambda^2\mathbf I\right)\mathbf y=\mathbf e_k,$

then calculate

$\Delta\mathbf q_{DLS}=\mathbf J^T\mathbf y.$

After that, multiply by `alpha`, limit the applied joint step, enforce the joint limits, and update `q`.

#### 7.4 Another option: Jacobian transpose

A simpler method replaces the inverse with the Jacobian transpose:

$\mathbf q_{k+1}=\mathbf q_k+\alpha\mathbf J^T(\mathbf q_k)\mathbf e_k.$

The transpose points generally in a direction that reduces the pose error. It is inexpensive because it does not solve a matrix equation. However, its convergence depends strongly on the step size `alpha` and is often slower than pseudoinverse or DLS IK.

#### 7.5 Compare the four updates

| Method | Joint correction | Main advantage | Main limitation |
|---|---|---|---|
| Newton / direct inverse | `inv(J) @ e` | fast near a well-behaved solution | requires a square, nonsingular Jacobian |
| pseudoinverse | `pinv(J) @ e` | handles non-square systems and least-squares solutions | may produce very large changes near singularities |
| damped least squares | damped pseudoinverse | stable near difficult configurations | requires choosing a damping value |
| Jacobian transpose | `alpha * J.T @ e` | inexpensive and simple | often slower and sensitive to step size |

All four methods follow the same overall idea: calculate FK, measure the pose error, use the Jacobian to choose a joint correction, and repeat. This lab uses **damped least squares** because it retains the Newton-style update while behaving more safely near singular or poorly conditioned configurations.

### 8. Put the numerical IK loop together

The complete algorithm is listed below as a reading guide, not as code to copy:

1. Start from a copy of the seed $\mathbf q$.
2. Use FK to calculate the current tool pose.
3. Calculate the position and orientation errors.
4. If both errors satisfy their tolerances, return a successful result.
5. Otherwise estimate the Jacobian, calculate a damped joint correction, limit the step, and enforce the joint limits.
6. Repeat from Step 2 until convergence or the iteration limit.
7. If convergence was not reached, return a failed result with a clear reason.

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


</details>
## Provided Files

- `worlds/lab03_starter.wbt` - protected UR5e world with two visual pose targets
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `controllers/lab03_controller/` - complete controller for Targets A and B
- `src/planar_fk.py` and `src/planar_ik.py` - complete analytical examples for reading
- `src/numerical_ik.py` - complete solver framework with exactly two student lines
- `src/run_ik_experiments.py` - complete offline test program
- `src/execute_pose_target.py` - complete validation and execution helpers
- `Lab03_Report_Template.docx` - results template
## Open the Word report template

VS Code can show the `.docx` file in the Explorer, but Microsoft Word should be used to edit it.

1. In the VS Code Explorer on the left, expand the `lab03_inverse_kinematics` folder.
2. Find `Lab03_Report_Template.docx`.
3. Right-click the file and choose:
   - **Reveal in File Explorer** on Windows;
   - **Reveal in Finder** on macOS; or
   - **Open Containing Folder** on Ubuntu.
4. In the folder that opens, double-click `Lab03_Report_Template.docx` to open it in Microsoft Word.
5. In Word, select **File -> Save As** and save a personal copy such as `LastName_Lab03_Report.docx`. Enter all requested results and screenshots in this personal copy.

Do not try to edit the Word report as text inside VS Code. Whenever the instructions say to paste something into `Lab03_Report_Template.docx`, paste it into the personal Word copy you created.

<details>
<summary><strong>Part 1 - Required setup and validation</strong></summary>

Expand and complete this section once before starting the IK activity.

> **Why this part matters:** Verifying Lab 2 FK, the starter world, Python, devices, and one-joint motion isolates environment problems before they can be mistaken for IK failures.

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

No report entry is required for these prerequisite checks. Stop at the first failure.

**Never overwrite `lab03_starter.wbt`.** Discard a damaged working copy and recreate it from the starter.


</details>
## Part 2 - Core IK Activity

> **Why this part matters:** You will enter the two equations that make numerical IK move from a pose error to a new joint estimate. The supporting programming is provided so you can focus on the robotics idea.

### Step 2 - Read the provided loop

Open `src/numerical_ik.py`. Do not rewrite the file. The following pieces are already complete:

- position and orientation pose error;
- the finite-difference Jacobian;
- input checks, joint limits, and maximum joint-step limits;
- the iteration loop and convergence test; and
- clear success or failure results.

Follow one pass through the loop: FK calculates the current tool pose, `pose_error` calculates the remaining correction, the Jacobian relates small joint changes to small tool motion, and the solver updates the joint estimate.

### Step 3 - Complete only the two marked lines

Search for `TODO 1` and `TODO 2` in `src/numerical_ik.py`. These are the only lines you edit in this lab.

For `TODO 1`, enter the damped-least-squares correction:

```python
step = jacobian.T @ np.linalg.solve(system, error)
```

The provided line immediately above has already formed

```math
\mathbf{system}=\mathbf J\mathbf J^T+\lambda^2\mathbf I.
```

Therefore your line calculates

```math
\Delta\mathbf q=\mathbf J^T(\mathbf J\mathbf J^T+\lambda^2\mathbf I)^{-1}\mathbf e_k.
```

`np.linalg.solve` solves the matrix equation without explicitly calculating an inverse.

For `TODO 2`, enter the joint update:

```python
q_proposed = q + alpha * delta_q
```

This implements

```math
\mathbf q_{k+1}=\mathbf q_k+\alpha\Delta\mathbf q.
```

The provided code then limits the size of the change and enforces the joint limits.

### Step 4 - Run the provided offline experiment

Open the VS Code Terminal with **Terminal -> New Terminal**. Make sure the prompt is at the repository root, the folder containing `lab03_inverse_kinematics`. Then run:

```bash
python lab03_inverse_kinematics/src/run_ik_experiments.py
```

On macOS or Ubuntu, use `python3` if `python` is not recognized.

The program runs Target A, Target B, and one unreachable target. Copy the full output into the Word report. Targets A and B should report `converged: True`. The unreachable target should report `converged: False`; failure is the correct and safe result for that case.

If the program stops at `TODO 1` or `TODO 2`, return to the corresponding marked line. Do not change the supplied Jacobian, loop, limits, or tolerances.

## Part 3 - Webots Experiment

> **Why this part matters:** The offline solver predicts joint angles. Webots checks whether commanding those angles makes the simulated tool reach the predicted position and orientation.

### Step 5 - Run the provided controller for Target A

1. Open your `lab03_work.wbt` copy in Webots and keep the simulation paused.
2. Select the UR5e robot. Set its controller to `lab03_controller`.
3. Open `controllers/lab03_controller/lab03_controller.py` and confirm `TARGET_LABEL = "A"`.
4. Reset the world, run the simulation, and wait for the motion to finish.
5. Copy the controller output into the report and take one screenshot showing the final robot pose and Target A.

The controller uses your two completed equations, but all device access, validation, interpolation, and safety checks are provided. It prints:

- the IK convergence result and final joint vector;
- the **predicted tool position and predicted tool roll-pitch-yaw (RPY)** calculated with FK; and
- the **Webots-measured tool position and tool RPY** after the motion settles.

RPY means roll, pitch, and yaw: rotations about the x, y, and z axes, reported in radians.

### Step 6 - Repeat for Target B

1. Stop and reset Webots.
2. Change only `TARGET_LABEL = "A"` to `TARGET_LABEL = "B"`.
3. Run the simulation again.
4. Copy the output and take one screenshot showing the final robot pose and Target B.

Do not command the unreachable target. The provided controller stops without moving if IK fails or returns invalid joint values.

## Part 4 - Short Analysis

> **Why this part matters:** Comparing prediction with measurement checks the complete chain from the IK equations through FK and robot motion.

For each pose separately, compare:

- the FK-predicted **tool position** with the Webots-measured **tool position**; and
- the FK-predicted **tool RPY** with the Webots-measured **tool RPY**.

Write 1-2 sentences for Target A and 1-2 sentences for Target B. State whether each predicted and measured tool pose agrees closely. Small differences can result from finite solver tolerance and joint tracking. You are not required to calculate a single combined pose-error formula or decide which pose has the largest error.

## Engineering Questions

Answer each in 1-2 sentences.

1. In one iteration, how does the pose-error vector influence the joint correction?
2. Why is damping useful when the Jacobian is near a singular configuration?
3. Why can two different initial joint seeds lead to different joint-angle solutions for the same tool pose?

## What to Submit

1. Completed `src/numerical_ik.py` containing your two equation lines.
2. Completed `Lab03_Report_Template.docx` containing:
   - the complete offline output for Targets A, B, and the unreachable target;
   - the Target A and Target B Webots outputs and screenshots;
   - a short pose-by-pose comparison of predicted and measured tool position and RPY; and
   - answers to the three Engineering Questions.

Do not submit `lab03_work.wbt`, provided helper code, vendor assets, or caches unless requested.

## Troubleshooting

| Problem | Check |
|---|---|
| Program stops at `TODO 1` | Enter the DLS equation exactly on the marked line. |
| Program stops at `TODO 2` | Enter the joint-update equation exactly on the marked line. |
| Lab 2 import or FK fails | Complete and test Lab 2 before continuing. |
| Reachable target does not converge | Check that matrix multiplication uses `@` and that both signs are `+`. |
| Controller does not appear in Webots | Close and reopen the world after updating the repository. |
| Controller reports failure | Do not move the robot; save the output and inspect the offline run first. |

For Webots recovery, reopen the protected starter, create a fresh working copy, and repeat the Part 1 checks. See [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) for repeated crashes.