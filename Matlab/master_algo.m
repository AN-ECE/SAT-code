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

    % <50-238
    % cnffile = '/Users/ananyanandy/Documents/ECE_PhD/RESEARCH/FALL_24/DARPA/DARPA_Sets_Jan2024/batch-07/003_2_2.dimacs'; 

    % 50-300
    % cnffile = '/Users/ananyanandy/Documents/ECE_PhD/RESEARCH/FALL_24/DARPA/DARPA_Sets_Jan2024/batch-04/3block-like-rand-00051-0093.cnf';

    % cnffile = '/Users/ananyanandy/Documents/ECE_PhD/RESEARCH/FALL_24/Instances_Test_Phase_1/tentative_batches/hardware/t_batch_4/73.cnf';

    cnffile = '/Users/ananyanandy/Documents/ECE_PhD/RESEARCH/FALL_24/Instances_Test_Phase_1/tentative_batches/hardware/t_batch_4/54.dimacs';


    cnffile_new = '';
    scheme =1;
    chip_size=50;
    digital_backup =0;
    coeff_tts =6.43335e-08;


    [file,Clauses,var,nc]= k_sat_read_cnf(cnffile,cnffile_new,scheme);
    [CMat]=generate_cmat(Clauses,var,nc);
    [A,S]=satgraph(CMat,var);

    if (var<=50) && (size(Clauses,1)<=238)

        % No need for decomposition in this case
        [X_final_mcmc,time]= MCMC_SAT(CMat,var,nc);

        tts = coeff_tts*time;

        fprintf("The SAT solution is : \n");
        disp(X_final_mcmc');

        fprintf("TTS(meu_seconds) : %d\n",tts);

    elseif (var<=100)

        start_comb =1; % Starting nodes for decomposition. Maximum possible points [1,2,3,4]

        tic;
        [node_set,Clause_set,Clause_inter,clause_comm_nodes,s_node] = decomposition(start_comb,chip_size,S,A,Clauses);
        decomp_time = toc;
        [X_final,sat_time,flip_time,total_time]=chip_solver_large(2,node_set,Clause_set,Clause_inter,clause_comm_nodes,S,Clauses);

        tts = coeff_tts*sum(sat_time) + (sum(flip_time)+sum(sat_time))*1e6;

        fprintf("The SAT solution is : \n");
        disp(X_final');

        fprintf("TTS(meu_seconds) : %d\n",tts);

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

            tts = coeff_tts*sum(sat_time) + (sum(flip_time)+sum(sat_time))*1e6;

            fprintf("The SAT solution is : \n");
            disp(X_final');

            fprintf("TTS(meu_seconds) : %d\n",tts);

        else

            [X_final,sat_time,flip_time,total_time]=chip_solver_large(K,node_set,Clause_set,Clause_inter,clause_comm_nodes,S,Clauses);

            tts = coeff_tts*sum(sat_time) + (sum(flip_time)+sum(sat_time))*1e6;

            fprintf("The SAT solution is : \n");
            disp(X_final');

            fprintf("TTS(meu_seconds) : %d\n",tts);

        end
    end
end

 