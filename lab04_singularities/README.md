# Lab 4 - Seeing a Robot Singularity in Webots

## Get the Latest Course Files

Before starting, save your work and close Webots. Follow [Updating the Course Repository](../docs/UPDATE_REPOSITORY.md). Do not force an update or discard local work when Git reports a conflict.

## Mission

Complete two lines of a supplied Cartesian path controller, then run a Webots experiment that compares a well-conditioned baseline with approaches to elbow and shoulder singularities. Watch different parts of the robot produce rapidly growing joint rates even though the stylus follows a simple straight path.

The path generator, Jacobian, safety limit, Webots interface, visualization, and plotting are supplied. Your code combines the supplied path velocity with pose-error feedback and converts that Cartesian command into joint rates.

## What You Should Learn

After the experiment, you should be able to:

- recognize elbow and shoulder singular configurations;
- identify the three common singularity families of a six-axis arm with a spherical wrist;
- use the minimum singular value and condition number to compare two poses;
- explain why an undamped inverse requests very large joint rates near a singularity; and
- explain why more Cartesian via points do not remove that rate amplification.

## Before You Start

Complete Lab 3 and the [setup prerequisites](../lab00_setup/README.md). Lab 3 already introduced inverse kinematics and damped least squares. This lab focuses only on seeing and explaining a singularity; it does not repeat the damping comparison.

For Jacobian derivations and additional theory, see [Optional Background](OPTIONAL_BACKGROUND.md). It is a reference, not required reading for completing the lab.

Use Webots R2025a. Do not save over the original starter world. Open `worlds/lab04_starter.wbt` while paused and immediately select **File -> Save World As...** to create `worlds/lab04_work.wbt`.

## Understand the Experiment Before Running It

### The three common singularity families

For a six-axis robot such as the UR5e, singularities are commonly grouped into three families:

- **Shoulder singularity:** the wrist center approaches the vertical base-joint axis. Joint 1 loses leverage for one Cartesian direction, so a small stylus motion can require a rapid base rotation.
- **Elbow singularity:** the arm becomes fully extended or folded. The robot loses effective motion in a direction that would require the arm to extend beyond its reachable boundary.
- **Wrist singularity:** wrist joint 2 approaches zero and two wrist rotation axes align. The robot loses one independent orientation direction, often producing large opposing wrist-joint rates.

This lab demonstrates the elbow and shoulder families because their geometry and growing joint rates are easy to see. The wrist family is included for the big picture but is not a required Webots trial because it needs an orientation target rather than the visible straight translation used here.

## Complete the Two-Line Path Controller

Open `src/cartesian_path_controller.py`. The supplied Webots controller has already calculated all four inputs:

- `J`: the current 6-by-6 Jacobian;
- `pose_error`: the six-element error from the measured pose to the moving reference pose;
- `feedforward_twist`: the requested six-element Cartesian velocity along the yellow path; and
- `gain`: the proportional feedback gain.

You do **not** need to construct `feedforward_twist`. The supplied controller creates a six-element zero vector, places `speed * path_direction` in its first three entries, and leaves its angular-velocity entries zero because tool orientation is fixed.

Replace the `NotImplementedError` with two lines. Use these hints in order:

1. Form the commanded Cartesian twist using `command = feedforward + gain * error`.
2. Solve `J @ joint_rate = command` without explicitly calculating `inv(J)`.

The function must return the six commanded joint rates. Save the file before opening Webots.

Check your implementation from the repository root:

```bash
python lab04_singularities/src/check_cartesian_path_controller.py
```

Continue when it prints `PASS: the Cartesian path controller is ready for Webots.`

<details>
<summary>Stuck? Reveal the two-line solution</summary>

```python
desired_twist = feedforward_twist + gain * pose_error
return np.linalg.solve(J, desired_twist)
```

</details>

These two lines are deliberately undamped. Near a singularity, the Cartesian command can remain small while `np.linalg.solve` returns very large joint rates. The supplied 3.00 rad/s limiter makes that consequence visible without sending the raw request directly to Webots.

All three trials hold tool orientation fixed and use the same slow 2 cm/s Cartesian speed. This makes robot configuration, rather than requested speed, the main difference between the trials.

A Jacobian maps joint rates to instantaneous tool motion. Near a singularity, the robot has little leverage in one direction, so the inverse requests large joint rates to maintain even a small tool velocity.

Two displayed numbers summarize this behavior:

