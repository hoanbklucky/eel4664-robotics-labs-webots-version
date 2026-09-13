# Lab 2 - UR5e Frames and Forward Kinematics

## Get the Latest Course Files

Before starting, save your work, close Webots, and update the repository.

Windows PowerShell:

```powershell
cd C:\eel4664-robotics-labs
git status --short
git pull --rebase
```

macOS or Ubuntu Terminal:

```bash
cd ~/eel4664-robotics-labs
git status --short
git pull --rebase
```

If Git reports local changes or a conflict, do not discard your work. Follow [the Lab 00 update instructions](../lab00_setup/README.md#if-the-repository-cannot-update-cleanly).

## Mission

**Complete two entries in a Craig modified-DH matrix, predict where the UR5e tool will move, watch the stylus air-draw a loop, and compare your FK predictions with Webots measurements.**

Webots represents the experimental robot that would normally provide measurements from physical hardware. A small prediction error supports the correctness of your frame convention, transform chain, and FK implementation.

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Success Criteria

You are finished when:

- the starter world and both diagnostic controllers pass;
- the one-joint motion reports `[TRACKING PASS]`;
- both FK tests produce valid rigid transforms; and
- predicted and measured tool poses are compared for Poses A-C.

## Learning Objectives

- Use Craig's modified-DH convention to construct a link transform.
- Chain six link transforms to calculate `T_0_6(q)`.
- Account for Webots joint-direction and tool-frame conventions.
- Validate FK quantitatively using measured joint angles and tool poses.

## Prerequisite

Complete [Lab 1 - UR5e Playground](../lab01_ur5e_playground/README.md) and configure Python/Webots through [Lab 00](../lab00_setup/README.md).

The workflow supports Windows, macOS, and Ubuntu. Commands use `python`; use `python3` if required on macOS or Ubuntu.

## Core Background

### What forward kinematics calculates

The six measured joint angles form

$$
\mathbf q=[q_1,q_2,q_3,q_4,q_5,q_6]^T.
$$

Forward kinematics maps those angles to the pose of frame `{6}` relative to the robot base:

$$
\mathbf q \longrightarrow {}^0T_6(\mathbf q).
$$

The upper-left 3-by-3 part of `T` is orientation, and the last column is position.

### Craig modified-DH transform

This lab uses the modified-DH convention from Craig:

$$
{}^{i-1}T_i=
\begin{bmatrix}
 c_{\theta_i} & -s_{\theta_i} & 0 & a_{i-1} \\
 s_{\theta_i}c_{\alpha_{i-1}} & c_{\theta_i}c_{\alpha_{i-1}} & -s_{\alpha_{i-1}} & -s_{\alpha_{i-1}}d_i \\
 s_{\theta_i}s_{\alpha_{i-1}} & c_{\theta_i}s_{\alpha_{i-1}} & c_{\alpha_{i-1}} & c_{\alpha_{i-1}}d_i \\
 0 & 0 & 0 & 1
\end{bmatrix}.
$$

The shorthand $c_x$ means $\cos(x)$, and $s_x$ means $\sin(x)$. You do not need to derive this matrix. Compare it with the supplied NumPy matrix and complete only two missing entries.

Use this table in meters and radians:

| Joint $i$ | $\alpha_{i-1}$ | $a_{i-1}$ | $d_i$ | $\theta_i$ from Webots |
|---:|---:|---:|---:|---:|
| 1 | $0$ | $0$ | $0.1625$ | $q_1$ |
| 2 | $\pi/2$ | $0$ | $0$ | $-q_2$ |
| 3 | $0$ | $0.4250$ | $0$ | $-q_3$ |
| 4 | $0$ | $0.3922$ | $-0.1333$ | $-q_4$ |
| 5 | $\pi/2$ | $0$ | $0.0997$ | $q_5$ |
| 6 | $-\pi/2$ | $0$ | $-0.0996$ | $-q_6$ |

This is still Craig modified DH. The signs in the last column only map Webots encoder-positive directions to the corresponding $\theta_i$ directions. The supplied `WEBOTS_TO_MDH_SIGN` array applies that mapping. The nominal dimensions and the rounded Webots geometry differ slightly, so errors around a millimeter are reasonable.

### Chaining the six transforms

The provided `forward_kinematics(q)` function is already written. **Read it to understand the sequence; do not copy or rewrite it.**

It begins with the identity transform, ${}^{0}T_0=I$. For each joint, it reads one row of the modified-DH table, converts the Webots joint reading to the corresponding $\theta_i$, and constructs ${}^{i-1}T_i$. It then appends that link by right multiplication:

$$
{}^{0}T_i={}^{0}T_{i-1}\,{}^{i-1}T_i.
$$

For six joints, the complete chain is

$$
{}^{0}T_6={}^{0}T_1\,{}^{1}T_2\,{}^{2}T_3\,{}^{3}T_4\,{}^{4}T_5\,{}^{5}T_6.
$$

For example, after the second multiplication, the result is ${}^{0}T_2$: the pose of frame `{2}` relative to frame `{0}`. Order matters because matrix multiplication is not commutative.

### Provided tool transform

Craig frame `{6}` and the Webots tool sensor use different axis directions. The course provides their fixed relationship:

$$
{}^{6}T_{tool}=
\begin{bmatrix}
-1 & 0 & 0 & 0 \\
0 & 0 & -1 & 0 \\
0 & -1 & 0 & 0 \\
0 & 0 & 0 & 1
\end{bmatrix}.
$$

This matrix is already defined as `T_6_TOOL` in `src/ur5e_fk_starter.py`. Read and use the supplied value; do not copy, estimate, or modify it. The predicted Webots tool pose is

$$
{}^{world}T_{tool}={}^{world}T_6\,{}^6T_{tool}.
$$

The robot base is at the world origin in this lab, so `T_world_0` is identity.

## Provided Files

- `worlds/lab02_starter.wbt` - protected starter world
- `controllers/diagnostic_minimal/` and `diagnostic_devices/` - startup checks
- `controllers/eel4664_ur5e/` - safe one-joint controller template
- `controllers/fk_experiment/` - A -> B -> C -> A experiment
- `src/transforms.py` and `src/transform_point.py` - complete support code; do not modify
- `src/ur5e_fk_starter.py` - the two-entry FK exercise
- `src/predict_fk_poses.py` - provided runner for the three pre-experiment FK predictions
- `Lab02_Report_Template.docx` - editable Word report for pasted results, screenshots, and interpretation
- `answers.md` - legacy text reference; students do not submit this file

## Student Workflow

### Step 1 - Prepare and open a working world

> **Why this part matters:** Using the pinned robot assets gives everyone the same model, and preserving the starter world provides a known-good recovery point if a working world becomes corrupted.

1. Open a terminal in the repository.
2. Close Webots and prepare the pinned R2025a assets:

   ```bash
   python lab00_setup/prepare_webots_sample.py
   python -c "from pathlib import Path; print(Path('webots/vendor/webots_r2025a/projects/robots/universal_robots/protos/UR5e.proto').is_file())"
   ```

   The first command should end with `[READY]` and the second must print `True`.

   ![Successful preparation of the pinned Webots R2025a UR5e assets](images/prepare_assets_success.png)

3. Open `lab02_webots_ur5e_frames/worlds/lab02_starter.wbt` in Webots R2025a while paused.
4. Confirm the robot, floor, stylus, and small world-frame reference are visible.
5. Immediately use **File -> Save World As...** and create `worlds/lab02_work.wbt`.
6. Make all changes in `lab02_work.wbt`. Never overwrite `lab02_starter.wbt`.

### Step 2 - Run the two diagnostics

> **Why this part matters:** These checks separate Webots, Python, and device-access problems from FK errors. A later failure is much easier to diagnose once this foundation is known to work.

Select `UR5e "UR5E"` in the Scene Tree, double-click its `controller` field, select a controller, press **Reset**, and then press **Run**.

| Controller | Expected Console result | Movement |
|---|---|---|
| `diagnostic_minimal` | `[DIAGNOSTIC PASS] completed 10 steps` | none |
| `diagnostic_devices` | 15 devices followed by `[DIAGNOSTIC PASS] all device handles enumerated` | none |

The device list must include six motors, six position sensors, `tool_position`, `tool_orientation`, and `tool_test_point_position`.

![Successful minimal and device diagnostics](images/diagnostics_pass.png)

Stop and use the Troubleshooting section if either diagnostic fails.

### Step 3 - Confirm one-joint motion

> **Why this part matters:** A small single-joint move verifies the motor command path, encoder feedback, joint name, and positive direction before six joints move together.

If `controllers/lab02_controller` does not exist, close Webots and run:

```bash
python -c "from pathlib import Path; import shutil; src=Path('lab02_webots_ur5e_frames/controllers/eel4664_ur5e'); dst=Path('lab02_webots_ur5e_frames/controllers/lab02_controller'); shutil.copytree(src,dst); (dst/'eel4664_ur5e.py').rename(dst/'lab02_controller.py')"
```

Assign `lab02_controller` in `lab02_work.wbt`. This supplied controller changes only the shoulder-pan target: $q_{goal,1}=q_{0,1}+0.10$ rad, while the other five targets remain at their initial values. It moves for four seconds and then waits one second before measuring. Read this behavior in the controller; do not copy or edit it for this step.

![Lab 2 working world with the one-joint controller assigned](images/one_joint_controller_ready.png)

Press **Reset**, then **Run**. The shoulder-pan joint should move smoothly by about `+0.10` rad, hold for one second, and print `[TRACKING PASS]`. Small differences between target and measured angles are normal. No values from this step are required in the report.

### Step 4 - Complete and test forward kinematics

> **Why this part matters:** This is the central mathematical task: converting joint angles into a tool pose. The zero and nonsymmetric tests catch different kinds of matrix and sign errors before the robot experiment.

Open `src/ur5e_fk_starter.py`. Fill only:

- `row_2_column_1`
- `row_3_column_4`

Use the Craig matrix above. Do not modify the table, `WEBOTS_TO_MDH_SIGN`, `T_6_TOOL`, or the chaining loop.

Run the zero configuration:

```bash
python -c "import numpy as np; from lab02_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; T=forward_kinematics(np.zeros(6)); print(T); print('orthogonality=',np.linalg.norm(T[:3,:3].T@T[:3,:3]-np.eye(3))); print('det=',np.linalg.det(T[:3,:3]))"
```

Then run the complete nonsymmetric test:

```bash
python -c "import numpy as np; from lab02_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; T=forward_kinematics(np.array([0.20,-0.80,1.00,-1.10,-0.70,0.30])); print(T); print('orthogonality=',np.linalg.norm(T[:3,:3].T@T[:3,:3]-np.eye(3))); print('det=',np.linalg.det(T[:3,:3]))"
```

For both runs:

- `T` must be 4-by-4 with last row `[0, 0, 0, 1]`;
- orthogonality error must be below `1e-8`; and
- determinant must be within `1e-8` of `1`.

The zero pose is easy to inspect, but many sine terms vanish there. The nonsymmetric pose activates more terms and is more likely to reveal a sign or placement mistake. Paste the two completed entries and both outputs into `Lab02_Report_Template.docx`.

### Step 5 - Predict the three tool poses

> **Why this part matters:** Predicting before running Webots keeps the experiment honest: you test the model against new observations instead of adjusting the prediction after seeing the answer.

The provided Webots controller will command these joint vectors:

| Pose | Target joint vector $\mathbf q_{goal}$ [rad] |
|---|---|
| A | `[0.0, -1.20, 1.20, -1.50, -1.57, 0.0]` |
| B | `[0.20, -0.80, 1.00, -1.10, -0.70, 0.30]` |
| C | `[-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]` |

Do **not** run the Webots motion yet. First run the provided prediction program from the **repository root**. The repository root is the main `eel4664-robotics-labs` folder that contains the root `README.md` and folders such as `lab00_setup` and `lab02_webots_ur5e_frames`.

To run the program using the VS Code terminal:

1. Start VS Code.
2. Select **File -> Open Folder...** and open the main `eel4664-robotics-labs` folder. Do not open only the `lab02_webots_ur5e_frames` subfolder.
3. Select **Terminal -> New Terminal**. The terminal panel opens at the bottom of VS Code.
4. Run `pwd` in the terminal. The displayed path should end with `eel4664-robotics-labs`.
5. If the terminal is in a different folder, use `cd` followed by the actual location of your repository. For example:

   **Windows PowerShell**

   ```powershell
   cd C:\eel4664-robotics-labs
   ```

   **macOS or Ubuntu**

   ```bash
   cd ~/eel4664-robotics-labs
   ```

   Your location may be different from these examples.
6. From that folder, run:

   ```bash
   python lab02_webots_ur5e_frames/src/predict_fk_poses.py
   ```

   On a system where the Python command is `python3`, use `python3` instead of `python`.

For each target joint vector, this program uses **your** `forward_kinematics` function and the supplied `T_6_TOOL` to calculate the predicted Webots tool pose:

$$
T_{predicted}=T_6(\mathbf q_{goal})\,{}^6T_{tool}.
$$

Paste the predicted tool position `[x, y, z]` and predicted tool orientation `[roll, pitch, yaw]` for poses A, B, and C into `Lab02_Report_Template.docx` before continuing. RPY means **roll, pitch, and yaw**: the three angles used here to describe the tool orientation about the x-, y-, and z-axes. If the program prints `[STOP]`, return to Step 4 and complete the two marked modified-DH entries.

### Step 6 - Move the robot and compare with Webots

> **Why this part matters:** The experiment now tests whether tool poses predicted from commanded joint angles agree with independent measurements from the simulated robot—the same basic validation process used with a physical robot.

#### What Webots measures

The Lab 2 world attaches two simulated sensors to the same tool frame used by the prediction:

- a Webots `GPS` sensor named `tool_position` reports the tool position `[x, y, z]` in the **world frame**, in meters; and
- a Webots `InertialUnit` sensor named `tool_orientation` reports the tool orientation `[roll, pitch, yaw]` relative to the **world frame**, in radians.

After the robot reaches each pose and holds for one second, the `fk_experiment` controller reads these sensors and prints their values. These are Webots simulation measurements; they are not calculated by the student's `forward_kinematics` function. The Step 5 prediction and Step 6 sensor output describe the same tool frame, so comparing them tests whether the FK model predicts what the simulated robot actually does.

Follow this sequence:

1. Open `lab02_work.wbt` while Webots is paused.
2. Select `UR5e "UR5E"` and assign the `fk_experiment` controller.
3. Press **Reset**, then **Run**.
4. Watch the stylus move through A, B, and C and then return to A. At each pose, the controller commands the listed $\mathbf q_{goal}$ for eight seconds, holds it for one second, and then prints:
   - the six measured joint angles;
   - the Webots tool position; and
   - the Webots tool RPY orientation.
5. Paste the three printed vectors for A, B, and C into `Lab02_Report_Template.docx` and add a screenshot of the completed Webots motion.
6. Pause Webots after `[EXPERIMENT DONE]` appears.

First check that the measured joint angles are close to the commanded target angles. Small differences are normal. If the difference is unexpectedly large, reset and repeat the motion before judging the FK model.

Next, compare the Step 5 prediction with the Step 6 Webots output for each pose. Place the values side by side in `Lab02_Report_Template.docx` and look at the corresponding:

- the **predicted tool position** `[x, y, z]` from Step 5 with the **Webots-measured tool position** `[x, y, z]` from Step 6; and
- the **predicted tool orientation** `[roll, pitch, yaw]` from Step 5 with the **Webots-measured tool orientation** `[roll, pitch, yaw]` from Step 6.

`RPY` is short for **roll, pitch, and yaw**. These are the three angles used here to describe the tool orientation about the x-, y-, and z-axes, respectively.

No error formula or additional comparison program is required. In the Word report, evaluate the poses one at a time:

- **Pose A:** State whether the predicted tool position and tool RPY agree closely with the Webots measurements.
- **Pose B:** State whether the predicted tool position and tool RPY agree closely with the Webots measurements.
- **Pose C:** State whether the predicted tool position and tool RPY agree closely with the Webots measurements.

Write one or two sentences for each pose.

Small differences are expected because the simulated joints may not stop at exactly the commanded values and the model dimensions are rounded. If the measured joints closely match their targets but the tool values are clearly different, recheck the modified-DH entries, joint signs, frame conversion, and transformation order.

Webots supplies an independent simulated measurement for checking the FK prediction; it does not calculate FK for the submitted work.

## What to Submit

1. Completed `src/ur5e_fk_starter.py`.
2. Completed `Lab02_Report_Template.docx` containing:
   - the two modified-DH entries;
   - both offline FK test outputs;
   - three pre-run tool-pose predictions;
   - pasted Webots output;
   - the requested screenshots; and
   - a short qualitative comparison of the predicted and Webots tool poses.

Do not submit `lab02_work.wbt`, downloaded vendor assets, installed software, or caches unless requested.

## Short Webots Recovery

If Webots crashes or behaves unexpectedly:

1. Close Webots.
2. Reopen `lab02_starter.wbt` while paused. If it opens, the working world was damaged.
3. Delete or rename only your `lab02_work.wbt`, then create a fresh working copy from the starter.
4. Test `void`, then `diagnostic_minimal`, then `diagnostic_devices`.
5. Run motion code only after those stages pass.
6. If the clean world works with `void` but crashes with a Python controller, recheck the Python command in Webots Preferences.

See [Webots Troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md) for safe-mode recovery and additional details.
