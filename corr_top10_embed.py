import sys
import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

import embed
import load_hcp
import corr_faster
import corr_full

filename = ['tmp_A.csv', 'tmp_A.csv', 'tmp_A.csv', 'tmp_A.csv', 'tmp_A.csv',
            'tmp_A.csv', 'tmp_A.csv', 'tmp_A.csv', 'tmp_A.csv', 'tmp_A.csv']

for i in range(0, len(filename)):
    print "loop", i    
    K = np.loadtxt(filename[i])    
    
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
print "full-binarized and averaged corrcoef matrix shape: ", SUM.shape 

print "do embed for corr matrix "

embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
    diffusion_time=0, skip_checks=True, overwrite=True)

print result['lambdas']

print "embedding done!"    
 
out_prfx = "/ptmp/sbayrak/corr_top10_out/top10_"
out_prec = "%g"       
np.savetxt(out_prfx + "embedding.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
