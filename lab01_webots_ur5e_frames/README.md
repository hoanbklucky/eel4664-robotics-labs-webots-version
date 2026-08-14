# Lab 1 - UR5e Frames and Forward Kinematics

## Mission

**Bring the UR5e online and predict its tool pose using your own forward-kinematics model.**

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

Open `worlds/lab01_starter.wbt` paused and immediately use **File -> Save World As...** to create `worlds/lab01_work.wbt`.

## Success Criteria

You have completed the mission when:

- the clean world, minimal controller, and device diagnostic pass in order;
- a one-joint motion behaves as predicted and repeats after Reset;
- your homogeneous-transform functions pass offline tests;
- your UR5e FK returns a valid transform for every tested joint vector;
- FK predicts the measured Webots tool pose at five or more configurations;
- position and orientation errors are reported quantitatively; and
- you explain the remaining difference between the nominal model and simulation.

## Learning Objectives

- Identify the UR5e joint order, link sequence, base frame, and tool frame.
- Implement and test rotation matrices and homogeneous transforms.
- Implement a six-link UR5e FK chain from an explicit DH convention.
- Read ordered Webots joint sensors without using simulator kinematics.
- Validate predicted tool position and orientation against read-only sensors.
- Separate mathematical models, Webots adapters, logging, and analysis.
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

For a point `p_b` expressed in frame `{b}`:

```text
[p_a; 1] = T_ab [p_b; 1]
```

A free direction has homogeneous coordinate zero, so translation does not affect it:

```text
[v_a; 0] = T_ab [v_b; 0]
```

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

In the supplied world, the robot base has zero world translation/rotation, so `T_world_0` is identity. Determine and document the single fixed frame-convention transform `T_6_tool` using the assigned alignment configuration, then keep it unchanged for every validation configuration. Do not fit a different offset at each pose.


## Provided Files

- `worlds/lab01_starter.wbt` - protected world with read-only tool validation sensors
- `controllers/diagnostic_minimal/` - Python startup test
- `controllers/diagnostic_devices/` - read-only device inventory
- `controllers/eel4664_ur5e/` - shared UR5e adapter and safe motion example
- `src/inspect_joint_states.py` - joint-state logging starter
- `src/send_joint_goal.py` - smooth joint-command starter
- `src/transform_point.py` - introductory point/direction transform starter
- `src/transforms.py` and `src/test_transforms.py` - reusable homogeneous-transform library and tests
- `src/ur5e_fk_starter.py` - official nominal DH table and FK starter
- `src/read_configuration.py` - ordered Webots joint-vector reader
- `src/query_transform.py` - read-only tool sensor adapter
- `answers.md` - engineering response template

## Part 1 - Setup / Validation

Complete these checkpoints in order. Stop at the first failure.

### Step 1 - Open the repository

Open PowerShell:

```powershell
cd C:\eel4664-robotics-labs
git status --short
```

A nonempty status is not automatically an error. Do not delete work you recognize. Confirm `lab00_setup` and `lab01_webots_ur5e_frames` are present.

### Step 2 - Prepare the pinned UR5e assets

Close Webots, then run:

```powershell
powershell -ExecutionPolicy Bypass -File .\lab00_setup\prepare_webots_sample.ps1
Test-Path C:\webots-eel4664-sample\projects\robots\universal_robots\protos\UR5e.proto
```

The preparation command should end with `[READY] Official Universal Robots sample:` and `Test-Path` must return `True`. Stop here if it returns `False`.

### Step 3 - Open the protected starter

1. Start Webots R2025a and keep it paused.
2. Select **File -> Open World...**.
3. Open `C:\eel4664-robotics-labs\lab01_webots_ur5e_frames\worlds\lab01_starter.wbt`.
4. Confirm the Scene Tree contains `WorldInfo`, `Viewpoint`, a floor `Solid`, and `UR5e "UR5E"`.
5. Confirm the robot and floor render in the 3-D view.
6. Select `UR5e "UR5E"` and verify its `controller` field is `void`.

If the Console reports a skipped UR5e, missing PROTO, or fallback URL error, stop and repeat Step 2.

### Step 4 - Save a working copy immediately

1. While paused, select **File -> Save World As...**.
2. Save beside the starter as `lab01_work.wbt`.
3. Confirm the title bar shows the working filename.
4. Make controller assignments and world changes only in this copy.

If that name already contains work you need, choose `lab01_work_yourname.wbt`. Never replace `lab01_starter.wbt`.

