# Lab 7 - Integrated Manipulation / Final Project

## Get the Latest Course Files

Before starting the lab, save your work, close Webots, and update the course repository. Open a terminal and use the commands for your operating system.

**Windows PowerShell:**

```powershell
cd C:\eel4664-robotics-labs
git status --short
git pull
```

**macOS or Ubuntu Terminal:**

```bash
cd ~/eel4664-robotics-labs
git status --short
git pull
```

A successful update reports either `Already up to date.` or the files that Git updated.

If `git pull` reports local changes or a conflict, do not force the update or discard your work. Keep the terminal message visible and ask your instructor for help.

**Do not save over the original starter world after running the simulation. Reset/revert first, or save into a separate working copy.**

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

Unlike Labs 1-6, the Lab 7 starter intentionally does not include the course stylus. The instructor-approved gripper or grasp interface becomes the new tool. Determine and validate its fixed tool transform once, then keep that transform unchanged during the project.

## Provided Files

- `worlds/lab07_starter.wbt` - physical table/object/obstacle and visual destination bin; never overwrite it
- `controllers/diagnostic_minimal/` and `controllers/diagnostic_devices/`
- `src/collision_planner.py` - explicit collision/planning starter
- `src/COLLISION_PLANNER_NOTES.md` - modeling and reproducibility guidance
- `src/mission_sequence.py` - manipulation state-machine scaffold
- `config/`, `results/`, `report/`, and `starter_code/` placeholders
- `answers.md`

## Part 1 - Setup / Validation

1. **World:** open `worlds/lab07_starter.wbt` paused; verify `MANIPULATION_TABLE`, `PICK_OBJECT`, `TRANSPORT_OBSTACLE`, and `DESTINATION_BIN`; then immediately use **File -> Save World As...** to create `worlds/lab07_work.wbt`.
2. **Minimal controller:** run `diagnostic_minimal`.
3. **Devices:** run `diagnostic_devices` and confirm all devices required by the final controller.
4. **One joint:** command one conservative joint through the final software stack.
5. **Full algorithm:** add only instructor-approved objects and run the complete mission after stages 1-4 pass.

Record frames, home configuration, object/goal poses, obstacle geometry, limits, tolerances, and random seeds before integration.

## Part 2 - Core Implementation

1. Complete configuration and edge collision checks using link geometry derived from your FK.
2. Inflate obstacles or explicitly include a safety margin; check interpolated edges, not endpoints alone.
3. Complete a waypoint or sampling-based planner and validate every smoothing shortcut.
4. Complete `mission_sequence.py` with explicit states, completion guards, timeouts, and a safe failure state.
5. Connect your own FK/IK, Jacobian logic where useful, trajectory generator, controller, and logger.
6. Check reachability, joint/rate limits, collision clearance, and IK continuity before each segment.

Do not use Webots, MoveIt, or another package to provide the submitted kinematics, trajectory, collision, or planning solution.

## Part 3 - Robot Experiment

Execute the autonomous sequence:

1. start at home;
2. move to a collision-free pregrasp pose;
3. approach and establish the approved grasp/equivalent;
4. retreat and transport around the obstacle;
5. place/release within the target tolerance; and
6. return safely home.

First demonstrate that the assigned direct transport path collides or enters the forbidden region, then execute your planned alternative. Reset and repeat the full mission. Run one controlled variation—target pose, obstacle pose, payload/model condition, or planner seed—and preserve one informative failure.

## Part 4 - Quantitative Analysis

Report:

- task success rate across repeated runs;
- end-effector/object placement error;
- total and per-state completion time;
- joint tracking error;
- planned path length and waypoint count;
- minimum modeled obstacle clearance; and
- planning computation time.

Compare the direct and planned paths and explain the controlled variation/failure using logs. State which simulator ground-truth values were reserved for validation.

## Engineering Questions

1. Which coordinate-frame interface created the greatest integration risk?
2. How did edge resolution affect clearance and computation time?
3. What conditions trigger each state transition and safe abort?
4. What evidence demonstrates repeatability rather than one successful animation?
5. Which earlier module required the most revision, and why?
6. What would have to change for transfer to a physical arm?

## What to Submit

- proposal and architecture/state diagram;
- source code and reproducible run instructions;
- configuration, parameters, limits, tolerances, gains, and seeds;
- collision representation and planning pseudocode;
- successful video or approved live demonstration;
- raw logs, plots, and required metrics;
- repeatability and failure analysis;
- final technical report; and
- completed `answers.md`.

## Troubleshooting

If Webots repeatedly crashes, close it, use the [safe-mode recovery procedure](../docs/TROUBLESHOOTING_WEBOTS.md), and reopen the untouched starter with controller `void`. Revert a damaged starter with Git. Isolate world -> minimal controller -> devices -> one joint -> one pose -> one segment -> full mission. If planning succeeds but execution fails, separate geometry, timing, feedback, and state-transition evidence. Never debug by repeatedly overwriting the starter world.
