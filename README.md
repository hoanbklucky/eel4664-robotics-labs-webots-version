# EEL 4664 - Kinematics and Control of Robotic Systems

## UR5e + Webots laboratory repository

Webots is the simulation and visualization layer. Python and NumPy are the primary implementation tools. Students implement the robotics mathematics explicitly; simulator measurements are used for visualization, experimentation, and validation.

Lecture, in-class work, and homework develop the analytical foundations. The six simulation labs emphasize:

- implementation and testing;
- visualizing frames and robot motion;
- collecting repeatable measurements;
- comparing predictions with simulated ground truth;
- quantifying error and controller performance; and
- integrating multiple robotics algorithms into one system.

ROS 2 and Gazebo remain optional advanced topics.

## Required semester environment

Complete [Lab 00 - Setup](lab00_setup/README.md) before Lab 1. The supported environment is:

- Windows 10 or Windows 11;
- stable **Webots R2025a**; nightly and development builds are unsupported;
- 64-bit CPython 3.11 or 3.12 installed from [python.org](https://www.python.org/downloads/windows/);
- Visual Studio Code;
- Git; and
- NumPy and Matplotlib.

Lab 00 covers software installation, Webots Python configuration, and required Webots Tutorials 1 and 4. UR5e-specific work begins in Lab 1.

## Lab 00 completion checklist

- [ ] Webots R2025a launches normally
- [ ] Python 3.11 or 3.12 is installed
- [ ] `python --version` works
- [ ] Webots **Python command** points to the full `python.exe` path
- [ ] Webots Tutorial 1 is complete
- [ ] The Python-controller portion of Webots Tutorial 4 is complete
- [ ] A Python controller runs without crashing
- [ ] NumPy imports successfully
- [ ] Git and VS Code are available


## Required lab roadmap

| Status | Lab | Topic | Robotic mission/outcome |
|---|---|---|---|
| Required | 00 | [Software Setup and Webots Basics](lab00_setup/README.md) | install the supported software and complete Webots Tutorials 1 and 4 |
| Required | 1 | [Webots, UR5e, and Coordinate Frames](lab01_webots_ur5e_frames/README.md) | bring the UR5e online, interpret its frames, and command verified motion |
| Required | 2 | [Forward and Inverse Kinematics](lab02_forward_inverse_kinematics/README.md) | reach a specified end-effector pose using student FK/IK |
| Required | 3 | [Jacobian, Differential Kinematics, and Singularities](lab03_jacobian_singularities/README.md) | command Cartesian motion and demonstrate degradation near singularity |
| Required | 4 | [Trajectory Generation and Tracking](lab04_trajectory_tracking/README.md) | execute and compare point-to-point and straight-line motion |
| Required | 5 | [Dynamics, Joint Control, and Parameter Identification](lab05_dynamics_control_identification/README.md) | track under changed payload/model conditions and identify a parameter |
| Required | 6 | [Integrated Manipulation / Final Project](lab06_integrated_manipulation/README.md) | complete a repeatable autonomous pick-and-place challenge |

The required sequence is Lab 00 followed by Labs 1 through 6. There are no separate required simulation labs for homogeneous transformations, singularities, dynamics, control, state estimation, parameter identification, or collision planning; those topics are integrated where simulation adds the most value.

## Optional Webots Basics

These simulator-enrichment tutorials are available but are **not prerequisites, graded activities, or required deliverables**:

| Status | Resource | Useful extra practice |
|---|---|---|
| Optional | [Tutorial 2 - Modification of the Environment](https://cyberbotics.com/doc/guide/tutorial-2-modification-of-the-environment?version=R2025a) | editing a world, using the Scene Tree, and adding or modifying objects and physical properties |
| Optional | [Tutorial 3 - Appearance](https://cyberbotics.com/doc/guide/tutorial-3-appearance?version=R2025a) | changing visual properties and inspecting rendering options |

Lab 1 directly teaches the small set of world-editing skills required by the course.

## Required safe workflow

Every required lab provides one tracked `*_starter.wbt` and the `diagnostic_minimal` and `diagnostic_devices` controllers.

1. Never overwrite the starter world.
2. Open the starter paused and immediately use **File -> Save World As...** to make `*_work.wbt`.
3. Validate incrementally: **world opens -> minimal controller -> devices found -> one joint moves -> full algorithm**.
4. Keep controllers and mathematical source under Git.
5. Reset before rerunning; reload/revert or restore from the starter after a bad world edit.
6. Use [Troubleshooting Webots](docs/TROUBLESHOOTING_WEBOTS.md), including `WEBOTS_SAFE_MODE` recovery, if Webots repeatedly crashes.

Avoid heavy Scene Tree modifications unless environment or collision modeling is part of the stated learning objective.

## Repository layout

```text
lab00_setup/                                required Lab 00 software setup and Webots basics
lab01_webots_ur5e_frames/                   required Lab 1
lab02_forward_inverse_kinematics/           required Lab 2
lab03_jacobian_singularities/               required Lab 3
lab04_trajectory_tracking/                  required Lab 4
lab05_dynamics_control_identification/      required Lab 5
lab06_integrated_manipulation/              required Lab 6 / final project
docs/                                       shared troubleshooting
webots/controllers/                         canonical shared controllers
optional_legacy/previous_lab_sequence/      archived material from the former sequence
optional_advanced/ros2_gazebo/              optional ROS 2/Gazebo track
```

## Start here

1. Complete [Lab 00 - Setup](lab00_setup/README.md), including Webots Tutorials 1 and 4.
2. Complete Labs 1-6 in order. Each lab reuses student code and evidence from earlier labs.

The official UR5e sample is prepared at the beginning of Lab 1, not during Lab 00.

## Rules for student implementations

- Keep mathematical functions separate from Webots I/O so they can be unit tested.
- Do not call Webots or third-party solvers to replace assigned FK, IK, Jacobian, trajectory, dynamics, control, estimation, identification, collision, or planning algorithms.
- Use simulator joint sensors and Supervisor ground truth only as measurements for validation.
- Use SI units and state every coordinate-frame convention and joint order.
- Use `robot.getTime()` for experiment timestamps.
- Reset to identical initial conditions before comparisons.
- Record commands, measurements, parameters, controller gains, and random seeds.

## Submission convention

Each lab README defines its required submission. In general, submit source code, `answers.md`, CSV/plot evidence, quantitative metrics, and enough run instructions to reproduce the result. Do not submit Webots installations, downloaded sample assets, caches, or `*_work.wbt` unless the instructor requests the working world.

## Optional and archived material

- [Optional advanced ROS 2/Gazebo material](optional_advanced/ros2_gazebo/README.md) preserves middleware, TF2, `ros2_control`, and MoveIt exercises.
- [Previous lab-sequence archive](optional_legacy/previous_lab_sequence/README.md) preserves superseded README/world/controller shells for instructor reference. It is not part of the required sequence.

## References

- [Correll manipulation Lab 0](https://introduction-to-autonomous-robots.github.io/lab-manipulation-introduction.html)
- [Webots R2025a User Guide](https://cyberbotics.com/doc/guide/index?version=R2025a)
- Cyberbotics Universal Robots sample and UR5e model
- *Introduction to Autonomous Robots*