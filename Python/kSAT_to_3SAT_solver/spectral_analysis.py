import numpy as np
from scipy.linalg import fractional_matrix_power

def spectral_analysis(A, S):
    nodes = list(range(S))
    partitions = recursive_partition(nodes, A, A, nodes)
    print(f"Size of partition: {len(partitions)}")
    return partitions

def recursive_partition(array, A, A_org, original_indices):
    if len(array) <= 50:
        return [original_indices]
    
    D = np.diag(np.sum(A, axis=1))
    disconnected_nodes = np.where(np.sum(A, axis=1) == 0)[0]
    
    if disconnected_nodes.size > 0:
        if len(disconnected_nodes) > 50:
            small_partitions = break_into_small_partitions(disconnected_nodes, 50)
        else:
            small_partitions = [disconnected_nodes.tolist()]
        small_partitions = [original_indices[i] for i in small_partitions]
        
        connected_nodes = np.setdiff1d(np.arange(len(array)), disconnected_nodes)
        if connected_nodes.size == 0:
            return small_partitions
        
        A_connected = A[np.ix_(connected_nodes, connected_nodes)]
        original_indices_connected = [original_indices[i] for i in connected_nodes]
        partitions_connected = recursive_partition(connected_nodes.tolist(), A_connected, A_org, original_indices_connected)
        
        return [small_partitions + partitions_connected]
    
    D_inv_sqrt = fractional_matrix_power(D, -0.5)  # D^(-1/2)
    L_normalized = D_inv_sqrt @ A @ D_inv_sqrt  # Matrix multiplication
    eigenvalues, eigenvectors = np.linalg.eigh(L_normalized)
    idx = np.argsort(eigenvalues)[::-1]
    eigenvectors = eigenvectors[:, idx]
    
    positive_indices = np.where(eigenvectors[:, 1] >= 0)[0]
    negative_indices = np.where(eigenvectors[:, 1] < 0)[0]
    
    Apos = [[A[i][j] for j in positive_indices] for i in positive_indices]
    Aneg = [[A[i][j] for j in negative_indices] for i in negative_indices]

    
    pos_mapped = [original_indices[i] for i in positive_indices]
    neg_mapped = [original_indices[i] for i in negative_indices]
    
    if len(neg_mapped) == 0:
        return break_into_small_partitions(pos_mapped, 50) if len(pos_mapped) > 50 else [pos_mapped]
    elif len(pos_mapped) == 0:
        return break_into_small_partitions(neg_mapped, 50) if len(neg_mapped) > 50 else [neg_mapped]
    
    partitions_left = recursive_partition(negative_indices.tolist(), Aneg, A_org, neg_mapped)
    partitions_right = recursive_partition(positive_indices.tolist(), Apos, A_org, pos_mapped)
    
    return partitions_left + partitions_right

def break_into_small_partitions(partition, max_size):
    small_partitions = []
    for i in range(0, len(partition), max_size):
        end_idx = min(i + max_size, len(partition))
        small_partitions.append(partition[i:end_idx])
    return small_partitions
    # return [partition[i:i + max_size] for i in range(0, len(partition), max_size)]

