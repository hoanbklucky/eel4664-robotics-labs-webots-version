#!/usr/bin/env python3
import numpy as np

def planar_3r_fk(q,lengths):
    """Return [x,y,phi]. TODO."""
    raise NotImplementedError

if __name__=='__main__':
    print(planar_3r_fk(np.deg2rad([20,-30,15]),[0.5,0.4,0.2]))
