# Lab 00: Set Up — Windows 11 + WSL2 + Ubuntu 24.04 + ROS 2 Jazzy + Gazebo + UR5e

Complete Lab 00 **before Lab 01**.

## 1. Install WSL2 and Ubuntu 24.04

From Windows PowerShell:

```powershell
wsl --install -d Ubuntu-24.04
```

After installation, launch Ubuntu and create your Linux username/password.

Verify inside Ubuntu:

```bash
cat /etc/os-release
```

You should see Ubuntu 24.04 / Noble.

> Do not install ROS inside the `docker-desktop` WSL distribution.

## 2. Install ROS 2 Jazzy

Follow the official ROS 2 Jazzy Ubuntu Deb installation instructions.

For this course, install the desktop package:

```bash
sudo apt update
sudo apt install ros-jazzy-desktop
```

Then:

```bash
source /opt/ros/jazzy/setup.bash
ros2 --help
```

Optional but recommended:

```bash
echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
```

## 3. Install common ROS development tools

```bash
sudo apt update
sudo apt install -y \
  python3-colcon-common-extensions \
  python3-rosdep \
  git \
  python3-numpy \
  ros-jazzy-ros2controlcli \
  ros-jazzy-ros2-controllers
```

Initialize rosdep if needed:

```bash
sudo rosdep init
rosdep update
```

If `rosdep init` reports that it is already initialized, continue.

## 4. Install Gazebo integration

```bash
sudo apt update
sudo apt install ros-jazzy-ros-gz
```

Test Gazebo:

```bash
gz sim shapes.sdf
```

Close Gazebo after confirming that the GUI opens.

## 5. Create the UR Gazebo workspace

The rest of the course assumes:

```text
~/workspaces/ur_gz
```

Create it:

```bash
mkdir -p ~/workspaces/ur_gz/src
cd ~/workspaces/ur_gz
```

Clone the official Universal Robots Gazebo simulation repository:

```bash
source /opt/ros/jazzy/setup.bash
cd ~/workspaces/ur_gz
git clone -b ros2 \
  https://github.com/UniversalRobots/Universal_Robots_ROS2_GZ_Simulation.git \
  src/ur_simulation_gz
```

Then resolve dependencies:

```bash
rosdep update
rosdep install --ignore-src --from-paths src -y
```

The upstream repository maintains ROS-distribution-specific dependency metadata (including Jazzy). If the course pins a later tested commit, use the commit listed by the instructor rather than updating arbitrarily during the semester.

Build:

```bash
colcon build --symlink-install
```

Source:

```bash
source ~/workspaces/ur_gz/install/setup.bash
```

Optional:

```bash
echo 'source ~/workspaces/ur_gz/install/setup.bash' >> ~/.bashrc
```

## 6. Verify the UR5e simulation

```bash
ros2 launch ur_simulation_gz ur_sim_control.launch.py ur_type:=ur5e
```

In a second terminal:

```bash
source /opt/ros/jazzy/setup.bash
source ~/workspaces/ur_gz/install/setup.bash
ros2 control list_controllers
```

Expected active controllers include:

```text
joint_state_broadcaster
joint_trajectory_controller
```

Check actions:

```bash
ros2 action list
```

You should find:

```text
/joint_trajectory_controller/follow_joint_trajectory
```

## 7. Move the UR5e once

With Gazebo still running:

```bash
ros2 action send_goal \
/joint_trajectory_controller/follow_joint_trajectory \
control_msgs/action/FollowJointTrajectory \
"{trajectory: {
  joint_names: [
    shoulder_pan_joint,
    shoulder_lift_joint,
    elbow_joint,
    wrist_1_joint,
    wrist_2_joint,
    wrist_3_joint
  ],
  points: [{
    positions: [0.0, -1.2, 1.2, -1.5, -1.57, 0.0],
    time_from_start: {sec: 5}
  }]
}}"
```

The robot should move over approximately five seconds.

## 8. Run the verification script

From this repository:

```bash
bash lab00_setup/verify_installation.sh
```

Fix all reported failures before Lab 01.
