# Lab 2 Answers

## Step 1 - Setup and Safety Check

| Check | Pass? | Evidence or error message |
|---|---|---|
| Lab 1 transforms and FK import | | |
| protected world opens | | |
| minimal controller | | |
| device-listing controller | | |
| one-joint motion | | |

## Step 2 - Planar IK

State the link lengths and targets used. Record both branches for the interior target and verify each with planar FK.

| Case | Target `[x, y]` | Returned `q` [rad] | Reconstructed `[x, y]` | Error | Result |
|---|---|---|---|---:|---|
| interior, branch 1 | | | | | |
| interior, branch 2 | | | | | |
| boundary | | | | | |
| unreachable | | | | | expected `ValueError` |

Explain what distinguishes the two branches physically.

## Step 3 - Pose Error and Finite-Difference Jacobian

State the frame used for rotational error and record the identity, translation-sign, rotation-sign, shape, and finite-value test results.

| Finite-difference `h` [rad] | Comparison result or change from previous `h` |
|---:|---|
| `1e-3` | |
| `1e-4` | |
| `1e-5` | |
| `1e-6` | |

Selected `h` and justification:

## Step 4 - Numerical IK Configuration

| Parameter | Value used |
|---|---:|
| `alpha` | |
| damping | |
| maximum joint step | |
| position tolerance | |
| orientation tolerance | |
| maximum iterations | |
| lower/upper joint limits | |

List every explicit solver failure guard and explain why success requires both tolerances.

## Step 5 - Target, Seed, and Failure Results

Record the one fixed `T_6_tool` reused from Lab 1 and confirm that `fk_tool(q) = forward_kinematics(q) @ T_6_tool` was used without recalibration.

| Target | Seed | Converged? | Reason | Iterations | Position residual | Orientation residual | Final `q` | Distance from seed | Accepted? |
|---|---|---|---|---:|---:|---:|---|---:|---|
| A | Reset | | | | | | | | |
| A | zero | | | | | | | | |
| A | nonsymmetric | | | | | | | | |
| B | Reset | | | | | | | | |
| B | zero | | | | | | | | |
| B | nonsymmetric | | | | | | | | |
| unreachable | assigned | | | | | | | | no |

Attach residual-history plots for a fast run, a slower or different-seed run, and the unreachable run. State why the selected Target A and B solutions are safe to execute.

## Steps 6-7 - Webots Execution

Record the stationary import check before enabling motion:

- finite 4-by-4 tool pose printed:
- robot remained stationary:

Then record the printed safety decision and execution results:

| Target | Trial | Selected `q_goal` | Measured final `q` | Motion completed safely? |
|---|---:|---|---|---|
| A | 1 | | | |
| A | 2 | | | |
| B | 1 | | | |
| B | 2 | | | |

Note any visible difference between the two motions or repeated trials.

## Step 8 - Three-Layer Error Analysis

Report position errors in millimeters and orientation errors in degrees.

| Target | Trial | Solver position | Solver orientation | Measured-joint position | Measured-joint orientation | Webots position | Webots orientation |
|---|---:|---:|---:|---:|---:|---:|---:|
| A | 1 | | | | | | |
| A | 2 | | | | | | |
| B | 1 | | | | | | |
| B | 2 | | | | | | |

Identify the dominant error layer and support the conclusion with the table. Compare the seed-dependent solutions and state whether they represent the same or different IK branches.

## Engineering Questions

Answer the seven Engineering Questions in the Lab 2 README.