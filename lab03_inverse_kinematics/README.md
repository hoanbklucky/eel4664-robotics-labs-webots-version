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

- the three marked IK equations are complete;
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

### Optional background

The required activity begins below. For derivations, examples, and a deeper explanation of analytical and numerical IK, read [Lab 3 Optional Background](OPTIONAL_BACKGROUND.md).


## Provided Files

- `worlds/lab03_starter.wbt` - protected UR5e world with two visual pose targets
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `controllers/lab03_controller/` - complete controller for Targets A and B
- OPTIONAL_BACKGROUND.md - optional IK derivations and numerical-method background
- `src/planar_fk.py` and `src/planar_ik.py` - complete analytical examples for reading
- `src/numerical_ik.py` - complete solver framework with exactly three student lines
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

## Part 1 - Required Setup and Validation


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
   | **Full algorithm:** | wait until Parts 2 and 3 are complete |

No report entry is required for these prerequisite checks. Stop at the first failure.

**Never overwrite `lab03_starter.wbt`.** Discard a damaged working copy and recreate it from the starter.


## Part 2 - Core IK Activity

> **Why this part matters:** You will enter the three equations that carry numerical IK from the current pose to a new joint estimate: calculate the position error, calculate a damped joint correction, and update the joints. The supporting programming is provided so you can focus on this robotics sequence.

### Step 1 - Read the provided loop

Open `src/numerical_ik.py`. Do not rewrite the file. The following pieces are already complete:

- the orientation-error calculation and assembly of the six-component pose error;
- the finite-difference Jacobian;
- input checks, joint limits, and maximum joint-step limits;
- the iteration loop and convergence test; and
- clear success or failure results.

Follow one pass through the loop: FK calculates the current tool pose, `pose_error` calculates the remaining correction, the Jacobian relates small joint changes to small tool motion, and the solver updates the joint estimate.

### Step 2 - Complete only the three marked lines

Search for `TODO 1`, `TODO 2`, and `TODO 3` in `src/numerical_ik.py`. These are the only lines you edit in this lab.

Use the equations and variable descriptions below to complete the blanks. Try each line yourself before opening the answer at the end of this step.

For `TODO 1`, calculate desired position minus current position. In a 4-by-4 transform, `[:3, 3]` selects the position vector.

```python
position = __________ - __________
```

This implements

> $\mathbf e_p=\mathbf p_{target}-\mathbf p_{current}.$

The sign matters: the error vector points from the current tool position toward the desired tool position. The provided code calculates the orientation part and joins it with this position error.

For `TODO 2`, use the `system` matrix and `error` vector that are already available. `np.linalg.solve(A, b)` solves the matrix equation `Ax = b`. Complete the two arguments:

```python
step = jacobian.T @ np.linalg.solve(__________, __________)
```

The provided line immediately above has already formed

> $\mathbf{system}=\mathbf J\mathbf J^T+\lambda^2\mathbf I.$

Your completed line should calculate

> $\Delta\mathbf q=\mathbf J^T(\mathbf J\mathbf J^T+\lambda^2\mathbf I)^{-1}\mathbf e_k.$

For `TODO 3`, combine the current joint vector `q`, step size `alpha`, and joint correction `delta_q`:

```python
q_proposed = __________ + __________ * __________
```

This implements

> $\mathbf q_{k+1}=\mathbf q_k+\alpha\Delta\mathbf q.$

The provided code then limits the size of the change and enforces the joint limits.

<details>
<summary><strong>Stuck? Show the three completed lines</strong></summary>

Try filling the blanks first. Open this only if Python syntax is preventing you from continuing.

```python
position = target[:3, 3] - current[:3, 3]
step = jacobian.T @ np.linalg.solve(system, error)
q_proposed = q + alpha * delta_q
```

Check each completed line against the equation above it before running the program.

</details>

### Step 3 - Run the provided offline experiment

Open the VS Code Terminal with **Terminal -> New Terminal**. Make sure the prompt is at the repository root, the folder containing `lab03_inverse_kinematics`. Then run:

```bash
python lab03_inverse_kinematics/src/run_ik_experiments.py
```

On macOS or Ubuntu, use `python3` if `python` is not recognized.

The program runs Target A, Target B, and one unreachable target. Targets A and B should report `converged: True`; copy those two result sections into the Word report. The unreachable target should report `converged: False`. Confirm that it does, but you do not need to paste or explain that result in the report. This final case demonstrates that the solver can reject a target instead of returning unsafe joint commands.

If the program stops at `TODO 1`, `TODO 2`, or `TODO 3`, return to the corresponding marked line. Do not change the supplied Jacobian, loop, limits, or tolerances.

## Part 3 - Webots Experiment

> **Why this part matters:** The offline solver predicts joint angles. Webots checks whether commanding those angles makes the simulated tool reach the predicted position and orientation.

### Step 1 - Run the provided controller for Target A

Before running the simulation, spend a few minutes reading `controllers/lab03_controller/lab03_controller.py`. You are not expected to rewrite it. Follow the data from the selected target to the final measurement:

