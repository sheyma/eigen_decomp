# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:03:07 2015

@author: bayrak
"""

import os, argparse, sys, h5py, numpy as np, glob
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed, align
import pandas as pd


# Load all embedding variables across subjects as arrays:
embeddings = [] 
filelist = []

# parse command line arguments for embedding components
parser = argparse.ArgumentParser()
#parser.add_argument("subject",nargs="+")
parser.add_argument('-o', '--outprfx', required=True)
args = parser.parse_args()

#subject_list = args.subject

#subject_list = ['/nobackup/kocher1/bayrak/test/100307_test.h5',
#                '/nobackup/kocher1/bayrak/test/100408_test.h5',
#                '/nobackup/kocher1/bayrak/test/101006_test.h5',
#                '/nobackup/kocher1/bayrak/test/101915_test.h5' ]

# get a list of embeddings for subjects
#for f in subject_list:
#    d =  np.array(h5py.File(f, 'r').get('tmp'))   
#    if (100 == d.shape[0]):
#        embeddings.append(d)
#        filelist.append(f)
#    else:
#        print "bad subject", f

#for f in subject_list:
#    d =  np.array(h5py.File(f, 'r').get('embedding'))   
#    if (29696 == d.shape[0]):
#        embeddings.append(d)
#        filelist.append(f)
#    else:
#        print "bad subject", f

subfile = pd.read_csv('/nobackup/kocher1/bayrak/subject_list.csv', header=None)
embeddings = []
for index, row in subfile.iterrows():
	S = h5py.File('/nobackup/kocher1/bayrak/hcp_embed/embedding_%s.h5' % str(row[0]) , 'r').get('embedding')
	embeddings.append(np.array(S))
	print row[0]



print "listed embedding input shape: ", np.shape(embeddings)

print "iterative alignment starts..."

realigned, xfms = align.iterative_alignment(embeddings, n_iters=10)

print "iterative alignment finishes..."
print "realigned shape: ", np.shape(realigned)
## Realign embeddings across subjects
#realigned, xfms = align.iterative_alignment_with_coords(embeddings, 
#                                                        coords=None, 
#                                                        n_iters=1, 
#                                                        n_samples=0.1, 
#                                                        use_mean=False)
#                                                        
# output prefix
out_prfx=args.outprfx

# write-out upper-triangular corr-array in HDF5 format
print "writing-out data in HDF5 format"
h = h5py.File(out_prfx, 'w')
h.create_dataset('rel', data=realigned)
h.close()




