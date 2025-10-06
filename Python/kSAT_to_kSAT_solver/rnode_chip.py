import numpy as np
def rnode_chip(N, X, small_eps, Clauses, nc):
    C = nc
    vali = np.zeros(N)
    val = 0
    CMat = np.zeros((C, N))
    
    for j in range(N):
        for k in range(C):
            if j+1 in Clauses[k]:  
                CMat[k, j] = 1
            if -(j+1) in Clauses[k]:
                CMat[k, j] = -1
    
    valtmp = (CMat == -1).astype(int) @ np.ones_like(X) + CMat @ X
    val_vec = (valtmp == 0).astype(int)  
    
    for i in range(N):
        vali[i] = np.sum(val_vec[CMat[:, i] != 0]) + small_eps
    
    val = np.sum(val_vec)
    
    return vali, val