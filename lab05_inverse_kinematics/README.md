# Lab 05 ? Inverse Kinematics

## Motivation

Tool goals are Cartesian, but actuators accept joint commands; IK connects those descriptions and exposes reachability and nonuniqueness.

## Learning objectives

Derive analytical planar 2R IK; implement iterative UR5e IK from your Lab 04 FK/Jacobian; recognize unreachable and ill-conditioned targets; and validate solutions in Webots.

## Investigation

1. Complete `src/planar_ik.py`, retaining both elbow branches and checking reachability.
2. Complete `src/numerical_ik.py` with explicit pose error, convergence criterion, joint limits, and iteration limit.
3. Test multiple initial guesses for reachable, near-boundary, and unreachable targets.
4. Command converged joint solutions through the Webots motor adapter using a smooth transition.
5. Compare predicted and measured final tool poses; report iterations and residuals.

## Rule

Do not use Webots, MoveIt, SciPy, or another IK solver. General linear algebra such as NumPy SVD is allowed.

## Submission

Submit derivations, source, convergence histories, Webots evidence, failure analysis, and `answers.md`.
