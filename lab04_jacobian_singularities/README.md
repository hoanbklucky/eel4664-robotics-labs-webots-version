# Lab 4 - Jacobian, Differential Kinematics, and Singularities

## Get the Latest Course Files

Before starting, save your work and close Webots. Follow [Updating the Course Repository](../docs/UPDATE_REPOSITORY.md). Do not force an update or discard local work when Git reports a conflict.

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

- Explain and verify the supplied UR5e geometric Jacobian.
- Verify `twist = J(q) qdot` using finite differences and Webots motion.
- Implement pseudoinverse and damped least-squares Cartesian motion.
- Measure minimum singular value, rank, condition number, and manipulability.
- Relate numerical conditioning to joint-rate amplification and physical mobility.
- Enforce safe joint, rate, and conditioning limits.

## Prerequisites

Complete Lab 3 and the [setup prerequisites](../lab00_setup/README.md). Bring the tested Lab 2 FK/transform modules, the Lab 3 IK results, frame convention, and Webots adapter. Review Jacobians and singularities from lecture/homework.


**Platform note:** The required workflow supports Windows, macOS, and Ubuntu when configured through Lab 00. Terminal examples use `python`; on macOS or Ubuntu, use `python3` instead if `python` is not recognized.

## Background

The Jacobian is the local derivative of forward kinematics: it maps small joint motion to small tool motion. A singularity occurs when that mapping loses a task-space direction. Near such a configuration, a pseudoinverse can request very large joint rates, while damped least squares limits amplification by accepting some tracking error.

For a concepts-first explanation that begins with a planar 2R derivation and then develops geometric Jacobian columns, singular directions, SVD, conditioning metrics, damped least squares, unit scaling, and finite-difference validation, read [Lab 4 Optional Background](OPTIONAL_BACKGROUND.md).

The required implementation uses the base/world frame and the same endpoint in both analytical and numerical Jacobians. The supplied modified-DH helper handles joint-axis bookkeeping; students enter only the two geometric column equations and one DLS equation.

## Provided Files

- `worlds/lab04_starter.wbt` - shared stylus, coordinate grid, tool-tip sensor, and Cartesian direction reference
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `controllers/one_joint_test/` - supplied safe test that moves one joint and compares predicted and measured tool displacement
- `src/jacobian_starter.py`
- `src/singularity_scan.py`
- `src/cartesian_direction_motion.py` - mission integration scaffold
- `Lab04_Report_Template.docx`



## Open the Word report template

Follow [Opening a Word Report Template](../docs/OPEN_WORD_REPORT.md) and create a personal copy of `Lab04_Report_Template.docx` before entering results.

## Part 1 - Setup / Validation

> **Why this part matters:** A trustworthy FK model and verified device path are prerequisites for interpreting Jacobian discrepancies or singular behavior correctly.

1. **World:** create `lab04_work.wbt`; verify the grid, stylus, and `CARTESIAN_DIRECTION_REFERENCE`, and confirm controller `void`.
2. **Minimal controller:** select `diagnostic_minimal` as the UR5e controller and run the simulation. Confirm that the console reports 10 successful steps.
3. **Devices:** reset Webots, select `diagnostic_devices`, and run again. Confirm that all six named motors and their six position sensors appear in the console output.
4. **One-joint test:** use the supplied controller as follows.
   1. Stop and reset the simulation.
   2. In the Scene Tree, select `DEF UR5E UR5e`.
   3. Find its `controller` field, click **Select...**, and choose `one_joint_test`.
   4. Run the simulation. The controller smoothly increases only `shoulder_pan_joint` by `0.10` rad (about $5.7^\circ$) over 3 seconds and holds the other five joints at their initial angles.
   5. Watch the arm and read the console. Compare the signs and dominant direction of `Predicted tool displacement` and `Measured tool displacement`; they should agree closely even though small simulation and settling differences are expected.
   6. Reset Webots before continuing. Do not drag a robot link manually because that bypasses the commanded joint and does not provide a controlled validation test.
5. **Full algorithm:** enable Cartesian and near-singular experiments only after stages 1-4 pass.

The default test is intentionally small and requires no student coding. To test a different joint later, change only `TEST_JOINT_INDEX` near the top of `controllers/one_joint_test/one_joint_test.py`, using the printed joint order, then reset and rerun.

Import your Lab 2 FK rather than duplicating it. Establish conservative joint-rate, joint-limit, and condition-number stop thresholds before motion.

## Part 2 - Core Implementation

