# Lab 1 - UR5e Playground

## Mission

**Take control of the UR5e, discover what its six joints do, and guide the orange stylus toward three target bubbles.**

This is an exploration lab. You are not expected to know forward kinematics, DH parameters, homogeneous transforms, or inverse kinematics yet. Use observation and trial and error. The difficulty you experience is the motivation for the mathematical models in the next labs.

Plan for approximately 45-60 minutes.

## Success Criteria

You have completed the mission when you have explored all six joints, brought the stylus near at least one target, recorded one target-pose joint vector, and can explain why a robot program needs something better than trial and error.

## Learning Objectives

- Operate a UR5e safely in Webots.
- Identify the shoulder, elbow, and wrist joints by observing motion.
- Describe how changing one joint affects the tool.
- Recognize that the effect of a joint depends on the robot's current configuration.
- Explain why an autonomous robot needs a model that predicts tool motion.

## Prerequisite

Complete [Lab 00 - Software Setup and Webots Basics](../lab00_setup/README.md), including Webots Tutorials 1 and 4. No robotics mathematics is required.

## Provided Files

- `worlds/lab01_starter.wbt` - UR5e playground with an orange stylus and three visual target bubbles
- `controllers/ur5e_playground/ur5e_playground.py` - complete keyboard controller; do not modify it
- `answers.md` - short observation and reflection template

## Part 1 - Open the Playground

1. From the repository root, prepare the pinned Webots R2025a UR5e assets:

   ```bash
   python lab00_setup/prepare_webots_sample.py
   ```

   On macOS or Ubuntu, use `python3` if `python` is not recognized.

2. Open `worlds/lab01_starter.wbt` in Webots while the simulation is paused.
3. Immediately select **File -> Save World As...** and create `worlds/lab01_work.wbt` beside the starter.
4. Confirm the UR5e controller is `ur5e_playground`.
5. Press **Run**, then click the 3D view so it receives keyboard input.

Never overwrite `lab01_starter.wbt`. If the working world becomes damaged, discard it and make a fresh copy from the starter.

## Part 2 - Meet the Six Joints

The controller starts from a safe exploration pose. Use these keys:

| Key | Action |
|---|---|
| `1`-`6` | select a joint |
| Up / Down arrow | increase / decrease the selected joint target |
| `R` | return to the safe exploration pose |
| `D` | start or stop a short preset robot dance |
| `P` | print the current joint angles, stylus position, and target distances |
| `H` | print the controls again |

Move slowly and watch the whole arm, not only the orange tip. If the arm approaches the floor or folds into itself, release the key and press `R`. The controller limits joint targets and motor speed, but you are still responsible for observing the motion.

Explore all six joints. For at least three joints, record:

- which links moved;
- whether the stylus position changed substantially; and
- whether the stylus orientation appeared to change.

Try one joint from two different robot configurations. Notice that the same joint does not always move the stylus in the same world direction.

## Part 3 - Target-Bubble Challenge

Use trial and error to bring the orange stylus tip near the colored target bubbles. The Console reports when the tip enters a target's 10 cm success region. The bubbles are visual only; they have no collision geometry and cannot damage or push the robot.

Complete these challenges:

1. Reach any one target bubble.
2. Reach a second target without pressing `R` between targets.
3. Press `P` and record the six joint angles for your best target pose.

Optional challenges:

- Reach all three targets in one run.
- Return close to a previous target using the recorded joint angles.
- Find two visibly different arm shapes that place the stylus in approximately the same region.
- Press `D` and explain why the stylus path is more complicated than the individual joint motions.

This is not an accuracy competition. A target attempt that teaches you something about the robot is useful even if it misses.

## Part 4 - Why Do We Need Forward Kinematics?

In this lab, you found joint angles by moving the robot and observing the result. That approach becomes slow and unreliable when a program must plan thousands of motions, avoid obstacles, or operate without a person watching.

The next lab asks the reverse question:

> Given the six joint angles, how can a program predict the tool position and orientation before the robot moves?

That prediction is **forward kinematics**.

## What to Submit

Submit one completed `answers.md` containing:

1. one screenshot showing the UR5e and a target attempt;
2. the three-joint observation table and one recorded target-pose joint vector; and
3. a short explanation of why trial and error is inadequate for an autonomous robot.

Do not submit controller code, `lab01_work.wbt`, installed software, downloaded vendor assets, or caches.

## Troubleshooting

| Problem | Check |
|---|---|
| UR5e is missing | rerun `python lab00_setup/prepare_webots_sample.py` and reopen the world |
| keyboard does nothing | press **Run**, click inside the 3D view, and press `H` |
| controller is not found | confirm the world is inside this lab's `worlds` folder and the controller is `ur5e_playground` |
| robot enters an awkward pose | release the key and press `R`; reset Webots if needed |
| starter world was changed | restore it with Git and create a new `lab01_work.wbt` |
