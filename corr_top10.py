"""
get correlation matrix of HCP subjects
find out top 10 percent value in corr. matrices
binarize corr. matrix via threshold
apply Satra's embedding algorithm
"""
import numpy as np
import numexpr as ne
import sys, os
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed
import argparse
import hcp_corr
import h5py

# here we go ...

## parse command line arguments
parser = argparse.ArgumentParser()
# left right or both hemispheres ...
parser.add_argument('--hem', default='LH', choices=['full','LH','RH'])
parser.add_argument('--N_first', default=None, type=int)
parser.add_argument('--N_cnt', default=None, type=int)
# output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_
parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/hcp/*
parser.add_argument("subject",nargs="+")
args = parser.parse_args()

## end parse command line arguments

# list of all subjects as numpy array
subject_list = np.array(args.subject) # e.g. /ptmp/sbayrak/hcp/*

N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    subject_basename = os.path.basename(subject)
    print "do loop %d/%d, %s" % (i+1, N, subject)
    
    # load time-series matrix of the subject    
    K = hcp_corr.t_series(subject, hemisphere=args.hem, N_first=args.N_first,
                          N_cnt=args.N_cnt)
    
    # get upper-triangular of correlation matrix of time-series as 1D array
    K = hcp_corr.corrcoef_upper(K)
    print "corrcoef data upper triangular shape: ", K.shape

    thr_percent = 10
    
    # get thr for top 10 % of UPPER-Triangular of corr-matrix
    thr = np.percentile(K, (100 - thr_percent))
    print "1D upper-triang THR: ", thr         
    # binarize K via thresholding
    K[np.where( K >= thr) ] = 1.0
    K[np.where( K < thr) ] = 0
    
    # convert upper triangular into full corr matrix
    N_orig = hcp_corr.N_original(K)
    K.resize([N_orig, N_orig])
    K = hcp_corr.upper_to_down(K)
    print "corr matrix shape ", K.shape

    embedding, result = embed.compute_diffusion_map(K, 
                                                    n_components=10)

    print "writing out embedding results..."
    name = 'embeddings_' + args.hem + '_' + subject_basename + '.h5'

    outfile = os.path.join(args.outprfx, name)
 
    print "outfile : ", outfile
    h = h5py.File(outfile , 'w')
    h.create_dataset('embedding', data=embedding)
    h.create_dataset('lambdas', data=result['lambdas'])
    h.create_dataset('vectors', data=result['vectors'])
    h.close()

print "loop done!"

