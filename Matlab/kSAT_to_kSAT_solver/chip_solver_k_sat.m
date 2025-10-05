% Function that accepts the smaller splits of the problem and returns the
% SAT solution of the big problem


% INPUT :
% cnffile - Path to the original cnf
% cnffile_new - Path to be provided if the problem is not 3-SAT and does not want to dump the reduced 3-SAT, can pass empty string in such case
% scheme - Scheme to be decided according to user choice, but currently fixed to 1


%Output : 
% X_final : The final SAT states for all the variables 
% sat_time : Array to store the max time to reach sat solution for chip1
% and chip2 for an initial X
% flip_time : Array to store flipping time of the nodes based on k1 and k2 of the
% algorithm for an initial X 
% total_time : Array to store the total time to reach a SAT solution for
% the larger problem



cnffile = '';

scheme =1;
cnffile_new='';

[~,~,~,~,k_sat,~]= k_sat_read_cnf(cnffile,cnffile_new,scheme);
[Clauses_k,var_k,C_k]= read_cnf(cnffile,k_sat);
[Clauses,var,C]=variable_split(Clauses_k,var_k,k_sat,C_k);
% [CMat]=generate_cmat(Clauses,var,C);
% [~,N]=satgraph(CMat,var);

X_final = ones(var,1);
small_eps=0.00;


tic;

num_groups = 5;
partition_size = var / num_groups;

% Random permutation of node indices
rand_nodes = randperm(var);

% Create random partitions
node_set = cell(1, num_groups);
for i = 1:num_groups
    idx = (i-1)*partition_size + 1 : i*partition_size;
    node_set{i} = rand_nodes(idx);
end

half = var_k;
decomp_time =toc;
% [node_set] = test_division(N);
K = size(node_set,2);

[Clause_set,Clause_inter,clause_comm_nodes] = clause_split(node_set,K,Clauses);
S= var;
parts = K;


node_set = cellfun(@sort, node_set, 'UniformOutput', false);
clause_comm_nodes = sort(clause_comm_nodes);


o_node_set = cellfun(@(x) [1:length(x)],node_set,'UniformOutput',false);
o_clause_comm_nodes = 1:size(clause_comm_nodes,2);

map = cellfun(@(x, y) [x', y'], node_set, o_node_set, 'UniformOutput', false);
map_inter = [clause_comm_nodes', o_clause_comm_nodes'];

Clause_set_org = Clause_set;
Clause_inter_org = Clause_inter;

for k=1:parts
    [rows, cols] = size(Clause_set{k});
    for i = 1:rows
        for j = 1:cols
            if Clause_set{k}(i,j)<0
                Clause_set{k}(i,j)=-map{k}(find(map{k}(:, 1) == abs(Clause_set{k}(i,j))),2);
            else
                Clause_set{k}(i,j)=map{k}(find(map{k}(:, 1) == Clause_set{k}(i,j)),2);
            end
        end
    end
end


[rows, cols] = size(Clause_inter);
for i = 1:rows
    for j = 1:cols
        if Clause_inter(i,j)<0
            Clause_inter(i,j)=-map_inter(find(map_inter(:, 1) == abs(Clause_inter(i,j))),2);
        else
            Clause_inter(i,j)=map_inter(find(map_inter(:, 1) == Clause_inter(i,j)),2);
        end
    end
end


K=10^7;
VC=1;
small_eps=0.00;
X_partial = binornd(ones(half,1), 0.5);  % Uniformly generating initial state
X_final = [X_partial; X_partial];
X_ini = X_final;
vtmpb=100;
c=1;
time=zeros(1,parts);
total_time=[];
unsatis_arr=[0,0,0,0,0,0,0,0,0];
flip_node_arr=cell(1,10);
vtmptn_arr=[];
X_arr={};

iter ={};

