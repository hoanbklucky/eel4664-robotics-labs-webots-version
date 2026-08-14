# EEL 4664 — Kinematics and Control of Robotic Systems

## UR5e + Webots Laboratory Repository

Webots is the primary simulator; Python and NumPy are the primary implementation tools. ROS 2 and Gazebo are optional advanced topics.

The course uses:

- the stable Webots R2025a release (nightly and development builds are unsupported);
- Cyberbotics' official **Universal Robots** sample world and UR5e model;
- 64-bit CPython 3.11 or 3.12, NumPy, Matplotlib, and CSV experiment logs.

The sequence follows a Correll-style pattern:

> **observe → predict → modify → experiment → measure → explain**

Webots is an experimental apparatus, not a replacement for mathematics. Students explicitly implement FK, IK, Jacobians, singularity metrics, trajectories, dynamics, controllers, estimators, identification, collision checking, and planning.

## Required semester environment

Complete the [Lab 00 setup prerequisites](lab00_setup/README.md#1-required-student-environment) before beginning any Webots lab. The supported student environment is:

- Windows 10 or Windows 11;
- stable **Webots R2025a** (nightly and development builds are unsupported);
- **64-bit CPython 3.11 or 3.12 installed from [python.org](https://www.python.org/downloads/windows/)**;
- Visual Studio Code;
- Git; and
- NumPy, which is required by later labs.

During Python installation, select **Add python.exe to PATH**. Use a normal python.org CPython installation; do not rely on the Microsoft Store package or Windows App Execution Alias. Verify the installation in PowerShell:

```powershell
python --version
where.exe python
py -0p
python -m pip install --upgrade pip
python -m pip install numpy
python -c "import numpy as np; print(np.__version__)"
```

In Webots, open **Tools -> Preferences -> General**, set **Python command** to the full path of the installed `python.exe`, and restart Webots. For example:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python312\python.exe
```

Lab 00 contains the required minimal Python-controller test. Do not proceed to a full lab controller until that test runs without a crash.

## Setup verification checklist

- [ ] Webots launches normally
- [ ] Python is installed
- [ ] `python --version` works
- [ ] Webots **Python command** is configured
- [ ] The minimal Python controller runs
- [ ] NumPy imports successfully
- [ ] Git and VS Code are available

## Required lab sequence

| Status | Lab | Topic | Main concepts |
|---|---|---|---|
| Required | 00 | Webots Fundamentals and Set Up | Tutorials 1 and 4; Python/Webots setup; official UR sample |
| Required | 01 | Webots and the UR5e | worlds, controllers, devices, sensing and actuation |
| Required | 02 | Coordinate Frames | frame trees, transformations, Supervisor measurements (Tutorial 8) |
| Required | 03 | Homogeneous Transformations | rotations, translations, transform composition |
| Required | 04 | Forward Kinematics | robot/joint modeling (Tutorials 5–6), DH chains, FK verification |
| Required | 05 | Inverse Kinematics | analytical planar IK, numerical UR5e IK |
| Required | 06 | Jacobian and Differential Kinematics | Jacobian, Cartesian velocity, pseudoinverse |
| Required | 07 | Singularities and Manipulability | rank, singular values, condition number |
| Required | 08 | Trajectory Generation | cubic/quintic trajectories, sampled motor commands |
| Required | 09 | Manipulator Dynamics | parameterized PROTOs (Tutorial 7), inertia, gravity, payload effects |
| Required | 10 | Joint-Space Control | P/PD/PID concepts, torque control, transient response |
| Required | 11 | State Estimation and Parameter Identification | differentiation, filtering, least-squares fitting |
| Required | 12 | Collision-Aware Planning | collision tests, waypoint planning, smoothing |
| Required | Final | Integrated Manipulation Project | integration and optional sim-to-real transfer |

## Optional Webots Basics

These simulator-enrichment tutorials are available but are **not prerequisites, graded activities, or required deliverables**:

| Status | Resource | Useful extra practice |
|---|---|---|
| Optional | [Tutorial 2 - Modification of the Environment](https://cyberbotics.com/doc/guide/tutorial-2-modification-of-the-environment?version=R2025a) | editing a world, navigating the Scene Tree, and adding or modifying environment objects |
| Optional | [Tutorial 3 - Appearance](https://cyberbotics.com/doc/guide/tutorial-3-appearance?version=R2025a) | changing visual properties, inspecting rendering options, and distinguishing visual from physical properties |

Use these resources if you want more Webots practice. Required labs provide the small amount of direct world-editing instruction needed for the robotics activities.

## Simulator version and safe workflow

The course is pinned to the stable **Webots R2025a** release. Do not use nightly/development builds or upgrade during a graded lab. Every Lab 00–12 and the final project provides a protected `*_starter.wbt` and two non-motion diagnostics. Immediately save a separate `*_work.wbt`, keep controllers under Git, and validate **world → minimal controller → device access → one joint → full algorithm**. See [Troubleshooting Webots](docs/TROUBLESHOOTING_WEBOTS.md) before recovering a crashing project.

## Start here

1. Complete [Lab 00 — Webots Fundamentals and UR5e Orientation](lab00_setup/README.md), including required Cyberbotics Tutorials 1 and 4.
2. Open the official Universal Robots `ure.wbt` sample and map the controller/device concepts to the UR5e.
3. Complete the required labs in numerical order; each lab reuses earlier student code.

If the managed Windows installation cannot download sample assets, run:

```powershell
powershell -ExecutionPolicy Bypass -File .\lab00_setup\prepare_webots_sample.ps1
```

Then open:

```text
C:\webots-eel4664-sample\projects\robots\universal_robots\worlds\ure.wbt
```

The repository's `webots/controllers/` directory contains Python controller starters to copy into the official sample project when instructed. The sample world and robot assets remain Cyberbotics files rather than duplicated course models.

## Rules for student code

- Keep mathematical functions separate from Webots I/O so they can be unit tested.
- Do not use simulator or third-party functions to replace assigned algorithms.
- Simulator joint sensors and ground-truth poses are measurements for verification only.
- Use SI units and state every coordinate-frame convention and joint order.
- Use `robot.getTime()` and reset to the same initial state before comparisons.
- Record commands, measurements, simulation timestamps, parameters, and random seeds.

## Submission convention

Submit modified starter code, plots or CSV evidence, and `answers.md`. Do not submit a Webots installation, downloaded sample assets, caches, or unrelated files.

## Optional advanced ROS 2/Gazebo material

The previous ROS 2, Gazebo, TF2, `ros2_control`, and MoveIt exercises are preserved in [`optional_advanced/ros2_gazebo/`](optional_advanced/ros2_gazebo/README.md).

## References

- [Correll manipulation Lab 0](https://introduction-to-autonomous-robots.github.io/lab-manipulation-introduction.html)
- Webots User Guide and Reference Manual
- Cyberbotics Universal Robots sample and UR5e model
- *Introduction to Autonomous Robots*