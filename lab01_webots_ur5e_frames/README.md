# Lab 1 - Webots, UR5e, and Coordinate Frames

**Do not save over the original starter world after running the simulation. Immediately save a working copy; reset/revert before preserving world changes.**

## Learning objectives

By the end of this lab, you should be able to:

1. launch the course UR5e environment and run a Python controller;
2. distinguish a Webots world, robot model/PROTO, controller, joint motor, and sensor;
3. identify the six UR5e joints in the required order;
4. inspect base, joint, tool, and world coordinate frames;
5. command safe joint motion and read measured joint positions; and
6. transform a point or direction between two stated frames and validate it with simulator measurements.

## Prerequisites

Complete the [course setup guide](../setup/README.md) and pass `setup\verify_installation.ps1`. Review coordinate-frame notation, rotation matrices, and homogeneous coordinates.

Complete Cyberbotics [Tutorial 1](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots?version=R2025a) and the Python controller portion of [Tutorial 4](https://cyberbotics.com/doc/guide/tutorial-4-more-about-controllers?version=R2025a). These are orientation activities; the graded evidence comes from the UR5e experiments below.

Tutorials 2 and 3 are optional resources in the root [Optional Webots Basics](../README.md#optional-webots-basics) section.

## Background

A `.wbt` world instantiates robot and environment models. The UR5e PROTO defines its rigid-body/joint hierarchy and named devices. A Python controller reads sensors and sends motor commands once per `robot.step()`. The simulator advances physics; it does not replace your frame reasoning.

For a point `p_b` expressed in frame `{b}`,

```text
p_a = T_ab p_b
```

where `T_ab` is constructed by your code. A direction uses rotation only; translation must not affect a free vector. Supervisor measurements are validation data, not transformation solvers.

## Provided files

- `worlds/lab01_starter.wbt` - protected known-good R2025a world
- `controllers/diagnostic_minimal/` - no-device Python startup test
- `controllers/diagnostic_devices/` - read-only device inventory
- `controllers/eel4664_ur5e/` - shared UR5e device adapter and conservative motion example
- `src/inspect_joint_states.py` - joint-sensor logging starter
- `src/send_joint_goal.py` - smooth joint-command starter
- `src/transform_point.py` - point/direction transformation starter
- `src/query_transform.py` - Supervisor ground-truth adapter
- `answers.md` - response template

## Minimum Webots skills

Keep Webots-specific work concise:

1. Open `worlds/lab01_starter.wbt` paused.
2. Immediately use **File -> Save World As...** and create `worlds/lab01_work.wbt`.
3. Use the Scene Tree to select the UR5e, inspect its `controller` field, and locate joints/devices.
4. Assign a controller through the robot's `controller` field.
5. Inspect or add one simple object only if the experiment requires it.
6. Use **Reset** to restore simulation state and **Reload/Revert World** to discard unwanted world edits.

Do not perform unrelated Scene Tree customization.

## Required Webots workflow and recovery

Validate in order and stop at the first failure:

1. **World:** open `lab01_work.wbt` paused with controller `void`.
2. **Minimal controller:** assign `diagnostic_minimal`, Reset, and confirm its pass message.
3. **Devices:** assign `diagnostic_devices`, Reset, and save the inventory.
4. **One joint:** assign `eel4664_ur5e` or your lab controller and command one small conservative displacement while the other joints hold.
5. **Full algorithm:** run sensing, motion, and frame-validation code only after stages 1-4 pass.

If the work world fails, close Webots, recover from `lab01_starter.wbt`, and consult [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md). A `void` failure indicates a world/asset/rendering problem; a minimal-controller failure indicates Python/controller startup; a device failure indicates assignment or device naming.

## Step-by-step instructions

1. Run the setup verifier and record the passing summary.
2. Create `lab01_work.wbt` and complete the staged workflow.
3. Record `WorldInfo.basicTimeStep` and the six joint motor/sensor names in order:
   - `shoulder_pan_joint`
   - `shoulder_lift_joint`
   - `elbow_joint`
   - `wrist_1_joint`
   - `wrist_2_joint`
   - `wrist_3_joint`
4. Sketch the path from world to UR5e base, joints, and tool. Label every frame used.
5. Run the device adapter, read `q0`, and predict the effect of one joint command before executing it.
6. Execute a small motion, Reset, and repeat it to confirm reproducibility.
7. Complete the transformation and Supervisor validation tasks.

## Implementation tasks

1. Complete CSV logging in `src/inspect_joint_states.py` using `robot.getTime()`.
2. Complete the zero-endpoint-velocity interpolation in `src/send_joint_goal.py`.
3. Complete `transform_point` and `transform_direction` with NumPy.
4. Configure `src/query_transform.py` with instructor-provided DEF names. Read position/orientation only after computing your own prediction.
5. Keep frame math separate from Webots I/O and state the meaning of every transform subscript.

## Required experiments

### Experiment A - devices and one-joint motion

Record the initial and final six-joint vectors, command, duration, and maximum joint-position difference. Explain which physical link moved.

### Experiment B - repeatable multi-joint pose

Command a conservative six-joint goal twice from the same reset state. Plot commanded and measured positions versus simulation time and report maximum absolute joint error.

### Experiment C - frame validation

Transform an instructor-provided point from tool to world coordinates using your matrix. Compare with Supervisor ground truth and report Euclidean position error.

## Questions and reflection

1. What information belongs in the world, robot PROTO, controller, motor, and sensor?
2. Why must device names and joint order be explicit?
3. Why does translation affect a point but not a free vector?
4. What does Reset change, and what does Reload/Revert World change?
5. Which discrepancy in Experiment C is most likely caused by a frame-convention error?

## What to submit

Submit:

- completed source/controller code;
- `answers.md`;
- device and frame table;
- joint command/measurement CSV and plot;
- frame sketch and transform calculation;
- Experiment C error calculation; and
- the setup-verifier summary.

Do not submit `lab01_work.wbt` unless requested.

## Troubleshooting

Use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md). Retry the last known passing stage before changing code. If motion fails after device listing passes, check joint order, motor type, target units, limits, and sampling period.