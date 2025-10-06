import numpy as np

def satgraph(CMat, var):
    A = [[0]*var for _ in range(var)]
        
    for i in range(var):
        cp = [r for r, row in enumerate(CMat) if row[i] != 0]
        if len(cp) == 0:
            continue
        else:
            for j in cp:
                rp = [idx for idx, val in enumerate(CMat[j]) if val != 0] 
                for k in rp:
                    if k > i:
                        A[i][k] = 1
                        A[k][i] = 1
    return A, var