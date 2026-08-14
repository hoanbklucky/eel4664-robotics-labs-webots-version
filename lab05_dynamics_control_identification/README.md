# Lab 5 - Dynamics, Joint Control, and Parameter Identification

**Do not save over the original starter world after running the simulation. Immediately save a working copy; reset/revert before preserving world changes.**

## Learning objectives

By the end of this lab, you should be able to:

1. connect inertia, gravity, damping/friction, and payload/model changes to measured motion;
2. implement and tune a P/PD/PID-type joint controller;
3. estimate joint velocity from sampled/noisy position and filter the estimate;
4. quantify rise time, overshoot, settling time, steady-state error, and trajectory RMSE;
5. identify at least one simple dynamic parameter by least squares; and
6. validate the identified parameter on data not used for fitting.

## Prerequisites

Complete Lab 4 and bring a tested joint trajectory generator and logger. Review manipulator dynamics, feedback control, sampled differentiation/filtering, and least-squares identification from lecture/homework.

The instructor will designate a safe matched pair of experimental conditions, such as baseline versus a course-provided payload/model, or two approved configurations with different gravity/dynamic demand. Do not edit the installed Cyberbotics UR5e PROTO.

## Background

A focused one-joint approximation is:

```text
tau = I_eff qddot + b_eff qdot + g_eff(q)
tau_cmd = Kp (q_des - q) + Kd (qdot_des - qdot_est) + Ki integral(e)
```

The simplified model does not replace full manipulator dynamics; it creates a testable relationship for interpreting controlled Webots data. Finite differences amplify measurement noise, so velocity estimation and filtering are part of the experiment.

Fit a stated linear-in-parameters model with your own NumPy least-squares implementation. Separate training and validation trials.

## Provided files

- `worlds/lab05_starter.wbt`
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/simple_dynamics.py` - simplified torque-model starter
- `src/pd_control_sim.py` - independent NumPy plant/controller starter
- `src/estimate_velocity.py` - differentiation/filtering starter
- `src/least_squares_id.py` - linear parameter-identification starter
- `answers.md`

These starters were merged from the former dynamics, control, and state-estimation/identification labs.

## Required Webots workflow and recovery

1. **World:** open `worlds/lab05_starter.wbt` paused and use **File -> Save World As...** to create `worlds/lab05_work.wbt`; verify `void`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and verify the selected joint sensor/motor.
4. **One joint:** run a conservative position-controlled motion before enabling any assigned torque-control extension.
5. **Full algorithm:** run feedback/payload/model experiments only after stages 1-4 pass and instructor safety limits are applied.

Recover from `lab05_starter.wbt` and use [Troubleshooting Webots](../docs/TROUBLESHOOTING_WEBOTS.md) after any failed stage. Reset between matched trials.

## Step-by-step instructions

1. Complete the simplified dynamics and offline PD simulation.
2. Predict responses for low, moderate, and excessive gains.
3. Create `lab05_work.wbt` and validate one-joint sensing/motion.
4. Implement velocity estimation from measured position and compare raw versus filtered estimates.
5. Implement the assigned P/PD/PID controller with saturation, anti-windup when applicable, and safe joint/rate limits.
6. Track the same reference under two approved dynamic conditions.
7. Repeat trials from identical reset states and save raw data.
8. Compute transient and trajectory metrics.
9. Define a linear regressor for one unknown parameter, fit it on one trial, and validate it on another.

## Implementation tasks

1. Complete `one_joint_torque` in `simple_dynamics.py` and test units/limiting cases.
2. Complete `simulate_pd` using your own numerical integration.
3. Complete backward/centered finite differences and filtering in `estimate_velocity.py`.
4. Implement `fit_linear_parameter` in `least_squares_id.py` without an identification library.
5. Create a Webots experiment controller under `controllers/` that logs:
   - simulation time;
   - desired/measured joint position;
   - raw/filtered velocity estimate;
   - error and integral error;
   - commanded effort or motor command;
   - experimental condition; and
   - controller gains.
6. Keep controller, estimator, metric, and identification functions testable outside Webots.

## Required experiments

### Experiment A - controller and estimator sanity check

Compare offline plant responses for at least three gain sets. On representative sampled data, compare raw finite-difference and filtered velocity against a known trajectory derivative or reserved simulator reference.

### Experiment B - matched Webots tracking

Track the same joint trajectory under two instructor-approved payload/model/gravity conditions. Report rise time, overshoot, settling time, steady-state error, RMSE, and maximum error. Explain which dynamic effects changed.

### Experiment C - parameter identification

Estimate one effective payload, friction, damping, gravity, or inertia-related parameter. Fit on one trial and validate on a different speed or condition. Report parameter units, residuals, and validation error.

## Questions and reflection

1. Which model term dominates static holding, slow motion, and rapid acceleration?
2. How did filtering trade noise reduction against delay?
3. Which gain change most affected rise time, overshoot, and steady-state error?
4. Why must the same reference and initial state be used across conditions?
5. Does the identified parameter retain the same meaning outside the fitted operating range?
6. Which residual pattern indicates missing model structure?

## What to submit

Submit:

- completed dynamics, control, estimator, and identification source;
- Webots experiment controller;
- controller gains and safety limits;
- raw and filtered logs;
- transient/tracking metric table and plots;
- regressor derivation and parameter units;
- held-out validation results;
- model-limit discussion; and
- `answers.md`.

## Troubleshooting

Begin with position mode and one joint. Use conservative effort limits for any instructor-approved torque-mode extension. If differentiation is noisy, verify timestamps before tuning the filter. If identification is unstable, inspect units, excitation, regressor conditioning, and train/validation separation.
