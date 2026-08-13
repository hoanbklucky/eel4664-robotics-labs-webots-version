# EEL 4664 — Kinematics and Control of Robotic Systems

## UR5e + ROS 2 Jazzy + Gazebo Laboratory Repository

This repository contains the hands-on laboratory sequence for **EEL 4664 — Kinematics and Control of Robotic Systems**.

The labs use one consistent robotics stack:

- **Windows 11 + WSL2**
- **Ubuntu 24.04 LTS**
- **ROS 2 Jazzy**
- **Gazebo Harmonic / Gazebo Sim**
- **Universal Robots UR5e**
- **Python + NumPy** for student implementations
- **TF2 / RViz** for verification and visualization
- **ros2_control** for trajectory and joint-control exercises
- **MoveIt 2** only in the later motion-planning lab

The philosophy of the lab sequence is:

> **derive → implement → simulate → measure → explain**

Students should not use MoveIt or another library to replace the mathematics in the kinematics labs. The simulator is primarily a way to verify the algorithms that you implement.

## Lab sequence

| Lab | Topic | Main concepts |
|---|---|---|
| 00 | Set Up | WSL2, Ubuntu, ROS 2 Jazzy, Gazebo, UR5e simulation |
| 01 | ROS 2, Gazebo, and UR5e | nodes, topics, actions, controllers, joint states |
| 02 | Coordinate Frames and TF2 | frames, TF tree, frame transformations |
| 03 | Homogeneous Transformations | rotations, translations, transform composition |
| 04 | Forward Kinematics | DH-style transform chains, FK verification with TF |
| 05 | Inverse Kinematics | analytical planar IK, numerical UR5e IK |
| 06 | Jacobian and Differential Kinematics | Jacobian, Cartesian velocity, pseudoinverse |
| 07 | Singularities and Manipulability | rank, singular values, condition number |
| 08 | Trajectory Generation | cubic/quintic trajectories, FollowJointTrajectory |
| 09 | Manipulator Dynamics | inertia, gravity, payload effects |
| 10 | Joint-Space Control | P/PD/PID concepts, transient response |
| 11 | State Estimation and Parameter Identification | numerical differentiation, filtering, parameter fitting |
| 12 | MoveIt 2 and Collision-Aware Planning | planning scene, obstacles, motion planning |
| Final | Integrated Manipulation Project | integration and optional sim-to-real transfer |

## Start here

1. Complete [Lab 00 - Set Up](lab00_setup/README.md).
2. Confirm that you can launch the UR5e in Gazebo and move it using the standard joint trajectory controller.
3. Complete labs in numerical order.

The expected workspace used in these instructions is:

```text
~/workspaces/ur_gz
```

If your workspace is somewhere else, replace that path in the commands.

## Common terminal setup

Open a new Ubuntu/WSL terminal and run:

```bash
source /opt/ros/jazzy/setup.bash
source ~/workspaces/ur_gz/install/setup.bash
```

If you have added both commands to `~/.bashrc`, you do not need to type them every time.

## Launch the UR5e simulation

Unless a lab says otherwise, use:

```bash
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e
```

Keep that terminal running.

In a second terminal, source ROS and the workspace again before running lab commands.

## Rules for student code

- Use **Python 3** and **NumPy** unless the lab explicitly asks for something else.
- Do not call MoveIt IK or trajectory planning functions in Labs 03–08 unless explicitly instructed.
- Clearly mark all code you add to starter files.
- Keep units in **SI units**: radians, meters, seconds, Newtons, and Newton-meters.
- Your code should run from the command line using the commands in the lab README.
- Do not change the UR5e model files supplied by Universal Robots unless a lab explicitly asks you to do so.

## Submission convention

For each lab, submit a ZIP or Git repository snapshot containing:

```text
labXX_.../
├── README.md
├── src/
├── results/
└── answers.md
```

Do **not** submit your entire ROS installation, `build/`, `install/`, or `log/` directories.

## Troubleshooting

Before asking for help, record the output of:

```bash
ros2 pkg list | grep ur_
ros2 control list_controllers
ros2 topic list
ros2 action list
```

Also include the exact command that failed and the full error message.

## External documentation

These labs are designed around the official Universal Robots ROS 2 and Gazebo documentation. Useful references include:

- Universal Robots ROS 2 documentation
- `ur_simulation_gz`
- Universal Robots custom workcell tutorial
- ROS 2 Jazzy documentation
- Gazebo Harmonic documentation
- MoveIt 2 documentation

The repository instructions take precedence for course assignments because they pin the workflow used in EEL 4664.
