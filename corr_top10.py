# -*- coding: utf-8 -*-
"""
top 10 percent of correlation matrices

"""
import numpy as np
import matplotlib.pyplot as pl 


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
subject_list = np.array(['100307']) # e.g. /ptmp/sbayrak/hcp/*

data_path = '/a/documents/connectome/_all'
template = 'MNINonLinear/Results/rfMRI_REST?_??/rfMRI_REST?_??_Atlas_hp2000_clean.dtseries.nii'
cnt_files = 4
N_user = 78

N = len(subject_list)

dN = 0.01


for i in range(0, N):
    subject = subject_list[i]
    print "do loop %d/%d, %s" % (i+1, N, subject)

    # load time-series matrix of the subject    
    K = load_hcp.t_series(data_path, subject, template, cnt_files, N_user, subject_path=None, dtype=None)

    # get upper-triangular of correlation matrix of time-series as 1D array
    K = corr_faster.corrcoef_upper(K)   
    print "corrcoef data shape: ", K.shape
    
    bins = np.arange(-1, 1+0.1, 0.1)
    x, bins = np.histogram(K, bins)
    
    pl.hist(K, bins)
    
    ten_percent = 0.10
    
    back_sum = 0
    for i in range(x.shape[0]-1, -1, -1):
        back_sum += x[i]/float(x.sum())    
        print i, back_sum, bins[i]        
        if back_sum >= ten_percent:
            thr = bins[i]
            print "top-10percent threshold:", thr
            break

  
#    K_length = K.shape[0]
#    
#    for j in range(0, K_length, 1):
#        if K[j] >= threshold:
#            K[j] = 1.0
#        else:
#            K[j] = 0
#
#    if i == 0:
#        SUM = K
#    else:
#        SUM = ne.evaluate('SUM + K')
#
#    del K
#
#print "loop done"
#
## get mean correlation upper triangular
#SUM = ne.evaluate('SUM / N')  
#
## get full correlation matrix
#N_orig = corr_full.N_original(SUM)
#SUM.resize([N_orig,N_orig])
#corr_full.upper_to_down(SUM)
#
## get similarity matrix
#SUM = (SUM +1.0) / 2.0 
#
#print "do embed for correlation matrix:", SUM.shape
#embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
#    diffusion_time=0, skip_checks=True, overwrite=True)
#
#print result['lambdas']
#    
        

