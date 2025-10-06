def generate_cmat(Clauses, var, nc):
    # Assign number of clauses and number of variables from input parameters
    C = nc
    N = var

    # Initialize CMat matrix with zeros of size (C x N)
    CMat = [[0] * N for _ in range(C)]
    for j in range(1,N+1):
        for k in range(C):
            if j in Clauses[k]:
                CMat[k][j-1] = 1
            if -j in Clauses[k]:
                CMat[k][j-1] = -1
    return CMat