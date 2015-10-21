import sys
import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import csv

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

import embed
import load_hcp
import corr_faster
import corr_full

# A replacement for numpy.loadtxt()
# This function can only read a 1 dimensional vector [n,1]!
def load_vector(file):
    # At the beginning we don't know how large this vector will be.
    chunk_rows = 32768
    cur_len = chunk_rows
    b = np.ndarray(shape=[cur_len], dtype=float)
    with open(file, 'r') as f:
        reader = csv.reader(f,'excel-tab')
        for i, row in enumerate(reader):
            if i >= cur_len:
                # Enlarge the vector if we have to.
                cur_len += chunk_rows
                b.resize([cur_len])
            b[i] = row[0]
    # Probably our vector is now a bit longer than the file ... shrink it!
    b.resize([i+1])
    return b

filenames = sys.argv[1:]

for i in range(0, len(filenames)):
    print "loop", i    
    K = load_vector(filenames[i])
    
    if i==0:
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')

    del K
    
print "loading data - loop done"
   
# total number of HCP subjects run with corr_top10.py
N = 476
# get mean correlation upper triangular
SUM = ne.evaluate('SUM / N')  

# get full correlation matrix
N_orig = corr_full.N_original(SUM)
SUM.resize([N_orig,N_orig])
corr_full.upper_to_down(SUM)

# get top left quadrant of full mtx
N_user = 29696
SUM = SUM[0:(N_user-1) , 0:(N_user-1)]

#print "full-binarized and averaged corrcoef matrix shape: ", SUM.shape 

print "top left quadrant (binarized, averaged, corrcoef mtx) shape: ", SUM.shape 

print "do embed for corr matrix "

embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
    diffusion_time=0, skip_checks=True, overwrite=True)

print result['lambdas']

print "embedding done!"    
 
out_prfx = "/ptmp/sbayrak/corr_top10_out/top10_LH_"
out_prec = "%g"       
np.savetxt(out_prfx + "embedding.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
