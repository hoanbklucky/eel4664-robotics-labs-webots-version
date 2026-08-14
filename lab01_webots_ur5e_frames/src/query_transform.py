#!/usr/bin/env python3
"""Webots ground-truth adapter for validating student-computed transforms."""
from controller import Supervisor
import numpy as np

supervisor = Supervisor()
time_step = int(supervisor.getBasicTimeStep())
# TODO: assign DEF names in a copied world and retrieve nodes with getFromDef().
# TODO: read getPosition() and getOrientation(); never use these values to solve FK.
while supervisor.step(time_step) != -1:
    print("TODO: print measured reference transform")
    break
