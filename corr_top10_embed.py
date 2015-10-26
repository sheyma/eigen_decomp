import sys
import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

import embed
import hcp_util

# here we go ...

## parse command line arguments
# first arg is output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_LH_
cliarg_out_prfx = sys.argv[1]
# the rest args are the path(s) to the partial SUMs,
# e.g. /ptmp/sbayrak/corr_top10_out/top10_histsum-*.csv
cliarg_rest = sys.argv[2:]

filenames = np.array(cliarg_rest)

for i in range(0, len(filenames)):
    print "loop", i    
    K = hcp_util.load_vector(filenames[i])
    
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
N_orig = hcp_util.N_original(SUM)
SUM.resize([N_orig,N_orig])
hcp_util.upper_to_down(SUM)

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
 
out_prfx = cliarg_out_prfx
out_prec = "%g"       
np.savetxt(out_prfx + "embedding.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
