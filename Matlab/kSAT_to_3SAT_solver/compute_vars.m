% Function to compute extra reduction variables 

% INPUT :
% X_ini - Binary States of the variables
% var - Number of variables after 3-SAT reduction
% var - Number of variables before 3-SAT reduction
% Clauses_d - Clauses after 3-SAT reduction

% OUTPUT : 
% va : Array with the states of the extra variables

function va = compute_vars(X_ini,var,varo,k_sat,Clauses_d)

va = zeros(1, var);
extra_per_cl = k_sat-2;

for i = 1:extra_per_cl:size(Clauses_d, 1)
    Cl_rows = Clauses_d(i:min(i+extra_per_cl-1, end), :);


    chunk = unique(abs(Cl_rows(abs(Cl_rows) > varo)))';

    row = any(abs(Cl_rows) <= varo,2);
    mat = Cl_rows(row,:);
    res = mat';
    pos = res(abs(res) <= varo);
    elem = (pos < 0);
    X=X_ini(abs(pos));
    X(elem==1)=1-X(elem==1);

    l=k_sat;
    v = zeros(l-3,1); % Initialize v variables
    % Determine v1 based on z1 and z2
    if X(1) == 1 || X(2) == 1
        v(1) = 0; % v1 can be 0 or 1, choosing 0
    else
        v(1) = 1;
    end

    % Propagate values for intermediate v_j
    for j = 2:l-3
        if X(j+1) == 1 || ~v(j-1) == 1
            v(j) = 0;
        else
            v(j) = 1;
        end
    end

    % Ensure the last clause is satisfied
    if X(l-1) == 1 || X(l) == 1
        % Clause C_{k-2} is already satisfied, keep v(k-3) as assigned
    else
        v(l-3) = 0; % Adjust v_{k-3} if needed
    end

    va(chunk)=v;


end


end


