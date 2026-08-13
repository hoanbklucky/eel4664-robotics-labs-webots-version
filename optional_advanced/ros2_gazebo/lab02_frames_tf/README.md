# Lab 02 — Coordinate Frames and TF2

## Learning objectives

- identify frames in the UR5e kinematic chain;
- distinguish a frame from a link;
- query transformations using TF2;
- transform a point between frames;
- interpret translation and quaternion orientation.


## Launch the simulator

Terminal 1:

```bash
source /opt/ros/jazzy/setup.bash
source ~/workspaces/ur_gz/install/setup.bash
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e
```

Leave this terminal running. Use a second terminal for commands and your code.


## Part 1 — Generate the TF tree

```bash
sudo apt install ros-jazzy-tf2-tools
ros2 run tf2_tools view_frames
```

Inspect `frames.pdf` and identify the chain from the robot base to the tool frame.

## Part 2 — Query a transform

```bash
ros2 run tf2_ros tf2_echo <base_frame> <tool_frame>
```

Use frame names from your generated tree.

## Part 3 — Python TF query

```bash
python3 lab02_frames_tf/src/query_transform.py --target base_link --source tool0
```

If your installed UR description uses different names, use those names instead.

## Part 4 — Transform a point manually

Choose:

```text
p_tool = [0.05, 0.00, 0.00, 1]^T
```

Use the measured transform to calculate the same point in the base frame.

## Part 5 — Verify numerically

Edit and run:

```bash
python3 lab02_frames_tf/src/transform_point.py
```

## Questions

1. What is the difference between a link and a coordinate frame?
2. Why use many frames rather than express everything in `world`?
3. What does the translation vector represent?
4. Why are quaternions common in ROS?
5. Which transforms change as the robot moves?