% Simulating for K jumps
while(vtmpb~=0)


    X_sat=cell(1,parts);
    parfor p =1:parts

        [X,TvalV,it] = MCMC_small_solver(S,K,VC,small_eps,X_final,node_set,Clause_set,p);
        iter{p} =it;

        X_sat{p} = X;
        time(p)=TvalV(end);
    end

    if sum(cell2mat(iter))~=parts
        disp("STOP! Increase iterations for MCMC small solver");
        break;
    end

    for k=1:parts
        X_final(map{k}(:,1))=X_sat{k};
    end
    
    X_inter = X_final(clause_comm_nodes);

    [vtmpx,vtmpb]=rnode_chip(size(X_inter,1),X_inter,small_eps,Clause_inter,size(Clause_inter,1));

    [~,vtmpt]=rnode_chip(size(X_final,1),X_final,small_eps,Clauses,size(Clauses,1));


    if vtmpb==0
        disp("Solution found");
        break;
    end

    tic;

    C= size(Clauses,1);
    CMat_all=zeros(C,S);
    for j=1:S
        for k=1:C
            if(any(Clauses(k,:)==j))
                CMat_all(k,j)=1;
            end
            if(any(Clauses(k,:)==-j))
                CMat_all(k,j)=-1;
            end
        end
    end


    X_i = X_final;
    n = size(X_i, 1);
    cl_matrix=zeros(S,S);


    for i = 1:half
        X_i_temp = X_final;  % Work on a temporary copy
        X_i_temp(i) = 1 - X_i_temp(i); % Flip the bit
        X_i_temp(half+i) = X_i_temp(i);
        [cl_matrix(i,:), cl_unsatis(i)] = rnode_MCMC(n, X_i_temp, small_eps, CMat_all, C);
    end


    unsatis_arr= [unsatis_arr,vtmpt];
    [~,flip_nodes] = find(cl_unsatis<vtmpt);

    
    flip_node_arr{end+1}= flip_nodes;
    flip_node_arr = flip_node_arr(end-9:end);

    if all(cellfun(@(x) isequal(x, flip_node_arr{1}), flip_node_arr)) || all(unsatis_arr(end-4:end) == unsatis_arr(end))
        X_partial = binornd(ones(half,1), 0.5);      
        X_final = [X_partial; X_partial];
        continue;
    end

    if isempty(flip_nodes)


        [~,equal] = find(cl_unsatis==vtmpt);
        if ~isempty(equal)
            new_flip_nodes = equal;

            numEqual = numel(equal);
            new_flip_nodes_cell = cell(1, numEqual); % Preallocate cell array

            parfor idx = 1:numEqual
                i = equal(idx);
                I_minus = find(cl_matrix(i, [1:i-1, i+1:end]) > 0);
                new_flip_nodes_cell{idx} = I_minus;
            end

            % Merge results after the parallel loop
            new_flip_nodes = unique(cell2mat(new_flip_nodes_cell));

            n = length(new_flip_nodes);
            idx = randperm(n, floor(n/2));
            flip_nodes = new_flip_nodes(idx);

        else
            X_partial = binornd(ones(half,1), 0.5);      
            X_final = [X_partial; X_partial];
            continue;
        end

    end
    
    flip_nodes = unique(flip_nodes(flip_nodes <= half));      % Only flip in first half
    X_final(flip_nodes) = 1 - X_final(flip_nodes);         % Flip original
    X_final(half + flip_nodes) = X_final(flip_nodes);


    exists = any(cellfun(@(x) isequal(x, X_final), X_arr));

    % Keep generating a new X_final until it is unique
    while exists
        X_partial = binornd(ones(half,1), 0.5);      % Generate again
        X_final = [X_partial; X_partial];
        exists = any(cellfun(@(x) isequal(x, X_final), X_arr));
    end
    X_arr{end+1} = X_final;

    sat_time(c) = max(time);
    flip_time(c)=toc;
    total_time(c) = sat_time(c)+flip_time(c);
    c=c+1;

end


fprintf("The SAT solution is : \n");
disp(X_final');
% end
