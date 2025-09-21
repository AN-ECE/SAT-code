%Function that takes in cnf file and return a matrix of Clauses C and the
%number of variables for the given UNSAT problem
 
function [Clauses,var,C]= read_cnf(cnffile,k_sat)
    
    C=0; % The number of clauses
    m=k_sat; % k-SAT problem 
    var=0; %The number of variables
    Clauses =0; % Storing the values for each clause in a matrix
    
    fid = fopen(cnffile);
    if fid<0
        return
    end
    k=1;
    while ~feof(fid)
        tline = fgetl(fid);
        tline = strtrim(tline);
        if isempty(tline)
            continue;
        end
        if (lower(tline(1))=='p')
            X = (string(split(tline)));
            var = str2num(X(end -1));
            C= str2num(X(end));
            Clauses = zeros(C,m); 
            continue;
        end
        
        if (tline(1)~= 'c') &&(k<=C)
            x = str2num(tline);
            Clauses(k,:)= x(1:end-1);
            k=k+1;
        end
    end
    fclose(fid);
end

    
