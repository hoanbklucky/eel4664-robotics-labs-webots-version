# Lab 7 - Integrated Manipulation / Final Project

## Get the Latest Course Files

Before starting, save your work and close Webots. Follow [Updating the Course Repository](../docs/UPDATE_REPOSITORY.md). Do not force an update or discard local work when Git reports a conflict.

## Mission

Complete an autonomous pick-and-place challenge.

### Why integrate the system in Webots?

A real pick-and-place task combines kinematics, planning, collision checking, trajectory execution, feedback, and safe recovery. Webots lets you test that complete chain against a physical scene before risking a robot, tool, or nearby object.

Success means more than watching one animation complete: the robot must reach measured pose tolerances, maintain clearance, handle failures safely, and repeat the task from Reset. This is the same evidence-driven validation expected before transferring a system to hardware.

## Success Criteria

You succeed when the robot autonomously completes home -> pregrasp -> grasp (or approved equivalent) -> obstacle-avoiding transport -> place -> home, satisfies stated joint/collision/pose tolerances, and repeats the task from Reset with quantitative evidence and a documented failure boundary.

## Learning Objectives

By the end of this project, you should be able to:

1. integrate transforms, FK/IK, Jacobians, trajectories, feedback, and estimation;
2. implement explicit collision checking and motion planning;
3. organize a manipulation task as auditable states with safe failure handling;
4. evaluate repeatability, clearance, task error, and completion time; and
5. communicate architecture, assumptions, evidence, limitations, and transfer risks.

## Prerequisites

Complete Labs 1-6 and the [setup prerequisites](../lab00_setup/README.md). Reuse tested mathematical modules rather than hiding them inside a monolithic controller. A physical robot extension is optional; successful Webots completion satisfies the required project.


**Platform note:** The required workflow supports Windows, macOS, and Ubuntu when configured through Lab 00. Terminal examples use `python`; on macOS or Ubuntu, use `python3` instead if `python` is not recognized.

## Background

The task combines the course pipeline: frame reasoning locates targets, FK/IK generates configurations, collision checks reject unsafe states/edges, trajectories time-parameterize the path, and feedback executes it. Webots supplies simulated devices, physics, and visualization; it must not replace submitted transformations, kinematics, Jacobian calculations, trajectory generation, collision predicates, planning, control, or evaluation.

The starter provides a default physical `PICK_OBJECT`, physical `TRANSPORT_OBSTACLE`, `MANIPULATION_TABLE`, and visual `DESTINATION_BIN`. The instructor will provide or approve a gripper or equivalent grasp interface and may approve controlled scene variations. If no gripper is provided, an approved attachment/contact proxy may mark grasp and release while the student implementation still controls approach, transport, and placement.

For a concepts-first explanation of interfaces, state machines, edge checking, safe aborts, and repeatability, read [Lab 7 Optional Integration Guide](OPTIONAL_BACKGROUND.md).

Unlike Labs 1-6, the Lab 7 starter intentionally does not include the course stylus. The instructor-approved gripper or grasp interface becomes the new tool. Determine and validate its fixed tool transform once, then keep that transform unchanged during the project.

## Provided Files