### Step 5 - Validate the world with void

1. Leave the controller as `void`.
2. Press **Reset**.
3. Run for about two seconds, then pause.

Pass: Webots stays open, the robot remains visible, and no controller error appears. Failure here indicates a world, asset, or rendering problem.

### Step 6 - Run the minimal controller

1. Pause and Reset.
2. Select the UR5e and double-click its `controller` field.
3. Choose `diagnostic_minimal`.
4. Reset and run.

Expected Console text includes:

```text
[DIAGNOSTIC PASS] controller started
[DIAGNOSTIC PASS] completed 10 steps
[DIAGNOSTIC DONE]
```

If the controller is unavailable, confirm the working world is in the Lab 1 `worlds` folder beside the `controllers` folder.

### Step 7 - Verify devices

1. Pause and Reset.
2. Assign `diagnostic_devices`.
3. Reset and run.
4. Copy the device inventory into your notes.

Confirm all six motors and six corresponding `_sensor` names. Also confirm `tool_position`, `tool_orientation`, and `tool_test_point_position`.

Pass: the Console ends with `[DIAGNOSTIC PASS] all device handles enumerated`. If the tool devices are absent, preserve needed work, reopen the current starter, and create a new work copy.

### Step 8 - Create your controller copy

Do not edit diagnostic controllers. Close Webots and run these two commands:

```powershell
Copy-Item .\lab01_webots_ur5e_frames\controllers\eel4664_ur5e .\lab01_webots_ur5e_frames\controllers\lab01_controller -Recurse
Rename-Item .\lab01_webots_ur5e_frames\controllers\lab01_controller\eel4664_ur5e.py lab01_controller.py
```

If `lab01_controller` already exists, do not copy again. Open `lab01_controller.py` and `ur5e_devices.py` in VS Code and keep this folder under Git.

### Step 9 - Run the one-joint checkpoint

Immediately after `q0` is measured in `lab01_controller.py`, use:

```python
q_goal = q0.copy()
q_goal[0] += 0.10
duration = 4.0
```

This commands +0.10 rad at the shoulder-pan joint while holding the other five targets.

1. Save the file and open `lab01_work.wbt`.
2. Assign `lab01_controller`.
3. Reset and confirm the arm is clear.
4. Predict which links move and record the expected sign.
5. Run until initial, target, and final vectors print.
6. Reset and repeat.

Pass: only target index 0 changes, the measured change is near +0.10 rad, and both runs move in the same direction without a jump.

### Step 10 - Record checkpoint evidence

Complete this table in `answers.md`:

| Stage | Controller | Expected | Actual | Pass? |
|---|---|---|---|---|
| World | `void` | stable world | | |
| Python | `diagnostic_minimal` | 10 steps | | |
| Devices | `diagnostic_devices` | all required names | | |
| **One joint:** | `lab01_controller` | joint 0 moves +0.10 rad | | |
| **Full algorithm:** | not yet | wait for Parts 2-3 | | |

Do not continue until the first four rows pass.

## Part 2 - Core Implementation

### Step 11 - Complete homogeneous-transform utilities

1. Finish the introductory `transform_point` and `transform_direction` functions in `src/transform_point.py`.
2. Finish `rotx`, `roty`, `rotz`, `homogeneous`, and `invert_transform` in `src/transforms.py`.
3. Keep both files free of Webots API calls.
4. Run the provided tests:

```powershell
python .\lab01_webots_ur5e_frames\src\test_transforms.py
```

Expected final line:

```text
All transformation tests passed.
```

Also run this point/direction check:

```powershell
python -c "import numpy as np; from lab01_webots_ur5e_frames.src.transform_point import transform_point,transform_direction; T=np.eye(4); T[:3,3]=[1,2,3]; print(transform_point(T,np.array([.1,.2,.3]))); print(transform_direction(T,np.array([1,0,0])))"
```

Expected output is `[1.1 2.2 3.3]` followed by `[1. 0. 0.]`.

### Step 12 - Document the FK convention before coding

In `answers.md`:

1. copy the six-row DH table from Background;
2. sketch frames `{0}` through `{6}`;
3. write the exact definition of `A_i`;
4. state that joint inputs are Webots sensor readings in radians;
5. state the multiplication order; and
6. define `T_world_0` and the fixed `T_6_tool`.

Do not change the DH table merely to force one pose to match. A fixed frame-convention transform must remain fixed across all poses.

