# Planar Robot FK and IK Simulator Activities

These browser activities build intuition before the UR5e forward- and inverse-kinematics experiments. They are intended for lecture demonstrations, guided practice, or an optional pre-lab exercise. No software installation is required.

Use:

- [SiliconWit Inverse Kinematics Simulator](https://siliconwit.com/product-development/inverse-kinematics-simulator/) as the primary IK simulator. It accepts a target position and lets you compare geometric IK, the Jacobian pseudoinverse, damped least squares (DLS), cyclic coordinate descent (CCD), and FABRIK.
- [Robot Arm Kinematics Web Simulator](https://zawhlainghtet.github.io/RobotKinematics/) for entering joint angles, checking 2-D FK, and independently verifying an IK result.

These are external teaching tools and may change independently of this course. Do not purchase downloads or enter personal information for these activities. If a site is unavailable, the instructor may demonstrate the same observations using screenshots or another simulator.

> **RobotKinematics link-length limit:** every link is forced into the range
>
> $$
> 10 \le L_i \le 240.
> $$
>
> This site displays link lengths in pixels. Enter values within this range; the simulator clamps values outside it.

> **Convention warning:** Do not use RobotKinematics' **DH mode** for course calculations. It uses standard DH, while Lab 2 uses Craig's modified DH. The frame assignment, parameter indexing, and transform order differ, so its standard-DH table cannot be copied into the Lab 2 implementation.

## Learning goals

After completing the activities, you should be able to:

- calculate a planar end-effector pose from link lengths and joint angles;
- explain why link orientations use cumulative joint angles;
- distinguish FK inputs from IK inputs;
- identify elbow-up and elbow-down IK branches;
- verify an IK solution by substituting its joint angles into FK;
- recognize unreachable targets and singular configurations; and
- explain why a numerical IK result depends on the algorithm, initial configuration, and task definition.

## Important model assumption

These activities use a **planar 3R arm**: three revolute joints rotate about parallel z-axes. Its complete end-effector pose is

$$
(x, y, \phi),
$$

where the orientation is

$$
\phi=q_1+q_2+q_3.
$$

The SiliconWit IK simulator specifies target position x and y, but it does not require a target orientation. A 3R arm therefore has one more joint variable than task constraints, so many joint configurations may reach the same point.

## Activity 1 - Explore 3R forward kinematics

Open the [Robot Arm Kinematics Web Simulator](https://zawhlainghtet.github.io/RobotKinematics/).

1. Select **FK 2D**.
2. Select **3 Links**.
3. Set these values, all of which satisfy the site's 10 <= Li <= 240 limit:
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

## Activity 2 - See multiple IK solutions

Open the [SiliconWit Inverse Kinematics Simulator](https://siliconwit.com/product-development/inverse-kinematics-simulator/).

### Part A: elbow-up and elbow-down for a 2R arm

1. Select **2 degrees of freedom**.
2. Set Link 1 Length = 120 mm and Link 2 Length = 100 mm.
3. Set Target X = 160 mm and Target Y = 80 mm.
4. Select **Geometric (Closed-Form)**.
5. Turn on **Show All Solutions**, then start the animation.
6. Record the two joint-angle solutions and identify the elbow-up and elbow-down drawings.

| Branch | q1 | q2 | Final position or error |
|---|---:|---:|---|
| Elbow up |  |  |  |
| Elbow down |  |  |  |

### Part B: redundancy for a 3R arm

1. Select **3 degrees of freedom** and set Link 3 Length = 80 mm.
2. Keep the same target position.
3. Select **Damped Least Squares** and solve.
4. Record q1, q2, q3, final error, and iteration count.
5. Reset or choose a different starting configuration, then solve the same target again.
6. Compare the two joint vectors and arm shapes.

### Questions

1. How can two different 2R joint vectors reach the same target?
2. Why can a 3R position-only problem have more solutions than a 2R problem?
3. Did the two 3R runs reach nearly the same position with different joint angles?

## Activity 3 - Verify an IK result with FK

Use one 3R result from Activity 2 Part B.

1. Return to RobotKinematics and select **FK 2D** with **3 Links**.
2. Enter L1 = 120, L2 = 100, and L3 = 80.
3. Enter the three joint angles produced by SiliconWit.
4. Record the FK tool position.
5. Compare it with the SiliconWit target (160, 80).
6. Add the three angles to find the resulting tool orientation phi.

Report whether the IK result is verified. Small differences caused by displayed-angle rounding are acceptable. A large difference usually indicates that an angle, sign, unit, or joint order was copied incorrectly.

### Questions

1. Why is running FK with the returned joint angles an independent check of IK?
2. Did SiliconWit prescribe phi, or did the numerical solver choose it indirectly?
3. Why might another valid 3R result reach the same point with a different phi?

## Activity 4 - Compare numerical IK methods

Continue in SiliconWit with the 3R arm.

1. Use the same link lengths and a reachable target away from the workspace boundary.
2. Solve it with **Jacobian Pseudoinverse**, **Damped Least Squares**, **CCD**, and **FABRIK**.
3. Record final error, iteration count, and whether the motion looked smooth and stable.
4. Use **Run Full Experiment** to view the algorithm comparison if available.

| Method | Final error | Iterations | Observation |
|---|---:|---:|---|
| Jacobian pseudoinverse |  |  |  |
| Damped least squares |  |  |  |
| CCD |  |  |  |
| FABRIK |  |  |  |

### Near the reach boundary

1. Add the three link lengths to predict maximum reach.
2. Move the target close to that boundary and repeat the pseudoinverse and DLS trials.
3. Move the target beyond maximum reach and observe the result.

### Questions

1. Why is a target beyond the sum of the link lengths unreachable?
2. What changes near a fully extended, singular configuration?
3. Which method was more stable near the boundary: the pseudoinverse or DLS?
4. What does damping trade away for improved stability?

## Short reflection

Answer in a few sentences each:

1. Explain FK and IK using the words **input** and **output**.
2. Explain why IK may have zero, one, two, or many solutions.
3. Describe how you verified an IK result without trusting the IK solver itself.
4. Explain why the UR5e numerical IK lab uses DLS, convergence tolerances, an iteration limit, and an initial seed.
5. State one limitation of these planar simulators compared with the UR5e experiment in Webots.

## Instructor-use suggestion

A concise lecture sequence is:

1. Activity 1 configuration B to introduce cumulative angles.
2. Activity 2 Part A to show two analytical IK branches.
3. Activity 2 Part B to introduce redundant position-only IK.
4. Activity 3 to demonstrate the FK-after-IK verification loop.
5. Activity 4 to compare numerical methods and motivate damping near singularities.