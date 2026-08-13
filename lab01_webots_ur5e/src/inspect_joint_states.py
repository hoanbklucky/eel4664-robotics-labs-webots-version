#!/usr/bin/env python3
"""Copy into a Webots controller directory and complete the sampling loop."""
from controller import Robot
import numpy as np

JOINT_NAMES = ("shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint",
               "wrist_1_joint", "wrist_2_joint", "wrist_3_joint")
robot = Robot()
time_step = int(robot.getBasicTimeStep())
sensors = [robot.getDevice(f"{name}_sensor") for name in JOINT_NAMES]
for sensor in sensors:
    sensor.enable(time_step)

while robot.step(time_step) != -1:
    q = np.array([sensor.getValue() for sensor in sensors])
    # TODO: append robot.getTime() and q to a CSV file at a sensible rate.
    print(f"t={robot.getTime():.3f}, q={np.array2string(q, precision=4)}")