### Step 13 - Implement and test UR5e forward kinematics offline

Open `src/ur5e_fk_starter.py`. The nominal parameters are provided; implement:

- `dh_transform(a, alpha, d, theta)`; and
- `forward_kinematics(q)` as an ordered product of six transforms.

Run this structural test:

```powershell
python -c "import numpy as np; from lab01_webots_ur5e_frames.src.ur5e_fk_starter import forward_kinematics; T=forward_kinematics(np.zeros(6)); print(T); print('orthogonality=',np.linalg.norm(T[:3,:3].T@T[:3,:3]-np.eye(3))); print('det=',np.linalg.det(T[:3,:3]))"
```

Pass conditions:

- `T` has shape `(4, 4)`;
- its last row is `[0, 0, 0, 1]`;
- orthogonality error is below `1e-8`; and
- the rotation determinant is within `1e-8` of 1.

Repeat with a nonsymmetric vector such as:

```python
q_test = np.array([0.20, -0.80, 1.00, -1.10, -0.70, 0.30])
```

Your function must reject a vector that is not six finite joint angles.

### Step 14 - Read one synchronized Webots configuration

Create an assignable copy of the provided reader:

```powershell
New-Item -ItemType Directory -Force .\lab01_webots_ur5e_frames\controllers\read_configuration
Copy-Item .\lab01_webots_ur5e_frames\src\read_configuration.py .\lab01_webots_ur5e_frames\controllers\read_configuration\read_configuration.py
```

1. Assign `read_configuration` in `lab01_work.wbt`.
2. Reset and run once.
3. Confirm it prints six values in the required joint order.
4. Record the vector with at least six decimal places.
5. Compute FK from that saved vector before reading tool ground truth.

### Step 15 - Read the tool reference and align frames

Create the tool-reference controller:

```powershell
New-Item -ItemType Directory -Force .\lab01_webots_ur5e_frames\controllers\query_transform
Copy-Item .\lab01_webots_ur5e_frames\src\query_transform.py .\lab01_webots_ur5e_frames\controllers\query_transform\query_transform.py
Copy-Item .\lab01_webots_ur5e_frames\src\transform_point.py .\lab01_webots_ur5e_frames\controllers\query_transform\transform_point.py
```

Assign `query_transform`, Reset, and run. It prints:

- `tool_position` in world coordinates;
- tool roll, pitch, and yaw; and
- `tool_test_point_position`.

Use the assigned alignment configuration to determine the single fixed `T_6_tool`. Then lock that value. Validate it on the remaining configurations; never refit it per pose.

For rotation comparison, form:

```text
R_world_tool_measured = Rz(yaw) Ry(pitch) Rx(roll)
```

### Step 16 - Add interpolation and synchronized logging

Complete `interpolate` in `src/send_joint_goal.py`. It must accept two six-element arrays, reject nonpositive duration, clamp time, return exact endpoints, and use a zero-endpoint-velocity blend.

Test:

```powershell
python -c "import numpy as np; from lab01_webots_ur5e_frames.src.send_joint_goal import interpolate; q0=np.zeros(6); qf=np.ones(6); print(interpolate(q0,qf,0,4)); print(interpolate(q0,qf,4,4))"
```

Create `lab01_webots_ur5e_frames\results` and add logging to `lab01_controller.py`. Each row must contain one simulation timestamp, six commanded joints, six measured joints, predicted tool position, measured tool position, and trial/configuration label. Save commands separately from measurements and use `robot.getTime()`.

## Part 3 - Robot Experiment

### Step 17 - Collect one alignment and five validation configurations

Use the measured joint vector after the robot has settled. Configuration 1 is used only to establish `T_6_tool`; Configurations 2-6 are held-out FK validations.

| Configuration | Requested condition/target |
|---:|---|
| 1 | Reset configuration; frame alignment only |
| 2 | Reset plus +0.10 rad at joint 0 |
| 3 | `[0.0, -1.20, 1.20, -1.50, -1.57, 0.0]` |
| 4 | `[0.20, -0.80, 1.00, -1.10, -0.70, 0.30]` |
| 5 | `[-0.30, -0.90, 1.10, -1.40, -1.20, -0.20]` |
| 6 | `[0.35, -1.05, 0.85, -1.25, -0.95, 0.25]` |

Use smooth motion of at least 8 seconds between multi-joint targets unless the instructor approves another duration. Stop before executing a target if a limit check fails or the visualized swept region is unsafe.

