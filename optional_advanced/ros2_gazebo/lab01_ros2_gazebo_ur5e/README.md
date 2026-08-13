# Lab 01 — ROS 2, Gazebo, and the UR5e

## Learning objectives

After this lab you should be able to:

1. launch a UR5e simulation in Gazebo;
2. identify ROS 2 topics, nodes, actions, and controllers;
3. read the UR5e joint state;
4. send a six-joint trajectory goal;
5. explain the path from a ROS 2 action goal to motion in Gazebo.

## Prerequisite

Complete [Lab 00 - Set Up](../lab00_setup/README.md).


## Launch the simulator

Terminal 1:

```bash
source /opt/ros/jazzy/setup.bash
source ~/workspaces/ur_gz/install/setup.bash
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e
```

Leave this terminal running. Use a second terminal for commands and your code.


## Part 1 — Confirm active controllers

Terminal 2:

```bash
source /opt/ros/jazzy/setup.bash
source ~/workspaces/ur_gz/install/setup.bash
ros2 control list_controllers
```

Record the active controllers in `answers.md`.

## Part 2 — Inspect ROS interfaces

```bash
ros2 node list
ros2 topic list
ros2 action list
ros2 topic info /joint_states
ros2 topic echo /joint_states --once
```

Record the six UR5e joint names, one position vector, and the units.

## Part 3 — Use the inspection script

```bash
python3 lab01_ros2_gazebo_ur5e/src/inspect_joint_states.py
```

Read the source code and identify where the subscription is created.

## Part 4 — Move the UR5e

```bash
python3 lab01_ros2_gazebo_ur5e/src/send_joint_goal.py
```

Then try:

```bash
python3 lab01_ros2_gazebo_ur5e/src/send_joint_goal.py --duration 7   --positions 0.20 -1.00 1.10 -1.40 -1.40 0.20
```

## Part 5 — Architecture sketch

Create a diagram showing:

```text
Python action client
      ↓
FollowJointTrajectory action
      ↓
joint_trajectory_controller
      ↓
ros2_control
      ↓
Gazebo physics
      ↓
UR5e joint motion
      ↓
/joint_states
```

For each arrow, write one sentence explaining what information crosses the interface.

## Questions

1. Why is `/joint_states` a topic instead of an action?
2. Why is `FollowJointTrajectory` an action rather than a topic?
3. What is the difference between a joint state and a joint command?
4. Which component executes the trajectory in this simulation?
5. If the action name exists but its controller is inactive, what do you expect?

## Submission

Submit your source files, architecture figure, and `answers.md`.

## Troubleshooting

If `ros2 control` is unavailable:

```bash
sudo apt install ros-jazzy-ros2controlcli ros-jazzy-ros2-controllers
```

If a client waits forever:

```bash
ros2 control list_controllers
ros2 action list
ros2 action info /joint_trajectory_controller/follow_joint_trajectory
```
