# Final Project — Integrated Robotic Manipulation

## Goal

Integrate multiple concepts from the semester into one reproducible robotic task.

At minimum, your system must use concepts from:

- coordinate frames / transformations;
- forward or inverse kinematics;
- trajectory generation or motion planning;
- feedback/state information;
- quantitative performance evaluation.

## Baseline simulation challenge

Using the UR5e in Gazebo:

1. begin from a documented home configuration;
2. move to a specified approach pose;
3. reach one or more target poses while respecting joint limits;
4. avoid at least one obstacle or forbidden region;
5. return to a safe final configuration;
6. log enough data to evaluate execution quantitatively.

A gripper/pick-and-place extension may be assigned depending on the available simulation model and semester schedule.

## Required evidence

- system architecture diagram;
- mathematical formulation;
- source code and launch instructions;
- at least one quantitative metric;
- successful demonstration;
- discussion of one failure mode and mitigation.

## Optional sim-to-real extension

Adapt selected algorithms to the course 3D-printed arm. Identify what transfers and what must change when geometry, joint limits, actuators, sensing, and control interfaces differ.
