# -*- coding: utf-8 -*-
"""
measure network caracteristics of connectivity matrices
    - degree centrality
"""

import numpy as np
import numexpr as ne
ne.set_num_threads(ne.ncores) # inclusive HyperThreading cores
import argparse
import h5py

# here we go ...

## parse command line arguments
parser = argparse.ArgumentParser()
# paths of connectivity matrices
# e.g. /ptmp/sbayrak/corr_percent10/sum_LH_**.h5
parser.add_argument("sum_file",nargs="+")
# total number of subjects in connectitivity matrices
parser.add_argument('--cntsubjects', type=int)
# output path/fileName 
parser.add_argument('-o', '--outprfx', required=True)
args = parser.parse_args()
## end of parse command line arguments

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
    
    del K

print "loading data - loop done"

# get degree centrality - hard coded
[ro, co] = np.shape(SUM)
# check if connectivity is a square matrix
if ro != co:
    print "Warning, mean connectivity is not a square matrix!"

deg_cent =np.zeros((ro,1))
# exclude NaN valued indices
ind = (np.where(np.isnan(SUM[0,:]) == False))

for j in range(0, 4000):
    
    row_sum = SUM[j, ind[0] ].sum()
    deg_cent[j] = row_sum
    row_sum = 0

N = args.cntsubjects
## get mean degree centrality of nodes
##deg_cent = deg_cent / N
    
print "length of degree centrality vector", len(deg_cent)
print "maximum of degree centrality: ", deg_cent.max()
print "minimum of degree centrality: ", deg_cent.min()
    
print "writing out centrality results..."
h = h5py.File(args.outprfx , 'w')
h.create_dataset('centrality', data=deg_cent)
h.close()

