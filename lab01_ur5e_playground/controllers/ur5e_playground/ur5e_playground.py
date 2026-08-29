#!/usr/bin/env python3
"""Keyboard playground for a first, math-free UR5e experience."""

from controller import Keyboard, Robot
import math


JOINT_NAMES = (
    "shoulder_pan_joint",
    "shoulder_lift_joint",
    "elbow_joint",
    "wrist_1_joint",
    "wrist_2_joint",
    "wrist_3_joint",
)

HOME = [0.0, -1.20, 1.20, -1.50, -1.57, 0.0]
DANCE_POSES = (
    HOME,
    [0.35, -0.90, 1.05, -1.25, -1.10, 0.35],
    [-0.30, -1.05, 1.30, -1.55, -1.75, -0.35],
    [0.20, -0.75, 0.90, -1.10, -0.75, 0.65],
    HOME,
)
TARGETS = {
    "blue": (0.42, -0.30, 0.48),
    "green": (0.15, -0.52, 0.62),
    "magenta": (-0.28, -0.35, 0.52),
}
TARGET_RADIUS = 0.10
JOINT_STEP = 0.04


def print_help():
    print("\n=== UR5e PLAYGROUND ===")
    print("1-6: select joint | UP/DOWN: move selected joint")
    print("R: safe reset | D: start dance | S: stop dance")
    print("P: print pose | H: help")
    print("Click the 3D view if Webots is not receiving your keys.\n")


def distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


robot = Robot()
time_step = int(robot.getBasicTimeStep())
keyboard = robot.getKeyboard()
keyboard.enable(time_step)

# Connect the ordered motor and joint-sensor devices.
motors = [robot.getDevice(name) for name in JOINT_NAMES]
sensors = [robot.getDevice(f"{name}_sensor") for name in JOINT_NAMES]
for motor in motors:
    motor.setVelocity(min(0.65, motor.getMaxVelocity()))
for sensor in sensors:
    sensor.enable(time_step)

tool_tip = robot.getDevice("tool_test_point_position")
tool_tip.enable(time_step)

q_command = HOME.copy()
selected = 0
dance_active = False
dance_index = 0
dance_switch_time = 0.0
reached = set()

for motor, target in zip(motors, q_command):
    motor.setPosition(target)

print_help()
print("Selected joint 1:", JOINT_NAMES[selected])

# The controller repeats: update automatic actions, process keys, send joint
# targets, and check whether the stylus has reached a target bubble.
while robot.step(time_step) != -1:
    now = robot.getTime()

    if dance_active and now >= dance_switch_time:
        q_command = list(DANCE_POSES[dance_index])
        dance_index += 1
        dance_switch_time = now + 2.8
        if dance_index >= len(DANCE_POSES):
            dance_active = False
            dance_index = 0
            print("[DANCE COMPLETE] Your turn again.")

    # Read and process every keyboard event currently waiting in the queue.
    key = keyboard.getKey()
    while key != -1:
        if ord("1") <= key <= ord("6"):
            selected = key - ord("1")
            print(f"Selected joint {selected + 1}: {JOINT_NAMES[selected]}")
        elif key == Keyboard.UP or key == Keyboard.DOWN:
            if dance_active:
                q_command = [sensor.getValue() for sensor in sensors]
                dance_active = False
                dance_index = 0
                print("[DANCE] Stopped by manual joint control.")
            direction = 1.0 if key == Keyboard.UP else -1.0
            proposed = q_command[selected] + direction * JOINT_STEP
            lower = motors[selected].getMinPosition()
            upper = motors[selected].getMaxPosition()
            if math.isfinite(lower):
                proposed = max(proposed, lower)
            if math.isfinite(upper):
                proposed = min(proposed, upper)
            q_command[selected] = proposed
        elif key in (ord("R"), ord("r")):
            q_command = HOME.copy()
            dance_active = False
            print("[RESET] Returning to the safe exploration pose.")
        elif key in (ord("D"), ord("d")):
            # D is intentionally idempotent. Keyboard auto-repeat can enqueue
            # several events for one physical press, so toggling here would
            # sometimes start and immediately stop the dance.
            if not dance_active:
                dance_active = True
                dance_index = 0
                dance_switch_time = now
                print("[DANCE] Started. Press S to stop.")
        elif key in (ord("S"), ord("s")):
            if dance_active:
                q_command = [sensor.getValue() for sensor in sensors]
                dance_active = False
                dance_index = 0
                print("[DANCE] Stopped and holding the current pose.")
        elif key in (ord("P"), ord("p")):
            q_measured = [sensor.getValue() for sensor in sensors]
            tip = tool_tip.getValues()
            print("q [rad] = [" + ", ".join(f"{value:.4f}" for value in q_measured) + "]")
            print("stylus tip [m] = [" + ", ".join(f"{value:.4f}" for value in tip) + "]")
            print("target distances [m] = " + ", ".join(
                f"{name}: {distance(tip, point):.3f}" for name, point in TARGETS.items()
            ))
        elif key in (ord("H"), ord("h")):
            print_help()
        key = keyboard.getKey()

    # Send the current six-angle command to the six joint motors.
    for motor, target in zip(motors, q_command):
        motor.setPosition(target)

    # Give visual exploration a simple quantitative success signal.
    tip = tool_tip.getValues()
    for name, point in TARGETS.items():
        if name not in reached and distance(tip, point) <= TARGET_RADIUS:
            reached.add(name)
            print(f"[TARGET REACHED] {name.upper()}! Reached {len(reached)} of {len(TARGETS)}.")
