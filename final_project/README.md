# Final Project ? Integrated Robotic Manipulation

## Goal

Integrate the semester's explicit algorithms into one reproducible Webots UR5e task.

At minimum use coordinate transformations, FK or IK, trajectory generation or collision-aware planning, feedback/state information, and quantitative evaluation.

## Baseline challenge

Using the supplied Webots project:

1. begin from a documented home configuration;
2. compute and reach a specified approach pose;
3. reach one or more targets while respecting joint limits;
4. avoid at least one obstacle or forbidden region;
5. return to a safe final configuration;
6. log enough data to evaluate execution quantitatively.

A gripper extension may be assigned. Simulator APIs may provide sensing and actuation, but must not replace submitted kinematics, planning, trajectory, control, estimation, or identification algorithms.

## Milestones

1. **Proposal:** task, frames, metric, risks.
2. **Model checkpoint:** validated geometry and reachable targets.
3. **Planning/control checkpoint:** collision-free offline tests.
4. **Integrated demonstration:** repeatable Webots execution and logs.
5. **Report:** prediction, evidence, discrepancy, failure, mitigation.

## Required evidence

Submit an architecture diagram, mathematical formulation, source and run instructions, at least two quantitative metrics, successful demonstration, and one failure analysis. Report seeds and initial conditions.

## Optional extensions

- add a Webots gripper or perception sensor;
- compare with the optional ROS 2/Gazebo track;
- transfer selected algorithms to the course arm and identify interface/model changes.
