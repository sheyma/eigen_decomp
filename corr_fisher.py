import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import sys

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))

import embed
import load_hcp
import corr_faster
import corr_full

def fisher_r2z(R):
    return ne.evaluate('arctanh(R)')

def fisher_z2r(Z):
    X = ne.evaluate('exp(2*Z)')
    return ne.evaluate('(X - 1) / (X + 1)')

# here we go ...

# list of all saubjects as numpy array
subject_list = np.array(sys.argv)[1:] # e.g. /ptmp/sbayrak/hcp/*

data_path = '/a/documents/connectome/_all'
template = 'MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'
cnt_files = 4
N_user = 10567

N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    print "do loop %d/%d, %s" % (i+1, N, subject)

    # load time-series matrix of the subject    
    K = load_hcp.t_series(data_path, subject, template, cnt_files, N_user, subject_path=None, dtype=None)

    # get upper-triangular of correlation matrix of time-series as 1D array
    K = corr_faster.corrcoef_upper(K)   
    print "corrcoef data shape: ", K.shape

    # Fisher r to z transform on the correlation upper triangular
    K = fisher_r2z(K)
        
    # sum all Fisher transformed 1D arrays
    if i == 0:
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')

    del K

print "loop done"

# get average 
SUM = ne.evaluate('SUM / N')

# Fisher z to r transform on average , now this is back to correlation array
SUM = fisher_z2r(SUM)

# transform correlation array into similarity array
SUM += 1.0
SUM /= 2.0

# get full similartiy matrix of correlations
N =corr_full.N_original(SUM)
SUM.resize([N,N])
corr_full.upper_to_down(SUM)

print "SUM.shape", SUM.shape

print "do embed for correlation matrix:", SUM.shape

# Satra's embedding algorithm 
embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
    diffusion_time=0, skip_checks=True, overwrite=True)

# output prefix
out_prfx="/home/raid/bayrak/tmp/fisher_"
# output precision
out_prec="%g"

np.savetxt(out_prfx + "embedding2.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "lambdas2.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "vectors2.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')

print result['lambdas']