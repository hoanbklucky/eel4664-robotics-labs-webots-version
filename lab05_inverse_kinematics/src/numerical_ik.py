#!/usr/bin/env python3
import numpy as np
def numerical_ik(fk_fn,jacobian_fn,q0,target,alpha=0.2,tol=1e-4,max_iter=500):
    q=np.asarray(q0,dtype=float).copy()
    for k in range(max_iter):
        # TODO: compute task-space error and pseudoinverse update
        pass
    raise RuntimeError('IK did not converge')
