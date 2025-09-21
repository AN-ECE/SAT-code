%Function that reads a cnf file and generate a SAT solution

% INPUT :
% cnffile - Path to the original cnf
% cnffile_new - Path to be provided if the problem is not 3-SAT and does not want to dump the reduced 3-SAT, can pass empty string in such case
% scheme - Scheme to be decided according to user choice, but currently fixed to 1

% OUTPUT : 
% X_final_mcmc - Final SAT solution when runnning the 1-chip MCMC algorithm
% X_final_decomp - Final SAT solution when running the solver-decomposition
% algorithm
% time_mcmc - Time in seconds needed to reach SAT solution for MCMC
% algorithm


tot_time=0;
for i = 1:1
    tic;

    cnffile = ''; %Input path to the cnf 


    cnffile_new = '';
    scheme =1;
    chip_size=50;
    digital_backup =0;


    [file,Clauses,var,nc]= k_sat_read_cnf(cnffile,cnffile_new,scheme);
    [CMat]=generate_cmat(Clauses,var,nc);
    [A,S]=satgraph(CMat,var);

    if (var<=50) && (size(Clauses,1)<=238)

        % No need for decomposition in this case
        [X_final_mcmc,time]= MCMC_SAT(CMat,var,nc);


        fprintf("The SAT solution is : \n");
        disp(X_final_mcmc');


    elseif (var<=100)

        start_comb =1; % Starting nodes for decomposition. Maximum possible points [1,2,3,4]

        tic;
        [node_set,Clause_set,Clause_inter,clause_comm_nodes,s_node] = decomposition(start_comb,chip_size,S,A,Clauses);
        decomp_time = toc;
        [X_final,sat_time,flip_time,total_time]=chip_solver_large(2,node_set,Clause_set,Clause_inter,clause_comm_nodes,S,Clauses);

        fprintf("The SAT solution is : \n");
        disp(X_final');


    else
        tic;
        [node_set] =  spectral_analysis(A,S,chip_size);
        decomp_time = toc;

        % The number of partitions for large problems
        K = size(node_set,2);

        [Clause_set,Clause_inter,clause_comm_nodes] = clause_split(node_set,K,Clauses);

        % Set to 1 if we need to run Solver Algorithm after some iterations 
        if digital_backup ==1

            [X_final,sat_time,flip_time,total_time,MCMC_time]=chip_solver_mix(K,node_set,Clause_set,Clause_inter,clause_comm_nodes,S,Clauses);

            fprintf("The SAT solution is : \n");
            disp(X_final');


        else

            [X_final,sat_time,flip_time,total_time]=chip_solver_large(K,node_set,Clause_set,Clause_inter,clause_comm_nodes,S,Clauses);

            fprintf("The SAT solution is : \n");
            disp(X_final');


        end
    end
end

 
