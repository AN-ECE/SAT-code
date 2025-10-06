import numpy as np

def clause_split(V_k_hat, K, Clauses):
    sets = {} 
    all_union = np.unique(np.concatenate(V_k_hat)).tolist()
    for i in range(K):
        ind_set = []
        V_i = V_k_hat[i]
        V_union = [x for x in all_union if x not in V_i]
        
        # Convert V_i and V_union to sets for membership testing
        V_i_set = [x for x in V_i]
        V_union_set = [x for x in V_union]
        
        for s1 in range(len(Clauses)):
            s2 = np.abs(Clauses[s1])
            if all(x-1 in V_i_set for x in s2) and not all(x-1 in V_union_set for x in s2):
                ind_set.append(s1)
    
        sets[i] = ind_set
        
    all_clauses_ind = sorted(set(x for sublist in sets.values() for x in sublist))
    clause_com_num = [i for i in range(len(Clauses)) if i not in all_clauses_ind]
    
    Clause_set = {key: [Clauses[i] for i in indices] for key, indices in sets.items()}
    Clause_inter = [Clauses[i] for i in clause_com_num]
    clause_comm_nodes = sorted(np.unique(np.abs(Clause_inter)).tolist())

    return Clause_set,Clause_inter,clause_comm_nodes