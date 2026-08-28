# Instructor Notes

## Recommended module mapping

| Module | Required simulation work |
|---|---|
| 1 | Setup verification and Lab 1 - UR5e Playground |
| 2-4 | Lab 2 - UR5e devices, frames, transforms, and FK validation |
| 5-6 | Lab 3 - IK convergence, execution, and failure analysis |
| 7-8 | Lab 4 - Jacobian, differential motion, and singularities |
| 9-10 | Lab 5 - trajectory generation and tracking |
| 11-12 | Lab 6 - dynamics, control, estimation, and identification |
| 13 | Lab 7 proposal/model checkpoint |
| 14 | Lab 7 planning/control checkpoint |
| 15 | Lab 7 demonstration and report |

The schedule may overlap lab work with the corresponding analytical homework and in-class derivations.

## Before release to students

1. Test the platform-specific commands on the supported Fall 2026 Windows, macOS, and Ubuntu environments with Python 3.11 or newer and Webots R2025a.
2. Confirm all seven `*_starter.wbt` files open from a clean clone and that the shared diagnostics run in Labs 2-7.
3. Validate Lab 1 keyboard controls, reset/dance poses, target reachability, and distance feedback on all supported platforms.
4. Validate the published UR5e DH/frame convention, fixed DH-to-tool transform, target configurations, and ground-truth method for Lab 2.
5. Validate Lab 3 target poses, initial guesses, joint limits, step limits, damping, convergence tolerances, and safe execution paths.
6. Select safe Cartesian requests, conditioning thresholds, joint-rate limits, and near-singular configurations for Lab 4.
7. Validate Lab 5 MoveJ/MoveL targets, IK waypoint feasibility, straightness tolerance, trajectory limits, and logging/plotting expectations.
8. For Lab 6, verify the R2025a motor-feedback/torque interface and provide:
   - one approved baseline/changed payload or model condition; or
   - a recorded dataset fallback if safe live parameter variation is unavailable.
9. Define Lab 7 target/obstacle geometry, minimum clearance, success metrics, and the supplied gripper or approved equivalent grasp/release interface.
10. Decide whether the optional physical-arm extension is offered; simulation must remain sufficient for full credit.
11. Run the link, Python syntax, starter-world, and README-structure audits before publishing.

Do not publish instructor solutions in the public student repository.

## Preserved reference material

The former Lab 00-12 shells are archived under `optional_legacy/previous_lab_sequence/`. Use them only for provenance or to recover an omitted explanation; their numbering and submissions are superseded.
