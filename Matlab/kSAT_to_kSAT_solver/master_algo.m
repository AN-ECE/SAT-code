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
    

    [X_final,sat_time,flip_time,total_time]=chip_solver_k_sat(cnffile,cnffile_new,scheme);

    fprintf("The SAT solution is : \n");
    disp(X_final');



end

 
