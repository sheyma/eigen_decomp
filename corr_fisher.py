import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import sys
import argparse

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))

import h5py
import hcp_corr

## parse command line arguments
parser = argparse.ArgumentParser()
# left right or both hemispheres ...
parser.add_argument('--hem', default='LH', choices=['full','LH','RH'])
# output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_
parser.add_argument('--N_first', default=None, type=int)
parser.add_argument('--N_cnt', default=None, type=int)
# output prefix, e.g. /ptmp/sbayrak/corr_top10_out/top10_
parser.add_argument('-o', '--outprfx', required=True)
# the rest args are the subject path(s), e.g. /ptmp/sbayrak/hcp/*
parser.add_argument("subject",nargs="+")
args = parser.parse_args()


def fisher_r2z(R):
    return ne.evaluate('arctanh(R)')

def fisher_z2r(Z):
    X = ne.evaluate('exp(2*Z)')
    return ne.evaluate('(X - 1) / (X + 1)')

# first arg is output prefix, e.g. /ptmp/sbayrak/fisher/fisher_
cliarg_out_prfx = args.outprfx

# list of all subjects as numpy array
subject_list = np.array(args.subject) # e.g. /ptmp/sbayrak/hcp/*

cnt_files = 4
N_user = None

N = len(subject_list)

for i in range(0, N):
    subject = subject_list[i]
    print "do loop %d/%d, %s" % (i+1, N, subject)

    # load time-series matrix of the subject    
    K = hcp_corr.t_series(subject, hemisphere=args.hem, N_first=args.N_first,
                          N_cnt=args.N_cnt)
    
    # get upper-triangular of correlation matrix of time-series as 1D array
    K = hcp_corr.corrcoef_upper(K)
    print "corrcoef data shape: ", K.shape

    # Fisher r to z transform on the correlation upper triangular
    print "do Fisher r2z..."    
    K = fisher_r2z(K)
        
    # sum all Fisher transformed 1D arrays
    if i == 0:
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')

    del K

print "SUM shape: ", SUM.shape
print "loop done"

# output prefix
out_prfx=args.outprfx

# write-out full matrix in HDF5 format
print "writing-out data in HDF5 format"
h = h5py.File(out_prfx, 'w')
h.create_dataset('sum', data=SUM)
h.close()
