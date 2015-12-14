# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 14:03:07 2015

@author: bayrak
"""

import os, argparse, sys, h5py, numpy as np, glob
sys.path.append(os.path.expanduser('~/devel/mapalign/mapalign'))
import embed, align

# Load all embedding variables across subjects as arrays:
embeddings = [] 
filelist = []

# parse command line arguments for embedding components
parser = argparse.ArgumentParser()
parser.add_argument("subject",nargs="+")
args = parser.parse_args()

subject_list = args.subject

# get a list of embeddings for subjects
for f in subject_list:
    d =  np.array(h5py.File(f, 'r').get('embedding'))   
    if (29696 == d.shape[0]):
        embeddings.append(d)
        filelist.append(f)
    else:
        print "bad subject", f

print "listed embedding input shape: ", np.shape(embeddings)

# Realign embeddings across subjects
realigned, xfms = align.iterative_alignment_with_coords(embeddings, 
                                                        coords=None, 
                                                        n_iters=1, 
                                                        n_samples=0.01, 
                                                        use_mean=False)
                                                        
h = h5py.File('tmp.h5', 'w')
h.create_dataset('rel', data=realigned)
h.close()





