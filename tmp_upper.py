import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import sys
from scipy.optimize import fsolve
import csv

sys.path.append(os.path.expanduser('/u/sbayrak/devel/mapalign/mapalign'))
import embed

def load_matrix(fname,n):
    b = np.ndarray(shape=[n*(n-1)/2], dtype=float)
    with open(fname , 'r') as f:
        reader = csv.reader(f,'excel-tab')
        for i, row in enumerate(reader):
            b[i] = row[0]
    return b

def N_original(a):
    x = a.shape[0]
    def func(N):
        return N*(N-1.0) / 2.0 -x
    n = int(round(fsolve(func, [x])))
    return n
    

def upper_to_down(M):
    a = len(M)    
    n = N_original(M)
    U = np.zeros([n,n])
        
    index = 0    
    for i in range(0, n):
        
        U[i,i] = 1.0          
        length = n-i-1
        
        if index < a:
                      
            U[i, i+1:n] = M[index : index+length]
            U[i+1:n,i] = M[index : index+length]
            
        index = index + length 
    
    return U

def upper_to_mat(M):

    if not M.flags['C_CONTIGUOUS']:
        raise Exception("C_CONTIGUOUS required")
    n = M.shape[0]
    size = (n - 1) * n / 2
    U = M.reshape([n*n,])
    k = size
    for i in range(n-1, -1, -1):
        len = n - 1 - i
        M[i+1:n,i] = U[k-len:k]
        M[i,i+1:n] = U[k-len:k]
        M[i,i] = 1.0
        k -= len
    return M

fname = sys.argv[1]
N_fname = int(sys.argv[2])
SUM = load_matrix(fname, N_fname)
SUM += 1.0
SUM /= 2.0
n = N_original(SUM)
SUM.resize([n,n])
upper_to_mat(SUM)

embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
    diffusion_time=0, skip_checks=True, overwrite=True)

 # output prefix
out_prfx="/ptmp/sbayrak/fisher/FISHER_"
# output precision
out_prec="%g"

np.savetxt(out_prfx + "embedding.csv", embedding, fmt='%5.5e', delimiter='\t', newline='\n')
np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')

print result['lambdas']
