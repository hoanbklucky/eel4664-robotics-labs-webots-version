#!/usr/bin/env python3
import numpy as np
def metrics(J):
    s=np.linalg.svd(J,compute_uv=False)
    cond=np.inf if np.min(s)<1e-10 else np.max(s)/np.min(s)
    return s,cond,np.prod(s)
# TODO: scan configurations using your Jacobian
