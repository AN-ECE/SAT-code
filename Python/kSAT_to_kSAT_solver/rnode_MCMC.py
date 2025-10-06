"""
Function that returns the number of violated clauses for a given variable.

Parameters:
N        - Number of variables
X        - N x 1 binary vector (configuration of oscillators)
small_eps - Currently 0
CMat     - Variable by clause dependency matrix
nc       - Number of clauses

Returns:
vali - The number of violated clauses for each variable
val  - The total number of violated clauses
"""
import numpy as np

def rnode_MCMC(N, X, small_eps, CMat, nc):
    
    vali = np.zeros(N)  # Initialize violation count for each variable
    val = 0  # Total number of violations

    CMat = np.array(CMat)

    valtmp = (CMat == -1).astype(int) @ np.ones_like(X) + CMat @ X
    val_vec = (valtmp == 0).astype(int)  
    
    for i in range(N):
        vali[i] = np.sum(val_vec[CMat[:, i] != 0]) + small_eps
    
    val = np.sum(val_vec)

    return vali, val