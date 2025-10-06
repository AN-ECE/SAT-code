import numpy as np
import rnode_MCMC

def MCMC_SAT(CMat,var,nc,K,X,X_arr):

    N=var;
    VC=1;
    small_eps=0.00;

    # Initializing oscillator nodes and state variables
    # X=np.random.binomial(1, 0.5, N) # Uniformly generating initial state

    L = np.zeros(N, dtype=int)  # Initially all nodes have full current
    Lmax = np.max(L)  # Initially equal to 0
    Y = X.copy()  # Size is N x (Lmax+1)
    
    rate_flag = np.zeros((N, K+1), dtype=int)
    QV = np.ones((K+1, N)) / VC
    
    L = np.zeros(N, dtype=int)
    Lmax = np.max(L)
    Y = X.copy()
    TvalV = np.zeros(K+1)
    
    for i in range(1, K+1):
        Xtmp = X.copy()
        Ltmp = L.copy()
        Lmaxtmp = Lmax
        
        vtmpj, vtmp = rnode_MCMC.rnode_MCMC(N, X, small_eps, CMat, nc)
        
        q = np.zeros(N)
        for j in range(N):
            tmp = 1 / VC
            if vtmpj[j] == 0:
                rate_flag[j, i] = 1
                q[j] = QV[i-1, j]
                L[j] += 1
            else:
                q[j] = vtmpj[j] * QV[i-1, j] if L[j] > 0 else vtmpj[j]
        
        # Termination condition when all rates are 0
        if vtmp == 0:
            break
        
        QV[i, :] = q
        times = np.random.exponential(1.0 / q)
        r = np.where(rate_flag[:, i] == 0)[0]
        Tval, Ival = np.min(times[r]), np.argmin(times[r])
        
        if i == 1:
            TvalV[i] = Tval
        else:
            TvalV[i] = TvalV[i-1] + Tval
        X_temp = X
        for j in r:
            if j == r[Ival]:  # Node that switches
                L[j] = 0
                X_temp[j] = 1 - X_temp[j]  # Toggle between 0 and 1
                exists = any(np.array_equal(x, X_temp) for x in X_arr)
                if exists:
                    continue
                else :
                    X = X_temp
            else:
                L[j] += 1  # X components stay the same
        
        Lmax = np.max(L)
    
    return X, TvalV