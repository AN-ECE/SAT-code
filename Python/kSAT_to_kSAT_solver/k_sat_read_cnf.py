# Function that takes in cnf file and return a matrix of Clauses C and the number of variables for the given UNSAT problem

# INPUT :
# path_to_old_cnf - path to original cnf
# path_to_new_cnf - path to dump cnf when it is not 3-SAT
# scheme - Scheme to be decided according to user choice

# OUTPUT :
# file - filepath to new 3-SAT reduced cnf that can be referenced later when needed
# var - The number of variables in the final problem
# NC - The number of Clauses in the final problem
# Clauses -  A matrix (NC by 3) storing the Clauses for easy calculation   


import numpy as np

def k_sat_read_cnf(path_to_old_cnf,path_to_new_cnf,scheme):
    
    
    NC=0; 
    m=3; 
    var=0; 
    Clauses =0;
    k=0;
    nc_o=1;
    l1=0;
    l2=0;
    l3=0;
    l4=0;
    k_sat=0
    comments={}
    modifiedLines={}
    Clauses =[]
    
    with open(path_to_old_cnf, "r") as fid:
    
        for line in fid:
            tline = line.strip()
            if ((tline.lower().startswith('c')) or (tline.lower().startswith('p'))) :
                comments[+1] = tline;
            
            if (tline.lower().startswith('p')) :
                X = tline.split()
                var = int(X[-2])
                varo = var
                NC = int(X[-1])
                continue;
    
            if (not tline.lower().startswith('c'))  and  (nc_o<= NC) :
                x = np.fromstring(tline,dtype = int, sep=' ')
                x = x.tolist()
                l=len(x)-1;
                k_sat = l;
                if scheme==1 :
                    if l==1 :
                        l1=l1+1;
                        v1=var+1;
                        v2=var+1;
                        Clauses.append(x[:-1]+[v1]+[v2])
                        Clauses.append(x[:-1]+[v1]+[-v2])
                        Clauses.append(x[:-1]+[-v1]+[v2])
                        Clauses.append(x[:-1]+[-v1]+[-v2])
                        k=k+4;
                        var=v2;
                    elif l==2 :
                        l2=l2+1;
                        v1=var+1;
                        Clauses.append(x[:-1]+[v1])
                        Clauses.append(x[:-1]+[-v1])
                        k=k+2;
                        var=v1;
                    elif l==3 :
                        l3=l3+1;
                        Clauses.append(x[:-1])
                        k=k+1;
                    else :
                        v=list(range(var + 1, var + l - 2))
                        l4=l4+1
                        for j in range(l-2):
                            if j==0 :
                                Clauses.append(x[0:2]+[v[j]])
                            elif j==l-3:
                                Clauses.append(x[l-2:l]+[-v[j-1]])
                            else :
                                Clauses.append([x[j+1]]+[-v[j-1]]+[v[j]])
                            
                            k=k+1;
                            
                        var = v[-1];
                    
                else :
                    if l==1:
                        l1=l1+1;
                        Clauses.append(x[:-1]+x[-1]+x[-1])
                        k=k+1;
                    elif l==2 :
                        l2=l2+1;
                        Clauses.append(x[:-1]+x[-1])
                        k=k+1;
                    elif l==3 :
                        l3=l3+1;
                        Clauses.append(x[:-1])
                        k=k+1;
                    else :
                        v=list(range(var + 1, var + l - 2))
                        l4=l4+1;
                        for j in range(l-2):
                            if j==0 :
                                Clauses.append(x[0:2]+[v[j]])
                            elif j==l-3:
                                Clauses.append(x[l-2:l]+[-v[j-1]])
                            else :
                                Clauses.append([x[j+1]]+[-v[j-1]]+[v[j]])
                            
                            k=k+1;
                        
                        var = v[-1];
                    
                    
                nc_o=nc_o+1; # Keeping track of number of original clauses
    
    NC = len(Clauses)
    print('k - SAT : %d\n',k_sat)  
    print('#Length 1 clauses before reduction : %d\n',l1)
    print('#Length 2 clauses before reduction : %d\n',l2)
    print('#Length 3 clauses before reduction : %d\n',l3)
    print('#Length >3 clauses before reduction : %d\n',l4)
    print('Total number of variables before reduction : %d\n',varo)
    print('Total number of variables after reduction : %d\n',var)
    print('Total number of clauses after reduction : %d\n',len(Clauses));

    return Clauses,var,NC,k_sat,varo