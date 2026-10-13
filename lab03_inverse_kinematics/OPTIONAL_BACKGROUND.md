# Lab 3 Optional Background

This page contains the optional derivations and examples for Lab 3. Return to the [Lab 3 instructions](README.md) when you are ready to complete the required activity.


## 1. What inverse kinematics does

Suppose you want the stylus tip at a chosen location and orientation. You know the desired **tool pose**, but not the six joint angles that produce it.

| Problem | Given | Find |
|---|---|---|
| Forward kinematics (FK) | joint angles `q` | tool pose `T_world_tool(q)` |
| Inverse kinematics (IK) | desired pose `T_target` | joint angles `q` |

FK asks, "Where will the hand be if the joints have these angles?" IK asks, "How should the joints bend to put the hand here?"

IK can have no solution, one solution, or several solutions. For example, a target may be outside the workspace, or two different arm shapes may reach the same pose.

## 2. Start with a two-link arm

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

## 3. Solve the UR5e by improving a guess

Instead of deriving every UR5e branch, this lab uses a numerical loop:

```text
start with q
   -> calculate the current pose with FK
   -> measure the error to the target
   -> calculate a small joint correction
   -> update q and repeat
```

Because the process begins with a guess, different initial guesses can lead to different valid solutions.

## 4. Use the same tool frame everywhere

Lab 2 FK ends at DH frame `{6}`, while Webots measures the attached tool frame. This lab follows Craig's frame notation.

In this notation, ${}^{A}_{B}T$ means "the pose of frame `{B}` expressed relative to frame `{A}`." The same matrix converts coordinates written in frame `{B}` into coordinates written in frame `{A}`.

The robot base is placed at the Webots world origin, so DH frame `{0}` and the Webots world frame coincide in this course world. Therefore:

- ${}^{0}_{6}T(\mathbf q)$ is the pose of DH frame `{6}` relative to frame `{0}`, calculated by Lab 2 FK;
- ${}^{6}_{tool}T$ is the fixed pose of the tool frame relative to frame `{6}`; and
- ${}^{0}_{tool}T(\mathbf q)$ is the resulting tool pose relative to frame `{0}`.

Chain the two transforms in this order:

$$
{}^{0}_{tool}T(\mathbf q) = {}^{0}_{6}T(\mathbf q) \cdot {}^{6}_{tool}T
$$

Read the chain from right to left when transforming a point: first go from the tool frame to frame `{6}`, and then from frame `{6}` to frame `{0}`. Transformation order matters; reversing the two matrices describes a different frame relationship.

In the code, `forward_kinematics(q)` returns the first transform named in the relationship above. The supplied `T_6_TOOL` stores the second, fixed transform. The wrapper `fk_tool(q)` multiplies them and returns the tool pose on the left side. Use this same wrapper for the current and target poses. Never recalculate `T_6_TOOL` for a new target.

The tool-frame origin is at the stylus mount. In tool coordinates, the visible orange tip is the fixed point

$$
{}^{tool}\mathbf p_{tip}=[0,\ 0.13,\ 0]^T\ \text{m}
$$

Its frame-`{0}` position is found by transforming this point with ${}^{0}_{tool}T(\mathbf q)$.

The stylus has no mass or collision geometry. It makes pose changes visible without changing the robot dynamics.

The starter also contains `TARGET_A` and `TARGET_B`. Each target has short red/green/blue pose axes at the tool-frame origin and a small translucent sphere at the desired stylus-tip point. These nodes are visual references only; the submitted solver must use the numerical `T_target`, not read target coordinates from Webots.

## 5. Describe the pose error

At each iteration, the solver compares the current tool pose with the target. Position error is

$$
\mathbf e_p = \mathbf p_{target} - \mathbf p_{current}
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
\mathbf e_R = \frac{1}{2}\sum_{i=1}^{3} \left(\mathbf R_{current}[:,i] \times \mathbf R_{target}[:,i]\right)
$$

Each rotation-matrix column is one tool axis expressed in the base frame. If the target is rotated approximately 2 degrees about world +z from the current orientation, then

```text
e_R approximately equals [0, 0, 0.0349] rad
```

because 2 degrees is 0.0349 rad. Stack position and orientation vertically:

