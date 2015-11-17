"Fisher - part 2..."

import sys
import os
import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import argparse
import h5py
import hcp_corr

sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))

import embed
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

def fisher_r2z(R):
    return ne.evaluate('arctanh(R)')

def fisher_z2r(Z):
    X = ne.evaluate('exp(2*Z)')
    return ne.evaluate('(X - 1) / (X + 1)')

filenames = np.array(args.sum_file)

for i in range(0, len(filenames)):
    print "do loop %d/%d, %s" % (i+1, len(filenames), filenames[i])
    
    K_init = h5py.File(filenames[i], 'r')
    K = K_init.get('sum')
    np.array(K)
   
    if i==0:
        print "loaded matrix shape:", K.shape
        SUM = K
    else:
        SUM = ne.evaluate('SUM + K')
    
    #del A

print "loading data - loop done"

# total number of HCP subjects run with corr_top10.py
N = args.cntsubjects
# get mean correlation 
SUM = ne.evaluate('SUM / N')  

# Fisher z to r transform on the (averaged) upper triangular
print "do Fisher z2r..."    
# Fisher z to r transform on average , now this is back to correlation array
SUM = fisher_z2r(SUM)

# transform correlation array into similarity array
SUM += 1.0
SUM /= 2.0

# get full similartiy matrix 
N = hcp_corr.N_original(SUM)
SUM.resize([N,N])
hcp_corr.upper_to_down(SUM)

print "SUM.shape", SUM.shape

## output prefix
#out_prfx=args.outprfx
#
## write-out full matrix in HDF5 format
#print "writing-out data in HDF5 format"
#h = h5py.File(out_prfx, 'w')
#h.create_dataset('sum', data=SUM)
#h.close()

# set NaN entries to 0
SUM[np.where(np.isnan(SUM) == True)] = 0
# ignore zero entries?
ind = np.where(np.sum(SUM,axis=1) != 1)

print "do embed for corr matrix "

embedding, result = embed.compute_diffusion_map(SUM[ind].T[ind].T, 
                                                n_components=10)
    
print result['lambdas']
print "embedding done!"

print "writing out embedding results..."
h = h5py.File(args.outprfx , 'w')
h.create_dataset('embedding', data=embedding)
h.create_dataset('lambdas', data=result['lambdas'])
h.create_dataset('vectors', data=result['vectors'])
h.close()

