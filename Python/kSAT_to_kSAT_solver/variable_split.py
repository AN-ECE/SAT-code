import numpy as np

def variable_split(Clauses, var, k_sat, C):
    
    v = var
    for i in range(1, var + 1):
        row = np.where(np.abs(Clauses) == i)[0]
        v1 = i
        
        second = row[len(row) // 2:]
        cl_s = [Clauses[i] for i in second.tolist()]
        
        v2 = v + i
        cl_s = [[v2 if item == i else item for item in row] for row in cl_s]
        cl_s = [[-v2 if item == -i else item for item in row] for row in cl_s]
    
        for j in range(len(second)):
            Clauses[second[j]] = cl_s[j]
    
        Clauses = np.vstack([Clauses, [v1, -v2] + [-v2] * (k_sat - 2)])
        Clauses = np.vstack([Clauses, [-v1, v2] + [v2] * (k_sat - 2)])
        C += 2
    
    var = v + i
    C = Clauses.shape[0]
    
    return Clauses, var, C