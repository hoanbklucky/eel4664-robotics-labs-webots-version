# Lab 4 - Seeing a Robot Singularity in Webots

## Mission

Run a supplied Webots experiment in which the stylus starts at a bent-elbow pose and moves toward a straight-elbow singularity. Compare a well-conditioned baseline with the rapidly growing joint rates near the singularity.

There is no required programming in this lab. The Jacobian, inverse calculations, safety limit, and Webots controller are supplied. Your task is to predict what will happen, observe the robot, record the printed evidence, and explain the physical result.

## What You Should Learn

After the experiment, you should be able to:

- recognize a straight-elbow singular configuration;
- use the minimum singular value and condition number to compare two poses;
- explain why an undamped inverse requests very large joint rates near a singularity; and
- explain why more Cartesian via points do not remove that rate amplification.

## Before You Start

Complete Lab 3 and the [setup prerequisites](../lab00_setup/README.md). Lab 3 already introduced inverse kinematics and damped least squares. This lab focuses only on seeing and explaining a singularity; it does not repeat the damping comparison.

Use Webots R2025a. Do not save over the original starter world. Open `worlds/lab04_starter.wbt` while paused and immediately select **File -> Save World As...** to create `worlds/lab04_work.wbt`.

## Understand the Experiment Before Running It

Both trials begin at the same visibly bent, well-conditioned pose. Trial 1 moves the stylus 20 cm away from the straight-elbow singularity. Trial 2 reverses the direction and moves 20 cm toward it while holding tool orientation fixed. The slow 2 cm/s motion lets you watch the elbow straighten and the inverse become progressively more sensitive.

A Jacobian maps joint rates to instantaneous tool motion. At the bent-elbow pose, its motion directions are sufficiently independent, so the inverse can produce the request with moderate joint rates. Near the straight-elbow singularity, one singular value becomes very small. Producing motion along the corresponding difficult Cartesian direction then requires a combination of large, opposing joint rates.

Two displayed numbers summarize this behavior:

- **Minimum singular value:** measures the robot's weakest instantaneous motion direction. **Larger is better; zero means singular.** A small value means substantial joint speed produces very little tool speed in one direction.
- **Condition number:** is the largest singular value divided by the smallest. **Smaller is better; 1 is ideal.** A very large value means the inverse is sensitive and strongly amplifies some commands.

These values should be compared using the same Jacobian units and scaling, as done in both trials.

The two trials isolate these effects:

| Trial | Configuration and inverse | What to expect | Why |
|---|---|---|---|
| 1 | Move away, undamped | The elbow remains bent and joint rates stay moderate | The motion moves away from the problematic straight-elbow configuration. |
| 2 | Approach singularity, undamped | Joint rates rise sharply near the end of the path and may reach the 3.00 rad/s simulation limit | The minimum singular value approaches zero, so the ordinary inverse strongly amplifies the request. |

Trial 2 pauses automatically when the condition number first reaches 200. At that instant, the elbow is close to straight and the display prominently reports the minimum singular value, condition number, elbow angle, raw requested peak joint rate, and applied peak joint rate. This later checkpoint makes the rate amplification easy to see before the final approach.

### What the Webots display shows

You do not need to infer the intended tool motion from the joint motion. During each trial, Webots displays:

- a **cyan sphere** at the visible stylus tip's starting point;
- a thick **yellow dotted path** beginning at the stylus tip and showing the requested 20 cm Cartesian translation;
- a **green sphere** at the requested stylus-tip endpoint;
- a **red line and sphere** showing the translation the stylus tip actually completed; and
- a compact status panel at the top and short instructions at the bottom, including the current joint rate and peak-so-far throughout both trials.

The singularity is not a place in the room; it is a robot configuration. An exactly straight elbow is at 0 degrees. The 20 cm target lies at the straight-elbow workspace boundary. The robot can approach this boundary, but it cannot continue farther along the same straight Cartesian line: beyond the boundary, the requested point is unreachable. This is why the demonstration approaches and stops at the singularity instead of claiming to pass through it.

### Why Trial 2 is rate limited

The undamped rate is moderate at the beginning of Trial 2 because the elbow is still bent. It grows rapidly only as the robot approaches the straight-elbow endpoint. The controller uniformly scales each updated joint-rate vector so no joint exceeds 3.00 rad/s, just below the Webots UR5e model's 3.14 rad/s joint limit. This higher simulation-only limit makes the rapid joint motion visible while still respecting the model limit; it is not a recommended hardware setting.

The controller recomputes the stylus-tip Jacobian and pose error at every simulation step. This keeps the stylus on the yellow line while preserving the increasing rate demand caused by the changing configuration.

### Why Cartesian via points still produce large joint rates

It is helpful to separate **IK computation time** from **robot motion time**. Suppose two neighboring points on the straight path are scheduled `dt` seconds apart. Numerical IK may take several internal iterations to find their joint configurations `q_k` and `q_(k+1)`, but the robot must still move between those configurations during the scheduled `dt`. Its physical joint rate is therefore approximately

`joint rate = (q_(k+1) - q_k) / dt`,

and locally the joint change satisfies

`q_(k+1) - q_k ~= inverse(J) * (x_(k+1) - x_k)`.

Near the singular configuration, the inverse Jacobian becomes very large in the weak direction. Consequently, two nearby Cartesian via points can correspond to joint configurations that are relatively far apart. If those points must still be reached within the same `dt`, the required joint rate becomes large.

Adding more via points makes the Cartesian path smoother, but it does not remove this amplification. To keep joint rates bounded, the Cartesian motion must slow down near the singularity.

