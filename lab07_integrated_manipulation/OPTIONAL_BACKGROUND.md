# Lab 7 Optional Integration Guide

This guide explains the systems ideas behind the final project. It does not prescribe one planner or grasp strategy; it shows how to connect independently tested modules into a repeatable and diagnosable mission.

Return to the [Lab 7 instructions](README.md) when you are ready to implement the project.

## 1. Integration succeeds through explicit interfaces

Each module should have a clear input, output, frame convention, units, and failure result.

```text
target pose -> IK -> candidate joint configuration
joint path + obstacles -> collision checker -> safe or unsafe
safe path + duration -> trajectory generator -> timed references
references + measurements -> controller -> actuator commands
```

A module should report failure rather than silently returning an unsafe or discontinuous result.

## 2. A state machine makes mission progress visible

A state machine divides the task into named stages such as home, pregrasp, grasp, transport, place, and return home. Each state needs:

- an entry action;
- a completion condition;
- a timeout;
- an expected observation; and
- a safe failure transition.

Do not advance merely because a fixed amount of wall-clock time passed. Use Webots simulation time and verify the relevant pose, contact, attachment, or tolerance.

## 3. Check edges, not only endpoints

Two collision-free joint configurations do not guarantee a collision-free motion between them. Sample the connecting edge at a stated joint-space resolution and check every sample.

Smaller spacing detects narrower collision regions but requires more FK and collision evaluations. Resolution is therefore an accuracy-versus-computation choice that must be reported.

## 4. Plan first, then execute

Before commanding a segment, verify:

1. IK convergence and joint limits;
2. branch continuity with the previous configuration;
3. collision clearance along every edge;
4. trajectory position, velocity, and acceleration limits; and
5. a safe stopping or retreat action.

Planning and execution should remain separate. A controller should not discover that a segment is invalid only after motion begins.

## 5. A safe abort is a designed outcome

`SAFE_ABORT` is not a software crash. It is an intentional state entered when a timeout, failed IK solve, unsafe edge, lost grasp, excessive tracking error, or limit violation occurs.

A useful abort records the state, time, reason, measured configuration, and planned recovery. It then stops or moves to an instructor-approved safe hold without continuing the mission.

## 6. Repeatability is stronger evidence than one animation

One successful run may be fortunate. Repeatability requires several reset-state trials with the same configuration and documented seeds. Report success rate, placement error, minimum clearance, tracking error, and completion time.

Also preserve one controlled failure. A well-designed system should explain why it failed and enter a safe state rather than producing unexplained motion.

## 7. Debug one interface at a time

```text
world and devices
    -> measured frames
    -> FK prediction
    -> IK solution
    -> collision-free path
    -> timed trajectory
    -> controller tracking
    -> state transition
```

Log the input and output of the first failing boundary. This is faster and safer than changing several modules simultaneously.
