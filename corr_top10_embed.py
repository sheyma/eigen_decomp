import sys
import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import argparse

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

import embed
import hcp_util

# here we go ...

## parse command line arguments
parser = argparse.ArgumentParser()
# total number of HCP subjects ... for division
parser.add_argument('--cntsubjects', default=476, type=int)
# output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_
parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/hcp/*
parser.add_argument("sum_file",nargs="+")
args = parser.parse_args()

filenames = np.array(args.sum_file)

for i in range(0, len(filenames)):
    print "do loop %d/%d, %s" % (i+1, len(filenames), filenames[i])
    K = hcp_util.load_vector(filenames[i])

    if i==0:
        print "loaded matrix shape:", K.shape
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')

    del K

print "loading data - loop done"

# total number of HCP subjects run with corr_top10.py
N = args.cntsubjects
# get mean correlation upper triangular
SUM = ne.evaluate('SUM / N')  

# get full correlation matrix
N_orig = hcp_util.N_original(SUM)
SUM.resize([N_orig,N_orig])
hcp_util.upper_to_down(SUM)

print "averaged corrcoef matrix shape: ", SUM.shape

print "do embed for corr matrix "

embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
    diffusion_time=0, skip_checks=True, overwrite=True)

print result['lambdas']
print "embedding done!"

out_prfx = args.outprfx
out_prec = "%g"
np.savetxt(out_prfx + "embedding.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
