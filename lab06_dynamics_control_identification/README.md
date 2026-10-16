# Lab 6 - Dynamics, Control, and Parameter Identification

## Get the Latest Course Files

Before starting, save your work and close Webots. Follow [Updating the Course Repository](../docs/UPDATE_REPOSITORY.md). Do not force an update or discard local work when Git reports a conflict.

## Mission

Track the same trajectory under different payloads, tune the controller, and identify an unknown model parameter.

### Why simulate dynamics and control?

Controller tuning and parameter-identification experiments require repeated motion under changed gains, payloads, and disturbances. On hardware, poor gains or an inaccurate model can cause unsafe motion. Webots provides a repeatable experimental system in which you can measure transient and tracking behavior before considering real-robot deployment.

Simulation does not reproduce every hardware effect, so successful Webots results are evidence that the method works under the modeled conditions—not a guarantee of identical physical performance. Your measurements and held-out validation must support the conclusion.

## Success Criteria

You succeed when the same reference is executed under two approved dynamic conditions, your tuned controller meets stated tracking/transient targets, raw and filtered velocity estimates are compared, and a parameter fitted on one dataset predicts a held-out dataset with reported error.

## Learning Objectives

By the end of this lab, you should be able to:

1. relate inertia, gravity, damping/friction, and payload to measured motion;
2. implement and tune a P, PD, or PID joint controller;
3. estimate velocity from sampled position and quantify filtering tradeoffs;
4. measure rise time, overshoot, settling time, steady-state error, and RMSE; and
5. identify and validate a simple dynamic parameter with NumPy least squares.

## Prerequisites

Complete Lab 5 and the [setup prerequisites](../lab00_setup/README.md). Bring a tested trajectory generator and logger. The instructor must approve the two payload/model conditions and any effort-control limits. Do not edit the installed Cyberbotics UR5e PROTO.

The standalone [Manipulator Dynamics: A Simple 1R Arm](../activities/manipulator-dynamics/README.md) activity is recommended preparation. It introduces the inertia, friction, gravity, payload, and torque-limit ideas used in this lab without requiring Webots.

**Platform note:** The required workflow supports Windows, macOS, and Ubuntu when configured through Lab 00. Terminal examples use `python`; on macOS or Ubuntu, use `python3` instead if `python` is not recognized.

## Background

Trajectory generation specifies the desired motion; feedback control determines how the robot responds when measured motion differs from that reference. In this lab, a focused one-joint model separates inertia, friction, gravity, feedback, and disturbances so their effects can be measured clearly.

For a concepts-first explanation of the feedback loop, the one-joint plant, P and PD control, gravity compensation, feedforward tracking, PID, windup, second-order behavior, and parameter identification, read [Lab 6 Optional Background](OPTIONAL_BACKGROUND.md). The required implementation begins below.

The starter keeps the visual stylus and `p_tool = [0, 0.13, 0]` m used in earlier labs. The stylus has no `Physics` or `boundingObject` node, so it adds no payload, inertia, or contact force. The green `BASELINE_CONDITION_PAD` and orange `PAYLOAD_CONDITION_PAD` are visual labels only. The actual Condition B model change must remain instructor-approved and explicitly logged.

## Provided Files

