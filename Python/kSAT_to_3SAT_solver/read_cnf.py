import numpy as np

def read_cnf(cnffile, k_sat):
    
    NC=0
    m=k_sat 
    var=0 
    Clauses =[]
    k=1
    with open(cnffile, "r") as fid:
    
        for line in fid:
            tline = line.strip()
            if (tline.lower().startswith('p')) :
                X = tline.split()
                var = int(X[-2])
                varo = var
                NC = int(X[-1])
                continue;
                
            if (not tline.lower().startswith('c'))  and  (k<= NC) :
                x = np.fromstring(tline,dtype = int, sep=' ')
                x = x.tolist()
                Clauses.append(x[:-1])
                k=k+1

    return Clauses,var,NC