#!/usr/bin/env python3
import numpy as np
# Each row: (a, alpha, d, theta_offset)
UR5E_DH = [
    # TODO: six rows from the course convention
]

def dh_transform(a,alpha,d,theta):
    raise NotImplementedError

def forward_kinematics(q):
    if len(q)!=6: raise ValueError('Need six joint angles')
    if len(UR5E_DH)!=6: raise RuntimeError('Enter six DH rows')
    T=np.eye(4)
    for qi,(a,alpha,d,offset) in zip(q,UR5E_DH):
        T=T@dh_transform(a,alpha,d,qi+offset)
    return T
