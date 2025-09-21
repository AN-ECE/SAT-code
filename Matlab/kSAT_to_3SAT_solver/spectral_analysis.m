%Function that creates partition of variables based on spectral decomposition

% INPUT :
% A - Dependency matrix of variables
% S - The number of variables
% chip_size - Maximum number of variables in each chip

% OUTPUT : 
% partitions - Partition of variables such that each partition is <= chip_size

function partitions = spectral_analysis(A,S,chip_size)

    nodes =[1:S];
    partitions = recursive_partition(nodes,A,A,nodes,chip_size);
    fprintf("Size of partition :%d \n",size(partitions,2));
end

function partitions = recursive_partition(array,A,A_org,original_indices,chip_size)

    % Base case
    if length(array) <= chip_size
        partitions = {original_indices};
        return;
    end

    % Divide the array into two parts based on spectral method

    % Degree matrix
    D = diag(sum(A, 2));

    % Check for disconnected nodes (degree = 0)
    disconnected_nodes = find(sum(A, 2) == 0);
    if ~isempty(disconnected_nodes)

        % Treat disconnected nodes as separate partitions
        if length(disconnected_nodes) > chip_size
            % Split disconnected nodes into smaller partitions of size <=chip_size
            small_partitions = break_into_small_partitions(disconnected_nodes, chip_size);
        else
            % Treat all disconnected nodes as a single partition
            small_partitions = {disconnected_nodes};
        end
        % disp(small_partitions);

        % Map indices back to original input indices
        small_partitions = cellfun(@(x) original_indices(x), small_partitions, 'UniformOutput', false);

        connected_nodes = setdiff(1:length(array), disconnected_nodes);
        if isempty(connected_nodes)
            partitions = small_partitions;
            return; % All nodes are disconnected
        end

        % Continue partitioning the remaining graph
        A_connected = A(connected_nodes, connected_nodes);
        original_indices_connected = original_indices(connected_nodes);
        partitions_connected = recursive_partition(connected_nodes, A_connected, A_org, original_indices_connected,chip_size);

        % Combine results
        partitions = [small_partitions, partitions_connected];
        return;

    end

    % Normalized Laplacian
    % L_normalized = eye(size(A)) - D^(-1/2) * A * D^(-1/2);
    L_normalized = D^(-1/2) * A * D^(-1/2);

    [eigenvectors, eigenvalues] = eig(L_normalized);

    % Sort eigenvalues in ascending order
    [eigenvalues,pos] = sort(diag(eigenvalues),"descend");

    % Find positions of positive elements
    positive_indices = find(eigenvectors(:,pos(2)) >= 0);

    % Find positions of negative elements
    negative_indices = find(eigenvectors(:,pos(2)) < 0);


    % Ensure partitions are sorted for consistency
    positive_indices = sort(positive_indices);
    negative_indices = sort(negative_indices);

    % Extract adjacency submatrices
    Apos = A(positive_indices, positive_indices);
    Aneg = A(negative_indices, negative_indices);

    % Map indices back to original input indices
    pos_mapped = original_indices(positive_indices);
    neg_mapped = original_indices(negative_indices);



    if size(neg_mapped,2)==0
        if length(pos_mapped) > chip_size
            partitions = break_into_small_partitions(pos_mapped, chip_size);
        else
            partitions = pos_mapped;
        end
        
    elseif size(pos_mapped,2)==0
        if length(neg_mapped) > chip_size
            partitions = break_into_small_partitions(neg_mapped, chip_size);
        else
            partitions = neg_mapped;
        end
    else

        % Recursively partition each part
        partitions_left = recursive_partition(negative_indices,Aneg,A_org,neg_mapped,chip_size);
        partitions_right = recursive_partition(positive_indices,Apos,A_org,pos_mapped,chip_size);

        % Combine results
        partitions = [partitions_left, partitions_right];
    end

end

function small_partitions = break_into_small_partitions(partition, max_size)
    small_partitions = {};
    for i = 1:max_size:length(partition)
        end_idx = min(i + max_size - 1, length(partition));
        small_partitions{end + 1} = partition(i:end_idx);
    end
end