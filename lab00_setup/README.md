# Lab 00 ? Set Up Webots, Python, and the UR5e

Complete Lab 00 before Lab 01.

## Motivation

A trustworthy experiment begins with a known apparatus. Install Webots, verify Python/NumPy, inspect the UR5e world, and make one repeatable joint-space motion.

## Learning objectives

After this lab you should be able to:

1. open and reset a Webots world;
2. distinguish a world, robot model, controller, motor, and sensor;
3. run a Python controller at the simulator basic time step;
4. command and measure all six UR5e joints.

## 1. Install Webots

Install the course-pinned Webots release from Cyberbotics. Webots R2025a or later is recommended. Native Windows, Linux, and macOS installations are supported; native Windows is usually simplest when the repository is stored on Windows.

On Ubuntu with the Cyberbotics APT repository configured:

```bash
sudo apt update
sudo apt install webots
webots --version
```

Otherwise launch Webots from the desktop application menu.

## 2. Install Python dependencies

Use a Python interpreter visible to Webots:

```bash
python3 -m pip install --user numpy matplotlib
python3 -c "import numpy, matplotlib; print(numpy.__version__)"
```

On Windows, use `py -m pip ...` if needed. In Webots, set **Tools ? Preferences ? Python command** to that interpreter.

## 3. Open the course world

Choose **File ? Open World** and select `webots/worlds/eel4664_ur5e.wbt`. The Scene Tree should contain `UR5e`; its controller should be `eel4664_ur5e`.

## 4. Observe and predict

Press Play. Record the six motor names, initial joint vector, basic time step, and target vector printed in the console. Predict which links will move and whether the tool will rise or fall.

## 5. Run the first-motion experiment

The controller reads each `PositionSensor`, generates a smooth cubic blend, and sends positions to the six `RotationalMotor` devices. It does not use ROS or a trajectory-planning API.

Press **Simulation ? Reset**, then Play. The robot should move once and hold. Compare observation with your prediction.

## 6. Inspect the controller

Read `webots/controllers/eel4664_ur5e/eel4664_ur5e.py` and `ur5e_devices.py`. Identify the sense?compute?act sequence and the single `robot.step(...)` call.

## 7. Verify installation

From the repository root:

```bash
python3 lab00_setup/verify_installation.py
```

The script checks assets and dependencies. The final motion check is visual because Webots owns the controller process.

## Reflection

1. Why use simulation time instead of wall-clock time?
2. How does a motor target differ from a sensor measurement?
3. Why reset before comparing trials?

## Submission

Submit verification output, a screenshot of the moving UR5e, and reflection answers.

## Optional advanced path

The former ROS 2/Gazebo setup is in [`optional_advanced/ros2_gazebo/lab00_setup/`](../optional_advanced/ros2_gazebo/lab00_setup/README.md).
