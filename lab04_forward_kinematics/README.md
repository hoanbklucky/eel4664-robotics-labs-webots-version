# Lab 04 ? Forward Kinematics of the UR5e

## Motivation

Given six encoder readings, predict where the tool is before asking the simulator where it appears.

## Learning objectives

Derive a planar warm-up, implement a DH-style transform, construct a six-link UR5e chain, read Webots joint sensors, and quantify FK position/orientation error.

## Important rule

Do not call a simulator or library FK solver. Webots GPS/InertialUnit data is a reference only after your FK is computed. State any fixed base/tool-frame offset explicitly.

## Investigation

1. Complete `src/planar_fk.py` and validate hand-selected cases.
2. Complete `dh_transform` and the chain in `src/ur5e_fk_starter.py` using instructor-approved parameters.
3. Copy `src/read_configuration.py` into a Webots controller and record ordered joint positions.
4. Evaluate at least five configurations, including home and a nonsymmetric pose.
5. Compare predicted tool position and orientation with shared-world sensors.
6. Plot error and diagnose convention, parameter, discretization, or model-frame causes.

## Submission

Submit derivation, code, parameter table with source, configuration data, error table/plot, and `answers.md`.