For each configuration:

1. Reset or move smoothly to the target.
2. Hold until measured joints stop changing appreciably.
3. Save measured `q` in the required order.
4. Compute `T_world_tool_predicted` using your FK and fixed transforms.
5. Only then record `tool_position` and `tool_orientation`.
6. Save one row in the FK comparison table.

### Step 18 - Repeat one complete trial

Choose Configuration 3 or another instructor-approved pose.

1. Reset.
2. Execute and log the complete motion as `trial1.csv`.
3. Record final measured `q` and tool pose.
4. Reset without changing code, target, duration, or sample rate.
5. Execute again as `trial2.csv`.
6. Compare final joints and FK/tool-pose errors.

### Step 19 - Demonstrate point transformation at the tool

At one held-out configuration:

1. use your predicted `T_world_tool`;
2. predict the world position of `p_tool = [0.05, 0, 0]` m;
3. record `tool_test_point_position` only after the prediction; and
4. compute the Euclidean point error.

The final outcome is a UR5e whose tool pose is predicted across multiple configurations by your own FK implementation.

## Part 4 - Quantitative Analysis

For each held-out configuration, compute position error:

```text
e_p = p_predicted - p_measured
position_error = ||e_p||_2
```

Compute orientation error:

```text
R_error = R_predicted^T R_measured
orientation_error = acos(clamp((trace(R_error) - 1) / 2, -1, 1))
```

Report:

1. a six-row table separating the alignment configuration from five validation configurations;
2. predicted and measured tool position;
3. position-error norm in meters and millimeters;
4. orientation error in radians and degrees;
5. maximum, mean, and RMS position error over held-out configurations;
6. maximum and mean orientation error;
7. command-versus-measured joint error for the repeated motion;
8. final-state repeatability between `trial1` and `trial2`; and
9. tool-test-point error.

Create:

- a 3-D scatter plot of predicted versus measured tool positions;
- a per-configuration position/orientation error plot; and
- a commanded-versus-measured joint plot for the repeated motion.

Do not use Configuration 1 when claiming held-out FK accuracy. Explain systematic versus configuration-dependent residuals and connect them to rounded dimensions, `T_6_tool`, joint order, units, or transform order.

## Engineering Questions

1. Why must joint order and transform multiplication order both be explicit?
2. What does each row of the DH table represent geometrically?
3. Why must `T_6_tool` remain fixed across configurations?
4. Why is a measured joint vector preferable to the commanded target when validating FK?
5. What residual pattern suggests a wrong joint sign or offset?
6. What residual pattern suggests rounded link dimensions?
7. Why must an alignment configuration be excluded from held-out accuracy claims?
8. Why does translation affect a point but not a free direction?

## What to Submit

- completed transform and FK source files;
- completed `lab01_controller` and Webots reader/controller copies;
- completed `answers.md` and checkpoint table;
- DH convention, frame sketch, `T_world_0`, and `T_6_tool`;
- offline transformation/FK test output;
- six-configuration data table with alignment clearly marked;
- `trial1.csv` and `trial2.csv`;
- required joint, position, and orientation plots;
- FK error and repeatability metrics; and
- tool-test-point prediction, measurement, and interpretation.

Do not submit `lab01_work.wbt` unless requested. Do not submit installed software, downloaded assets, or caches.

## Troubleshooting

| Last passing stage | First failing stage | Likely problem |
|---|---|---|
| none | `void` world | missing assets, damaged world, or rendering |
| `void` | `diagnostic_minimal` | Python command or controller discovery |
| minimal | devices | wrong work world, assignment, or device names |
| devices | one joint | joint order, units, target, or timing |
| transform tests | FK structural test | DH transform implementation or multiplication |
| FK structure | alignment pose | base/tool frame convention or joint offset |
| alignment | held-out poses | DH values, joint order/sign, or per-pose refitting |
| motion | tool test point | rotation order or homogeneous-coordinate error |

Recovery:

1. Pause Webots and save needed code/logs.
2. Test transform and FK functions outside Webots.
3. Reopen `lab01_starter.wbt`, not **Open Recent**.
4. Use **File -> Save World As...** for a fresh work copy.
5. Repeat `void -> diagnostic_minimal -> diagnostic_devices -> one joint`.
6. Recheck one alignment configuration, then one held-out configuration.
7. Reintroduce only the last change.

For repeated crashes or safe mode, use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md).
