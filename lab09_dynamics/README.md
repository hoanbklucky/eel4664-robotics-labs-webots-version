# Lab 09 ? Manipulator Dynamics

## Motivation

Kinematics predicts motion; dynamics explains the effort required and why payload and acceleration matter.

## Learning objectives

Interpret `M(q)qdd + C(q,qd)qd + g(q) = tau`; implement a simplified model; separate gravity, inertia, and velocity effects; and compare predictions with Webots physics trials.

## Investigation

1. Complete `src/simple_dynamics.py` and validate units/limiting cases.
2. Predict which term dominates static holding, slow motion, and rapid acceleration.
3. In a copied world/controller, use motor torque feedback when available or prescribed experiment data.
4. Repeat matched trajectories at two durations and two payload conditions.
5. Compare predicted trends and measured torque; explain unmodeled friction and multi-link coupling.

## Rule and submission

Do not use a simulator inverse-dynamics function. Submit equations, source, trial table/plots, residual analysis, and `answers.md`.
