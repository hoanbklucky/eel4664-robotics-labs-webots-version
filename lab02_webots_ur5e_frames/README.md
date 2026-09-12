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

Here, `c_x=\cos(x)` and `s_x=\sin(x)`. You do not need to derive this matrix. Compare it with the supplied NumPy matrix and complete only two missing entries.

Use this table in meters and radians:

| Joint `i` | `\alpha_{i-1}` | `a_{i-1}` | `d_i` | `\theta_i` from Webots |
|---:|---:|---:|---:|---:|
| 1 | `0` | `0` | `0.1625` | `q_1` |
| 2 | `\pi/2` | `0` | `0` | `-q_2` |
| 3 | `0` | `0.4250` | `0` | `-q_3` |
| 4 | `0` | `0.3922` | `-0.1333` | `-q_4` |
| 5 | `\pi/2` | `0` | `0.0997` | `q_5` |
| 6 | `-\pi/2` | `0` | `-0.0996` | `-q_6` |

This is still Craig modified DH. The signs in the last column only map Webots encoder-positive directions to the corresponding `\theta_i` directions. The supplied `WEBOTS_TO_MDH_SIGN` array applies that mapping. The nominal dimensions and the rounded Webots geometry differ slightly, so errors around a millimeter are reasonable.

### Chaining the six transforms

The provided `forward_kinematics(q)` function starts with identity and appends one link transform at a time:

```python
T = np.eye(4)
for qi, direction, parameters in zip(q, WEBOTS_TO_MDH_SIGN, UR5E_MDH):
    alpha_previous, a_previous, d, offset = parameters
    theta = direction * qi + offset
    T = T @ dh_transform(alpha_previous, a_previous, d, theta)
return T
```

After each multiplication, `T` advances one frame:

```text
T_0_1
T_0_1 T_1_2 = T_0_2
...
T_0_1 T_1_2 T_2_3 T_3_4 T_4_5 T_5_6 = T_0_6
```

Order matters because matrix multiplication is not commutative.

### Provided tool transform

Craig frame `{6}` and the Webots tool sensor use different axis directions. The course provides their fixed relationship:

```python
T_6_TOOL = np.array([
    [-1.0,  0.0,  0.0, 0.0],
    [ 0.0,  0.0, -1.0, 0.0],
    [ 0.0, -1.0,  0.0, 0.0],
    [ 0.0,  0.0,  0.0, 1.0],
])
```

It is already defined in `src/ur5e_fk_starter.py`. Do not estimate or modify it. Calculate the predicted Webots tool pose with

```python
T_world_tool = forward_kinematics(q) @ T_6_TOOL
```

The robot base is at the world origin in this lab, so `T_world_0` is identity.

## Provided Files

- `worlds/lab02_starter.wbt` - protected starter world
- `controllers/diagnostic_minimal/` and `diagnostic_devices/` - startup checks
- `controllers/eel4664_ur5e/` - safe one-joint controller template
- `controllers/fk_experiment/` - A -> B -> C -> A experiment
- `src/transforms.py` and `src/transform_point.py` - complete support code; do not modify
- `src/ur5e_fk_starter.py` - the two-entry FK exercise
- `answers.md` - response template

## Student Workflow

### Step 1 - Prepare and open a working world

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

Select `UR5e "UR5E"` in the Scene Tree, double-click its `controller` field, select a controller, press **Reset**, and then press **Run**.

| Controller | Expected Console result | Movement |
|---|---|---|
| `diagnostic_minimal` | `[DIAGNOSTIC PASS] completed 10 steps` | none |
| `diagnostic_devices` | 15 devices followed by `[DIAGNOSTIC PASS] all device handles enumerated` | none |

The device list must include six motors, six position sensors, `tool_position`, `tool_orientation`, and `tool_test_point_position`.

![Successful minimal and device diagnostics](images/diagnostics_pass.png)

Stop and use the Troubleshooting section if either diagnostic fails.

