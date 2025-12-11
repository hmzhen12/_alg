import math
import numpy as np
from numpy.linalg import norm

np.set_printoptions(precision=4)

def df(f, p, k, step=0.01):
    p1 = p.copy()
    p1[k] = p[k]+step
    return (f(p1) - f(p)) / step

def grad(f, p, step=0.01):
    gp = p.copy()
    for k in range(len(p)):
        gp[k] = df(f, p, k, step)
    return gp

def gradientDescendent(f, p0, step=0.01, max_loops=100000, dump_period=1000):
    p = p0.copy()
    fp0 = f(p)
    for i in range(max_loops):
        fp = f(p)
        gp = grad(f, p) 
        glen = norm(gp) 
        if i%dump_period == 0: 
            print('{:05d}:f(p)={:.3f} p={:s} gp={:s} glen={:.5f}'.format(i, fp, str(p), str(gp), glen))
        if glen < 0.00001: 
            break
        gstep = np.multiply(gp, -1*step) 
        p +=  gstep 
        fp0 = fp
    print('{:05d}:f(p)={:.3f} p={:s} gp={:s} glen={:.5f}'.format(i, fp, str(p), str(gp), glen))
    return p # 傳回最低點！
