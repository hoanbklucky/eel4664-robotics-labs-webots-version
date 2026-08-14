# Lab 5 - Dynamics, Control, and Parameter Identification

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

## Mission

Track the same trajectory under different payloads, tune the controller, and identify an unknown model parameter.

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

Complete Lab 4 and the [setup prerequisites](../setup/README.md). Bring a tested trajectory generator and logger. The instructor must approve the two payload/model conditions and any effort-control limits. Do not edit the installed Cyberbotics UR5e PROTO.

## Background

For a focused one-joint experiment,

```text
tau = I_eff qddot + b_eff qdot + g_eff(q)
tau_cmd = Kp (q_des - q) + Kd (qdot_des - qdot_est) + Ki integral(e)
```

This approximation supports a controlled comparison; it does not replace full manipulator dynamics. Numerical differentiation amplifies noise, filtering introduces delay, and parameter estimates are credible only when units, excitation, conditioning, and held-out validation are reported.

## Provided Files

- `worlds/lab05_starter.wbt` - clean, known-good starter; never overwrite it
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/simple_dynamics.py` - simplified torque-model starter
- `src/pd_control_sim.py` - independent NumPy plant/controller starter
- `src/estimate_velocity.py` - differentiation/filtering starter
- `src/least_squares_id.py` - parameter-identification starter
- `src/run_payload_experiment.py` - matched-trial mission scaffold
- `answers.md`

## Part 1 - Setup / Validation

1. **World:** open `worlds/lab05_starter.wbt` paused, verify it, and immediately use **File -> Save World As...** to create `worlds/lab05_work.wbt`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and verify the selected motor and sensor.
4. **One joint:** execute a conservative position command before any instructor-approved effort-mode extension.
5. **Full algorithm:** enable the feedback/payload experiment only after safety limits and stages 1-4 pass.

Complete the offline dynamics/controller sanity checks first. Reset to identical initial conditions for every matched trial.

## Part 2 - Core Implementation

1. Complete the simplified dynamics model and independent P/PD/PID simulation.
2. Implement raw finite differences and a stated causal filter for velocity.
3. Implement feedback, saturation, and anti-windup when integral action is used.
4. Complete a NumPy linear least-squares estimator; state the regressor and parameter units.
5. Complete `run_payload_experiment.py` so condition, gains, commands, measurements, and timestamps are logged deterministically.
6. Keep plant model, estimator, controller, identification, metrics, and Webots I/O separable and testable.

Do not use a simulator or identification API to compute the model/controller quantities students are required to implement.

## Part 3 - Robot Experiment

Track the identical assigned reference under:

- Condition A: the instructor-approved baseline; and
- Condition B: an instructor-provided payload/model change.

If a safe payload-changing world is unavailable, use the instructor-provided paired dataset for the identification portion while still completing the baseline Webots tracking run. Log `q_des`, measured `q`, error, raw/filtered velocity estimate, command/effort, gains, condition, and simulation time. Use at least three gain sets during tuning, then apply one justified final set to both matched conditions.

## Part 4 - Quantitative Analysis

1. Compare raw and filtered velocity against an analytic trajectory derivative or reserved simulator measurement.
2. For both conditions report rise time, percent overshoot, settling time, steady-state error, RMSE, maximum error, and control magnitude.
3. Fit one effective inertia, damping/friction, gravity, or payload-related parameter on a training trial.
4. Predict a held-out trial at a different speed or condition and report residual plots and validation error.
5. Discuss whether changes reflect physics, controller saturation, estimator delay, or model mismatch.

## Engineering Questions

1. Which model term dominates static holding, slow motion, and rapid acceleration?
2. How did filtering trade noise suppression against phase delay?
3. Which gain most affected rise time, overshoot, and steady-state error?
4. Why must initial state and reference be matched across payload conditions?
5. What residual pattern indicates missing model structure?
6. Does the identified parameter retain its physical meaning outside the fitted range?

## What to Submit

- completed dynamics, controller, estimator, identification, and experiment code;
- stated gains, limits, parameter units, and condition definitions;
- raw CSV logs for tuning and matched trials;
- velocity, tracking, transient, command, and residual plots;
- metric comparison table;
- training/validation identification results; and
- completed `answers.md`.

## Troubleshooting

If Webots repeatedly crashes, close it, use the [safe-mode recovery procedure](../docs/TROUBLESHOOTING_WEBOTS.md), and reopen the untouched starter with controller `void`. Revert a damaged starter with Git. If `diagnostic_minimal` fails, fix Python/controller configuration; if device listing fails, fix names; if only feedback motion fails, inspect sign, units, timestep, gains, and saturation. Return to conservative position mode and one joint before retrying the full experiment.