- **Minimum singular value:** measures the robot's weakest instantaneous motion direction. **Larger is better; zero means singular.** A small value means substantial joint speed produces very little tool speed in one direction.
- **Condition number:** is the largest singular value divided by the smallest. **Smaller is better; 1 is ideal.** A very large value means the inverse is sensitive and strongly amplifies some commands.

The three trials isolate these effects:

| Trial | Configuration and inverse | What to expect | Why |
|---|---|---|---|
| 1 | Move away, undamped | The elbow remains bent and joint rates stay moderate | The motion moves away from the problematic straight-elbow configuration. |
| 2 | Approach elbow singularity, undamped | The elbow reaches about 1 degree from straight and joint rates rise sharply | The two elbow IK branches meet near the straight configuration. |
| 3 | Approach shoulder singularity, undamped | The elbow stays bent while the wrist center approaches the base axis and the base joint rotates rapidly | Joint 1 loses Cartesian leverage near the base axis. |

The condition-number markers in Trials 2 and 3 are observation points for these supplied paths, not universal definitions of singularity.

### What the Webots display shows

You do not need to infer the intended tool motion from the joint motion. During each trial, Webots displays:

- in Trials 2 and 3, a banner directly below the trial title stating the central idea: **small Cartesian motion can require large joint motion** near a singularity;
- a **cyan sphere** at the visible stylus tip's starting point;
- a thick **yellow dotted path** beginning at the stylus tip and showing the requested Cartesian translation;
- a **green sphere** at the requested stylus-tip endpoint;
- a **red line and sphere** showing the translation the stylus tip actually completed; and
- a compact status panel at the top and short instructions at the bottom, with the lower joint-rate or action line emphasized in red.

### What happens in Trial 2: elbow singularity

Trial 2 moves from a bent elbow toward a straight elbow at constant tool speed. As the elbow angle approaches zero, `sigma_min` falls, the condition number rises, and the inverse requests rapidly increasing joint rates. At the singular configuration, the arm cannot maintain the requested velocity in its weak direction, so rate limiting may make the stylus briefly lag.

### What happens in Trial 3: shoulder singularity

Trial 3 keeps the elbow bent while the wrist center crosses the vertical base axis. Joint 1 loses leverage near that axis, so its requested rate rises and then falls after the crossing. Both IK branches can produce high rates; the supplied controller encourages the higher-rate branch so the large shoulder movement is easy to see.

### Why both singularity trials are rate limited

Trials 2 and 3 limit every joint to 3.00 rad/s, just below the Webots model's 3.14 rad/s limit. The limiter prevents an excessive command while preserving the visible rate spike; brief lag or jerk is therefore expected. This is a simulation setting, not a recommended hardware limit.

### Why more via points do not remove high joint rates

