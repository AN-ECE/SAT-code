import k_sat_read_cnf
import read_cnf
import variable_split
import copy
import generate_cmat
import satgraph
import time
import spectral_analysis
import numpy as np
import random
import clause_split
import MCMC_small_solver
import rnode_chip
import rnode_MCMC


def chip_solver_k_sat(cnffile,cnffile_new, scheme):
    
    
    _, _, _, k_sat, _ = k_sat_read_cnf.k_sat_read_cnf(cnffile, cnffile_new, scheme)
    Clauses_k,var_k,C_k = read_cnf.read_cnf(cnffile,k_sat)
    Clauses,var,C = variable_split.variable_split(Clauses_k,var_k,k_sat,C_k)
    Clauses_org= copy.deepcopy(Clauses)
    CMat = generate_cmat.generate_cmat(Clauses, var, nc)
    CMat_org= copy.deepcopy(CMat)
    A, N = satgraph.satgraph(CMat, var)
    
    start_time = time.time()
    num_groups = 4
    partition_size = var // num_groups  # integer division
    
    # Random permutation of node indices
    rand_nodes = np.random.permutation(np.arange(1, N + 1))
    
    # Create random partitions
    node_set = []
    for i in range(num_groups):
        start = i * partition_size
        end = (i + 1) * partition_size
        node_set.append(rand_nodes[start:end])
    decomp_time = time.time() - start_time
    
    K = len(node_set)
    Clause_set, Clause_inter, clause_comm_nodes = clause_split.clause_split(node_set, K, Clauses)
    S = N
    parts = K
    half = var_k
    
    node_set = [[nodes+1 for nodes in ns] for ns in node_set]
    node_set = [sorted(ns) for ns in node_set]
    clause_comm_nodes.sort()
    
    o_node_set = [list(range(1,len(ns)+1)) for ns in node_set]
    o_clause_comm_nodes = list(range(1,len(clause_comm_nodes)+1))
    
    map_list = [list(zip(ns, o_ns)) for ns, o_ns in zip(node_set, o_node_set)]
    map_inter = list(zip(clause_comm_nodes, o_clause_comm_nodes))
    
    for k in range(parts):
        for i in range(len(Clause_set[k])):
            for j in range(len(Clause_set[k][i])):
                if Clause_set[k][i][j] < 0:
                    # Find the corresponding value from the map for negative clause
                    Clause_set[k][i][j] = -next(value[1] for value in map_list[k] if abs(Clause_set[k][i][j]) == value[0])
                else:
                    # Find the corresponding value from the map for positive clause
                    Clause_set[k][i][j] = next(value[1] for value in map_list[k] if Clause_set[k][i][j] == value[0])
    for i in range(len(Clause_inter)):
        for j in range(len(Clause_inter[i])):
            if Clause_inter[i][j] < 0:
                Clause_inter[i][j] = -next(y for x, y in map_inter if x == abs(Clause_inter[i][j]))
            else:
                Clause_inter[i][j] = next(y for x, y in map_inter if x == Clause_inter[i][j])
    
    K = 10**6
    VC = 1
    small_eps = 0.00
    X_partial = np.random.binomial(1, 0.5, half)  # Generate initial state
    X_final = np.append(X_partial,X_partial)
    vtmpb = 100
    c = 1
    time_arr = [0]*parts
    total_time = []
    unsatis_arr = [0] * 9
    flip_node_arr = [0] * 9
    X_arr = []
    sat_time=[]
    flip_time=[]
    
    
    while vtmpb != 0:
        X_sat = [None] * parts
    
        count =0
        for p in range(parts):
            X, TvalV, it = MCMC_small_solver.MCMC_small_solver(S, K, VC, small_eps, X_final, node_set, Clause_set, p)
            count = count +it
            X_sat[p] = X
            time_arr[p] = TvalV[-1]
    
        if count!=parts:
            print("STOP! Increase iterations for MCMC small solver")
            break
        
        
        for k in range(parts):
            indices = [x-1 for x, _ in map_list[k]]
            X_final[indices] = X_sat[k]
    
        X_inter = X_final[[x - 1 for x in clause_comm_nodes]]
        vtmpx, vtmpb = rnode_chip.rnode_chip(len(X_inter), X_inter, small_eps, Clause_inter, len(Clause_inter))
        _, vtmpt = rnode_chip.rnode_chip(len(X_final), X_final, small_eps, Clauses_org, len(Clauses_org))
    
        
        
        if vtmpb == 0:
            print("Solution found")
            _, vtmpt = rnode_chip.rnode_chip(len(X_final), X_final, small_eps, Clauses_org, len(Clauses_org))
            break
        
        start_flip_time = time.time()
        flip_nodes = []
        
        cl_matrix = np.zeros((half, S))
        cl_unsatis = np.zeros(half)
        
        for i in range(half):
            X_temp = X_final.copy()
            X_temp[i] = 1 - X_temp[i]  # Flip bit
            X_temp[half+i] = X_temp[i]
            cl_matrix[i, :], cl_unsatis[i] = rnode_MCMC.rnode_MCMC(S, X_temp, small_eps, CMat_org, len(Clauses_org))
    
        unsatis_arr.append(vtmpt)
        flip_nodes = [i for i in range(half) if cl_unsatis[i] < vtmpt]
        
        flip_node_arr.append(flip_nodes)
        flip_node_arr = flip_node_arr[-10:]
    
    
        if all(np.array_equal(x, flip_node_arr[0]) for x in flip_node_arr) or all(unsatis_arr[-5:] == unsatis_arr[-1]):
            X_partial = np.random.binomial(1, 0.5, half)
            X_final = np.append(X_partial,X_partial)
            continue
        
        if not flip_nodes:
            equal = [i for i in range(half) if cl_unsatis[i] == vtmpt]
            if equal:
                new_flip_nodes = set(equal)
                for i in equal:
                    I_minus = np.where(cl_matrix[i, :i] > 0)[0].tolist() + np.where(cl_matrix[i, i+1:] > 0)[0].tolist()
                    new_flip_nodes.update(I_minus)
                flip_nodes = np.random.choice(list(new_flip_nodes), size=len(new_flip_nodes)//2, replace=False).tolist()
            else:
                X_partial = np.random.binomial(1, 0.5, half)
                X_final = np.append(X_partial,X_partial)
                continue
    
        flip_nodes = np.unique([x for x in flip_nodes if x < S])  # Only flip in first S
        X_final[flip_nodes] = 1 - X_final[flip_nodes]
        X_final[half + flip_nodes] = X_final[flip_nodes];
    
        # Check if X_final already exists in X_arr (a list of NumPy arrays)
        exists = any(np.array_equal(x, X_final) for x in X_arr)
        
        
        # Keep generating a new X_final until it is unique
        if exists:
            X_final = np.random.binomial(1, 0.5, S)  # Generate again
            exists = any(np.array_equal(x, X_final) for x in X_arr)
            
        
        X_arr.append(X_final)
        X_arr= copy.deepcopy(X_arr)
        flip_time.append(time.time() - start_flip_time)
        
        
        
        sat_time.append(max(time_arr))
        total_time.append(sat_time[-1] + flip_time[-1])
        c += 1

    return X_final,sat_time,flip_time,total_time

