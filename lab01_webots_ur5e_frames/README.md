# Lab 1 - Webots, UR5e, and Coordinate Frames

## Mission

**Bring the UR5e online, understand its coordinate structure, and command a simple verified motion.**

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

Open `worlds/lab01_starter.wbt` paused and immediately use **File -> Save World As...** to create `worlds/lab01_work.wbt`.

## Success Criteria

You have completed the mission when:

- the Lab 00 checklist and minimal Python controller pass;
- you can identify the six UR5e joints, motors, sensors, and key frames;
- your controller reads a complete ordered joint vector;
- the robot executes a repeatable, conservative joint motion; and
- your predicted frame transformation agrees with Webots ground truth within an explained error.

## Learning Objectives

- Distinguish a Webots world, robot model/PROTO, controller, joint motor, and sensor.
- Identify the UR5e joint order and relevant coordinate frames.
- Implement the sense-compute-act loop in Python.
- Read measured joint positions and command safe joint motion.
- Transform a point or direction between stated frames.
- Use simulator measurements for validation rather than as the mathematical solution.

## Prerequisites

Complete [Lab 00 - Software Setup and Webots Basics](../lab00_setup/README.md), including Webots Tutorials 1 and 4. Review coordinate-frame notation, rotation matrices, and homogeneous coordinates.

Tutorials 2 and 3 remain optional in [Optional Webots Basics](../README.md#optional-webots-basics).

## Background

A `.wbt` world instantiates robot and environment models. The UR5e PROTO defines the rigid-body/joint hierarchy and named devices. A Python controller reads sensors and sends motor commands once per `robot.step()`. Webots advances the simulation but does not replace frame reasoning.

For a point `p_b` expressed in frame `{b}`:

```text
p_a = T_ab p_b
```

A free direction uses rotation only. Supervisor pose measurements are reserved for checking a transform constructed by your NumPy code.

## Provided Files

- `worlds/lab01_starter.wbt` - protected R2025a world
- `controllers/diagnostic_minimal/` - Python startup test
- `controllers/diagnostic_devices/` - read-only device inventory
- `controllers/eel4664_ur5e/` - shared UR5e adapter and safe motion example
- `src/inspect_joint_states.py` - joint-state logging starter
- `src/send_joint_goal.py` - smooth joint-command starter
- `src/transform_point.py` - point/direction transform starter
- `src/query_transform.py` - Supervisor validation adapter
- `answers.md` - engineering response template

## Part 1 - Setup / Validation

Prepare the local official UR5e sample once from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\lab00_setup\prepare_webots_sample.ps1
```

This UR5e-specific step belongs to Lab 1. Then validate in this order and stop at the first failure:

1. **World:** create `lab01_work.wbt` and open it paused with controller `void`.
2. **Minimal controller:** assign `diagnostic_minimal`, Reset, and confirm its pass message.
3. **Devices:** assign `diagnostic_devices`, Reset, and save the device list.
4. **One joint:** assign `eel4664_ur5e` or your controller and command one small joint displacement while the other joints hold.
5. **Full algorithm:** proceed only after the first four stages pass.

In the Scene Tree, select the UR5e and inspect only its `controller` field, joint/device hierarchy, and relevant frames. Avoid unrelated environment customization. Record `WorldInfo.basicTimeStep` and the six joints in this order:

1. `shoulder_pan_joint`
2. `shoulder_lift_joint`
3. `elbow_joint`
4. `wrist_1_joint`
5. `wrist_2_joint`
6. `wrist_3_joint`

## Part 2 - Core Implementation

1. Complete CSV logging in `inspect_joint_states.py` using `robot.getTime()`.
2. Complete the zero-endpoint-velocity interpolation in `send_joint_goal.py`.
3. Complete `transform_point` and `transform_direction` with NumPy.
4. Configure `query_transform.py` with instructor-provided DEF names.
5. Keep frame mathematics separate from Webots I/O and state the meaning of every transform subscript.

## Part 3 - Robot Experiment

1. Sketch world, base, joint, and tool frames.
2. Predict which link moves for an assigned one-joint command.
3. Execute the command, Reset, and repeat it.
4. Command one conservative multi-joint pose twice from the same reset state.
5. Transform an assigned tool-frame point into world coordinates.
6. Read Supervisor ground truth only after computing the prediction.

The final robotic outcome is a UR5e that starts reliably, reports its state, and reaches a simple commanded pose with a verified frame calculation.

## Part 4 - Quantitative Analysis

- Plot commanded and measured joint positions versus simulation time.
- Report maximum absolute joint error for both repeated trials.
- Report repeatability error between trials.
- Compute Euclidean error between the predicted and measured transformed point.
- Attribute discrepancies to sampling, controller tracking, or frame conventions.

## Engineering Questions

1. How does a Python joint command propagate through controller, motor, physics, and sensor?
2. Why must device names and joint order be explicit?
3. Why does translation affect a point but not a free vector?
4. What is the difference between Reset and Reload/Revert World?
5. Which evidence shows the motion is reproducible rather than a one-time animation?

## What to Submit

- completed source/controller code and `answers.md`;
- setup-verifier summary and device/frame table;
- labeled UR5e frame sketch;
- joint command/measurement CSV and plot;
- repeatability and maximum-error calculations; and
- transformation prediction, Webots reference, and error interpretation.

Do not submit `lab01_work.wbt` unless requested.

## Troubleshooting

Use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md). A `void` failure indicates world/assets/rendering; a minimal-controller failure indicates Python startup; a device failure indicates controller assignment or naming. After device validation, check joint order, units, limits, and sampling period before changing the world.