$$
\mathbf e=[\mathbf e_p^T,\ \mathbf e_R^T]^T\in\mathbb R^6
$$

Thus, `e[0:3]` describes translation and `e[3:6]` describes rotation. `pose_error` and the Jacobian must use the same frame and sign convention.

## 6. Estimate how each joint moves the tool

Let

$$
\Delta \mathbf q = [\Delta q_1,\ldots,\Delta q_6]^T
$$

be a small change in the six joints. Let

$$
\Delta \mathbf x = [\Delta p_x,\Delta p_y,\Delta p_z, \Delta \theta_x,\Delta \theta_y,\Delta \theta_z]^T
$$

be the resulting small tool-pose change. The task Jacobian gives the local linear approximation

$$
\boxed{\Delta \mathbf x \approx \mathbf J(\mathbf q)\Delta \mathbf q}
$$

`J` is 6-by-6. Column `j` answers: "If only joint `j` changes by one small radian, how does the tool position and orientation change?"

Estimate that column by nudging joint `j` in both directions:

$$
\mathbf q^+ = \mathbf q + h\mathbf u_j, \qquad \mathbf q^- = \mathbf q - h\mathbf u_j
$$

$$
\mathbf J_j \approx \mathbf e_{pose}(T^-,T^+)/(2h)
$$

Here, $\mathbf J_j$ means column `j` of the Jacobian. Calculate `T_minus = fk_tool(q_minus)` and `T_plus = fk_tool(q_plus)`, then use `pose_error(T_minus, T_plus)` for $\mathbf e_{pose}(T^-,T^+)$. The symbol `u_j` is zero except for a 1 at joint `j`. For example, if `h = 0.001` rad and the positive and negative evaluations differ by `0.0008` m in tool x, then that Jacobian entry is

```text
0.0008 / (2 * 0.001) = 0.4 m/rad
```

Repeat for all six joints. Large `h` gives a crude approximation; extremely small `h` exposes floating-point roundoff. Lab 4 derives the Jacobian directly.

## 7. From local tool motion to numerical IK

The numerical IK update follows directly from the local relationship between a small joint change and the resulting small tool motion. No prior knowledge of Newton's method is required.

### 7.1 Use small motions to reduce the pose error

At iteration $k$, the current joint estimate is $\mathbf q_k$, and forward kinematics gives the current tool pose. The **pose_error** function compares that pose with the desired pose and constructs

$$
\mathbf e_k=[(\mathbf p_d-\mathbf p_k)^T,\ \mathbf e_R^T]^T
$$

where the first three entries are position error and the last three entries form a small orientation-error vector.

The IK goal is to find joint angles $\mathbf q^*$ for which

$$
\mathbf e(\mathbf q^*)=\mathbf 0
$$

That makes IK a root-finding problem: the function whose root we seek is the pose-error function.

The easiest way to derive the joint update is to ask how a small joint change affects the tool. For a one-variable function, the derivative converts a small input change into an approximate output change:

$$
\Delta y\approx f'(q_k)\Delta q
$$

A robot has several joint inputs and several tool-motion outputs, so the derivatives are collected in the Jacobian matrix. Near the current joint estimate, a first-order Taylor approximation gives

$$
\mathbf f(\mathbf q_k+\Delta\mathbf q)\approx\mathbf f(\mathbf q_k)+\mathbf J(\mathbf q_k)\Delta\mathbf q
$$

Subtract the current pose $\mathbf f(\mathbf q_k)$. The resulting local tool-pose change is approximately

$$
\Delta\mathbf x\approx\mathbf J(\mathbf q_k)\Delta\mathbf q
$$

Here, $\Delta\mathbf x$ is not the subtraction of two homogeneous matrices. It is a six-component local motion: three small position changes and three small orientation changes. Column $j$ of the Jacobian answers: "If joint $j$ changes slightly, how does that six-component tool motion change?"

The tool change we want is exactly the remaining pose correction:

$$
\Delta\mathbf x_{\mathrm{desired}}=\mathbf e_k
$$

Require the joint correction to produce that desired tool change:

$$
\mathbf J(\mathbf q_k)\Delta\mathbf q\approx\mathbf e_k
$$

If the Jacobian is square and safely invertible, solve for the joint correction:

