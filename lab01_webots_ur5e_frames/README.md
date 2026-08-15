# Lab 1 - UR5e Frames and Forward Kinematics

## Mission

**Predict where the UR5e tool will move, watch its stylus air-draw a loop, and test your forward-kinematics model against Webots measurements.**

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

Open `worlds/lab01_starter.wbt` paused and immediately use **File -> Save World As...** to create `worlds/lab01_work.wbt`.

## Success Criteria

You have completed the mission when:

- the world and two quick diagnostics pass;
- the robot completes a safe one-joint motion by Step 3;
- you can explain the provided homogeneous-transform code;
- your UR5e FK returns a valid transform;
- one fixed tool-frame alignment is reused while the robot air-draws through three held-out poses; and
- position, orientation, and tool-point errors are reported quantitatively.

## Learning Objectives

- Identify the UR5e joint order, link sequence, base frame, and tool frame.
- Read, explain, and verify NumPy implementations of rotation matrices and homogeneous transforms.
- Implement a six-link UR5e FK chain from an explicit DH convention.
- Read ordered Webots joint sensors without using simulator kinematics.
- Validate predicted tool position and orientation against read-only sensors.
- Diagnose errors caused by units, joint order, offsets, and frame conventions.

## Prerequisites

Complete [Lab 00 - Software Setup and Webots Basics](../lab00_setup/README.md), including Webots Tutorials 1 and 4. Review coordinate frames, rotation matrices, homogeneous transforms, and the forward-kinematics derivation from lecture.

