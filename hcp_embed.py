"""
load HCP t-series
get correlation matrix
1) get similarity matrix, or
2) threshold the matrix
apply Satra's embedding algorithm
"""
import numpy as np
import hcp_corr
import sys
import os
import h5py
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed
import argparse

## begin parse command line arguments
parser = argparse.ArgumentParser()

# left right or both hemispheres ...
parser.add_argument('--hem', default='LH', choices=['full','LH','RH'])
parser.add_argument('--N_first', default=None, type=int)
parser.add_argument('--N_cnt', default=None, type=int)
parser.add_argument('--thr', action='store_false')
# output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_
parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/hcp/*
parser.add_argument("subject",nargs="+")

args = parser.parse_args()
## end parse command line arguments

subject_list = np.array(args.subject)

N = len(subject_list)


for i in range(0, N):
    subject = subject_list[i]
    subject_basename = os.path.basename(subject)
    print "do loop %d/%d, %s" % (i+1, N, subject)
    # load time-series matrix
    K = hcp_corr.t_series(subject,  hemisphere=args.hem,
                          N_first=args.N_first, N_cnt=args.N_cnt)
    # get upper triangular of corr matrix
    K = hcp_corr.corrcoef_upper(K)
        
    if args.thr:    
        # get similarity matrix (Kernel matrix / Gram matrix)
        K +=1.0
        K /=2.0
    else:
        # set negative entries to 0
        K[np.where(K < 0)] = 0     

    # convert upper triangular into full corr matrix
    N_orig = hcp_corr.N_original(K)
    K.resize([N_orig, N_orig])
    K = hcp_corr.upper_to_down(K)
    print "corr matrix shape ", K.shape    
 
    # do embedding on similarity matrix or thresholded matrix
    print "do embedding..."

    try:	
         embedding, result = embed.compute_diffusion_map(K, 
                                                         n_components=10,
							 skip_checks=True)
    except:
	print "AAAAAAAAAAAAAAAA", subject_basename
        continue

    # write out embedding components, eigenvalues and eigenvectors
    print "writing out embedding results..."
    name = 'embeddings_' + args.hem + '_' + subject_basename + '.h5'

    outfile = os.path.join(args.outprfx, name)
 
    print "outfile : ", outfile
    h = h5py.File(outfile , 'w')
    print outfile
    h.create_dataset('embedding', data=embedding)
    h.create_dataset('lambdas', data=result['lambdas'])
    h.create_dataset('vectors', data=result['vectors'])
    h.close()

print "loop done!"
