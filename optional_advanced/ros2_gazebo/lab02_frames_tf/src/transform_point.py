#!/usr/bin/env python3
import numpy as np
T = np.eye(4)  # TODO: replace with measured transform
p_source = np.array([0.05,0.0,0.0,1.0])
print('p_target =', T @ p_source)
