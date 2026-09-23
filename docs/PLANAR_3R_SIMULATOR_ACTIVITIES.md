# Planar Robot FK and IK Simulator Activities

These browser activities build intuition before the UR5e forward- and inverse-kinematics experiments. They are intended for lecture demonstrations, guided practice, or an optional pre-lab exercise. No software installation is required.

Use:

- [Robot Arm Kinematics Web Simulator](https://zawhlainghtet.github.io/RobotKinematics/) for 2-D FK, standard DH transforms, analytical 2-link IK, and iterative IK with three or more links.
- [Robotics Project Hub Robot Arm Simulator](https://roboticsprojecthub.com/robot-arm-simulator/#introduction) for a planar arm with adjustable geometry, draggable targets, elbow-branch visualization, reachability, and singularity demonstrations.

These are external teaching tools and may change independently of this course. Do not enter personal information. If a site is unavailable, the instructor may demonstrate the same observations using screenshots or another simulator.

## Learning goals

After completing the activities, you should be able to:

- calculate a planar end-effector pose from link lengths and joint angles;
- explain why link orientations use cumulative joint angles;
- verify a DH transform using a graphical arm;
- distinguish FK inputs from IK inputs;
- identify elbow-up and elbow-down IK branches;
- verify an IK solution by substituting its joint angles into FK;
- recognize unreachable targets and singular configurations; and
- explain why a numerical IK solution depends on the initial guess and task definition.

## Important model assumption

These activities use a **planar 3R arm**: three revolute joints rotate about parallel z-axes. Its complete end-effector pose is

$$
(x, y, \phi),
$$

where the orientation is

$$
\phi=q_1+q_2+q_3.
$$

If IK specifies only `x` and `y`, the 3R arm has one more joint variable than task constraints, so many joint configurations may reach the same point. Specifying `x`, `y`, and `phi` usually reduces the analytical solutions to two branches.

## Activity 1 - Explore 3R forward kinematics

Open the [Robot Arm Kinematics Web Simulator](https://zawhlainghtet.github.io/RobotKinematics/).

1. Select **FK 2D**.
2. Select **3 Links**.
3. Set:
   - `L1 = 120`
   - `L2 = 100`
   - `L3 = 80`
4. Enter each joint configuration below.
5. Before reading the simulator output, predict the end-effector orientation by adding the three joint angles.
6. Record the displayed end-effector position and compare it with your own FK calculation.

Use

$$
x=L_1\cos q_1+L_2\cos(q_1+q_2)+L_3\cos(q_1+q_2+q_3),
$$

$$
y=L_1\sin q_1+L_2\sin(q_1+q_2)+L_3\sin(q_1+q_2+q_3).
$$

| Configuration | `q1` | `q2` | `q3` | Predicted `phi` | Predicted `(x, y)` | Simulator `(x, y)` |
|---|---:|---:|---:|---:|---|---|
| A | 0 deg | 0 deg | 0 deg |  |  |  |
| B | 30 deg | -45 deg | 60 deg |  |  |  |
| C | 90 deg | 0 deg | 0 deg |  |  |  |

### Questions

1. In configuration B, why is link 3 oriented at `q1 + q2 + q3`, rather than at `q3` alone?
2. Which change has the larger positional effect: changing `q1` or changing `q3`? Why?
3. Does the simulator use degrees or radians at the interface? Which unit must your Python trigonometric functions use?

## Activity 2 - Connect the picture to DH transformations

Continue in the first simulator.

1. Open **DH** mode.
2. Choose three revolute joints.
3. Use the planar standard-DH parameters:
   - `d_i = 0`
   - `alpha_i = 0`
   - `a_i = L_i`
   - `theta_i = q_i`
4. Enter the link lengths and configuration B from Activity 1.
5. Inspect the displayed end-effector transform.
6. Compare its translation entries with the FK position from Activity 1.
7. Compare its rotation with the predicted orientation `phi`.

### Questions

1. Which two entries of the homogeneous transform contain the end-effector position?
2. Why do all three planar links use `d_i = 0` and `alpha_i = 0`?
3. What information does the transform contain that an `(x, y)` coordinate alone does not?

## Activity 3 - Observe elbow-up and elbow-down IK

Open the [Robotics Project Hub Robot Arm Simulator](https://roboticsprojecthub.com/robot-arm-simulator/#introduction).

1. Select its inverse-kinematics mode.
2. Use three links and set their lengths to approximately 120, 100, and 80 pixels.
3. Set the tool orientation to approximately 20 degrees.
4. Drag the target to a clearly reachable point away from the workspace boundary, such as approximately `x = 200, y = 80`.
5. Record the displayed joint angles for the first elbow branch.
6. Switch the elbow branch and record the second set of angles.
7. Confirm visually that both configurations place the tool at the same target with the same requested orientation.

| Branch | `q1` | `q2` | `q3` | Tool x | Tool y | Tool angle |
|---|---:|---:|---:|---:|---:|---:|
| Elbow up |  |  |  |  |  |  |
| Elbow down |  |  |  |  |  |  |

The exact values may differ slightly because the target is positioned by dragging.

### Questions

1. Which joint angle changes sign most clearly between the two branches?
2. Why can two different joint vectors produce the same end-effector pose?
3. Which branch would require less motion from the current arm configuration?

## Activity 4 - Verify IK by running FK

Use the two joint-angle solutions recorded in Activity 3.

1. Switch the simulator to forward-kinematics mode.
2. Enter the elbow-up joint angles.
3. Record the resulting tool position and orientation.
4. Repeat with the elbow-down joint angles.
5. Compare both FK results with the IK target.

For each branch, report:

- position agreement in x and y;
- orientation agreement in `phi`; and
- whether the IK solution is verified.

A small difference caused by display rounding or target dragging is acceptable. A large difference usually indicates that an angle, sign, unit, or joint order was copied incorrectly.

## Activity 5 - Find unreachable targets and singularities

Continue in the Robotics Project Hub simulator.

### Unreachable target

1. Add the link lengths to predict the maximum straight-line reach.
2. Drag the target beyond that distance.
3. Record the simulator's status and what happens to the arm.
4. Return the target inside the workspace.

### Singular configuration

1. Move the target close to the outer workspace boundary.
2. Toggle between elbow-up and elbow-down.
3. Observe the two branches approach one another.
4. Move the target to full extension and observe that the branches coincide.
5. Move the target a small distance near the boundary and watch how much the joint angles change.

### Questions

1. Why do the two IK branches become one at full extension?
2. Why can a small Cartesian movement require a large joint movement near this configuration?
3. Why should a robot trajectory avoid operating exactly at the reach boundary?

## Activity 6 - Compare analytical and numerical IK

Return to the [Robot Arm Kinematics Web Simulator](https://zawhlainghtet.github.io/RobotKinematics/).

1. Select **IK 2D** with **2 Links**.
2. Choose a reachable target and compare its elbow-up and elbow-down analytical solutions.
3. Change to **3 Links**. The site indicates that three-to-five-link IK uses cyclic coordinate descent (CCD), an iterative numerical method.
4. Solve for a position target.
5. Change the initial arm shape using the joint controls or presets and solve the same position target again.
6. Compare the two resulting joint vectors and end-effector orientations.

### Questions

1. Why can the 3R numerical solver return different joint vectors for the same position target?
2. What task constraint is missing when the solver controls x and y but not `phi`?
3. How is dependence on the starting configuration similar to the seed dependence of Lab 3 numerical IK?
4. Why does the UR5e lab use convergence tolerances and an iteration limit?

## Short reflection

Answer in a few sentences each:

1. Explain FK and IK using the words **input** and **output**.
2. Explain why IK may have zero, one, two, or many solutions.
3. Describe how you verified an IK solution without trusting the IK solver itself.
4. State one limitation of these planar simulators compared with the UR5e experiment in Webots.

## Instructor-use suggestion

A concise lecture sequence is:

1. Activity 1 configuration A to establish the zero pose.
2. Activity 1 configuration B to introduce cumulative angles.
3. Activity 3 to show two IK branches.
4. Activity 4 to demonstrate the FK-after-IK verification loop.
5. Activity 5 to introduce reachability and singularities.
6. Activity 6 to motivate numerical IK, seeds, tolerances, and damping.
