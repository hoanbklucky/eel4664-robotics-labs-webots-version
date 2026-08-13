#!/usr/bin/env python3
import numpy as np
def numerical_jacobian(fk_position_fn,q,eps=1e-6):
    q=np.asarray(q,dtype=float); p0=np.asarray(fk_position_fn(q),dtype=float)
    J=np.zeros((len(p0),len(q)))
    for i in range(len(q)):
        qp=q.copy(); qp[i]+=eps; J[:,i]=(np.asarray(fk_position_fn(qp))-p0)/eps
    return J
def analytic_jacobian(q):
    raise NotImplementedError
