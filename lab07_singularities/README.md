# Lab 07 ? Singularities and Manipulability

## Motivation

Some reachable poses are poor operating points: a modest Cartesian request can demand extreme joint motion.

## Learning objectives

Compute Jacobian rank, singular values, condition number, and manipulability; locate poor configurations; and connect numerical conditioning with observed UR5e motion.

## Investigation

1. Complete `src/singularity_scan.py` using your Lab 06 Jacobian.
2. Scan a documented joint-space slice and visualize the smallest singular value.
3. Select well- and poorly-conditioned configurations before running Webots.
4. Request the same small Cartesian velocity at both using your pseudoinverse.
5. Compare joint-speed norm, achieved tool velocity, and sensitivity to perturbation.

## Rule and submission

Webots demonstrates consequences; it does not compute the Jacobian or metric. Submit code, map/plot, two trials, interpretation, and `answers.md`.
