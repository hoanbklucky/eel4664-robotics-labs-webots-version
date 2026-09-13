# Lab 4 - Jacobian, Differential Kinematics, and Singularities

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

**Move the end effector along a Cartesian direction and experimentally demonstrate what happens near a singularity.**

### Why experiment in Webots?

The Jacobian predicts how small joint velocities produce tool velocity, but its physical meaning becomes clearer when the robot moves. Webots lets you compare that local prediction with measured tool motion and observe how the same Cartesian command becomes difficult near a singularity.

This simulated experiment also permits repeatable approaches to problematic configurations without risking a physical robot. Numerical singularity metrics remain the evidence; the animation helps you interpret what motion capability is being lost.

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

Open `worlds/lab04_starter.wbt` paused and immediately use **File -> Save World As...** to create `worlds/lab04_work.wbt`.

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

Complete Lab 3 and the [setup prerequisites](../lab00_setup/README.md). Bring the tested Lab 2 FK/transform modules, the Lab 3 IK results, frame convention, and Webots adapter. Review Jacobians and singularities from lecture/homework.


**Platform note:** The required workflow supports Windows, macOS, and Ubuntu when configured through Lab 00. Terminal examples use `python`; on macOS or Ubuntu, use `python3` instead if `python` is not recognized.

## Background

### What the Jacobian means

For a small joint displacement $\Delta\mathbf q$, the Jacobian predicts the corresponding small tool-pose change:

$$
\Delta\mathbf x \approx J(\mathbf q)\Delta\mathbf q.
$$

For joint velocity $\dot{\mathbf q}$, it predicts the tool twist:

$$
\begin{bmatrix}\mathbf v\\\boldsymbol\omega\end{bmatrix}
=J(\mathbf q)\dot{\mathbf q}.
$$

The upper three rows describe linear velocity $\mathbf v$; the lower three describe angular velocity $\boldsymbol\omega$. Every vector must be expressed in the same frame. This lab uses the robot base/world frame used in Lab 2.

### One column for one revolute joint

For revolute joint $i$, let $\mathbf p_i$ be a point on its axis, $\mathbf z_i$ be its unit axis direction, and $\mathbf p_e$ be the endpoint position, all expressed in the base frame. Column $i$ is

$$
J_i=
\begin{bmatrix}
\mathbf z_i\times(\mathbf p_e-\mathbf p_i)\\
\mathbf z_i
\end{bmatrix}.
$$

The cross product gives the endpoint's instantaneous linear motion caused by rotation about the joint axis. The lower part says that a revolute joint's angular-velocity direction is its axis.

### Important modified-DH detail

Lab 2 uses the modified-DH order $\alpha_{i-1},a_{i-1},d_i,\theta_i$. Joint $i$ rotates only after the fixed operations $R_x(\alpha_{i-1})$ and $T_x(a_{i-1})$. Therefore, do **not** automatically use the z-axis and origin of the previously completed transform ${}^{0}T_{i-1}$.

For each row of the Lab 2 table:

1. begin with the transform accumulated through the previous link;
2. apply the fixed $R_x(\alpha_{i-1})T_x(a_{i-1})$ part;
3. record that intermediate frame's origin $\mathbf p_i$ and map its z-axis through the supplied Webots-to-MDH direction sign; and
4. apply the complete modified-DH transform to continue the chain.

Because Lab 2 uses $\theta_i=s_iq_i$ with $s_i\in\{+1,-1\}$, the axis derivative with respect to the Webots reading $q_i$ is $s_i\mathbf z_i$. The supplied `WEBOTS_TO_MDH_SIGN` array provides $s_i$; omitting it reverses four Jacobian columns.

The supplied `modified_dh_joint_axes` function performs these frame bookkeeping steps. Students complete only the two geometric relationships in `analytic_jacobian`.

### Verify instead of trusting the derivation

Use a centered finite difference for every joint:

$$
J[:,i]\approx
\frac{\mathrm{poseDifference}(T(\mathbf q-\varepsilon\mathbf e_i),
T(\mathbf q+\varepsilon\mathbf e_i))}{2\varepsilon}.
$$

Compare one column first, then all six. The analytical and numerical functions must use the same endpoint: frame `{6}`, the tool origin, or the stylus tip. Mixing endpoints creates a real translational difference even when both calculations are correct.

### Singularities and damping

Near a singularity, at least one singular value approaches zero. Some Cartesian direction becomes difficult or impossible, and an inverse or pseudoinverse may request very large joint rates. Damped least squares bounds commands by accepting some task-space error. Webots measures the resulting motion; it must not compute the assigned Jacobian or inverse differential solution.

The starter uses the same visual-only stylus as Labs 1-2. Its orange tip is `p_tool = [0, 0.13, 0]` m in the tool frame, so students can see the direction and amplification of differential motion. Predict the tip with `transform_point(T_world_tool, p_tool)`. The stylus has no mass or collision geometry.

The `CARTESIAN_DIRECTION_REFERENCE` triad shows world +x (red), +y (green), and +z (blue) near the workspace. Use it to interpret the assigned Cartesian direction; it is not a commanded trajectory or a singularity detector.
## Provided Files