Tutorials 2 and 3 remain optional in [Optional Webots Basics](../README.md#optional-webots-basics).

## Background

A `.wbt` world instantiates the robot and environment. The UR5e PROTO defines its links, joints, motors, sensors, and tool slot. A Python controller repeats:

```text
read sensors -> compute command -> send motor targets -> robot.step()
```

Use radians, meters, seconds, and simulation time from `robot.getTime()`.

| Index | Motor | Position sensor |
|---:|---|---|
| 0 | `shoulder_pan_joint` | `shoulder_pan_joint_sensor` |
| 1 | `shoulder_lift_joint` | `shoulder_lift_joint_sensor` |
| 2 | `elbow_joint` | `elbow_joint_sensor` |
| 3 | `wrist_1_joint` | `wrist_1_joint_sensor` |
| 4 | `wrist_2_joint` | `wrist_2_joint_sensor` |
| 5 | `wrist_3_joint` | `wrist_3_joint_sensor` |

A **point** is a location, such as the tool tip or an object center. A **direction** is an arrow with length and orientation but no fixed location, such as "move along +x" or the direction of a surface normal. The same three numbers can represent either one; their meaning determines how a coordinate transform treats them.

For a point `p_b` expressed in frame `{b}`:

```text
p_a = R_ab p_b + t_ab
[p_a; 1] = T_ab [p_b; 1]
```

The homogeneous coordinate 1 causes the translation column to be added. For example, if a frame moves 2 m in +x, the point `[1, 0, 0]` moves to `[3, 0, 0]` before any rotation is considered.

A free direction has homogeneous coordinate zero:

```text
v_a = R_ab v_b
[v_a; 0] = T_ab [v_b; 0]
```

Multiplying the translation column by zero removes its effect. Translating a frame does not change which way its +x arrow points; only rotation changes a direction.

Webots supplies read-only tool sensors to validate your calculation. It does not perform the transformation for you.

For the UR5e, compute:

```text
T_0_6(q) = A_1(q1) A_2(q2) ... A_6(q6)
A_i = Rotz(theta_i) Transz(d_i) Transx(a_i) Rotx(alpha_i)
```

Use this standard DH table in meters and radians:

| Joint | `a_i` | `alpha_i` | `d_i` | `theta_i` |
|---:|---:|---:|---:|---|
| 1 | 0 | `pi/2` | 0.1625 | `q1` |
| 2 | -0.4250 | 0 | 0 | `q2` |
| 3 | -0.3922 | 0 | 0 | `q3` |
| 4 | 0 | `pi/2` | 0.1333 | `q4` |
| 5 | 0 | `-pi/2` | 0.0997 | `q5` |
| 6 | 0 | 0 | 0.0996 | `q6` |

The values are the nominal UR5e parameters published by [Universal Robots](https://www.universal-robots.com/articles/ur/application-installation/dh-parameters-for-calculations-of-kinematics-and-dynamics). The pinned Webots geometry contains rounded dimensions, so a small residual is expected.

Relate the DH result to the measured tool frame explicitly:

```text
T_world_tool = T_world_0 T_0_6(q) T_6_tool
```

### How to read a transform chain

The notation `T_a_b` means "convert coordinates from frame `{b}` into frame `{a}`." Therefore:

- `forward_kinematics(q_goal)` returns `T_0_6`: the pose of DH frame `{6}` relative to base frame `{0}`;
- `T_6_tool` converts from the tool frame to frame `{6}`; and
- multiplying them gives `T_0_tool`, the tool pose relative to the base.

```python
T_0_tool = forward_kinematics(q_goal) @ T_6_tool
```

The NumPy `@` symbol means matrix multiplication. Read the chain from right to left: first convert tool coordinates into frame `{6}`, then convert frame `{6}` coordinates into frame `{0}`. The adjacent frame labels match and "cancel":

```text
T_0_6 T_6_tool = T_0_tool
      ^ ^
      same intermediate frame
```

Order matters. In general, `T_0_6 @ T_6_tool` is not equal to `T_6_tool @ T_0_6`. Use `@` for transform composition; do not use `*`, which performs element-by-element multiplication in NumPy.

In the supplied world, the robot base has zero world translation/rotation, so `T_world_0` is identity. Consequently, `T_world_tool` and `T_0_tool` have the same numerical value in this lab. Determine `T_6_tool` once from the alignment configuration and keep it unchanged for every validation configuration.


## Provided Files

- `worlds/lab01_starter.wbt` - protected UR5e world with validation sensors
- `controllers/diagnostic_minimal/` - confirms that Python starts
- `controllers/diagnostic_devices/` - lists the required devices
- `controllers/eel4664_ur5e/` - safe one-joint motion and Webots device adapter
- `controllers/fk_experiment/` - ready-to-run FK prediction and air-drawing challenge
- `src/transforms.py` and `src/transform_point.py` - complete, commented transform utilities
- `src/test_transforms.py` - short offline transform test
- `src/ur5e_fk_starter.py` - DH table and student FK starter
- `src/read_configuration.py` and `src/query_transform.py` - optional debugging helpers, not required in the main workflow
- `answers.md` - concise response template

## Part 1 - Setup / Validation: Get the Robot Moving

The robot moves in Step 3. Complete Steps 1-2 quickly, but stop if either diagnostic fails.

### Step 1 - Prepare and open the working world

1. Open PowerShell and go to the repository:

   ```powershell
   cd C:\eel4664-robotics-labs
   ```

2. Close Webots and prepare the pinned R2025a UR5e assets:

   ```powershell
   powershell -ExecutionPolicy Bypass -File .\lab00_setup\prepare_webots_sample.ps1
   Test-Path .\webots\vendor\webots_r2025a\projects\robots\universal_robots\protos\UR5e.proto
   ```

   The script downloads one known-good copy of the official UR5e model and its dependencies inside the repository. The final command must return `True`.

3. Start Webots R2025a while paused and open:

   ```text
   C:\eel4664-robotics-labs\lab01_webots_ur5e_frames\worlds\lab01_starter.wbt
   ```

4. Confirm the complete robot, floor, and short stylus and bright orange tip are visible and the robot controller is `void`.
5. Immediately select **File -> Save World As...** and save `lab01_work.wbt` beside the starter.
6. Confirm the title bar shows `lab01_work.wbt`.

**Never overwrite `lab01_starter.wbt`.** Make all controller assignments in the working copy. If you created `lab01_work.wbt` before the stylus was added, discard that old working copy and create a fresh one from the updated starter.

### Step 2 - Run two quick diagnostics

To assign a controller, select `UR5e "UR5E"` in the Scene Tree, double-click its `controller` field, choose the controller name, press **Reset**, and then press **Run**.

| Controller | Expected result | Movement? |
|---|---|---|
| `diagnostic_minimal` | Console prints `[DIAGNOSTIC PASS] completed 10 steps` | none |
| `diagnostic_devices` | Console ends with `[DIAGNOSTIC PASS] all device handles enumerated` | none |

For the device check, confirm six motors, six joint sensors, `tool_position`, `tool_orientation`, and `tool_test_point_position` appear. These diagnostics do not command joints. If either fails, use the Troubleshooting section before continuing.

### Step 3 - Move one joint and save the alignment data

If `controllers\lab01_controller` does not already exist, close Webots and run:

```powershell
Copy-Item .\lab01_webots_ur5e_frames\controllers\eel4664_ur5e .\lab01_webots_ur5e_frames\controllers\lab01_controller -Recurse
Rename-Item .\lab01_webots_ur5e_frames\controllers\lab01_controller\eel4664_ur5e.py lab01_controller.py
```

Confirm `lab01_controller.py` contains:

```python
q_goal = q0.copy()
q_goal[0] += 0.10
duration = 4.0
```

1. Open `lab01_work.wbt` and assign `lab01_controller`.
2. Before running, predict which links will move and in which direction.
3. Press **Reset**, then **Run**.
4. Confirm the shoulder-pan joint moves smoothly by approximately +0.10 rad while the other joint targets remain at their measured starting values.
5. Copy these final Console values into `answers.md`:
   - six measured joint angles `q_align` with at least six decimal places;
   - tool position `[x, y, z]`;
   - tool orientation `[roll, pitch, yaw]`; and
   - tool test-point position.

These synchronized final measurements are the one alignment data set used later. Do not calculate anything yet - first get the robot moving and preserve the measurements.

## Part 2 - Core Implementation

### Step 4 - Read and check the provided transform code

Do not rewrite `src/transforms.py` or `src/transform_point.py`. Read the comments and be able to answer:

- Which coordinate stays fixed in `rotx`, `roty`, and `rotz`?
- Why does a point use homogeneous coordinate 1 while a direction uses 0?
- Why is the inverse translation `-R.T @ p` rather than simply `-p`?

Before running the code, consider this operation:

```python
v_before = np.array([1.0, 0.0, 0.0])  # unit vector along +x
v_after = rotz(np.pi / 2.0) @ v_before
```

`rotz(np.pi / 2.0)` creates a matrix for a positive 90-degree rotation about the z-axis. The NumPy `@` operator multiplies that rotation matrix by the vector. Using the right-hand rule, predict where the +x vector points afterward. Also predict what happens when translation `[1, 2, 3]` is applied to a point versus a direction. Then run:

```powershell
python .\lab01_webots_ur5e_frames\src\test_transforms.py
python -c "import numpy as np; from lab01_webots_ur5e_frames.src.transform_point import transform_point,transform_direction; T=np.eye(4); T[:3,3]=[1,2,3]; print(transform_point(T,np.array([.1,.2,.3]))); print(transform_direction(T,np.array([1,0,0])))"
```

Expected output includes:

```text
All transformation tests passed.
[1.1 2.2 3.3]
[1. 0. 0.]
```

Record your predictions and one-sentence explanations in `answers.md`.

### Step 5 - Implement forward kinematics

The Background section defines the standard-DH convention, parameter table, and multiplication order. In `src/ur5e_fk_starter.py`, complete:

- `dh_transform(a, alpha, d, theta)`; and
- `forward_kinematics(q)` as the ordered product `A_1 A_2 ... A_6`.

Write the definition of `A_i` and the frame order in `answers.md`, then run:

```powershell
python -c "import numpy as np; from lab01_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; T=forward_kinematics(np.zeros(6)); print(T); print('orthogonality=',np.linalg.norm(T[:3,:3].T@T[:3,:3]-np.eye(3))); print('det=',np.linalg.det(T[:3,:3]))"
```

Pass conditions:

- `T` is 4-by-4 with last row `[0, 0, 0, 1]`;
- rotation orthogonality error is below `1e-8`; and
- the rotation determinant is within `1e-8` of 1.

Repeat once with `q = [0.20, -0.80, 1.00, -1.10, -0.70, 0.30]`. Webots must not be used to calculate FK.

### Step 6 - Determine the fixed tool transform once

The DH calculation ends at frame `{6}`, while Webots measures the tool frame. Their constant relationship is `T_6_tool`:

```text
T_world_tool = T_world_6 T_6_tool
T_6_tool = inverse(T_world_6) T_world_tool
```

Use only the alignment data recorded in Step 3. Create a small analysis script from this pattern and replace each `...` with the recorded numbers:

```python
import numpy as np
from lab01_webots_ur5e_frames.src.transforms import (
    homogeneous, invert_transform, rotx, roty, rotz
)
from lab01_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics

q_align = np.array([...])
origin_world = np.array([...])
rpy_world_tool = np.array([...])

roll, pitch, yaw = rpy_world_tool
R_world_tool = rotz(yaw) @ roty(pitch) @ rotx(roll)
T_world_tool_measured = homogeneous(R_world_tool, origin_world)
T_world_6 = forward_kinematics(q_align)  # T_world_0 is identity
T_6_tool = invert_transform(T_world_6) @ T_world_tool_measured
print(np.array2string(T_6_tool, precision=8, suppress_small=True))
```

Save the printed 4-by-4 matrix in `answers.md`. This is a one-time frame alignment. Reuse it unchanged at every validation pose; recomputing it would hide FK errors.

## Part 3 - Robot Experiment

### Step 7 - Predict, air-draw a loop, and compare three poses

The provided `fk_experiment` controller moves the UR5e through Poses A, B, and C, then returns to A to close an air-drawn loop. The supplied visual stylus extends 0.05 m along the tool frame's +x axis. Its bright orange tip marks `p_tool = [0.05, 0, 0]` m, making the motion easy to follow and tying the visual experiment to Step 8. It has no collision geometry or physics, so it cannot contact or disturb the environment. This is air drawing: the tip shows the path while moving but does not leave a permanent line. Do not edit the targets.

| Pose | Commanded `q_goal` [rad] |
|---|---|
| A | `[0.0, -1.20, 1.20, -1.50, -1.57, 0.0]` |
| B | `[0.20, -0.80, 1.00, -1.10, -0.70, 0.30]` |
| C | `[-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]` |

#### Predict before running Webots

For each commanded `q_goal`, calculate:

```python
T_world_tool_predicted_from_q_goal = forward_kinematics(q_goal) @ T_6_tool
p_world_tool_predicted_from_q_goal = T_world_tool_predicted_from_q_goal[:3, 3]
```

Record the three predicted tool positions before starting the controller. Also make a simple qualitative prediction for A to B, B to C, and C back to A: will the tool move mainly left/right, forward/backward, or up/down? These are genuine predictions; do not look at Webots measurements first.

#### Watch the robot execute the experiment

1. Open `lab01_work.wbt` and leave it paused.
2. Select `UR5e "UR5E"`, double-click its `controller` field, and choose `fk_experiment`.
3. Press **Reset** and visually confirm that the arm's workspace is clear.
4. Press **Run** and follow the orange stylus tip as the robot moves A -> B -> C -> A. Each smooth move takes eight seconds, followed by a short settling pause.
5. Confirm that the stylus tip returns to its starting point and the Console finishes with:

   ```text
   [LOOP CLOSED] Returned to Pose A.
   [EXPERIMENT DONE] Air-drawn loop A -> B -> C -> A completed.
   ```

6. Copy the labeled measurement block for Poses A, B, and C into your results. Each block contains measured `q`, tool position, tool RPY, and tool-test-point position. The return to A is a visual closure check, so the controller does not print a duplicate measurement block for it.

The three segments may look curved rather than perfectly straight. This controller interpolates the six **joint angles**, so it does not command a straight Cartesian tool path. Generating and tracking straight tool-space paths is a later trajectory-planning objective.

#### Make the quantitative comparison

Commanded and measured joint angles can differ slightly. For the final accuracy calculation, recompute each prediction with the **measured** joint vector printed at that pose:

```python
T_world_tool_predicted_from_q_measured = forward_kinematics(q_measured) @ T_6_tool
```

Compare this result with the Webots tool measurement. Keep the pre-run commanded-angle prediction as evidence that you predicted the motion before observing it. Do not change the DH parameters or `T_6_tool` after seeing Poses A-C.
### Step 8 - Check a point attached to the tool

For Pose C, use:

```python
p_tool = np.array([0.05, 0.0, 0.0])
p_world_predicted = transform_point(T_world_tool_predicted_from_q_measured, p_tool)
```

Compare this prediction with the printed `tool_test_point_position`. This checks the predicted tool orientation and translation together.

## Part 4 - Quantitative Analysis

For Poses A-C, compute:

```text
position_error = ||p_predicted - p_measured||_2
R_error = R_predicted^T R_measured
orientation_error = acos(clamp((trace(R_error) - 1) / 2, -1, 1))
```

Submit one four-row table: the alignment row plus three held-out validation rows. Include measured `q`, predicted/measured tool position, position error in millimeters, and orientation error in degrees. Clearly mark the alignment row and exclude it from held-out error statistics.

Report:

- mean and maximum position error over Poses A-C;
- mean and maximum orientation error over Poses A-C;
- Pose C tool-test-point error; and
- one plot comparing position and orientation error across A-C.

Briefly explain whether the remaining error is more consistent with rounded model dimensions, a constant frame error, or an incorrect joint/transform convention.

## Engineering Questions

1. Why must joint order and transform multiplication order be explicit?
2. What physical relationship does each row of the DH table describe?
3. Why must `T_6_tool` remain fixed for Poses A-C?
4. Why should FK use measured joint angles instead of commanded targets?
5. What error pattern would suggest a wrong joint sign or transform order?
6. Why does translation affect a point but not a free direction?

## What to Submit

- completed `ur5e_fk_starter.py`;
- completed `answers.md` with transform-code explanations and the DH convention;
- Step 3 alignment measurements and fixed `T_6_tool`;
- the three pre-run target-position predictions;
- the alignment plus three-pose measured comparison table;
- position, orientation, and tool-test-point errors;
- one error plot; and
- answers to the six Engineering Questions.

Do not submit `lab01_work.wbt`, installed software, downloaded vendor assets, or caches unless requested.

## Troubleshooting

| Last passing stage | First failing stage | Likely problem |
|---|---|---|
| none | world opens | missing vendor assets or damaged world |
| world | minimal controller | Webots Python command or controller discovery |
| minimal | device diagnostic | wrong working world or missing devices |
| devices | one-joint motion | joint order, target, or controller copy |
| transform test | FK structural test | DH matrix or multiplication order |
| FK test | alignment | RPY order or frame-chain direction |
| alignment | held-out poses | joint sign/order, DH convention, or changing `T_6_tool` |

Recovery:

1. Pause Webots and save needed code or measurements.
2. Reopen `lab01_starter.wbt` directly and create a fresh working copy.
3. Repeat `diagnostic_minimal -> diagnostic_devices -> one-joint motion`.
4. Test FK outside Webots before returning to the experiment.
5. Reuse the original Step 3 alignment; do not recalibrate on a validation pose.

For repeated crashes or safe mode, see [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md).