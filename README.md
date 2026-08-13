# EEL 4664 - Kinematics and Control of Robotic Systems

## UR5e + Webots Laboratory Repository

This repository contains the hands-on laboratory sequence for **EEL 4664 - Kinematics and Control of Robotic Systems**. Webots is the primary simulator; Python and NumPy are the primary implementation tools. ROS 2 and Gazebo are optional advanced topics, not prerequisites.

The course uses one consistent stack:

- **Webots R2025a or a course-pinned later release**
- the built-in **Universal Robots UR5e** model
- **Python 3 + NumPy** for student algorithms
- Webots motors, position sensors, physics, and Supervisor measurements for experiments
- Matplotlib and CSV files for analysis and evidence

The sequence follows a Correll-style pattern: begin with an observable robotics problem, form a prediction, implement the mathematics, test it in simulation, quantify the discrepancy, and explain what the result means.

> **derive ? predict ? implement ? simulate ? measure ? explain**

Webots is an experimental apparatus, not a replacement for the mathematics. Students must implement FK, IK, Jacobians, singularity metrics, trajectories, dynamics, controllers, estimators, and identification methods explicitly.

## Lab sequence

| Lab | Topic | Main concepts |
|---|---|---|
| 00 | Set Up | Webots, Python, NumPy, UR5e project, first controller |
| 01 | Webots and the UR5e | worlds, controllers, devices, simulation loop |
| 02 | Coordinate Frames | frame trees, transformations, simulator measurements |
| 03 | Homogeneous Transformations | rotations, translations, transform composition |
| 04 | Forward Kinematics | DH-style chains, FK verification in Webots |
| 05 | Inverse Kinematics | analytical planar IK, numerical UR5e IK |
| 06 | Jacobian and Differential Kinematics | Jacobian, Cartesian velocity, pseudoinverse |
| 07 | Singularities and Manipulability | rank, singular values, condition number |
| 08 | Trajectory Generation | cubic/quintic trajectories, sampled motor commands |
| 09 | Manipulator Dynamics | inertia, gravity, payload effects |
| 10 | Joint-Space Control | P/PD/PID concepts, torque control, transient response |
| 11 | State Estimation and Parameter Identification | differentiation, filtering, least-squares fitting |
| 12 | Collision-Aware Planning | collision tests, waypoint planning, smoothing |
| Final | Integrated Manipulation Project | integration and optional sim-to-real transfer |

## Start here

1. Complete [Lab 00 ? Set Up](lab00_setup/README.md).
2. Open [`webots/worlds/eel4664_ur5e.wbt`](webots/worlds/eel4664_ur5e.wbt) and run the first-motion controller.
3. Complete labs in numerical order. Each lab reuses code that you wrote earlier.

## Shared Webots project

```text
webots/
??? controllers/eel4664_ur5e/
?   ??? eel4664_ur5e.py
?   ??? ur5e_devices.py
??? libraries/
??? worlds/eel4664_ur5e.wbt
```

Open the world from the Webots GUI or run:

```bash
webots webots/worlds/eel4664_ur5e.wbt
```

Use Reset before each measured trial. Use simulation time from `robot.getTime()` rather than wall-clock time.

## Rules for student code

- Use Python 3 and NumPy unless a lab states otherwise.
- Keep mathematical functions separate from Webots I/O so they can be unit tested.
- Do not use simulator or third-party functions to replace assigned robotics algorithms.
- Simulator joint sensors and ground-truth poses are measurements for verification only.
- Keep units in SI and state the coordinate-frame convention and joint order.
- Record commands, measurements, simulation timestamps, and experiment parameters.

## Submission convention

For each lab, submit modified starter code, plots or CSV evidence, and `answers.md`. Do not submit a Webots installation, caches, or unrelated assets.

## Troubleshooting

Before asking for help, record the Webots version, complete console error, pause state, world and controller names, Python version, NumPy version, and whether the unmodified world runs after Reset.

## Optional advanced ROS 2/Gazebo material

The previous ROS 2 Jazzy, Gazebo, TF2, `ros2_control`, and MoveIt exercises are preserved in [`optional_advanced/ros2_gazebo/`](optional_advanced/ros2_gazebo/README.md). They are not needed for the Webots sequence.

## References

- Webots User Guide and Reference Manual
- Webots Universal Robots UR5e model documentation
- NumPy documentation
- *Introduction to Autonomous Robots* and associated Correll robotics materials

Repository instructions take precedence because they define the tested course workflow.
