function [Clauses,var,C]=variable_split(Clauses,var,k_sat,C)
v=var;
for i =1:var
    [row,~] =find(abs(Clauses)==i);
    row = sort(row);

    % first = row(1: floor(length(row)/2))';
    v1 = i;
    
    second = row(floor(length(row)/2)+1:end)';
    cl_s = Clauses(second,:);
    v2=v+i;
    cl_s(cl_s==i)=v2; 
    cl_s(cl_s==-i)=-v2;
    Clauses(second, :) = cl_s;

    Clauses(C+1,:)= [v1,-v2,-v2* ones(1, (k_sat-2))];
    Clauses(C+2,:)= [-v1,v2,v2* ones(1, (k_sat-2))];
    C=C+2;
end
var=v+i;
C= size(Clauses,1);
end