Locally, `joint rate = inverse(J) * Cartesian velocity`. Near a singularity, the inverse strongly amplifies motion in the weak direction. More via points make the path smoother, but they do not reduce the joint speed needed to follow it at the same Cartesian speed. The robot must slow down or use a method such as damping that accepts some tracking error. See [Optional Background](OPTIONAL_BACKGROUND.md#11-via-points-and-robot-motion-time) for the detailed explanation.

Before running, write one prediction: Which joints or visible robot features will change most near the elbow and shoulder singularities?

## Run the Three Trials

1. Open `worlds/lab04_work.wbt` in Webots. The robot starts directly at the bent-elbow Trial 1 pose.
2. Reset the simulation, then click **Run**. The supplied world already selects the `singularity_demo` controller.
3. Keep the 3D view and Webots console visible.
4. At each trial preview, read the on-scene explanation, click inside the Webots 3D view, and press **Space** when you are ready. All three motions then run continuously.
5. **Trial 1:** Press Space and watch the stylus move away from the straight-elbow singularity. The bottom readout continuously displays the current rate sent to Webots, the peak raw inverse request, and the peak rate sent after applying the limit. At the end, record the displayed Trial 1 peaks, then press Space to continue.
6. **Trial 2:** Before pressing Space, read the three preview lines explaining what will change and what to watch. The robot then moves continuously from the bent start toward the straight-elbow singularity. Watch `sigma_min` fall, the condition number rise, and the current and peak joint rates grow near the green target. The condition-200 message is a marker only; it does not pause the robot.
7. At the end of Trial 2, record the result, capture a screenshot near the straight-elbow endpoint, and press Space. The robot moves to the shoulder-test starting pose.
8. **Trial 3:** Before pressing Space, read the three preview lines: the first half approaches the base axis, the second half crosses it and moves away, and the raw rate spike is clipped by the 3.00 rad/s limit. Then press Space and watch continuously. The running message remains fixed so you can focus on the brief jerk, large shoulder rotation, and changing rate readout as the wrist center crosses the singular region.
9. When `[DEMONSTRATION COMPLETE]` appears, inspect the final pose and pause the simulation.

The controller creates `lab04_singularities/joint_rate_comparison.svg` inside the repository and prints its complete location in the Webots console. Open it after Trial 3. It plots `max |joint rate|` against active motion time, marks the elbow and shoulder checkpoints, and shows the 3.00 rad/s simulation limit. The green Trial 1 curve should stay moderate, the red elbow curve should rise near its endpoint, and the purple shoulder curve should rise and fall near the middle of its path.

The demonstration has no fixed duration because it advances only when you press Space. Reset Webots if you want to repeat it.

## What to Record

Copy these three values printed for each trial into the report:

| Quantity | What it tells you |
|---|---|
| Minimum singular value, `sigma_min` | **Larger is better.** Zero means the Jacobian is singular; a value near zero means the robot has almost lost one Cartesian motion direction. |
| Condition number, `sigma_max / sigma_min` | **Smaller is better.** A value of 1 is ideal; a large value means inverse motion is sensitive and can strongly amplify joint rates. |
| Peak commanded joint rate | **Larger means faster joint motion.** Compare it with the 3.00 rad/s Webots simulation limit. Sharp increases in Trials 2 and 3 are visible evidence of approaching singularities. |

Paste one Webots screenshot of Trial 1, one of Trial 2 near its straight-elbow endpoint, and one captured during Trial 3's continuous singularity crossing. Keep the on-scene geometry and joint-rate readouts visible. Also include the generated joint-rate comparison plot, which provides the clearest record of the brief peaks.

You may optionally preview the configuration metrics without Webots:

```bash
python lab04_singularities/src/singularity_scan.py
```

This command is not a required submission.

## How to Interpret the Results

Use the sequence below when interpreting the output:

1. Follow Trial 2 continuously from its well-conditioned start toward the nearly straight elbow. The changing metrics establish that singularity is caused by the evolving robot configuration.
2. Compare Trial 1's moderate curve with the rising Trial 2 curve.
3. Compare Trials 2 and 3. Connect the nearly straight elbow in Trial 2 and the small wrist-center radius in Trial 3 to their increasing joint-rate requests.

The simulation limit scales an already excessive command so it can be displayed safely. It does not remove the singularity or change why the undamped inverse requests the large rate.

## Questions

Answer this question in two to four sentences. Use one observation from the Webots trials in your explanation:

1. Why can a small requested Cartesian motion require very large joint motion near a singularity?

## What to Submit

Submit the completed `Lab04_Report_Template.docx` containing:

- your prediction;
- the three recorded quantities for all three trials;
- one screenshot from each trial;
- the generated joint-rate comparison plot; and
- your answer to the singularity question.

Also submit your completed `src/cartesian_path_controller.py`. Do not submit Webots world files.

## Troubleshooting

| Problem | Action |
|---|---|
| The controller does not appear in Webots | Close and reopen the world after updating the repository. |
| Webots reports that `get_from_def()` requires a Supervisor | Your work world was created from an older starter. Close it and create a fresh `lab04_work.wbt` from the updated starter; the updated UR5e has `supervisor TRUE`. |
| The robot does not move | Confirm that you created the work world from the updated starter, then reset and click Run. |
| The console reports `NotImplementedError` | Complete and save the two lines in `src/cartesian_path_controller.py`, then reset Webots. Use the hints or collapsed solution above if needed. |
| Only one or two trials appear | Let the simulation run until `[DEMONSTRATION COMPLETE]` appears. |
| Trial 2 prints a safety scale below 1 | This is expected; it prevents the excessive raw inverse rate from exceeding the 3.00 rad/s simulation limit. |
| Trial 3 is mistaken for an elbow singularity | Check the display: the elbow remains bent while the wrist-center radius approaches zero and the base joint accelerates. |
| The red trace stops before the green target | The controller permits up to three seconds of feedback-only completion after the scheduled path request. If it still stops short, read the final console error and confirm that the updated controller is running. |
| Pressing Space does nothing | Click once inside the Webots 3D view to give it keyboard focus, then press Space again. |
| The terminal scan reports an unfinished Lab 2 function | Complete the required Lab 2 FK equations before running Lab 4. |
| The world or robot pose becomes corrupted | Close without saving and make a fresh copy of `lab04_starter.wbt`. |