- `worlds/lab06_starter.wbt` - clean starter with stylus, grid, and two condition pads; never overwrite it
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/simple_dynamics.py` - simplified torque-model starter
- `src/pd_control_sim.py` - independent NumPy plant/controller starter
- `src/estimate_velocity.py` - differentiation/filtering starter
- `src/least_squares_id.py` - parameter-identification starter
- `src/run_payload_experiment.py` - matched-trial mission scaffold
- `Lab06_Report_Template.docx`



## Open the Word report template

Follow [Opening a Word Report Template](../docs/OPEN_WORD_REPORT.md) and create a personal copy of `Lab06_Report_Template.docx` before entering results.

## Part 1 - Setup / Validation

> **Why this part matters:** Conservative staged checks and identical reset conditions are essential because dynamics and controller comparisons are meaningful only when the experiment is safe and repeatable.

1. **World:** open `worlds/lab06_starter.wbt` paused; verify the stylus, grid, `BASELINE_CONDITION_PAD`, and `PAYLOAD_CONDITION_PAD`; then immediately use **File -> Save World As...** to create `worlds/lab06_work.wbt`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and verify the selected motor and sensor.
4. **One joint:** execute a conservative position command before any instructor-approved effort-mode extension.
5. **Full algorithm:** enable the feedback/payload experiment only after safety limits and stages 1-4 pass.

Complete the offline dynamics/controller sanity checks first. Reset to identical initial conditions for every matched trial.

## Part 2 - Core Implementation

> **Why this part matters:** Three equations connect the physical model, feedback correction, and parameter estimation. Simulation, velocity estimation, filtering, experiment logging, matched-trial checks, saturation, and safe hold are supplied.

Complete only these marked lines:

1. `TODO 1` in `simple_dynamics.py`: the one-joint inertia, damping, and gravity torque equation.
2. `TODO 2` in `pd_control_sim.py`: the PD feedback torque equation.
3. `TODO 3` in `least_squares_id.py`: the NumPy least-squares solve.

Then run the supplied offline checks, compare raw and filtered velocity, and read `run_payload_experiment.py` to trace how the identical reference and gains are enforced across conditions. Do not rewrite the supplied loop, estimator, filtering, saturation, logging, or matched-trial validation.

## Part 3 - Robot Experiment

> **Why this part matters:** Matched baseline and changed-payload trials reveal how dynamics, gain selection, saturation, and estimation affect actual closed-loop tracking.

Track the identical assigned reference under:

- Condition A: the instructor-approved baseline; and
- Condition B: an instructor-provided payload/model change.

If a safe payload-changing world is unavailable, use the instructor-provided paired dataset for the identification portion while still completing the baseline Webots tracking run. Log `q_des`, measured `q`, error, raw/filtered velocity estimate, command/effort, gains, condition, and simulation time. Use at least three gain sets during tuning, then apply one justified final set to both matched conditions.

## Part 4 - Quantitative Analysis

> **Why this part matters:** Time-domain metrics and held-out parameter validation determine whether the controller and identified model generalize beyond one visually successful run.

1. Compare raw and filtered velocity against an analytic trajectory derivative or reserved simulator measurement.
2. For both conditions report rise time, percent overshoot, settling time, steady-state error, RMSE, maximum error, and control magnitude.
3. Fit one effective inertia, damping/friction, gravity, or payload-related parameter on a training trial.
4. Predict a held-out trial at a different speed or condition and report residual plots and validation error.
5. Discuss whether changes reflect physics, controller saturation, estimator delay, or model mismatch.

## Engineering Question

Answer in 2-3 sentences.

When tracking a changing trajectory, what different jobs are performed by model-based feedforward torque and error-based feedback torque? Refer to one result from your experiment.

## What to Submit

1. The three completed equation lines in `simple_dynamics.py`, `pd_control_sim.py`, and `least_squares_id.py`.
2. Completed `Lab06_Report_Template.docx` containing the offline checks, matched-condition logs and plots, metric table, training and held-out validation, and the Engineering Question response.

Do not submit supplied helper code, `lab06_work.wbt`, vendor assets, or caches unless requested.

## Troubleshooting

If Webots repeatedly crashes, close it, use the [safe-mode recovery procedure](../docs/TROUBLESHOOTING_WEBOTS.md), and reopen the untouched starter with controller `void`. Revert a damaged starter with Git. If `diagnostic_minimal` fails, fix Python/controller configuration; if device listing fails, fix names; if only feedback motion fails, inspect sign, units, timestep, gains, and saturation. Return to conservative position mode and one joint before retrying the full experiment.
