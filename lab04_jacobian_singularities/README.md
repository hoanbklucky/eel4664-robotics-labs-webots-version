# Lab 4 - Seeing a Robot Singularity in Webots

## Mission

Run a supplied Webots experiment and observe how the same requested tool motion behaves at a bent-elbow pose and near a straight-elbow singularity. At the near-singular pose, compare an undamped inverse with a damped inverse.

There is no required programming in this lab. The Jacobian, inverse calculations, safety limit, and Webots controller are supplied. Your task is to predict what will happen, observe the robot, record the printed evidence, and explain the physical result.

## What You Should Learn

After the experiment, you should be able to:

- recognize a straight-elbow singular configuration;
- use the minimum singular value and condition number to compare two poses;
- explain why an undamped inverse requests very large joint rates near a singularity; and
- explain how damping limits joint motion by accepting Cartesian tracking error.

## Before You Start

Complete Lab 3 and the [setup prerequisites](../lab00_setup/README.md). Lab 3 already introduced inverse kinematics and damped least squares; this lab uses those ideas without asking you to implement them again.

Use Webots R2025a. Do not save over the original starter world. Open `worlds/lab04_starter.wbt` while paused and immediately select **File -> Save World As...** to create `worlds/lab04_work.wbt`.

## Understand the Experiment Before Running It

The controller asks for the same 6 cm translation in all three trials while also asking the tool orientation to remain fixed. The requested translation points approximately along the Cartesian direction that becomes difficult when the elbow is straight.

A Jacobian maps joint rates to instantaneous tool motion. At the bent-elbow pose, its motion directions are sufficiently independent, so the inverse can produce the request with moderate joint rates. Near the straight-elbow singularity, one singular value becomes very small. Producing motion along the corresponding difficult Cartesian direction then requires a combination of large, opposing joint rates.

The three trials isolate these effects:

| Trial | Configuration and inverse | What to expect | Why |
|---|---|---|---|
| 1 | Bent elbow, undamped | Moderate joint motion and a tool translation close to 6 cm | The Jacobian is well conditioned, so ordinary inverse motion works normally. |
| 2 | Almost straight elbow, undamped | The raw calculation requests extremely large joint rates. The controller rate-limits them before execution. Several joints move visibly, but the tool completes only a small part of the request. | The inverse divides by a very small singular value, amplifying the joint command. |
| 3 | Almost straight elbow, damped | Much smaller joint motion and only a small tool translation | Damping suppresses the amplified singular direction. This protects the robot but introduces tracking error. |

### Why Trial 2 is rate limited

The near-singular undamped calculation requests a peak joint rate of roughly 5 rad/s for this experiment. Sending that raw command would create an unnecessarily large configuration change and could exceed the intended demonstration limits. The controller therefore prints the raw result, then uniformly scales the joint-rate vector so the cubic motion never exceeds 0.50 rad/s at any joint. This preserves the undamped inverse's joint-motion direction while making the Webots trial controlled and repeatable.

Trial 3 starts again from the same near-singular pose. This reset is important: it allows the undamped and damped results to be compared from the same geometry.

Before running, write one prediction: Which trial will show the most joint motion, and which trial will move the tool closest to the requested 6 cm?

## Run the Three Trials

1. Open `worlds/lab04_work.wbt` in Webots.
2. In the Scene Tree, select `DEF UR5E UR5e`.
3. Change its `controller` field from `void` to `singularity_demo`.
4. Reset the simulation, then click **Run**.
5. Keep the 3D view and Webots console visible.
6. **Trial 1:** Watch the bent elbow and the visible tool translation.
7. **Trial 2:** Watch the joints move at the safety limit near the almost straight elbow. Compare that large joint motion with the small tool displacement.
8. **Trial 3:** The controller returns to the same almost straight-elbow pose, applies damping, and repeats the request. Watch how much less the joints move.
9. When `[DEMONSTRATION COMPLETE]` appears, pause the simulation.

The full run takes about 27 seconds. Reset Webots if you want to repeat it.

## What to Record

Copy these values printed for each trial into the report:

| Quantity | What it tells you |
|---|---|
| Minimum singular value | A value near zero indicates lost or nearly lost motion capability. |
| Condition number | A large value indicates sensitive, poorly conditioned inverse motion. |
| Raw undamped joint-rate norm | How strongly the ordinary inverse amplifies the request before safety limiting or damping. |
| Applied joint-rate-vector norm | The magnitude of the joint command actually used for that trial. |
| Safety scale | A value below 1 means the proposed command was uniformly reduced before execution. |
| Measured translation magnitude | How far the tool actually moved in Webots. |

Take one screenshot from each trial. For Trials 2 and 3, capture the almost straight-elbow pose so the two inverse methods can be compared from the same geometry.

You may optionally preview the configuration metrics without Webots:

```bash
python lab04_jacobian_singularities/src/singularity_scan.py
```

This command is not a required submission.

## Explain What You Observed

Use the sequence below when interpreting the output:

1. Compare Trial 1 with Trials 2 and 3 using the minimum singular value and condition number. This establishes that the change comes from the robot configuration.
2. Compare the raw undamped rate in Trials 1 and 2. This shows amplification near the singularity.
3. Compare Trials 2 and 3. Trial 2 shows the rate-limited undamped behavior; Trial 3 shows how damping reduces joint motion but accepts tool-motion error.

The safety limit and damping solve different problems. The safety limit scales an already excessive command so it can be executed. Damping changes the inverse calculation itself so that the difficult singular direction is not amplified as strongly.

## Questions

Answer each question in two or three sentences.

1. Which configuration was closer to a singularity? Support your answer using the minimum singular value and condition number.
2. In Trial 2, why did the raw undamped inverse request large joint rates even though the requested tool translation was only 6 cm?
3. Compare Trials 2 and 3. How did damping change the applied joint motion and measured tool displacement?
4. Why was it necessary to rate-limit Trial 2 instead of sending the raw undamped command directly to Webots?

## What to Submit

Submit the completed `Lab04_Report_Template.docx` containing:

- your prediction;
- the six recorded quantities for all three trials;
- one screenshot from each trial; and
- answers to the four questions.

No Python files or Webots world files are submitted.

## Troubleshooting

| Problem | Action |
|---|---|
| The controller does not appear in Webots | Close and reopen the world after updating the repository. |
| The robot does not move | Confirm that the UR5e controller is `singularity_demo`, reset, and click Run. |
| Only one or two trials appear | Let the simulation run until `[DEMONSTRATION COMPLETE]` appears. |
| Trial 2 prints a safety scale below 1 | This is expected; it prevents the excessive raw inverse rate from being commanded directly. |
| The terminal scan reports an unfinished Lab 2 function | Complete the required Lab 2 FK equations before running Lab 4. |
| The world or robot pose becomes corrupted | Close without saving and make a fresh copy of `lab04_starter.wbt`. |