> **Why this part matters:** You will connect a supplied geometric-Jacobian implementation to its physical meaning, then enter one damped-least-squares equation that converts a desired Cartesian velocity into joint rates. The scan, logging, validation, and saturation infrastructure is supplied.

### Step 1 - Understand the supplied Jacobian and complete one equation

1. Read the supplied geometric-Jacobian loop in `src/jacobian_starter.py` and connect each code line to the diagram and equations below.
2. In `src/cartesian_direction_motion.py`, complete `TODO 1` for the damped-least-squares joint-rate equation using the supplied `system` and `desired_twist`.

The geometric Jacobian was not assumed from lecture, so its implementation is provided. It is the 3D version of the endpoint partial derivatives used for a planar 2R robot. For joint $i$, the supplied modified-DH code first returns the joint-axis direction $\mathbf z_i$, a point $\mathbf p_i$ on that axis, and the endpoint position $\mathbf p_e$, all in the base frame. The loop then executes:

```python
lever_arm = p_endpoint - origin
linear_column = np.cross(axis, lever_arm)
angular_column = axis

J[:3, joint] = linear_column
J[3:, joint] = angular_column
```

Interpret the lines in this order:

1. `lever_arm` is the vector $\mathbf p_e-\mathbf p_i$ from the joint axis to the endpoint.
2. `np.cross(axis, lever_arm)` gives the tangent direction in which that joint moves the endpoint. It is the position derivative $\partial\mathbf p_e/\partial q_i$.
3. A revolute joint's angular-velocity contribution points along its own axis, so the lower column is `axis`.
4. The two three-element vectors become one six-element Jacobian column.

The loop repeats for all six joints. Read the expanded derivation, planar check, figure, and code walkthrough in [Optional Background, Section 3](OPTIONAL_BACKGROUND.md#from-the-2r-partial-derivatives-to-a-3d-geometric-jacobian). You are responsible for explaining what the supplied code calculates, but you do not have to reproduce this unfamiliar derivation from memory.

Do not rewrite the supplied modified-DH bookkeeping, SVD metrics, scan loop, rate saturation, logging loop, or stop logic.

<details>
<summary>Stuck? Reveal the DLS equation</summary>

```python
qdot = J.T @ np.linalg.solve(system, desired_twist)
```

Use this only after you have identified the roles of `J.T`, `system`, and `desired_twist` from the surrounding code and the optional background.

</details>

### Step 2 - Verify before inverse motion

Use `endpoint_fk=forward_kinematics` in both analytical and numerical calculations. Compare one column first, then all six columns at three nonsymmetric configurations and several `eps` values. After frame `{6}` passes, repeat with the same `fk_tool(q)` endpoint in both calculations.

```bash
python -c "import numpy as np; from lab02_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; from lab04_jacobian_singularities.src.jacobian_starter import analytic_jacobian,numerical_jacobian; q=np.array([0.2,-0.8,1.0,-1.1,-0.7,0.3]); Ja=analytic_jacobian(q); Jn=numerical_jacobian(forward_kinematics,q); print('error=',np.linalg.norm(Ja-Jn)); print(Ja)"
```

Do not proceed until the analytical/numerical error is small and decreases appropriately for a reasonable centered-difference step.

### Step 3 - Run the supplied scan and guarded motion

Use `singularity_scan.py` to report singular values, `sigma_min`, rank, condition number, and manipulability for the instructor-provided well-conditioned and near-singular configurations. Then use the guarded DLS step through the Webots adapter. Keep SI-unit scaling and rank tolerance fixed across comparisons.

| Observation | Well conditioned | Near singular |
|---|---|---|
| Minimum singular value | clearly above zero | much smaller |
| Undamped joint-rate norm | moderate | strongly amplified |
| Damped command | close to request | bounded with visible task error |
| Analytical/numerical agreement | close | still close |

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

## Engineering Question

Answer in 2-3 sentences.

As the minimum singular value decreases, what happens to the required joint-rate magnitude, and how does damping change the commanded motion? Refer to your measured results.

## What to Submit

1. The completed DLS equation line in `cartesian_direction_motion.py`.
2. Completed `Lab04_Report_Template.docx` containing finite-difference validation, the normal/near-singular comparison, the damped/undamped result and plot, and the Engineering Question response.

Do not submit supplied helper code, `lab04_work.wbt`, vendor assets, or caches unless requested.

## Troubleshooting

Validate FK first, then one Jacobian column, then all columns, then a tiny Cartesian command. A sudden sign/frame discrepancy is not evidence of singularity. Stop if joint-rate, joint-limit, or conditioning thresholds are exceeded. Recover from `lab04_starter.wbt` after world/controller failures.