- `worlds/lab04_starter.wbt` - shared stylus, coordinate grid, tool-tip sensor, and Cartesian direction reference
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/jacobian_starter.py`
- `src/singularity_scan.py`
- `src/cartesian_direction_motion.py` - mission integration scaffold
- `Lab04_Report_Template.docx`



## Open the Word report template

VS Code can show the `.docx` file in the Explorer, but Microsoft Word should be used to edit it.

1. In the VS Code Explorer on the left, expand the `lab04_jacobian_singularities` folder.
2. Find `Lab04_Report_Template.docx`.
3. Right-click the file and choose:
   - **Reveal in File Explorer** on Windows;
   - **Reveal in Finder** on macOS; or
   - **Open Containing Folder** on Ubuntu.
4. In the folder that opens, double-click `Lab04_Report_Template.docx` to open it in Microsoft Word.
5. In Word, select **File -> Save As** and save a personal copy such as `LastName_Lab04_Report.docx`. Enter all requested results and screenshots in this personal copy.

Do not try to edit the Word report as text inside VS Code. Whenever the instructions say to paste something into `Lab04_Report_Template.docx`, paste it into the personal Word copy you created.

## Part 1 - Setup / Validation

> **Why this part matters:** A trustworthy FK model and verified device path are prerequisites for interpreting Jacobian discrepancies or singular behavior correctly.

1. **World:** create `lab04_work.wbt`; verify the grid, stylus, and `CARTESIAN_DIRECTION_REFERENCE`, and confirm controller `void`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm ordered joint sensing.
4. **One joint:** move one joint slightly and verify predicted tool-motion direction.
5. **Full algorithm:** enable Cartesian and near-singular experiments only after stages 1-4 pass.

Import your Lab 2 FK rather than duplicating it. Establish conservative joint-rate, joint-limit, and condition-number stop thresholds before motion.

## Part 2 - Core Implementation

> **Why this part matters:** Deriving the geometric Jacobian and checking it with finite differences connects joint motion to Cartesian motion while exposing frame and sign mistakes.

1. Run all commands from the repository root so `jacobian_starter.py` can import the tested Lab 2 FK module.
2. Read `modified_dh_joint_axes`. For one configuration, print the six recorded origins and axes and explain why joint 2's axis is not obtained by blindly reusing the completed frame `{1}` z-axis.
3. In `analytic_jacobian`, complete only:
   - `linear_column`, using the cross-product relationship; and
   - `angular_column`, using the revolute-joint axis.
4. Use `endpoint_fk=forward_kinematics` in both analytical and numerical calculations for the first test. Compare column 1, then all six columns.
5. Repeat the comparison for at least three nonsymmetric configurations and several `eps` values. Report the matrix norm $\lVert J_{analytic}-J_{numeric}\rVert$.
6. After frame `{6}` passes, define the same `fk_tool(q)` used in Labs 2-3 and pass it as `endpoint_fk`. Do not compare a frame-`{6}` analytical Jacobian with a tool-origin numerical Jacobian.
7. Implement an SVD pseudoinverse and damped least squares explicitly with NumPy.
8. Complete `singularity_scan.py` to record `sigma_min`, rank, condition number, manipulability, and `q`.
9. Complete `cartesian_direction_motion.py` with step size, damping, saturation, and stop conditions. Keep Webots sensing/actuation separate from the Jacobian mathematics.

A useful offline check after completing the two blanks is:

```bash
python -c "import numpy as np; from lab02_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; from lab04_jacobian_singularities.src.jacobian_starter import analytic_jacobian,numerical_jacobian; q=np.array([0.2,-0.8,1.0,-1.1,-0.7,0.3]); Ja=analytic_jacobian(q); Jn=numerical_jacobian(forward_kinematics,q); print('error=',np.linalg.norm(Ja-Jn)); print(Ja)"
```

Stop and correct the frame convention if the error is not small before proceeding to inverse differential motion.
## Part 3 - Robot Experiment

> **Why this part matters:** Moving the robot makes the local velocity prediction visible and shows physically why Cartesian motion becomes difficult near a singularity.

1. Select a well-conditioned starting pose.
2. Command a small tool displacement or velocity along the assigned Cartesian direction.
3. Log requested, predicted, and measured motion.
4. Approach an instructor-approved near-singular configuration in conservative increments.
5. Repeat a comparable Cartesian request.
6. Stop before rate/conditioning thresholds are violated.
7. Repeat near-singular motion with damping and compare behavior.

The final robotic outcome is a visible Cartesian-direction motion whose degradation near singularity is predicted by your metrics.

## Part 4 - Quantitative Analysis

> **Why this part matters:** Singular values, condition number, tracking error, and joint-rate amplification distinguish a real loss of mobility from an implementation or visualization problem.

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
- `Lab04_Report_Template.docx`.

## Troubleshooting

Validate FK first, then one Jacobian column, then all columns, then a tiny Cartesian command. A sudden sign/frame discrepancy is not evidence of singularity. Stop if joint-rate, joint-limit, or conditioning thresholds are exceeded. Recover from `lab04_starter.wbt` after world/controller failures.
