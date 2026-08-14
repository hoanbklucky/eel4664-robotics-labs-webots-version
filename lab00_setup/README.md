# Lab 00 — Webots Fundamentals and UR5e Orientation

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

Complete Lab 00 before Lab 01. Allow approximately 2–2.5 hours.

## Motivation

Learn the simulator with Cyberbotics' small e-puck exercises before adding the complexity of a six-joint manipulator. Following the instructional style used in Correll's labs, you will predict, modify, observe, and explain a working example. You will then transfer the same Webots concepts to the official Universal Robots factory sample.

## Learning objectives

After this lab you should be able to:

1. create, open, save, reset, and run a Webots project;
2. navigate the Scene Tree and distinguish visual geometry, collision geometry, and physics;
3. connect a Python controller to a robot and implement a sense–compute–act loop;
4. identify motors and sensors by their Webots device names;
5. explain simulation time steps, rendering modes, and controller sampling;
6. map the introductory e-puck concepts to the UR5e.

## 1. Install Webots and Python

Install the stable Webots R2025a release—not a nightly or development build—and a Python interpreter with NumPy and Matplotlib:

```powershell
py -m pip install numpy matplotlib
py -c "import numpy, matplotlib; print(numpy.__version__)"
```

In Webots, set **Tools → Preferences → Python command** to that interpreter if necessary.

Keep course work in a short local path such as `C:\eel4664-ur5e-labs`. Avoid OneDrive, SharePoint, network drives, and deeply nested project paths.

Run the pinned sample-preparation command in Section 3 even if Webots can open its built-in samples. Later starter worlds deliberately reference this local R2025a asset copy so every student uses the same UR5e model.

Before proceeding, bookmark [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md), including its safe recovery procedure and staged controller checks.

## Required Webots workflow and recovery

Use the semester-pinned stable **Webots R2025a** release only; nightly and development builds are unsupported.

The known-good world is `worlds/lab00_starter.wbt`. Never overwrite it. Before making any change, pause and reset the simulation, then use **File → Save World As…** to create `worlds/lab00_work.wbt`. If you have not opened Webots yet, copying the file to that name is equivalent. Confirm that the title bar shows the work copy before pressing Play.

Keep every controller under `controllers/<controller_name>/<controller_name>.py` and commit it to Git. Validate in this order, stopping at the first failure:

1. **World:** open the work copy paused with controller `void`.
2. **Minimal controller:** select `diagnostic_minimal`, Reset, and confirm its pass messages.
3. **Devices:** select `diagnostic_devices`, Reset, and save the device inventory.
4. **One joint:** use the lab controller to enable sensors and move one joint a small, conservative amount while all other joints hold.
5. **Full algorithm:** run the complete lab only after the first four stages pass.

Do not modify the Scene Tree except where this lab explicitly makes world/model modification a learning objective. Prefer controller and NumPy changes.

**Recovery:** close Webots instead of repeatedly reopening a crashing work world. Start Webots without using **Open Recent**, open the clean starter in paused mode, and immediately save a new work copy. Use **Reset** to restore simulated state; use **Reload/Revert World** to discard world edits and return to the last saved definition. If `void` fails, diagnose the world/assets/rendering. If `void` passes but `diagnostic_minimal` fails, diagnose Python/controller startup. If minimal passes but device listing fails, diagnose the robot/controller assignment or device hierarchy. See [Webots troubleshooting](../docs/TROUBLESHOOTING_WEBOTS.md).
## 2. Complete the Webots fundamentals

