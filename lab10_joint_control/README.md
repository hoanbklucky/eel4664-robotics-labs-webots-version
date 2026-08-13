# Lab 10 ? Joint-Space Control

## Motivation

Feedback converts model mismatch and disturbances into measurable corrections, but gains trade speed against overshoot and effort.

## Learning objectives

Implement P and PD control; quantify rise time, overshoot, settling time, steady-state error, and effort; and transfer the same law from a NumPy plant to one Webots UR5e joint.

## Investigation

1. Complete `src/pd_control_sim.py` using your own numerical integration.
2. Predict responses for low, moderate, and excessive gains.
3. In a copied Webots world, isolate a safe joint trial and switch its motor to torque mode with `setPosition(float('inf'))` and `setTorque(tau)`.
4. Estimate velocity from position samples; apply your explicit `tau = Kp e - Kd qdot` law with saturation.
5. Compare Python-plant and Webots metrics; explain differences.

## Safety and submission

Use conservative torque limits, one joint first, and Reset between trials. Submit controller code, gains, plots/metrics, comparison, and `answers.md`.