$$
\Delta\mathbf q\approx\mathbf J^{-1}(\mathbf q_k)\mathbf e_k
$$

Then update the joint estimate:

$$
\mathbf q_{k+1}=\mathbf q_k+\Delta\mathbf q
$$

This local correction is closely related to multivariable Newton's method, but that connection is not required to apply the IK update. The optional reading below explains the relationship.

The approximation is accurate only for small changes near $\mathbf q_k$. One correction usually does not reach the target exactly. The solver therefore repeats the cycle: evaluate FK, calculate the remaining pose error, calculate the Jacobian, solve for another joint correction, and update the joint estimate.

### Optional reading: Connection to Newton's root-finding method

For one variable, Newton's method seeks a value $x$ that makes $g(x)=0$. Starting from $x_k$, it replaces the curved function locally by its tangent line and uses the tangent's zero crossing as the next estimate.

The scalar correction is $\Delta x=-g(x_k)/g'(x_k)$, followed by $x_{k+1}=x_k+\Delta x$. The numerator measures how far the function is from zero, and the derivative predicts how strongly the function changes when $x$ changes.

For IK, define the root function as the pose error: $\mathbf g(\mathbf q)=\mathbf e(\mathbf q)=\mathbf x_d-\mathbf f(\mathbf q)$. An IK solution is a root because it satisfies $\mathbf e(\mathbf q^*)=\mathbf 0$.

The minus sign comes from the definition of the error. Differentiate $\mathbf e(\mathbf q)=\mathbf x_d-\mathbf f(\mathbf q)$ with respect to $\mathbf q$: $\partial\mathbf e/\partial\mathbf q=\partial\mathbf x_d/\partial\mathbf q-\partial\mathbf f/\partial\mathbf q$.

The desired pose does not change when the joint estimate changes, so $\partial\mathbf x_d/\partial\mathbf q=\mathbf 0$. The derivative of forward kinematics is the Jacobian, $\partial\mathbf f/\partial\mathbf q=\mathbf J(\mathbf q)$. Therefore, $\partial\mathbf e/\partial\mathbf q\approx-\mathbf J(\mathbf q)$.

For the position error, this negative sign is exact: moving the current tool position toward the target decreases the remaining position error by the same amount. For orientation, the lab represents the difference between two rotations with the small vector $\mathbf e_R$. A small current-tool rotation $\Delta\boldsymbol\phi\approx\mathbf J_\omega\Delta\mathbf q$ changes the remaining orientation error in the opposite direction, so $\Delta\mathbf e_R\approx-\mathbf J_\omega\Delta\mathbf q$. This local small-angle step is why the combined six-component relation uses approximately equal rather than exactly equal.

The vector Newton correction is $\Delta\mathbf q=-[\partial\mathbf e/\partial\mathbf q]^{-1}\mathbf e_k$. Substituting the local error derivative gives $\Delta\mathbf q\approx-[-\mathbf J(\mathbf q_k)]^{-1}\mathbf e_k$.

Since $(-\mathbf J)^{-1}=-\mathbf J^{-1}$, the two minus signs cancel, leaving $\Delta\mathbf q\approx\mathbf J^{-1}(\mathbf q_k)\mathbf e_k$.

Thus, $\mathbf e_k$ corresponds to $g(x_k)$, while $\mathbf J^{-1}$ includes the sign that comes from $-1/g'(x_k)$. Newton's method can converge quickly from a good initial guess, but it can fail when the derivative or Jacobian is singular, poorly conditioned, or evaluated too far from the solution.


A direct inverse is not reliable for general robot IK. Some robots have a non-square Jacobian, and even the UR5e's 6-by-6 task Jacobian becomes singular or poorly conditioned at certain configurations. Near those configurations, a small pose error can produce a very large joint correction.

### 7.2 Replace the inverse with a pseudoinverse

The Moore-Penrose pseudoinverse generalizes the inverse. It is written as `J+` in plain text and with a superscript `+` on `J` in the equation below. The update becomes

$$
\Delta\mathbf q=\mathbf J^{+}(\mathbf q_k)\mathbf e_k,\qquad \mathbf q_{k+1}=\mathbf q_k+\Delta\mathbf q
$$

When the task rows are independent, one useful form is

$$
\mathbf J^{+}=\mathbf J^T\left(\mathbf J\mathbf J^T\right)^{-1}
$$

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