At the exact straight-elbow workspace boundary, the Jacobian loses a motion direction. The endpoint itself can have an IK solution, but continuing farther along the same line has no solution. With the finite 3.00 rad/s simulation limit, the robot may fall slightly behind the constant-speed reference near that endpoint. After the scheduled ten-second path motion, the controller therefore allows up to three additional seconds of feedback-only motion and stops immediately when the target is reached. Reaching the boundary while maintaining the original constant Cartesian speed would instead require unbounded joint rates; merely allowing more IK iterations does not change that geometry.

Before running, write one prediction: In which part of Trial 2 will the joint rate be largest, and what will happen to the elbow there?

## Run the Three Trials

1. Open `worlds/lab04_work.wbt` in Webots. The robot starts directly at the bent-elbow Trial 1 pose.
2. Reset the simulation, then click **Run**. The supplied world already selects the `singularity_demo` controller.
3. Keep the 3D view and Webots console visible.
4. At each trial preview or singularity checkpoint, click inside the Webots 3D view and press **Space** when you are ready to continue.
5. **Trial 1:** Press Space and watch the stylus move away from the straight-elbow singularity. The scene continuously displays the current and peak commanded joint rates. At the end, record the displayed Trial 1 peak, then press Space to return the arm to the bent starting pose.
6. **Trial 2:** The robot returns to the bent start and reverses direction. Watch the elbow progressively straighten. When the condition number reaches 200, the controller pauses automatically; read the large on-scene raw and applied joint rates, then press Space to finish the approach.
7. When `[DEMONSTRATION COMPLETE]` appears, inspect the final pose and pause the simulation. No extra key press is required after Trial 2.

The controller creates `lab04_singularities/joint_rate_comparison.svg` inside the repository and prints its complete location in the Webots console. Open it after Trial 2. It plots `max |joint rate|` against active motion time, marks when Trial 2 crosses condition number 200, and shows the 3.00 rad/s simulation limit. The green Trial 1 curve should stay moderate while the red Trial 2 curve rises sharply as the singularity is approached.

The demonstration has no fixed duration because it advances only when you press Space. Reset Webots if you want to repeat it.

## What to Record

Copy these three values printed for each trial into the report:

| Quantity | What it tells you |
|---|---|
| Minimum singular value, `sigma_min` | **Larger is better.** Zero means the Jacobian is singular; a value near zero means the robot has almost lost one Cartesian motion direction. |
| Condition number, `sigma_max / sigma_min` | **Smaller is better.** A value of 1 is ideal; a large value means inverse motion is sensitive and can strongly amplify joint rates. |
| Peak commanded joint rate | **Larger means faster joint motion.** Compare it with the 3.00 rad/s Webots simulation limit. A sharp increase in Trial 2 is visible evidence of the approaching singularity. |

Paste one Webots screenshot of Trial 1 and one screenshot of Trial 2 at the condition-200 pause with the on-scene joint rate visible. Also include the generated joint-rate comparison plot.

You may optionally preview the configuration metrics without Webots:

```bash
python lab04_singularities/src/singularity_scan.py
```

This command is not a required submission.

## Explain What You Observed

Use the sequence below when interpreting the output:

1. Follow Trial 2 from its well-conditioned start to the condition-200 pause. The changing metrics establish that singularity is caused by the evolving robot configuration.
2. Compare Trial 1's moderate curve with the rising Trial 2 curve.
3. At the condition-200 checkpoint, connect the nearly straight elbow and small minimum singular value to the large on-scene joint-rate request.

The simulation limit scales an already excessive command so it can be displayed safely. It does not remove the singularity or change why the undamped inverse requests the large rate.

## Questions

Answer each question in two or three sentences.

1. What happened to the minimum singular value and condition number as Trial 2 approached the straight-elbow configuration?
2. Why did the undamped joint rate rise sharply near the end of Trial 2 even though Cartesian speed remained constant?
3. Why was it necessary to rate-limit Trial 2 instead of sending the raw undamped command directly to Webots?

## What to Submit

Submit the completed `Lab04_Report_Template.docx` containing:

- your prediction;
- the three recorded quantities for both trials;
- one screenshot from each of the two trials;
- the generated joint-rate comparison plot; and
- answers to the three questions.

No Python files or Webots world files are submitted.

## Troubleshooting

| Problem | Action |
|---|---|
| The controller does not appear in Webots | Close and reopen the world after updating the repository. |
| Webots reports that `get_from_def()` requires a Supervisor | Your work world was created from an older starter. Close it and create a fresh `lab04_work.wbt` from the updated starter; the updated UR5e has `supervisor TRUE`. |
| The robot does not move | Confirm that you created the work world from the updated starter, then reset and click Run. |
| Only one or two trials appear | Let the simulation run until `[DEMONSTRATION COMPLETE]` appears. |
| Trial 2 prints a safety scale below 1 | This is expected; it prevents the excessive raw inverse rate from exceeding the 3.00 rad/s simulation limit. |
| The red trace stops before the green target | The controller permits up to three seconds of feedback-only completion after the ten-second path request. If it still stops short, read the final console error and confirm that the updated controller is running. |
| Pressing Space does nothing | Click once inside the Webots 3D view to give it keyboard focus, then press Space again. |
| The terminal scan reports an unfinished Lab 2 function | Complete the required Lab 2 FK equations before running Lab 4. |
| The world or robot pose becomes corrupted | Close without saving and make a fresh copy of `lab04_starter.wbt`. |