- `worlds/lab07_starter.wbt` - physical table/object/obstacle and visual destination bin; never overwrite it
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/collision_planner.py` - explicit collision/planning starter
- `src/COLLISION_PLANNER_NOTES.md` - modeling and reproducibility guidance
- `src/mission_sequence.py` - manipulation state-machine scaffold
- `config/`, `results/`, `report/`, and `starter_code/` placeholders
- `Lab07_Report_Template.docx`



## Open the Word report template

Follow [Opening a Word Report Template](../docs/OPEN_WORD_REPORT.md) and create a personal copy of `Lab07_Report_Template.docx` before entering results.

## Part 1 - Setup / Validation

> **Why this part matters:** Recording frames, geometry, limits, devices, and seeds before integration creates a reproducible foundation for debugging a multi-stage autonomous mission.

1. **World:** open `worlds/lab07_starter.wbt` paused; verify `MANIPULATION_TABLE`, `PICK_OBJECT`, `TRANSPORT_OBSTACLE`, and `DESTINATION_BIN`; then immediately use **File -> Save World As...** to create `worlds/lab07_work.wbt`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm all devices required by the final controller.
4. **One joint:** command one conservative joint through the final software stack.
5. **Full algorithm:** add only instructor-approved objects and run the complete mission after stages 1-4 pass.

Record frames, home configuration, object/goal poses, obstacle geometry, limits, tolerances, and random seeds before integration.

## Part 2 - Core Implementation

> **Why this part matters:** The final project should integrate course concepts through explicit interfaces. Generic edge sampling, plan validation, state sequencing, timeout handling, and safe-abort mechanics are supplied so students can focus on project-specific decisions.

1. Define link segments from your tested FK and the project obstacle representation.
2. Supply the collision predicate used by the provided configuration and edge checkers.
3. Choose and justify candidate waypoint configurations; the provided planner tests the direct path and each one-waypoint alternative.
4. Define the state-completion, failure, timeout, and entry-action callbacks used by `mission_sequence.py`.
5. Connect your own FK/IK, trajectory generator, controller, and logger through these interfaces.
6. Validate reachability, limits, clearance, IK continuity, and trajectory limits before each segment.

Read the supplied helpers before integrating them. Do not rewrite generic interpolation or state-transition mechanics unless your approved project requires a documented extension. Do not use Webots, MoveIt, or another package to replace the submitted kinematics or collision model.

## Part 3 - Robot Experiment

> **Why this part matters:** A complete pick-transport-place run demonstrates that the separate course algorithms can cooperate safely, recoverably, and autonomously around an obstacle.

Execute the autonomous sequence:

1. start at home;
2. move to a collision-free pregrasp pose;
3. approach and establish the approved grasp/equivalent;
4. retreat and transport around the obstacle;
5. place/release within the target tolerance; and
6. return safely home.

First demonstrate that the assigned direct transport path collides or enters the forbidden region, then execute your planned alternative. Reset and repeat the full mission. Run one controlled variation—target pose, obstacle pose, payload/model condition, or planner seed—and preserve one informative failure.

## Part 4 - Quantitative Analysis

> **Why this part matters:** Success rate, placement error, clearance, path length, tracking, and timing provide evidence of reliable manipulation rather than one fortunate demonstration.

Report:

- task success rate across repeated runs;
- end-effector/object placement error;
- total and per-state completion time;
- joint tracking error;
- planned path length and waypoint count;
- minimum modeled obstacle clearance; and
- planning computation time.

Compare the direct and planned paths and explain the controlled variation/failure using logs. State which simulator ground-truth values were reserved for validation.

## Engineering Question

Answer in one short paragraph.

What evidence shows that your integrated system is repeatable and handles an unsafe or failed condition deliberately, rather than succeeding once by chance?

## What to Submit

1. Proposal and architecture/state diagram.
2. Source code and reproducible run instructions.
3. Completed `Lab07_Report_Template.docx` containing configuration and limits, successful-run evidence and metrics, repeatability and one failure analysis, and the Engineering Question response.
4. Successful video or approved live demonstration.

Do not submit `lab07_work.wbt`, vendor assets, or caches unless requested.

## Troubleshooting

If Webots repeatedly crashes, close it, use the [safe-mode recovery procedure](../docs/TROUBLESHOOTING_WEBOTS.md), and reopen the untouched starter with controller `void`. Revert a damaged starter with Git. Isolate world -> minimal controller -> devices -> one joint -> one pose -> one segment -> full mission. If planning succeeds but execution fails, separate geometry, timing, feedback, and state-transition evidence. Never debug by repeatedly overwriting the starter world.