### 7.3 Add damping for stability

Damped least squares modifies the pseudoinverse so the solver does not react too aggressively near a singularity:

$$
\Delta\mathbf q_{DLS}=\mathbf J^T\left(\mathbf J\mathbf J^T+\lambda^2\mathbf I\right)^{-1}\mathbf e_k
$$

It balances two goals:

1. make the predicted tool motion match the requested pose correction; and
2. keep the joint correction reasonably small.

This balance can be written as

$$
\min_{\Delta\mathbf q}\quad \left\|\mathbf J\Delta\mathbf q-\mathbf e_k\right\|^2+\lambda^2\left\|\Delta\mathbf q\right\|^2
$$

The first term penalizes remaining pose error. The second term penalizes a large joint correction. The damping value `lambda` controls how strongly large joint changes are discouraged.

A useful analogy is steering a shopping cart through a narrow doorway. An undamped solver may react to a small alignment error with a large steering change. Damping prefers a smaller, steadier correction, even if several iterations are needed.

This lab also applies only a fraction `alpha` of the DLS proposal:

$$
\mathbf q_{k+1}=\mathbf q_k+\alpha\Delta\mathbf q_{DLS}
$$

The safeguards have different jobs:

- `damping` reduces sensitivity to singular or poorly conditioned Jacobians;
- `alpha` controls how cautiously the solver follows the proposed correction;
- `max_joint_step` places a hard limit on each joint's change during one iteration; and
- the joint limits prevent the estimate from leaving the permitted range.

Too little damping can allow very large or unstable corrections. Too much damping makes the updates conservative and may slow convergence. A small `alpha` is cautious but slow, while a large `alpha` moves faster but can overshoot.

Do not form the inverse in the displayed DLS equation explicitly. First solve

$$
\left(\mathbf J\mathbf J^T+\lambda^2\mathbf I\right)\mathbf y=\mathbf e_k
$$

then calculate

$$
\Delta\mathbf q_{DLS}=\mathbf J^T\mathbf y
$$

After that, multiply by `alpha`, limit the applied joint step, enforce the joint limits, and update `q`.

### 7.4 Another option: Jacobian transpose

A simpler method replaces the inverse with the Jacobian transpose:

$$
\mathbf q_{k+1}=\mathbf q_k+\alpha\mathbf J^T(\mathbf q_k)\mathbf e_k
$$

The transpose points generally in a direction that reduces the pose error. It is inexpensive because it does not solve a matrix equation. However, its convergence depends strongly on the step size `alpha` and is often slower than pseudoinverse or DLS IK.

### 7.5 Compare the four updates

| Method | Joint correction | Main advantage | Main limitation |
|---|---|---|---|
| Newton / direct inverse | `inv(J) @ e` | fast near a well-behaved solution | requires a square, nonsingular Jacobian |
| pseudoinverse | `pinv(J) @ e` | handles non-square systems and least-squares solutions | may produce very large changes near singularities |
| damped least squares | damped pseudoinverse | stable near difficult configurations | requires choosing a damping value |
| Jacobian transpose | `alpha * J.T @ e` | inexpensive and simple | often slower and sensitive to step size |

All four methods follow the same overall idea: calculate FK, measure the pose error, use the Jacobian to choose a joint correction, and repeat. This lab uses **damped least squares** because it retains the Newton-style update while behaving more safely near singular or poorly conditioned configurations.

## 8. Put the numerical IK loop together

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

## 9. Stop safely and interpret the result

Return `converged=False` with a clear reason if the iteration limit is reached, a value becomes NaN/Inf, or joint limits prevent progress. Never command a failed result in Webots. Even a converged endpoint must pass joint-limit and sampled-path safety checks.

After execution, separate:

1. **solver error:** `T_target` versus `fk_tool(q_goal)`;
2. **tracking effect:** `fk_tool(q_goal)` versus `fk_tool(q_measured)`; and
3. **model discrepancy:** `fk_tool(q_measured)` versus the Webots tool measurement.

For example, a tiny solver error but a large Webots error suggests that the numerical IK converged and the remaining problem lies in tracking, frame alignment, or model mismatch. Webots may measure and visualize the result, but it may not solve FK or IK for you.
