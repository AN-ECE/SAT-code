import numpy as np

def compute_vars(X_ini, var, varo, Clauses, C, k_sat, Clauses_d):
    va = np.zeros(var)  # Initialize va with zeros
    
    extra_per_cl = k_sat - 2
    extra_per_var = k_sat - 3

    for i in range(0, len(Clauses_d), extra_per_cl):
        Cl_rows = Clauses_d[i:min(i + extra_per_cl, len(Clauses_d))]

        Cl_rows = np.array(Cl_rows)  # Convert list to NumPy array
        chunk = np.unique(np.abs(Cl_rows[np.abs(Cl_rows) > varo]))
        
        row = np.any(np.abs(Cl_rows) <= varo, axis=1)
        mat = Cl_rows[row, :]
        pos = mat[np.abs(mat) <= varo]
        
        elem = pos < 0
        X = X_ini[np.abs(pos)-1]
        X[elem] = 1 - X[elem]  # Flip bits for negative elements

        l = k_sat
        v = np.zeros(l - 3)  # Initialize v variables

        # Determine v1 based on z1 and z2
        if X[0] == 1 or X[1] == 1:
            v[0] = 0  # v1 can be 0 or 1, choosing 0
        else:
            v[0] = 1

        # Propagate values for intermediate v_j
        for j in range(1, l - 3):
            if X[j + 1] == 1 or not v[j - 1] == 1:
                v[j] = 0
            else:
                v[j] = 1

        # Ensure the last clause is satisfied
        if X[l - 2] == 1 or X[l - 1] == 1:
            pass  # Clause C_{k-2} is already satisfied
        else:
            v[l - 4] = 0  # Adjust v_{k-3} if needed

        va[chunk.astype(int)-1] = v  # Assign values to va

    return va
