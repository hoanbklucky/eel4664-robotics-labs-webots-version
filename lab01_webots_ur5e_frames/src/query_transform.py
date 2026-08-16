#!/usr/bin/env python3
"""Read-only tool-frame references for validating student transforms."""
from controller import Robot
import numpy as np

robot = Robot()
time_step = int(robot.getBasicTimeStep())

tool_position = robot.getDevice("tool_position")
tool_orientation = robot.getDevice("tool_orientation")
tool_test_point = robot.getDevice("tool_test_point_position")

for device in (tool_position, tool_orientation, tool_test_point):
    device.enable(time_step)

if robot.step(time_step) == -1:
    raise SystemExit("Simulation ended before validation data was available")

origin_world = np.array(tool_position.getValues(), dtype=float)
rpy_world_tool = np.array(tool_orientation.getRollPitchYaw(), dtype=float)
test_point_world = np.array(tool_test_point.getValues(), dtype=float)

print("tool origin in world [m]:", np.array2string(origin_world, precision=6))
print("tool RPY in world [rad]:", np.array2string(rpy_world_tool, precision=6))
print("test point in world [m]:", np.array2string(test_point_world, precision=6))

# TODO: construct R_world_tool = Rz(yaw) @ Ry(pitch) @ Rx(roll).
# TODO: build T_world_tool and call your transform_point implementation
#       for p_tool = np.array([0.0, 0.13, 0.0]).
# TODO: report Euclidean prediction error without a simulator transform solver.