### Step 3 - Confirm one-joint motion

If `controllers/lab02_controller` does not exist, close Webots and run:

```bash
python -c "from pathlib import Path; import shutil; src=Path('lab02_webots_ur5e_frames/controllers/eel4664_ur5e'); dst=Path('lab02_webots_ur5e_frames/controllers/lab02_controller'); shutil.copytree(src,dst); (dst/'eel4664_ur5e.py').rename(dst/'lab02_controller.py')"
```

Assign `lab02_controller` in `lab02_work.wbt`. Before running, note that only the shoulder-pan target changes:

```python
q_goal = q0.copy()
q_goal[0] += 0.10
duration = 4.0
settle_duration = 1.0
```

![Lab 2 working world with the one-joint controller assigned](images/one_joint_controller_ready.png)

Press **Reset**, then **Run**. The shoulder-pan joint should move smoothly by about `+0.10` rad, hold for one second, and print `[TRACKING PASS]`. Small differences between target and measured angles are normal. No values from this step are required in `answers.md`.

### Step 4 - Complete and test forward kinematics

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

The zero pose is easy to inspect, but many sine terms vanish there. The nonsymmetric pose activates more terms and is more likely to reveal a sign or placement mistake. Record the two completed entries and both outputs in `answers.md`.

### Step 5 - Predict, then run the robot experiment

The provided controller visits:

| Pose | `q_goal` [rad] |
|---|---|
| A | `[0.0, -1.20, 1.20, -1.50, -1.57, 0.0]` |
| B | `[0.20, -0.80, 1.00, -1.10, -0.70, 0.30]` |
| C | `[-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]` |

Before opening the controller, calculate and record the predicted tool position for each pose:

```python
import numpy as np
from lab02_webots_ur5e_frames.src.ur5e_fk_starter import (
    T_6_TOOL,
    forward_kinematics,
)

targets = {
    "A": np.array([0.0, -1.20, 1.20, -1.50, -1.57, 0.0]),
    "B": np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30]),
    "C": np.array([-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]),
}

for label, q_goal in targets.items():
    T_predicted = forward_kinematics(q_goal) @ T_6_TOOL
    print(label, T_predicted[:3, 3])
```

Now assign `fk_experiment` in `lab02_work.wbt`, press **Reset**, and press **Run**. Watch the stylus move A -> B -> C -> A. Copy the measured `q`, tool position, and tool RPY for A-C from the Console.

### Step 6 - Compare FK with Webots

For each pose, calculate the prediction again using its **measured** joint angles:

```python
T_predicted = forward_kinematics(q_measured) @ T_6_TOOL
p_predicted = T_predicted[:3, 3]
R_predicted = T_predicted[:3, :3]
```

Construct the measured rotation from the Webots RPY values:

```python
roll, pitch, yaw = measured_rpy
R_measured = rotz(yaw) @ roty(pitch) @ rotx(roll)
```

Then calculate

```python
position_error_m = np.linalg.norm(p_predicted - p_measured)
R_error = R_predicted.T @ R_measured
orientation_error_rad = np.arccos(
    np.clip((np.trace(R_error) - 1.0) / 2.0, -1.0, 1.0)
)
```

Complete one A-C comparison table containing:

- measured `q`;
- predicted and measured tool position;
- position error in millimeters; and
- orientation error in degrees.

Report mean and maximum position error, mean and maximum orientation error, and two or three sentences interpreting the results. Errors near 1 mm can result from nominal dimensions being slightly different from the rounded Webots geometry. Large or pose-dependent errors usually indicate an incorrect DH entry, joint sign, or multiplication order.

Webots may provide measurements, but it must not calculate FK for the submitted work.

## What to Submit

1. Completed `src/ur5e_fk_starter.py`.
2. Completed `answers.md` containing:
   - the two modified-DH entries;
   - both offline FK test outputs;
   - three pre-run position predictions;
   - the A-C comparison table; and
   - the error summary and interpretation.

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
