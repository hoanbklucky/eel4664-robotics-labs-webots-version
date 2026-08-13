"""Thin Webots device adapter; course algorithms belong outside this module."""
import numpy as np

JOINT_NAMES = (
    "shoulder_pan_joint", "shoulder_lift_joint", "elbow_joint",
    "wrist_1_joint", "wrist_2_joint", "wrist_3_joint",
)

class UR5eDevices:
    """Expose ordered motors and sensors without supplying robotics algorithms."""
    def __init__(self, robot):
        self.robot = robot
        self.time_step = int(robot.getBasicTimeStep())
        self.motors = [robot.getDevice(name) for name in JOINT_NAMES]
        self.sensors = [robot.getDevice(f"{name}_sensor") for name in JOINT_NAMES]
        for sensor in self.sensors:
            sensor.enable(self.time_step)
        self.tool_position = robot.getDevice("tool_position")
        self.tool_orientation = robot.getDevice("tool_orientation")
        self.tool_position.enable(self.time_step)
        self.tool_orientation.enable(self.time_step)

    def positions(self):
        return np.array([sensor.getValue() for sensor in self.sensors], dtype=float)

    def command_positions(self, q):
        q = np.asarray(q, dtype=float)
        if q.shape != (6,) or not np.all(np.isfinite(q)):
            raise ValueError("Expected six finite joint positions")
        for motor, target in zip(self.motors, q):
            motor.setPosition(float(target))

    def measured_tool_pose(self):
        """Return ground truth for validation, never for solving FK or IK."""
        return (np.array(self.tool_position.getValues(), dtype=float),
                np.array(self.tool_orientation.getRollPitchYaw(), dtype=float))