1. `TARGET_LABEL` selects A or B. The corresponding vector in `TARGET_JOINTS` is passed through FK only to create a reachable **desired tool pose**.
2. `UR5eDevices` connects the controller to the six joint motors, joint sensors, and tool-pose sensors. The controller reads the initial joint vector as `q0`.
3. `numerical_ik(fk_tool, q0, target, ...)` receives the desired tool pose and the initial guess. It does **not** receive the target joint vector as its answer.
4. If IK fails, returns invalid values, or violates a joint limit, the controller exits without commanding motion.
5. If the result is valid, the controller gradually changes the motor commands from `q0` to the IK solution over eight seconds. The cubic blend avoids an abrupt jump in the commanded joint angles.
6. After one second of settling time, the controller reads the measured joint angles and the Webots tool-position and orientation sensors. It prints those measurements so you can compare them with the FK prediction.

This file shows the complete robotics sequence: choose a tool pose, solve IK, check the solution, command the motors, measure the result, and compare prediction with measurement. Only `TARGET_LABEL` needs to be changed when you repeat the experiment for Target B.

1. Open your `lab03_work.wbt` copy in Webots and keep the simulation paused.
2. Select the UR5e robot. Set its controller to `lab03_controller`.
3. Open `controllers/lab03_controller/lab03_controller.py` and confirm `TARGET_LABEL = "A"`.
4. Reset the world, run the simulation, and wait for the motion to finish.
5. Copy the controller output into the report and take one screenshot showing the final robot pose and Target A.

The controller uses your three completed equations, but all device access, validation, interpolation, and safety checks are provided. It prints:

- the desired target tool position and target roll-pitch-yaw (RPY);
- the IK convergence result and **IK solution joint vector**;
- the **predicted tool position and predicted tool RPY** calculated by applying FK to the IK solution; and
- the **Webots-measured joint vector, tool position, and tool RPY** after the motion settles.

RPY means roll, pitch, and yaw: rotations about the x, y, and z axes, reported in radians.

### Step 2 - Change the controller to Target B

Use VS Code to change the target selection in the provided controller:

1. In Webots, click **Stop** so the simulation is not running.
2. Return to VS Code. In the Explorer on the left, expand these folders in order:

   ```text
   lab03_inverse_kinematics
     controllers
       lab03_controller
   ```

3. Click `lab03_controller.py` to open it.

   If you cannot find the file in the Explorer, press **Ctrl+P** on Windows or Ubuntu, or **Command+P** on macOS. Type:

   ```text
   lab03_inverse_kinematics/controllers/lab03_controller/lab03_controller.py
   ```

   Then press **Enter**.

4. Near the top of the file, find this line:

   ```python
   TARGET_LABEL = "A"
   ```

5. Change only the letter `A` to `B`:

   ```python
   TARGET_LABEL = "B"
   ```

   Keep the quotation marks and do not change `TARGET_JOINTS` or any other code.

6. Save the file with **Ctrl+S** on Windows or Ubuntu, or **Command+S** on macOS.
7. Return to Webots and click **Reset** so the controller restarts from the initial robot configuration.
8. Click **Run**. Confirm that the Console begins with `Target: B`.
9. After the motion finishes, copy the output and take one screenshot showing the final robot pose and Target B.

Do not command the unreachable target. The provided controller stops without moving if IK fails or returns invalid joint values.

## Part 4 - Short Analysis

> **Why this part matters:** Comparing prediction with measurement checks the complete chain from the IK equations through FK and robot motion.

For each pose separately, compare:

- the FK-predicted **tool position** with the Webots-measured **tool position**; and
- the FK-predicted **tool RPY** with the Webots-measured **tool RPY**.

Write 1-2 sentences for Target A and 1-2 sentences for Target B. State whether each predicted and measured tool pose agrees closely. Small differences can result from finite solver tolerance and joint tracking. You are not required to calculate a single combined pose-error formula or decide which pose has the largest error.

## Engineering Question

Answer in 1-2 sentences.

During one IK iteration, what does the solver calculate by comparing the desired and current tool poses, and how does it use that result to update the joint angles?

## What to Submit

1. Completed `src/numerical_ik.py` containing your three equation lines.
2. Completed `Lab03_Report_Template.docx` containing:
   - the complete offline output for Targets A and B;
   - the Target A and Target B Webots outputs and screenshots;
   - a short pose-by-pose comparison of predicted and measured tool position and RPY; and
   - your answer to the Engineering Question.

Do not submit `lab03_work.wbt`, provided helper code, vendor assets, or caches unless requested.

## Troubleshooting

| Problem | Check |
|---|---|
| Program stops at `TODO 1` | Enter desired position minus current position on the marked line. |
| Program stops at `TODO 2` | Enter the DLS equation exactly on the marked line. |
| Program stops at `TODO 3` | Enter the joint-update equation exactly on the marked line. |
| Lab 2 import or FK fails | Complete and test Lab 2 before continuing. |
| Reachable target does not converge | Check that matrix multiplication uses `@` and that both signs are `+`. |
| Controller does not appear in Webots | Close and reopen the world after updating the repository. |
| Controller reports failure | Do not move the robot; save the output and inspect the offline run first. |

For Webots recovery, reopen the protected starter, create a fresh working copy, and repeat the Part 1 checks. See [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) for repeated crashes.
