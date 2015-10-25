# -*- coding: utf-8 -*-
"""
top 10 percent of correlation matrices

"""
import numpy as np
import os
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import sys
import argparse

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
sys.path.append(os.path.expanduser('~/devel/hcp_corr'))

import embed
import hcp_util

# here we go ...

## parse command line arguments
parser = argparse.ArgumentParser()
# output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_
parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/hcp/*
parser.add_argument("subject",nargs="+")
args = parser.parse_args()

# list of all subjects as numpy array
subject_list = np.array(args.subject) # e.g. /ptmp/sbayrak/hcp/*

cnt_files = 4
# nodes of left hemispheres only
N_user = 29696

N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    print "do loop %d/%d, %s" % (i+1, N, subject)
    
    # load time-series matrix of the subject    
    K = hcp_util.t_series(subject, cnt_files=cnt_files, N_cnt=N_user)

    # get upper-triangular of correlation matrix of time-series as 1D array
    K = hcp_util.corrcoef_upper(K)
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

# output prefix
out_prfx=args.outprfx
# output precision
out_prec="%g"

# write out averaged upper triangular
hcp_util.write_upper(out_prfx + "SUM.csv", SUM, fmt=out_prec)

# get mean correlation upper triangular
#SUM = ne.evaluate('SUM / N')  

## get full correlation matrix
#N_orig = hcp_util.N_original(SUM)
#SUM.resize([N_orig,N_orig])
#hcp_util.upper_to_down(SUM)
#print "full-binarized and averaged corrcoef matrix shape: ", SUM.shape 

#print "do embed for corr matrix "

#embedding, result = embed.compute_diffusion_map(SUM, alpha=0, n_components=20,
#    diffusion_time=0, skip_checks=True, overwrite=True)

#print result['lambdas']

#print "embedding done!"    
        
#np.savetxt(out_prfx + "embedding.csv", embedding, fmt=out_prec, delimiter='\t', newline='\n')
#np.savetxt(out_prfx + "lambdas.csv", result['lambdas'], fmt=out_prec, delimiter='\t', newline='\n')
#np.savetxt(out_prfx + "vectors.csv", result['vectors'], fmt=out_prec, delimiter='\t', newline='\n')
