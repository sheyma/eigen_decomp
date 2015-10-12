# -*- coding: utf-8 -*-
"""
top 10 percent of correlation matrices

"""
import numpy as np
import os
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import sys

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))

import embed
import load_hcp
import corr_faster
import corr_full

# here we go ...

# list of all saubjects as numpy array
#subject_list = np.array(['100307', '912447']) 
subject_list = np.array(sys.argv)[1:]

data_path = '/a/documents/connectome/_all'
template = 'MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'
cnt_files = 4
N_user = None

N = len(subject_list)


for i in range(0, N):
    subject = subject_list[i]
    print "do loop %d/%d, %s" % (i+1, N, subject)

    # load time-series matrix of the subject    
    K = load_hcp.t_series(data_path, subject, template, cnt_files, N_user, subject_path=None, dtype=None)

    # get upper-triangular of correlation matrix of time-series as 1D array
    K = corr_faster.corrcoef_upper(K)   
    print "corrcoef data upper triangular shape: ", K.shape
    
    # get histogram of upper-triangual array
    dbins = 0.01
    bins = np.arange(-1, 1+dbins, dbins)
    x, bins = np.histogram(K, bins)
    
    # find out threshold value for top 10 percent    
    ten_percent = 0.10
    back_sum = 0
    
    for idx in range(x.shape[0]-1, -1, -1):
        back_sum += x[idx]/float(x.sum())    
        if back_sum >= ten_percent:
            thr = bins[idx]
            print "top-10percent threshold:", thr
            break

    # binarize K via thresholding
    K[np.where( K >= thr) ] = 1.0    
    K[np.where( K < thr) ] = 0
    
    if i == 0:
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')

    del K

print "loop done"

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
        
# output prefix
out_prfx="/home/raid/bayrak/tmp/top10_"
# output precision
out_prec="%g"

np.savetxt(out_prfx + "embedding.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
