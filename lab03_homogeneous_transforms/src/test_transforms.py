#!/usr/bin/env python3
import numpy as np
from transforms import rotx,roty,rotz,homogeneous,invert_transform

def check(R):
    assert R.shape==(3,3)
    assert np.allclose(R.T@R,np.eye(3),atol=1e-8)
    assert np.isclose(np.linalg.det(R),1.0,atol=1e-8)
for fn in (rotx,roty,rotz):
    check(fn(0.37)); assert np.allclose(fn(0),np.eye(3))
R=rotz(0.5)@roty(-0.2)
T=homogeneous(R,[0.3,-0.1,0.8])
assert np.allclose(T@invert_transform(T),np.eye(4),atol=1e-8)
print('All transformation tests passed.')