Use the [Cyberbotics Webots tutorials](https://cyberbotics.com/doc/guide/tutorials?version=R2025a) in the order below. When a tutorial presents language tabs, select **Python**. Create the tutorial project outside the course repository so its generated files do not become part of your submission.

### Required: Tutorial 1 — Your First Simulation

Complete [Tutorial 1](https://cyberbotics.com/doc/guide/tutorial-1-your-first-simulation-in-webots?version=R2025a).

Before running the controller, predict what the e-puck will do. Confirm that you can identify:

- the project, `worlds`, and `controllers` directories;
- the `.wbt` world and its Scene Tree;
- the robot's `controller` field;
- the wheel motors; and
- Play, Pause, Reset, and simulation time.

### Required: Tutorial 2 — Modification of the Environment

Complete [Tutorial 2](https://cyberbotics.com/doc/guide/tutorial-2-modification-of-the-environment?version=R2025a).

For the ball or another rigid object, sketch this relationship:

```text
Solid
├── children / Shape       visual representation
├── boundingObject         collision representation
└── Physics                mass and dynamic behavior
```

Record one sentence explaining `DEF/USE` and one explaining why collision geometry is often simpler than visual geometry.

### Selected exercise: Tutorial 3 — Appearance

Read the introduction and complete only the **Rendering Options** exercise in [Tutorial 3](https://cyberbotics.com/doc/guide/tutorial-3-appearance?version=R2025a):

1. enable wireframe rendering;
2. identify how the display differs from missing lighting or missing assets;
3. restore **View → Plain Rendering**; and
4. locate the coordinate-system optional rendering control.

The remaining appearance and texture exercises are optional.

### Required: Tutorial 4 — More About Controllers

Complete [Tutorial 4](https://cyberbotics.com/doc/guide/tutorial-4-more-about-controllers?version=R2025a) using Python.

Annotate your controller with these three phases:

```python
while robot.step(time_step) != -1:
    # 1. Sense: read enabled sensors
    # 2. Compute: calculate the command
    # 3. Act: send commands to motors
```

Be prepared to explain why sensors must be enabled, why device names must match the Scene Tree, and why `time_step` must be compatible with `WorldInfo.basicTimeStep`.

Tutorials 5–8 are not prerequisites for Lab 01. Tutorial 8 is assigned in Lab 02, Tutorials 5–6 in Lab 04, and Tutorial 7 in Lab 09, where their Supervisor, robot-modeling, physics, and PROTO concepts are used.

## 3. Open the official Universal Robots sample

In Webots choose:

**File → Open Sample World → robots → Universal Robots**

Open `ure.wbt`. You should see a factory containing UR3e, UR5e, and UR10e robots moving cans. This follows the sample-first workflow used by [Correll's manipulation Lab 0](https://introduction-to-autonomous-robots.github.io/lab-manipulation-introduction.html).

### Prepare the pinned local sample

Close every Webots window and run this command from the course repository. It prepares the exact R2025a assets used by all later lab starter worlds and also fixes installations that report `changed by fallback mechanism` or `Skipped PROTO`:

```powershell
powershell -ExecutionPolicy Bypass -File .\lab00_setup\prepare_webots_sample.ps1
```

Then open:

```text
C:\webots-eel4664-sample\projects\robots\universal_robots\worlds\ure.wbt
```

This remains Cyberbotics' official R2025a sample; the script makes its required assets local and does not modify `C:\Program Files\Webots`. If the Scene Tree appears but the view is black or contains only outlines, close Webots, rerun the command, and reopen the local `ure.wbt` so Webots reloads the repaired HDR path.

## 4. Transfer the concepts to the UR5e

Pause and reset the sample before inspecting it. Complete this mapping in your notes:

| Webots concept | e-puck tutorial | UR5e sample |
|---|---|---|
| Actuator | left/right wheel motor | six revolute-joint motors |
| Sensor | distance sensor | joint position sensor |
| Controller output | wheel velocity | joint target position or torque |
| Robot motion | planar mobile motion | articulated 3D motion |
| Feedback loop | obstacle avoidance | joint-space or task-space control |

In the Scene Tree, locate the UR5e and record:

- its controller name;
- the six joint motor names;
- the six corresponding position-sensor names;
- `WorldInfo.basicTimeStep`; and
- the relationship between the UR5e PROTO and the world that instantiates it.

Sketch `controller → motor → physics → sensor → controller` and label which parts belong to Webots and which parts students will implement in Python.

## 5. Simulation-time experiment

Following Correll's exercise, run the sample in Fast mode and record the speed-up factor. Reset before every trial. Change `WorldInfo.basicTimeStep` from 8 ms to 80 ms and then 160 ms, predicting the effect before each run. Restore 8 ms when finished.

Explain the tradeoff among computation speed, numerical fidelity, collision behavior, and controller sampling.

## 6. Prepare for Lab 01

The fallback preparation script copies the course controller starter into the sample project. Otherwise, choose **Wizards → New Robot Controller**, select Python, and name it `eel4664_ur5e`.

Do not replace the UR5e controller during Lab 00. Lab 01 will connect the Python controller and begin explicit sensing and actuation.

From the course repository, verify the installation:

```powershell
py .\lab00_setup\verify_installation.py
```

## Reflection

1. What information belongs in a world file, a PROTO, and a controller?
2. Why is collision geometry commonly simpler than rendered geometry?
3. How does the e-puck sense–compute–act loop transfer to a six-joint arm?
4. Why can a larger basic time step run faster while producing worse physics or control?
5. Why should a simulation be paused and reset before editing and saving its initial state?

## Submission

Submit one PDF containing:

1. screenshots showing completion of Tutorials 1, 2, and 4;
2. a screenshot of Tutorial 3 in wireframe mode and another after restoring plain rendering;
3. the `Solid` structure sketch and the completed e-puck-to-UR5e mapping;
4. a screenshot of the official Universal Robots factory sample;
5. the simulation-time experiment table;
6. the labeled UR5e feedback-loop sketch;
7. answers to the reflection questions; and
8. the output of `verify_installation.py`.

## Optional advanced path

The former ROS 2/Gazebo setup is in [`optional_advanced/ros2_gazebo/lab00_setup/`](../optional_advanced/ros2_gazebo/lab00_setup/README.md).
