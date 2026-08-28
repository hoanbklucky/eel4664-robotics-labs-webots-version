#!/usr/bin/env python3
"""Student starter: interpolate measured q0 to qf using Webots motors."""
import numpy as np

def interpolate(q0, qf, elapsed, duration):
    """TODO: return a smooth six-joint command with zero endpoint velocity."""
    raise NotImplementedError

# Webots adapter outline:
# robot = Robot(); motors = [...]; sensors = [...]; enable sensors
# step once; read q0; then call interpolate using robot.getTime() in one loop
# command each motor with motor.setPosition(float(q_command[i])).
